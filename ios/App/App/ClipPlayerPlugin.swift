import Foundation
import Capacitor
import AVFoundation
import MediaPlayer
import UIKit

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
    private var remoteReady = false

    /// Lock screen / steering wheel buttons: pause mutes the voice, play turns it back on (JS decides what that means).
    private func setUpRemote() {
        if remoteReady { return }
        remoteReady = true
        let c = MPRemoteCommandCenter.shared()
        c.pauseCommand.isEnabled = true
        c.playCommand.isEnabled = true
        c.togglePlayPauseCommand.isEnabled = true
        c.nextTrackCommand.isEnabled = false
        c.previousTrackCommand.isEnabled = false
        c.pauseCommand.addTarget { [weak self] _ in self?.remote("pause"); return .success }
        c.playCommand.addTarget { [weak self] _ in self?.remote("play"); return .success }
        c.togglePlayPauseCommand.addTarget { [weak self] _ in self?.remote("toggle"); return .success }
    }

    private func remote(_ action: String) {
        if action != "play" { player?.stop(); finish(completed: false, release: true) }
        notifyListeners("remote", data: ["action": action])
    }

    private func showNowPlaying(title: String, artist: String, duration: TimeInterval) {
        var info: [String: Any] = [
            MPMediaItemPropertyTitle: title,
            MPMediaItemPropertyArtist: artist,
            MPMediaItemPropertyAlbumTitle: "Spot-a-Crop",
            MPMediaItemPropertyPlaybackDuration: duration,
            MPNowPlayingInfoPropertyElapsedPlaybackTime: 0,
            MPNowPlayingInfoPropertyPlaybackRate: 1.0,
        ]
        if let icon = UIImage(named: "AppIcon") ?? Bundle.main.icon {
            info[MPMediaItemPropertyArtwork] = MPMediaItemArtwork(boundsSize: icon.size) { _ in icon }
        }
        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
    }

    /// play({ data: base64 m4a, volume?: 0...1, title?, artist? }) resolves { completed: Bool } when the line ends or is cut off.
    @objc func play(_ call: CAPPluginCall) {
        guard let b64 = call.getString("data"), let data = Data(base64Encoded: b64) else {
            call.reject("data (base64 audio) is required")
            return
        }
        let volume = call.getFloat("volume") ?? 1.0
        let title = call.getString("title") ?? "Spot-a-Crop"
        let artist = call.getString("artist") ?? ""
        DispatchQueue.main.async {
            self.setUpRemote()
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
                self.showNowPlaying(title: title, artist: artist, duration: p.duration)
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

private extension Bundle {
    /// The app icon as an image, for the lock-screen card.
    var icon: UIImage? {
        guard let icons = infoDictionary?["CFBundleIcons"] as? [String: Any],
              let primary = icons["CFBundlePrimaryIcon"] as? [String: Any],
              let files = primary["CFBundleIconFiles"] as? [String],
              let last = files.last else { return nil }
        return UIImage(named: last)
    }
}
