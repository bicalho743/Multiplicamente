package com.solano.multiplicamente;

import com.getcapacitor.BridgeActivity;
import android.os.Bundle;
import android.webkit.WebSettings;
import com.codetrixstudio.capacitor.GoogleAuth.GoogleAuth;

public class MainActivity extends BridgeActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        registerPlugin(BillingPlugin.class);
        registerPlugin(ReviewPlugin.class);
        registerPlugin(GoogleAuth.class);
        super.onCreate(savedInstanceState);
        // Fonte do sistema muito grande quebra o layout do jogo: limita o zoom de texto a 115%
        WebSettings ws = getBridge().getWebView().getSettings();
        float scale = getResources().getConfiguration().fontScale;
        ws.setTextZoom((int) Math.min(scale * 100, 115));
    }
}