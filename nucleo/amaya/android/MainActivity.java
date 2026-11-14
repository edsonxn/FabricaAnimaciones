package mx.clicknbusiness.amaya;

// App «Estudio Amaya» (10-nov-2026): la hija de Edson habla con Claude para crear videos con la fábrica.
// Un WebView a pantalla completa que abre clicknbusiness.com.mx/amaya/ (reenvía al túnel de hoy) con SU llave en el «#»
// (no viaja en la petición: la página la guarda en el teléfono). Fotos (selector), micrófono (notas de voz), descargas de
// sus videos (DownloadManager con la cookie) y una pantalla propia cuando no hay internet.
// Lo construye nucleo/amaya/android/construir_apk.py, sin Gradle (@CLAVE@ se rellena al compilar; el .apk no va a git).

import android.Manifest;
import android.app.Activity;
import android.app.DownloadManager;
import android.content.ClipData;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.CookieManager;
import android.webkit.PermissionRequest;
import android.webkit.URLUtil;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.Toast;

public class MainActivity extends Activity {
    static final String INICIO = "https://clicknbusiness.com.mx/amaya/#k=@CLAVE@";
    static final int FONDO = Color.parseColor("#1a1033");
    static final int PIDE_ARCHIVO = 41, PIDE_MICRO = 42;
    private WebView web;
    private FrameLayout raiz;
    private View pantallaCompleta;
    private WebChromeClient.CustomViewCallback alCerrar;
    private ValueCallback<Uri[]> archivosCb;
    private PermissionRequest microPendiente;
    private String agente;

    static final String PAGINA_ERROR = "<!doctype html><html lang=es><head><meta charset=utf-8>"
        + "<meta name=viewport content='width=device-width,initial-scale=1'><style>"
        + "body{margin:0;min-height:100vh;display:grid;place-items:center;background:radial-gradient(120% 80% at 50% 0%,#3a1d6e,#1a1033 60%);"
        + "color:#fff;font:17px/1.45 system-ui,sans-serif;text-align:center;padding:24px;box-sizing:border-box}"
        + ".e{font-size:72px}h1{font-size:23px;margin:8px 0}p{color:#d7c9ff;margin:6px 0 22px}"
        + "a{display:block;padding:15px;border-radius:16px;background:linear-gradient(90deg,#ff5fa8,#ffb35c);color:#2a0f3d;font-weight:800;text-decoration:none}"
        + "small{display:block;margin-top:16px;color:#a996e0}</style></head><body><div style='width:min(340px,100%)'>"
        + "<div class=e>📡</div><h1>Sin conexión</h1><p>Tu teléfono no tiene internet ahorita.<br>Revisa el wifi o los datos y vuelve a intentar.</p>"
        + "<a href='" + INICIO + "'>Reintentar</a><small>Estudio Amaya 💜 hecho por papá Edson</small></div></body></html>";

