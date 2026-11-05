package mx.clicknbusiness.envivo;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.URL;

/**
 * Control remoto del EN VIVO de la Fábrica, solo en la wifi de la casa (4-nov-2026): busca la PC por UDP («ENVIVO?» al
 * puerto 8792, contesta «ENVIVO1|puerto|canal»), o usa la última IP que funcionó, y abre http://PC:8790/movil en un
 * WebView. El código de 4 cifras para controlar lo pide la propia página (sale en la tele al arrancar el directo).
 */
public class MainActivity extends Activity {
    private static final int PUERTO_UDP = 8792;
    private WebView web;
    private SharedPreferences prefs;

    @Override
    protected void onCreate(Bundle b) {
        super.onCreate(b);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        getWindow().setStatusBarColor(Color.rgb(11, 10, 9));
        prefs = getSharedPreferences("envivo", MODE_PRIVATE);
        web = new WebView(this);
        web.setBackgroundColor(Color.rgb(11, 10, 9));
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        web.addJavascriptInterface(new Puente(), "App");
        web.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView v, WebResourceRequest req, WebResourceError err) {
                if (req.isForMainFrame()) pantallaBuscar("La PC dejó de contestar (" + err.getDescription() + ").");
            }
        });
        setContentView(web);
        buscar();
    }

    /** Primero la última IP que sirvió; si no contesta, broadcast por UDP. */
    private void buscar() {
        pantallaBuscar(null);
        new Thread(() -> {
            String ip = prefs.getString("ip", "");
            int puerto = prefs.getInt("puerto", 8790);
            if (ip.isEmpty() || !contesta(ip, puerto)) {
                String[] hallada = porUdp();
                if (hallada != null) { ip = hallada[0]; puerto = Integer.parseInt(hallada[1]); } else ip = "";
            }
            final String fIp = ip;
            final int fPuerto = puerto;
            runOnUiThread(() -> {
                if (fIp.isEmpty()) {
                    pantallaBuscar("No encontré la PC en la wifi. ¿Está corriendo <b>python fab.py envivo</b>?");
                } else {
                    prefs.edit().putString("ip", fIp).putInt("puerto", fPuerto).apply();
                    web.loadUrl("http://" + fIp + ":" + fPuerto + "/movil");
                }
            });
        }).start();
    }

    private boolean contesta(String ip, int puerto) {
        try {
            HttpURLConnection c = (HttpURLConnection) new URL("http://" + ip + ":" + puerto + "/api/estado").openConnection();
            c.setConnectTimeout(1500);
            c.setReadTimeout(2500);
            return c.getResponseCode() == 200;
        } catch (Exception e) {
            return false;
        }
    }

    private String[] porUdp() {
        WifiManager wm = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        WifiManager.MulticastLock candado = wm.createMulticastLock("envivo");
        candado.acquire();
        try (DatagramSocket so = new DatagramSocket()) {
            so.setBroadcast(true);
            so.setSoTimeout(1200);
            byte[] q = "ENVIVO?".getBytes("UTF-8");
            for (int intento = 0; intento < 3; intento++) {
                so.send(new DatagramPacket(q, q.length, InetAddress.getByName("255.255.255.255"), PUERTO_UDP));
                try {
                    byte[] buf = new byte[256];
                    DatagramPacket p = new DatagramPacket(buf, buf.length);
                    so.receive(p);
                    String[] r = new String(p.getData(), 0, p.getLength(), "UTF-8").split("\\|");
                    if (r.length >= 2 && r[0].equals("ENVIVO1")) return new String[]{p.getAddress().getHostAddress(), r[1]};
                } catch (java.net.SocketTimeoutException ignorado) {
                    // otro intento
                }
            }
        } catch (Exception ignorado) {
            // sin wifi o sin permiso: se queda en la pantalla de buscar
        } finally {
            candado.release();
        }
        return null;
    }

    private void pantallaBuscar(String nota) {
        String ip = prefs.getString("ip", "");
        String html = "<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'>"
            + "<body style='margin:0;min-height:100vh;display:grid;place-items:center;background:#0b0a09;color:#ece6d6;"
            + "font:16px system-ui,sans-serif;text-align:center;padding:24px;box-sizing:border-box'><div>"
            + "<div style='color:#c4261e;font-weight:700;letter-spacing:.14em'>● EN VIVO</div>"
            + "<h2 style='margin:10px 0'>" + (nota == null ? "Buscando la PC en la wifi…" : "Sin conexión") + "</h2>"
            + "<p style='color:#968f84'>" + (nota == null ? "" : nota) + "</p>"
            + (nota == null ? "" : "<button onclick='App.reintentar()' style='font:inherit;padding:12px 20px;border-radius:10px;"
            + "border:0;background:#d6ba78;color:#1b160f;font-weight:700'>Reintentar</button>"
            + "<p style='color:#968f84;margin-top:22px'>o escribe la IP de la PC</p>"
            + "<input id=ip value='" + ip + "' inputmode=decimal style='font:inherit;padding:10px;border-radius:10px;"
            + "border:1px solid #2e2820;background:#1f1b16;color:#ece6d6;width:180px;text-align:center'> "
            + "<button onclick='App.usarIp(document.getElementById(\"ip\").value)' style='font:inherit;padding:10px 14px;"
            + "border-radius:10px;border:1px solid #2e2820;background:#1f1b16;color:#ece6d6'>Ir</button>")
            + "</div>";
        web.loadDataWithBaseURL(null, html, "text/html", "UTF-8", null);
    }

    private class Puente {
        @JavascriptInterface
        public void reintentar() { runOnUiThread(MainActivity.this::buscar); }

        @JavascriptInterface
        public void usarIp(String ip) {
            prefs.edit().putString("ip", ip.trim()).putInt("puerto", 8790).apply();
            runOnUiThread(MainActivity.this::buscar);
        }
    }

    @Override
    public void onBackPressed() {
        if (web.canGoBack()) web.goBack(); else super.onBackPressed();
    }
}
