package com.solano.multiplicamente;

import com.getcapacitor.*;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.google.android.play.core.review.ReviewInfo;
import com.google.android.play.core.review.ReviewManager;
import com.google.android.play.core.review.ReviewManagerFactory;

// Abre a janela de avaliação do Google Play sem sair do app.
// O Google decide se mostra ou não (há limite de vezes por usuário).
@CapacitorPlugin(name = "Review")
public class ReviewPlugin extends Plugin {

    @PluginMethod
    public void requestReview(PluginCall call) {
        ReviewManager manager = ReviewManagerFactory.create(getContext());
        manager.requestReviewFlow().addOnCompleteListener(task -> {
            if (!task.isSuccessful()) {
                call.reject("Review flow unavailable");
                return;
            }
            ReviewInfo info = task.getResult();
            manager.launchReviewFlow(getActivity(), info).addOnCompleteListener(t -> call.resolve());
        });
    }
}
