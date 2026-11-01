package mx.clicknbusiness.fabrica;

// App «Fábrica» (28-oct-2026): un WebView a pantalla completa que abre la dirección fija del panel en el dominio
// (clicknbusiness.com.mx/panel/ reenvía al túnel de hoy). La clave se escribe una vez en la página «Entrar» y queda en la
// cookie del WebView (30 días). Lo construye nucleo/app_movil/android/construir_apk.py, sin Gradle.

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.CookieManager;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;

public class MainActivity extends Activity {
    static final String INICIO = "https://clicknbusiness.com.mx/panel/";
    static final int FONDO = Color.parseColor("#090b12");
    private WebView web;
    private FrameLayout raiz;
    private View pantallaCompleta;
    private WebChromeClient.CustomViewCallback alCerrar;

    @Override
    protected void onCreate(Bundle estado) {
        super.onCreate(estado);
        getWindow().setStatusBarColor(FONDO);
        getWindow().setNavigationBarColor(FONDO);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
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
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        // ngrok gratis muestra «You are about to visit…» solo a los navegadores: con un agente propio entra directo
        // «v=<versionCode>»: actualiza.js compara con el APK publicado y ofrece la app nueva al entrar
        long version = 0;
        try { version = getPackageManager().getPackageInfo(getPackageName(), 0).versionCode; } catch (Exception e) { }
        s.setUserAgentString("FabricaApp/1.0 (Android " + android.os.Build.VERSION.RELEASE + ") v=" + version);
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(web, true);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) {
                Uri u = r.getUrl();
                String host = u.getHost() == null ? "" : u.getHost();
                String ruta = u.getPath() == null ? "" : u.getPath();
                boolean nuestro = host.equals("clicknbusiness.com.mx") || host.endsWith(".ngrok-free.app")
                        || host.endsWith(".ngrok.app") || host.endsWith(".trycloudflare.com");
                if (nuestro && !ruta.endsWith(".apk")) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (Exception e) { }
                return true;
            }
        });
        web.setWebChromeClient(new WebChromeClient() {                 // video a pantalla completa
            @Override
            public void onShowCustomView(View vista, CustomViewCallback cb) {
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
