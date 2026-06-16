package com.solano.multiplicamente;

import com.getcapacitor.BridgeActivity;
import android.os.Bundle;
import com.codetrixstudio.capacitor.GoogleAuth.GoogleAuth;

public class MainActivity extends BridgeActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        registerPlugin(BillingPlugin.class);
        registerPlugin(GoogleAuth.class);
        super.onCreate(savedInstanceState);
    }
}