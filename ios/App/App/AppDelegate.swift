import UIKit
import Capacitor
import StoreKit
import AuthenticationServices

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
        bridge?.registerPluginInstance(AppleSignInPlugin())
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

// MARK: - Entrar com a Apple (iPhone/iPad)

/// Usado pelo www/index.html: SignInWithApple.authorize({ nonce, scopes, state }).
/// Feito à mão para não depender de plugin de terceiros (o Capacitor 8 do app exige isso).
@objc(AppleSignInPlugin)
public class AppleSignInPlugin: CAPPlugin, CAPBridgedPlugin, ASAuthorizationControllerDelegate, ASAuthorizationControllerPresentationContextProviding {
    public let identifier = "AppleSignInPlugin"
    public let jsName = "SignInWithApple"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "authorize", returnType: CAPPluginReturnPromise)
    ]

    private var pendingCall: CAPPluginCall?
    private var authController: ASAuthorizationController?

    @objc func authorize(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            let request = ASAuthorizationAppleIDProvider().createRequest()
            var scopes: [ASAuthorization.Scope] = []
            let scopesStr = call.getString("scopes") ?? ""
            if scopesStr.contains("name") { scopes.append(.fullName) }
            if scopesStr.contains("email") { scopes.append(.email) }
            request.requestedScopes = scopes
            request.state = call.getString("state")
            // Com o nonce já em SHA-256 (o JS envia o hash; o Firebase recebe o original)
            request.nonce = call.getString("nonce")

            self.pendingCall = call
            self.bridge?.saveCall(call)
            let controller = ASAuthorizationController(authorizationRequests: [request])
            controller.delegate = self
            controller.presentationContextProvider = self
            self.authController = controller
            controller.performRequests()
        }
    }

    public func authorizationController(controller: ASAuthorizationController, didCompleteWithAuthorization authorization: ASAuthorization) {
        guard let call = pendingCall else { return }
        pendingCall = nil
        guard let cred = authorization.credential as? ASAuthorizationAppleIDCredential,
              let tokenData = cred.identityToken,
              let identityToken = String(data: tokenData, encoding: .utf8) else {
            call.reject("Token da Apple não recebido.")
            self.bridge?.releaseCall(call)
            return
        }
        let code = cred.authorizationCode.flatMap { String(data: $0, encoding: .utf8) } ?? ""
        call.resolve([
            "response": [
                "user": cred.user,
                "email": cred.email ?? "",
                "givenName": cred.fullName?.givenName ?? "",
                "familyName": cred.fullName?.familyName ?? "",
                "identityToken": identityToken,
                "authorizationCode": code
            ]
        ])
        self.bridge?.releaseCall(call)
    }

    public func authorizationController(controller: ASAuthorizationController, didCompleteWithError error: Error) {
        guard let call = pendingCall else { return }
        pendingCall = nil
        let nsErr = error as NSError
        if nsErr.code == ASAuthorizationError.canceled.rawValue {
            call.reject("The user canceled the authorization attempt.")
        } else {
            call.reject(error.localizedDescription)
        }
        self.bridge?.releaseCall(call)
    }

    public func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {
        let windows = UIApplication.shared.connectedScenes
            .compactMap { $0 as? UIWindowScene }
            .flatMap { $0.windows }
        return windows.first(where: { $0.isKeyWindow }) ?? windows.first ?? UIWindow()
    }
}
