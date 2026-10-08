import Foundation
import Capacitor
import AVFoundation

/// Plays one recorded voice line at a time, even with the screen locked.
/// Music and podcasts duck (or pause, for spoken audio) while a line plays, then come back.
@objc(ClipPlayerPlugin)
public class ClipPlayerPlugin: CAPPlugin, CAPBridgedPlugin, AVAudioPlayerDelegate {
    public let identifier = "ClipPlayerPlugin"
    public let jsName = "ClipPlayer"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "play", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "stop", returnType: CAPPluginReturnPromise),
    ]

    private var player: AVAudioPlayer?
    private var pending: CAPPluginCall?

    /// play({ data: base64 m4a, volume?: 0...1 }) resolves { completed: Bool } when the line ends or is cut off.
    @objc func play(_ call: CAPPluginCall) {
        guard let b64 = call.getString("data"), let data = Data(base64Encoded: b64) else {
            call.reject("data (base64 audio) is required")
            return
        }
        let volume = call.getFloat("volume") ?? 1.0
        DispatchQueue.main.async {
            do {
                let session = AVAudioSession.sharedInstance()
                try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers, .interruptSpokenAudioAndMixWithOthers])
                try session.setActive(true)
                self.finish(completed: false, release: false)
                let p = try AVAudioPlayer(data: data)
                p.delegate = self
                p.volume = volume
                self.player = p
                self.pending = call
                if !p.play() { self.finish(completed: false, release: true) }
            } catch {
                call.reject("Couldn't play the clip: \(error.localizedDescription)")
            }
        }
    }

    @objc func stop(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            self.player?.stop()
            self.finish(completed: false, release: true)
            call.resolve()
        }
    }

    public func audioPlayerDidFinishPlaying(_ p: AVAudioPlayer, successfully flag: Bool) {
        finish(completed: flag, release: true)
    }

    private func finish(completed: Bool, release: Bool) {
        if let c = pending {
            pending = nil
            c.resolve(["completed": completed])
        }
        if release {
            player = nil
            // Let ducked music come back up.
            try? AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)
        }
    }
}
