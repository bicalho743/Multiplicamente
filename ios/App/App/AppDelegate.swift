import UIKit
import Capacitor
import StoreKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }

    func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey: Any] = [:]) -> Bool {
        // Called when the app was launched with a url. Feel free to add additional processing here,
        // but if you want the App API to support tracking app url opens, make sure to keep this call
        return ApplicationDelegateProxy.shared.application(app, open: url, options: options)
    }

    func application(_ application: UIApplication, continue userActivity: NSUserActivity, restorationHandler: @escaping ([UIUserActivityRestoring]?) -> Void) -> Bool {
        // Called when the app was launched with an activity, including Universal Links.
        // Feel free to add additional processing here, but if you want the App API to support
        // tracking app url opens, make sure to keep this call
        return ApplicationDelegateProxy.shared.application(application, continue: userActivity, restorationHandler: restorationHandler)
    }

}

// MARK: - Tela principal: registra os plugins nativos do app

/// Usada no Main.storyboard no lugar da CAPBridgeViewController padrão.
class MainViewController: CAPBridgeViewController {
    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(BillingPlugin())
        bridge?.registerPluginInstance(ReviewPlugin())
    }
}

// MARK: - Compra do Premium pela App Store (StoreKit 2)

/// Mesmo nome e mesmos métodos do BillingPlugin do Android ("Billing"),
/// para o JavaScript funcionar igual nas duas lojas.
@objc(BillingPlugin)
public class BillingPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "BillingPlugin"
    public let jsName = "Billing"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "initBilling", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "getPrice", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "checkPurchase", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "purchasePremium", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "restore", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "redeemCode", returnType: CAPPluginReturnPromise)
    ]

    /// Produto "não consumível" criado no App Store Connect com este mesmo ID.
    private let productId = "premium_unlock"
    private var updatesTask: Task<Void, Never>?

    override public func load() {
        // Compras aprovadas fora da tela de compra (pagamento pendente, Ask to Buy,
        // código de oferta) chegam aqui e precisam ser finalizadas.
        updatesTask = Task.detached {
            for await result in Transaction.updates {
                if case .verified(let transaction) = result {
                    await transaction.finish()
                }
            }
        }
    }

    deinit {
        updatesTask?.cancel()
    }

    @objc func initBilling(_ call: CAPPluginCall) {
        call.resolve(["connected": true])
    }

    @objc func getPrice(_ call: CAPPluginCall) {
        Task {
            do {
                let products = try await Product.products(for: [productId])
                guard let product = products.first else {
                    call.reject("Price not available")
                    return
                }
                call.resolve(["price": product.displayPrice])
            } catch {
                call.reject("Price not available")
            }
        }
    }

    /// Compra válida (não reembolsada) na conta Apple deste aparelho.
    @objc func checkPurchase(_ call: CAPPluginCall) {
        Task {
            var hasPremium = false
            for await result in Transaction.currentEntitlements {
                if case .verified(let transaction) = result,
                   transaction.productID == productId,
                   transaction.revocationDate == nil {
                    hasPremium = true
                }
            }
            call.resolve(["hasPremium": hasPremium])
        }
    }

    @objc func purchasePremium(_ call: CAPPluginCall) {
        Task {
            do {
                guard let product = try await Product.products(for: [productId]).first else {
                    call.reject("Product not found")
                    return
                }
                let result = try await product.purchase()
                switch result {
                case .success(let verification):
                    switch verification {
                    case .verified(let transaction):
                        await transaction.finish()
                        call.resolve(["success": true])
                    case .unverified:
                        call.reject("Purchase failed: unverified")
                    }
                case .pending:
                    // Ask to Buy (compra que depende da aprovação de um responsável) ou pagamento pendente
                    call.resolve(["success": false, "pending": true])
                case .userCancelled:
                    call.reject("USER_CANCELED")
                @unknown default:
                    call.reject("Purchase failed")
                }
            } catch {
                call.reject("Purchase failed: \(error.localizedDescription)")
            }
        }
    }

    /// "Restaurar compra": sincroniza com a App Store (pode pedir o ID Apple).
    @objc func restore(_ call: CAPPluginCall) {
        Task {
            do {
                try await AppStore.sync()
                call.resolve()
            } catch {
                call.reject("Restore failed")
            }
        }
    }

    /// Abre a tela da Apple para resgatar um código de oferta (substitui o cupom no iPhone).
    @objc func redeemCode(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            SKPaymentQueue.default().presentCodeRedemptionSheet()
            call.resolve()
        }
    }
}

// MARK: - Pedido de avaliação na App Store

/// Mesmo nome do ReviewPlugin do Android ("Review").
@objc(ReviewPlugin)
public class ReviewPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "ReviewPlugin"
    public let jsName = "Review"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "requestReview", returnType: CAPPluginReturnPromise)
    ]

    @objc func requestReview(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            // A Apple decide se mostra (há limite de vezes por ano)
            if let scene = UIApplication.shared.connectedScenes
                .first(where: { $0.activationState == .foregroundActive }) as? UIWindowScene {
                SKStoreReviewController.requestReview(in: scene)
            }
            call.resolve()
        }
    }
}