    @Override
    protected void onCreate(Bundle estado) {
        super.onCreate(estado);
        getWindow().setStatusBarColor(FONDO);
        getWindow().setNavigationBarColor(FONDO);
        raiz = new FrameLayout(this);
        raiz.setBackgroundColor(FONDO);
        web = new WebView(this);
        web.setBackgroundColor(FONDO);
        raiz.addView(web, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        setContentView(raiz);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setAllowFileAccess(false);
        // ngrok gratis enseña «You are about to visit…» a los navegadores: con un agente propio entra directo
        long version = 0;
        try { version = getPackageManager().getPackageInfo(getPackageName(), 0).versionCode; } catch (Exception e) { }
        agente = "AmayaApp/1.0 (Android " + Build.VERSION.RELEASE + ") v=" + version;
        s.setUserAgentString(agente);
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(web, true);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                Uri u = r.getUrl();
                String host = u.getHost() == null ? "" : u.getHost();
                boolean nuestro = host.equals("clicknbusiness.com.mx") || host.endsWith(".ngrok-free.app")
                        || host.endsWith(".ngrok.app") || host.endsWith(".trycloudflare.com");
                if (nuestro && u.getQueryParameter("bajar") != null) { bajar(u.toString(), null, "video/mp4"); return true; }
                if (nuestro) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (Exception e) { }
                return true;
            }

            @Override
            public void onReceivedError(WebView v, WebResourceRequest r, WebResourceError e) {
                if (r.isForMainFrame()) v.loadDataWithBaseURL(null, PAGINA_ERROR, "text/html", "utf-8", null);
            }
        });
        web.setDownloadListener((url, ua, disposicion, tipo, largo) -> bajar(url, disposicion, tipo));
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams p) {
                if (archivosCb != null) archivosCb.onReceiveValue(null);
                archivosCb = cb;
                Intent i = p.createIntent();
                if (p.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE) i.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                try { startActivityForResult(Intent.createChooser(i, "Elige tus fotos"), PIDE_ARCHIVO); }
                catch (Exception e) { archivosCb = null; return false; }
                return true;
            }

            @Override
            public void onPermissionRequest(PermissionRequest pedido) {
                boolean audio = false;
                for (String r : pedido.getResources()) if (PermissionRequest.RESOURCE_AUDIO_CAPTURE.equals(r)) audio = true;
                if (!audio) { pedido.deny(); return; }
                if (checkSelfPermission(Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
                    pedido.grant(new String[]{PermissionRequest.RESOURCE_AUDIO_CAPTURE});
                } else {
                    microPendiente = pedido;
                    requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, PIDE_MICRO);
                }
            }

            @Override
            public void onShowCustomView(View vista, CustomViewCallback cb) {         // video a pantalla completa
                if (pantallaCompleta != null) { cb.onCustomViewHidden(); return; }
                pantallaCompleta = vista;
                alCerrar = cb;
                raiz.addView(vista, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
                web.setVisibility(View.GONE);
            }

            @Override
            public void onHideCustomView() {
                if (pantallaCompleta == null) return;
                raiz.removeView(pantallaCompleta);
                pantallaCompleta = null;
                web.setVisibility(View.VISIBLE);
                if (alCerrar != null) alCerrar.onCustomViewHidden();
            }
        });
        if (estado != null) web.restoreState(estado);
        else web.loadUrl(INICIO);
    }

    void bajar(String url, String disposicion, String tipo) {
        try {
            Uri u = Uri.parse(url);
            String nombre = u.getQueryParameter("bajar");
            if (nombre == null || nombre.isEmpty()) nombre = URLUtil.guessFileName(url, disposicion, tipo);
            nombre = nombre.replaceAll("[\\\\/:*?\"<>|]", "_");
            DownloadManager.Request q = new DownloadManager.Request(u);
            String galleta = CookieManager.getInstance().getCookie(url);
            if (galleta != null) q.addRequestHeader("Cookie", galleta);
            q.addRequestHeader("User-Agent", agente);
            q.addRequestHeader("ngrok-skip-browser-warning", "1");
            q.setMimeType(tipo == null || tipo.isEmpty() ? "video/mp4" : tipo);
            q.setTitle(nombre);
            q.setDescription("Estudio Amaya");
            q.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            q.setDestinationInExternalPublicDir(Environment.DIRECTORY_MOVIES, "Estudio Amaya/" + nombre);
            ((DownloadManager) getSystemService(Context.DOWNLOAD_SERVICE)).enqueue(q);
            Toast.makeText(this, "Guardando «" + nombre + "» en Películas/Estudio Amaya ⬇️", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            Toast.makeText(this, "No pude guardar el video: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    @Override
    protected void onActivityResult(int pedido, int resultado, Intent datos) {
        if (pedido != PIDE_ARCHIVO || archivosCb == null) { super.onActivityResult(pedido, resultado, datos); return; }
        Uri[] res = null;
        if (resultado == RESULT_OK && datos != null) {
            ClipData clip = datos.getClipData();
            if (clip != null) {
                res = new Uri[clip.getItemCount()];
                for (int i = 0; i < clip.getItemCount(); i++) res[i] = clip.getItemAt(i).getUri();
            } else if (datos.getData() != null) {
                res = new Uri[]{datos.getData()};
            }
        }
        archivosCb.onReceiveValue(res);
        archivosCb = null;
    }

    @Override
    public void onRequestPermissionsResult(int pedido, String[] permisos, int[] r) {
        if (pedido != PIDE_MICRO || microPendiente == null) return;
        if (r.length > 0 && r[0] == PackageManager.PERMISSION_GRANTED)
            microPendiente.grant(new String[]{PermissionRequest.RESOURCE_AUDIO_CAPTURE});
        else {
            microPendiente.deny();
            Toast.makeText(this, "Sin micrófono no puedo oír tus notas de voz 🎤", Toast.LENGTH_LONG).show();
        }
        microPendiente = null;
    }

    @Override
    public void onBackPressed() {
        if (pantallaCompleta != null) { web.getWebChromeClient().onHideCustomView(); return; }
        if (web.canGoBack()) web.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onSaveInstanceState(Bundle salida) {
        super.onSaveInstanceState(salida);
        web.saveState(salida);
    }

    @Override
    protected void onPause() {
        super.onPause();
        web.onPause();
        CookieManager.getInstance().flush();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
    }
}
