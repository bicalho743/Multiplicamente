package com.solano.multiplicamente;

import android.app.Activity;
import android.util.Log;
import androidx.annotation.NonNull;
import com.android.billingclient.api.*;
import com.getcapacitor.*;
import com.getcapacitor.annotation.CapacitorPlugin;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.List;

@CapacitorPlugin(name = "Billing")
public class BillingPlugin extends Plugin implements PurchasesUpdatedListener {

    private static final String TAG = "BillingPlugin";
    private static final String PRODUCT_ID = "premium_unlock";
    private BillingClient billingClient;
    private PluginCall pendingPurchaseCall;

    @Override
    public void load() {
        billingClient = BillingClient.newBuilder(getContext())
                .setListener(this)
                .enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())
                // Billing 8: reconecta sozinho se o serviço do Google Play cair
                .enableAutoServiceReconnection()
                .build();
    }

    @PluginMethod
    public void initBilling(PluginCall call) {
        billingClient.startConnection(new BillingClientStateListener() {
            @Override
            public void onBillingSetupFinished(@NonNull BillingResult result) {
                if (result.getResponseCode() == BillingClient.BillingResponseCode.OK) {
                    JSObject ret = new JSObject();
                    ret.put("connected", true);
                    call.resolve(ret);
                } else {
                    call.reject("Billing setup failed: " + result.getDebugMessage());
                }
            }
            @Override
            public void onBillingServiceDisconnected() {
                Log.w(TAG, "Billing service disconnected");
            }
        });
    }

    @PluginMethod
    public void checkPurchase(PluginCall call) {
        if (!billingClient.isReady()) {
            call.reject("BillingClient not ready");
            return;
        }
        billingClient.queryPurchasesAsync(
                QueryPurchasesParams.newBuilder()
                        .setProductType(BillingClient.ProductType.INAPP)
                        .build(),
                (billingResult, purchases) -> {
                    boolean hasPremium = false;
                    for (Purchase p : purchases) {
                        if (p.getProducts().contains(PRODUCT_ID) &&
                                p.getPurchaseState() == Purchase.PurchaseState.PURCHASED) {
                            hasPremium = true;
                            if (!p.isAcknowledged()) {
                                acknowledgePurchase(p);
                            }
                        }
                    }
                    JSObject ret = new JSObject();
                    ret.put("hasPremium", hasPremium);
                    call.resolve(ret);
                }
        );
    }

    // Preço formatado do produto como está cadastrado na Play Console (ex.: "R$ 9,99")
    @PluginMethod
    public void getPrice(PluginCall call) {
        if (!billingClient.isReady()) {
            call.reject("BillingClient not ready");
            return;
        }
        List<QueryProductDetailsParams.Product> products = new ArrayList<>();
        products.add(
                QueryProductDetailsParams.Product.newBuilder()
                        .setProductId(PRODUCT_ID)
                        .setProductType(BillingClient.ProductType.INAPP)
                        .build()
        );
        billingClient.queryProductDetailsAsync(
                QueryProductDetailsParams.newBuilder().setProductList(products).build(),
                (billingResult, queryResult) -> {
                    List<ProductDetails> list = queryResult.getProductDetailsList();
                    if (billingResult.getResponseCode() != BillingClient.BillingResponseCode.OK
                            || list.isEmpty()
                            || list.get(0).getOneTimePurchaseOfferDetails() == null) {
                        call.reject("Price not available");
                        return;
                    }
                    JSObject ret = new JSObject();
                    ret.put("price", list.get(0).getOneTimePurchaseOfferDetails().getFormattedPrice());
                    call.resolve(ret);
                }
        );
    }

    @PluginMethod
    public void purchasePremium(PluginCall call) {
        if (!billingClient.isReady()) {
            call.reject("BillingClient not ready");
            return;
        }
        pendingPurchaseCall = call;
        List<QueryProductDetailsParams.Product> products = new ArrayList<>();
        products.add(
                QueryProductDetailsParams.Product.newBuilder()
                        .setProductId(PRODUCT_ID)
                        .setProductType(BillingClient.ProductType.INAPP)
                        .build()
        );
        billingClient.queryProductDetailsAsync(
                QueryProductDetailsParams.newBuilder().setProductList(products).build(),
                (billingResult, queryResult) -> {
                    // Billing 8: a resposta vem em QueryProductDetailsResult
                    List<ProductDetails> productDetailsList = queryResult.getProductDetailsList();
                    if (billingResult.getResponseCode() != BillingClient.BillingResponseCode.OK
                            || productDetailsList.isEmpty()) {
                        call.reject("Product not found: " + billingResult.getDebugMessage());
                        pendingPurchaseCall = null;
                        return;
                    }
                    ProductDetails productDetails = productDetailsList.get(0);

                    // Para INAPP (one-time purchase), NÃO usar setOfferToken
                    BillingFlowParams.ProductDetailsParams.Builder paramsBuilder =
                            BillingFlowParams.ProductDetailsParams.newBuilder()
                                    .setProductDetails(productDetails);

                    // Só usa offerToken para assinaturas
                    if (productDetails.getSubscriptionOfferDetails() != null &&
                            !productDetails.getSubscriptionOfferDetails().isEmpty()) {
                        paramsBuilder.setOfferToken(
                                productDetails.getSubscriptionOfferDetails().get(0).getOfferToken()
                        );
                    }

                    List<BillingFlowParams.ProductDetailsParams> detailsParams = new ArrayList<>();
                    detailsParams.add(paramsBuilder.build());

                    Activity activity = getActivity();
                    BillingFlowParams flowParams = BillingFlowParams.newBuilder()
                            .setProductDetailsParamsList(detailsParams)
                            .build();
                    BillingResult billingResult2 = billingClient.launchBillingFlow(activity, flowParams);
                    Log.d(TAG, "launchBillingFlow result: " + billingResult2.getResponseCode() + " " + billingResult2.getDebugMessage());
                    // Se a janela de compra não abriu, avisa o app em vez de deixá-lo esperando
                    if (billingResult2.getResponseCode() != BillingClient.BillingResponseCode.OK && pendingPurchaseCall != null) {
                        pendingPurchaseCall.reject("Purchase failed: " + billingResult2.getDebugMessage());
                        pendingPurchaseCall = null;
                    }
                }
        );
    }

    @Override
    public void onPurchasesUpdated(@NonNull BillingResult result, List<Purchase> purchases) {
        // Compras aprovadas mais tarde (ex.: pagamento pendente) chegam sem chamada aberta:
        // precisam ser reconhecidas mesmo assim, senão o Google reembolsa em 3 dias
        if (pendingPurchaseCall == null) {
            if (result.getResponseCode() == BillingClient.BillingResponseCode.OK && purchases != null) {
                for (Purchase purchase : purchases) {
                    if (purchase.getProducts().contains(PRODUCT_ID) &&
                            purchase.getPurchaseState() == Purchase.PurchaseState.PURCHASED &&
                            !purchase.isAcknowledged()) {
                        acknowledgePurchase(purchase);
                    }
                }
            }
            return;
        }
        if (result.getResponseCode() == BillingClient.BillingResponseCode.OK && purchases != null) {
            for (Purchase purchase : purchases) {
                if (purchase.getProducts().contains(PRODUCT_ID) &&
                        purchase.getPurchaseState() == Purchase.PurchaseState.PURCHASED) {
                    if (!purchase.isAcknowledged()) acknowledgePurchase(purchase);
                    JSObject ret = new JSObject();
                    ret.put("success", true);
                    ret.put("purchaseToken", purchase.getPurchaseToken());
                    pendingPurchaseCall.resolve(ret);
                    pendingPurchaseCall = null;
                    return;
                }
            }
        } else if (result.getResponseCode() == BillingClient.BillingResponseCode.USER_CANCELED) {
            pendingPurchaseCall.reject("USER_CANCELED");
        } else {
            pendingPurchaseCall.reject("Purchase failed: " + result.getDebugMessage());
        }
        pendingPurchaseCall = null;
    }

    private void acknowledgePurchase(Purchase purchase) {
        AcknowledgePurchaseParams params = AcknowledgePurchaseParams.newBuilder()
                .setPurchaseToken(purchase.getPurchaseToken())
                .build();
        billingClient.acknowledgePurchase(params, r ->
                Log.d(TAG, "Acknowledge result: " + r.getResponseCode())
        );
    }
}