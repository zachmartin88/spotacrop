import WidgetKit
import SwiftUI

/// Home-screen widget: today's crop of the day (the same one the app features), refreshed at midnight.
struct Entry: TimelineEntry { let date: Date; let crop: Crop }

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> Entry { Entry(date: Date(), crop: CropDays.crop(on: Date())) }
    func getSnapshot(in context: Context, completion: @escaping (Entry) -> Void) { completion(placeholder(in: context)) }
    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> Void) {
        let cal = Calendar.current, now = Date()
        // Today, then each of the next few midnights.
        var entries = [Entry(date: now, crop: CropDays.crop(on: now))]
        var day = cal.startOfDay(for: now)
        for _ in 0..<7 {
            day = cal.date(byAdding: .day, value: 1, to: day)!
            entries.append(Entry(date: day, crop: CropDays.crop(on: day.addingTimeInterval(60))))
        }
        completion(Timeline(entries: entries, policy: .atEnd))
    }
}

private let gold = Color(red: 232 / 255, green: 193 / 255, blue: 112 / 255)
private let ink = Color(red: 15 / 255, green: 18 / 255, blue: 24 / 255)

struct CropWidgetView: View {
    @Environment(\.widgetFamily) var family
    let entry: Entry
    var body: some View {
        Group {
            if family == .systemMedium {
                HStack(spacing: 14) {
                    Text(entry.crop.emoji).font(.system(size: 64))
                    VStack(alignment: .leading, spacing: 4) {
                        Text("CROP OF THE DAY").font(.system(size: 11, weight: .heavy)).foregroundColor(gold).kerning(1)
                        Text(entry.crop.name).font(.system(size: 24, weight: .heavy)).foregroundColor(.white).lineLimit(1).minimumScaleFactor(0.7)
                        Text(entry.crop.note.isEmpty ? "Keep an eye out on your next drive." : "Look for: \(entry.crop.note)")
                            .font(.system(size: 13, weight: .medium)).foregroundColor(.white.opacity(0.7)).lineLimit(2)
                    }
                    Spacer(minLength: 0)
                }
            } else {
                VStack(alignment: .leading, spacing: 2) {
                    Text("CROP OF THE DAY").font(.system(size: 10, weight: .heavy)).foregroundColor(gold).kerning(0.8)
                    Spacer(minLength: 0)
                    Text(entry.crop.emoji).font(.system(size: 48))
                    Spacer(minLength: 0)
                    Text(entry.crop.name).font(.system(size: 18, weight: .heavy)).foregroundColor(.white).lineLimit(1).minimumScaleFactor(0.6)
                }
                .frame(maxWidth: .infinity, alignment: .leading)
            }
        }
        .widgetURL(URL(string: "spotacrop://cotd"))
        .containerBackground(for: .widget) {
            ZStack {
                ink
                RadialGradient(colors: [gold.opacity(0.28), .clear], center: .topTrailing, startRadius: 0, endRadius: 220)
            }
        }
    }
}

@main
struct CropWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "CropOfTheDay", provider: Provider()) { entry in
            CropWidgetView(entry: entry)
        }
        .configurationDisplayName("Crop of the day")
        .description("A new crop to spot every day.")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
