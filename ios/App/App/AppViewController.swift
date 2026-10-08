import UIKit
import Capacitor

/// The app's web view controller. Registers plugins that live in this app (not in npm packages).
class AppViewController: CAPBridgeViewController {
    override open func capacitorDidLoad() {
        bridge?.registerPluginInstance(ClipPlayerPlugin())
    }
}
