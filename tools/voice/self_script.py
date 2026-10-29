# Read-aloud scripts for characters voiced by a real person (no voice cloning).
# Most-heard lines are read whole; everything else is stitched at pack time from short pieces
# (a crop name + a side tail, a welcome intro + a state name), so the reading stays around 250 lines.
#   self_script.py            -> writes ~/spotacrop-voices/self/<char>/script.json and prints each script as markdown
import json, os
from pathlib import Path
from lines import CROPS, STATES

OUT = Path(os.path.expanduser('~/spotacrop-voices/self'))
TOP = [1, 5, 37, 24, 36, 2, 23, 4, 3, 21, 6, 43]   # crops heard most: read as whole sentences

CHARS = {
    'cornbeard': {
        'title': 'Captain Cornbeard',
        'left': ["{X} off the port bow! That's your left, matey.", "Arr, {x} to port!"],
        'right': ["{X} off the starboard bow! That's your right, matey.", "Arr, {x} to starboard!"],
        'both': ["{X} to port and starboard! Both sides, matey!"],
        'tails': {'left': ["Off the port bow! That's your left, matey.", "To port, me hearties!"],
                  'right': ["Off the starboard bow! That's your right, matey.", "To starboard, me hearties!"],
                  'around': ["On every side! We be surrounded, crew!"], 'both': ["To port and starboard! Both sides!"]},
        'welcome': ["Ahoy! We've sailed into...", "Land ho! Welcome to..."],
        'moments': {
            'hello': ["Ahoy! Captain Cornbeard at the helm. I'll call out the crops, port and starboard!", "Ahoy, matey! Let's sail these fields!", "All hands on deck! Crop spottin' time!"],
            'start:morning': ["Mornin', crew! Raise the anchor!"], 'start:afternoon': ["Afternoon, crew! Fair winds today!"],
            'start:evening': ["Evening, crew! Red sky at night, sailor's delight!"], 'start:night': ["A night voyage! Steer by the stars, matey."],
            'end': ["Drop anchor! Good voyage, matey.", "And that's the end of the voyage. Arr!"],
            'card': ["A new card for the treasure chest!", "New card! Into the chest it goes!"],
            'rare': ["A rare treasure! Rarer than gold doubloons!"], 'badge': ["A badge! Ye've earned yer stripes, matey!"],
            'bingo:square': ["A bingo square! Mark it on the map!"], 'bingo': ["Bingo! Arr, we found the treasure!"],
            'gps:lost': ["We've lost our bearings! Hold fast, crew!"], 'gps:back': ["Back on course, matey!"],
            'streak': ["Same crop for leagues and leagues!", "Still the same, crew. Steady as she goes."],
            'streak:1': ["Still corn! A whole ocean of it!"],
            'spot:town': ["A port town! Shore leave, crew."], 'spot:water': ["Water! Now that's more like it."],
            'spot:woods': ["Trees! Good timber for a ship."], 'spot:pasture': ["Pasture. The cows be grazin', calm as a sea at dawn."],
            'spot:bridge': ["Water on both sides! Now this is proper sailin'!"],
            'speed:fast': ["Easy on the sails, matey! Slow 'er down!"], 'speed:slow': ["Becalmed, matey! No wind in the sails!"],
            'miles:10': ["Ten miles! A fine start, matey!"], 'miles:50': ["Fifty miles! A fine voyage!"], 'miles:100': ["A hundred miles! Arr, what a voyage!"],
        },
        'extras': {
            'joke': ["Why did the scarecrow win an award? He was outstanding in his field. Arr!", "What did the corn say when it got a compliment? Aw, shucks!",
                     "Why are pigs bad drivers? They hog the road!", "What kind of music do tractors like? Heavy metal! Arr!", "Why did the corn go to the party? To get popped!"],
            'banter': ["A pirate's life for me. Well, a farm pirate.", "If ye see a scarecrow with an eye patch, that's me cousin.", "Arr, these roads be calmer than the open sea."],
            'meme': ["Arr, the treasure was the friends we made along the way.", "This crew has rizz. Arr.", "Hold me grog!"],
            'holiday:halloween': ["Halloween! A pirate's favorite night!"], 'season:fall': ["Harvest season! The farmers be haulin' in their treasure!"],
        },
    },
    'earl': {
        'title': 'Earl',
        'left': ["{X} on your left.", "Lookee yonder, {x} on your left, partner."],
        'right': ["{X} on your right.", "Lookee yonder, {x} on your right, partner."],
        'both': ["{X} on both sides, partner."],
        'tails': {'left': ["On your left, partner.", "Off to the left there."],
                  'right': ["On your right, partner.", "Off to the right there."],
                  'around': ["All around us, partner."], 'both': ["On both sides, partner."]},
        'welcome': ["Well, welcome to...", "Here we are, partner..."],
        'moments': {
            'hello': ["Howdy. I'll holler out the crops as we go.", "Alright, partner. I'll keep an eye on the fields.", "Well, let's see what's growin'."],
            'start:morning': ["Mornin'. Good day for a drive."], 'start:afternoon': ["Afternoon. Let's see what's growin'."],
            'start:evening': ["Evenin'. Fields look their best this time of day."], 'start:night': ["Night drive, huh. I'll keep talkin' so you stay awake."],
            'end': ["Good drive, partner. See ya next time.", "That's a wrap. Fields'll be here when ya get back."],
            'card': ["New crop card for the collection.", "Well, there's a new card."],
            'rare': ["Well, I'll be. That's a rare one."], 'badge': ["You earned yourself a badge."],
            'bingo:square': ["Check that one off the bingo card."], 'bingo': ["Bingo! Well, how about that."],
            'gps:lost': ["Lost the signal there. Hang tight."], 'gps:back': ["There we go. Back on track."],
            'streak': ["Same crop for a while now. Consistent.", "Long stretch of the same. Farmers like what works."],
            'streak:1': ["Still corn. I'd act surprised, but I'd be lyin'."],
            'spot:town': ["Bit of town here. Houses ain't a crop, last I checked."], 'spot:water': ["Little water there. The ducks are happy."],
            'spot:woods': ["Bit of woods. Good shade for the deer."], 'spot:pasture': ["Pasture. That's the cow buffet."],
            'spot:bridge': ["Crossin' the water. Good fishin' down there, I bet."],
            'speed:fast': ["Easy there, partner. The corn ain't goin' anywhere."], 'speed:slow': ["Slow goin'. Gives ya time to admire the scenery."],
            'miles:10': ["That's ten miles. Not bad, partner."], 'miles:50': ["Fifty miles. Not bad at all."], 'miles:100': ["A hundred miles, partner. Now that's a drive."],
        },
        'extras': {
            'joke': ["Here's one for ya. Why did the scarecrow win an award? He was outstanding in his field.", "What did the corn say when it got a compliment? Aw, shucks.",
                     "Why did the farmer ride his horse to town? It was too heavy to carry.", "What do you call a sleeping bull? A bulldozer.", "How does a farmer mend his overalls? With cabbage patches."],
            'banter': ["Ever notice how the barns are all red? Cheap paint, back in the day.", "A farmer's best friend is a good forecast.", "Combines cost more than most houses. True story."],
            'meme': ["Hold my sweet tea.", "Somebody told me 'no cap.' I said I got three caps, all of 'em John Deere.", "My grandson says I got main character energy. I told him I got tractor energy."],
            'holiday:halloween': ["Halloween's comin'. Them pumpkins are nervous."], 'season:fall': ["Harvest time. Best time of year, if ya ask me."],
        },
    },
    'auntie': {
        'title': 'Caribbean auntie',
        'left': ["Ooh, {x} on the left, darlin'!", "Look at the {x} on your left!"],
        'right': ["Ooh, {x} on the right, darlin'!", "Look at the {x} on your right!"],
        'both': ["{X} on both sides, sweetheart!"],
        'tails': {'left': ["On your left, darlin'!", "Over on the left, sweetheart!"],
                  'right': ["On your right, darlin'!", "Over on the right, sweetheart!"],
                  'around': ["All around us, darlin'!"], 'both': ["On both sides, sweetheart!"]},
        'welcome': ["Welcome, welcome, to...", "Ooh, darlin', we're in..."],
        'moments': {
            'hello': ["Hello, darlin'! I'll tell you what's growin' as we go.", "Come, let's go spot some crops!", "Auntie's here! Let's see what's growin'!"],
            'start:morning': ["Good mornin', darlin'! You ate breakfast?"], 'start:afternoon': ["Good afternoon, sweetheart! Drive careful now."],
            'start:evening': ["Good evenin', darlin'! Look how pretty the light is."], 'start:night': ["It's late, darlin'. Drive careful, you hear?"],
            'end': ["That was a lovely drive, darlin'. Go rest yourself.", "Bye bye, sweetheart! Call me when you get home!"],
            'card': ["A new card, darlin'! Look at you!", "Ooh, another card for the collection!"],
            'rare': ["Ooh, that's a rare one, darlin'!"], 'badge': ["A badge! Auntie so proud of you!"],
            'bingo:square': ["A bingo square! Mark it down!"], 'bingo': ["Bingo! Oh, I love bingo!"],
            'gps:lost': ["Uh oh, we lost the signal, darlin'. Don't worry."], 'gps:back': ["There we go! We're back!"],
            'streak': ["My, there's a lot of it out here!", "Still the same, darlin'. They really love it here."],
            'streak:1': ["Still corn! Oh my, so much corn!"],
            'spot:town': ["A little town! I wonder if they have a good bakery."], 'spot:water': ["Ooh, look at the water. So peaceful."],
            'spot:woods': ["Trees, darlin'. Watch for deer!"], 'spot:pasture': ["Pasture! Look at the cows, so relaxed."],
            'spot:bridge': ["A bridge! Hold the wheel steady, darlin'."],
            'speed:fast': ["Slow down, nah! The corn not goin' anywhere!"], 'speed:slow': ["A little traffic, darlin'. Deep breath."],
            'miles:10': ["Ten miles already, darlin'!"], 'miles:50': ["Fifty miles! Stretch your legs soon, you hear?"], 'miles:100': ["A hundred miles! Look at us go!"],
        },
        'extras': {
            'joke': ["Why did the scarecrow win an award? He was outstanding in his field!", "What did the corn say when it got a compliment? Aw, shucks!",
                     "Why do potatoes make good detectives? They keep their eyes peeled!", "How do you fix a broken pumpkin? With a pumpkin patch!", "What do you call a sad strawberry? A blueberry!"],
            'banter': ["Are you drinkin' enough water, darlin'?", "Back home, we grew everything. Breadfruit, mangoes, sugarcane, everything!", "Did you call your mother today?"],
            'meme': ["Darlin', the vibes are immaculate.", "Very demure. Very mindful. Very corn.", "Touch grass, they say. Well, there's plenty of grass right here!"],
            'holiday:halloween': ["Halloween! I'm handin' out the good candy this year!"], 'season:fall': ["Harvest time, darlin'! Everybody busy, busy!"],
        },
    },
}

def cap(s): return s[:1].upper() + s[1:]

def build(ch):
    c = CHARS[ch]
    sections = []
    def sec(title, tip, items): sections.append({'title': title, 'tip': tip, 'items': items})
    n = [0]
    def item(text, use):
        n[0] += 1
        return {'n': n[0], 'text': text, 'use': use}
    sec('1. Hello and big moments', 'Full energy. Pause one second between lines.',
        [item(t, k) for k, ts in c['moments'].items() for t in ts])
    calls = []
    for code in TOP:
        x = CROPS[code][0]
        for side in ('left', 'right', 'both'):
            for t in c[side]:
                calls.append(item(t.replace('{X}', cap(x)).replace('{x}', x), f'crop:{code}:{side}'))
    sec('2. The crops you pass most', 'Lots of corn and soybeans. Keep each one fresh and fun.', calls)
    tails = [item(t, f'tail:{side}') for side, ts in c['tails'].items() for t in ts]
    names = [item(f"{CROPS[code][1]}!", f'name:{code}') for code in CROPS]
    half = len(names) // 2
    sec('3. Crop names, part 1', 'Just the name, said like you just spotted it. Short and punchy.', names[:half])
    sec('4. Crop names, part 2, and side phrases', 'Same for these names. Then the side phrases, which get joined after a crop name.', names[half:] + tails)
    sec('5. States', 'First the two welcome intros, then each state name on its own, as if it ends the welcome.',
        [item(t, 'welcome') for t in c['welcome']] + [item(f'{s}!', f'statename:{st}') for st, (s, _, _) in STATES.items()])
    sec('6. Jokes and fun stuff', 'Ham it up. Laugh if you want to.', [item(t, k) for k, ts in c['extras'].items() for t in ts])
    k = 0
    for s in sections:   # number in reading order
        for it in s['items']:
            k += 1; it['n'] = k
    return sections

def markdown(ch, sections):
    out = [f"## {CHARS[ch]['title']}", '']
    for s in sections:
        out += [f"### {s['title']}", '', s['tip'], '']
        out += [f"{it['n']}. {it['text']}" for it in s['items']]
        out.append('')
    return '\n'.join(out)

if __name__ == '__main__':
    for ch in CHARS:
        secs = build(ch)
        d = OUT / ch; d.mkdir(parents=True, exist_ok=True)
        json.dump(secs, open(d / 'script.json', 'w'), indent=1)
        open(d / 'script.md', 'w').write(markdown(ch, secs))
        print(ch, sum(len(s['items']) for s in secs), 'lines', [len(s['items']) for s in secs])
