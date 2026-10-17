# Round 4: five more characters (Captain Cornbeard, Auctioneer Al, Tyler, Zib Zorble, Mortimer Gourd), and new
# moments for the whole cast: seasons and holidays, speed, bridges, more memes, more jokes and facts, more ways
# to call the crops you pass most, and two-character duets for "Take turns".
# Imported by lines.py. The new moments are added by extend(), with their own random seed, so the lines
# recorded in earlier rounds keep exactly the same wording (and don't need re-recording).
import random

NEW = ['cornbeard', 'al', 'tyler', 'zib', 'mortimer']
ALL = ['earl', 'dot', 'buck', 'penny', 'kernel', 'sam', 'nigel', 'brody', 'hank', 'rye', 'delphine'] + NEW

# ---------------------------------------------------------------- the new five: crop calls
T = {
    'cornbeard': {
        'left': ["{X} off the port bow! That's your left, matey.", "Arr, {x} to port! Port be left, landlubber.", "Avast! {X} on the left!",
                 "Port side, {x}! Steady as she goes.", "Land ho! {X}, off to the left!", "{X} on the left, me hearties! Arr!"],
        'right': ["{X} off the starboard bow! That's your right, matey.", "Arr, {x} to starboard! Starboard be right, landlubber.", "Avast! {X} on the right!",
                  "Starboard side, {x}! Steady as she goes.", "Land ho! {X}, off to the right!", "{X} on the right, me hearties! Arr!"],
        'around': ["{X} on every side! We be surrounded, crew!", "A whole sea of {x}! Arr!", "{X}, as far as the spyglass can see!"],
        'both': ["{X} to port and starboard! Both sides, matey!", "{X} on both sides! Arr, what a haul!"],
    },
    'al': {
        'left': ["On the left, {x}! Do I hear a bid? Sold!", "Left side, {x}, going once, going twice, sold!", "{X} on the left, folks, what a lot, what a lot!",
                 "Lot number one, on your left, {x}! Sold to the driver!", "Look left, {x}, fine condition, fine condition!"],
        'right': ["On the right, {x}! Do I hear a bid? Sold!", "Right side, {x}, going once, going twice, sold!", "{X} on the right, folks, what a lot, what a lot!",
                  "Lot number one, on your right, {x}! Sold to the driver!", "Look right, {x}, fine condition, fine condition!"],
        'around': ["{X} all around, folks, the whole lot, every acre, sold!", "We got {x} on every side, bid it up, bid it up!"],
        'both': ["{X} on both sides! Two for one! Sold!", "{X} left and right, a matched pair, folks!"],
    },
    'tyler': {
        'left': ["{X}. On the left. Cool, I guess.", "Ugh. {X} on the left.", "Left side, {x}. Whatever.", "Oh wow. {X}. On the left. Thrilling.",
                 "{X} on the left. Can I have my phone back now?"],
        'right': ["{X}. On the right. Cool, I guess.", "Ugh. {X} on the right.", "Right side, {x}. Whatever.", "Oh wow. {X}. On the right. Thrilling.",
                  "{X} on the right. Can I have my phone back now?"],
        'around': ["It's literally all {x}. Cool. Great.", "{X} everywhere. This is my life now."],
        'both': ["{X} on both sides. Wow. Amazing. Not.", "{X} left and right. Can we stop for snacks?"],
    },
    'zib': {
        'left': ["On your left, Earthling, {x}. Fascinating.", "Left side! The humans call this {x}.", "Scanning left. Result: {x}. Delicious, probably.",
                 "{X} on the left! I must report this to my planet.", "Behold, on the left, {x}! Take me to its leader."],
        'right': ["On your right, Earthling, {x}. Fascinating.", "Right side! The humans call this {x}.", "Scanning right. Result: {x}. Delicious, probably.",
                  "{X} on the right! I must report this to my planet.", "Behold, on the right, {x}! Take me to its leader."],
        'around': ["We are surrounded by {x}. Is this an invasion?", "{X} in every direction! Your planet is very generous."],
        'both': ["{X} on both sides! Two of them! Earth is generous.", "{X}, left and right. Most excellent, Earthling."],
    },
    'mortimer': {
        'left': ["On the left... {x}. Or is it?", "{X}, to the left. They say it rustles at night.", "Look left, if you dare. {X}.",
                 "To the left, {x}. Nothing spooky about that. Probably.", "{X} on the left. [chuckle] How delightfully eerie."],
        'right': ["On the right... {x}. Or is it?", "{X}, to the right. They say it rustles at night.", "Look right, if you dare. {X}.",
                  "To the right, {x}. Nothing spooky about that. Probably.", "{X} on the right. [chuckle] How delightfully eerie."],
        'around': ["{X} all around us. [chuckle] There's no escape.", "We're surrounded by {x}. Just as the legend foretold."],
        'both': ["{X} on both sides. Watching from the left, and the right.", "{X} to the left. {X} to the right. Spooky."],
    },
}

FLAVOR = {
    'cornbeard': {1: ["Corn! The finest treasure on dry land. No digging required.", "Arr, corn. Pirates prefer it popped, with a bit of butter."],
                  5: ["Soybeans. A humble crew, but they pull their weight."], 70: ["Christmas trees! A whole forest of masts for me fleet!"]},
    'al': {1: ["Corn, folks! Top of the market! Who'll give me a hundred? Sold!", "Corn, corn, beautiful corn, the best lot in the county!"],
           5: ["Soybeans! Strong demand, strong demand!"], 37: ["Hay! Big round bales, fine condition, sold to the cows!"]},
    'tyler': {1: ["Corn. Again. Shocker.", "My friends are at the mall. I'm looking at corn."],
              5: ["Soybeans. Like, they make tofu out of those. Gross. Kind of cool, though."], 229: ["Okay, pumpkins are actually kind of cool. Don't tell anyone."]},
    'zib': {1: ["Corn! On my planet, we worship a giant ear of corn. Kidding. Or am I?", "Corn. The humans pop it and watch moving pictures. Strange ritual."],
            5: ["Soybeans! Tiny green pods. Like little spaceships."], 2: ["Cotton! The humans grow clouds. Remarkable technology."]},
    'mortimer': {1: ["Corn. Tall enough to hide in. [chuckle] Not that anyone would.", "The corn whispers when the wind blows. Listen."],
                 229: ["Pumpkins! [gasp] My people! My beautiful, glowing people."], 5: ["Soybeans. Ordinary. Too ordinary."]},
}

SPOTS = {
    'town': {'cornbeard': ["A port town! Shore leave, crew. Back to the fields soon."], 'al': ["Town! Houses! Not for auction today, folks!"],
             'tyler': ["Town. Finally. Is there a coffee place?"], 'zib': ["A human nest! They stack themselves in boxes."],
             'mortimer': ["A quiet little town. A little too quiet."]},
    'water': {'cornbeard': ["Water! Now that's more like it. Me natural habitat."], 'al': ["Waterfront property, folks! Prime lot!"],
              'tyler': ["Water. Neat. I guess."], 'zib': ["Liquid! The humans drink this. And swim in it. Both!"],
              'mortimer': ["Still water. Who knows what lurks beneath?"]},
    'woods': {'cornbeard': ["Trees! Good timber for a ship."], 'al': ["Timber! Fine standing timber, folks!"],
              'tyler': ["Trees. Wow. So many trees."], 'zib': ["Very tall plants. They do not move. Suspicious."],
              'mortimer': ["The woods. Dark and deep. [chuckle] Stay on the road."]},
    'wetland': {'cornbeard': ["A swamp! Not deep enough to sail, not dry enough to farm."], 'al': ["Wetlands, folks! Not for sale, the frogs own it!"],
                'tyler': ["A swamp. Smells like gym socks probably."], 'zib': ["A wet land. Not quite water. Not quite land. I relate."],
                'mortimer': ["The marsh. Where the mist rises at night."]},
    'pasture': {'cornbeard': ["Pasture. The cows be grazing, calm as a sea at dawn."], 'al': ["Pasture! Good grass, happy cows, who'll bid?"],
                'tyler': ["Cows. Hi, cows. You're more fun than this car."], 'zib': ["Large spotted beings, eating the ground. I wish to meet them."],
                'mortimer': ["Pasture. The cows are watching. They always are."]},
    'fallow': {'cornbeard': ["That field be in dry dock this year. Resting up."], 'al': ["That field's off the market this year, folks!"],
               'tyler': ["That field's doing nothing. Same."], 'zib': ["An empty field. Perfect for landing."],
               'mortimer': ["An empty field. Nothing grows there this year. [chuckle] Nothing."]},
    'scrub': {'cornbeard': ["Dry land, nothing but brush. A pirate's nightmare."], 'al': ["Scrubland! Going cheap, folks, going cheap!"],
              'tyler': ["It's just bushes. Can we go home?"], 'zib': ["Dry and brown. Like my home planet. I am homesick."],
              'mortimer': ["Scrubland. Tumbleweeds, drifting like lost souls."]},
}

STATE_T = {
    'cornbeard': "Ahoy, {S}! The {N}! {F} Arr!",
    'al': "Welcome to {S}, folks, the {N}! {F} Sold!",
    'tyler': "We're in {S} now. The {N}. {F} Cool.",
    'zib': "Greetings, {S}! The humans call you the {N}. {F}",
    'mortimer': "We now enter {S}. The {N}. {F} [chuckle] Welcome.",
}
BELT_T = {
    'cornbeard': ["Arr, we've sailed into {B}! {F}"], 'al': ["Folks, we just entered {B}! {F} What a lot!"],
    'tyler': ["Okay so we're in {B} now. {F} Yay."], 'zib': ["We have entered the region called {B}. {F}"],
    'mortimer': ["We've crossed into {B}. {F} There's no turning back."],
}
FACT_T = {
    'cornbeard': ["Here be a fact, matey. {F}", "Listen close, crew. {F}"],
    'al': ["Here's a fact, folks, and it's free! {F}", "Fact for the crowd! {F}"],
    'tyler': ["Okay, random fact. {F} Whatever.", "Fun fact, I guess. {F}"],
    'zib': ["My research shows: {F}", "Earth fact, for my notes. {F}"],
    'mortimer': ["A curious tale. {F}", "Here's something they don't tell you. {F}"],
}
MOMENTS = {
    'hello': {'cornbeard': ["Ahoy! Captain Cornbeard at the helm. I'll call out the crops, port and starboard!", "Ahoy, matey! Let's sail these fields!"],
              'al': ["Folks, it's Auctioneer Al! Every field's for sale, and I'll call 'em all!", "Alright, folks, let's get this auction started!"],
              'tyler': ["Hey. It's Tyler. I'll tell you the crops, I guess.", "Ugh, fine. I'll call out the fields."],
              'zib': ["Greetings, Earthling! I am Zib Zorble. I will name your crops!", "Hello, human! Zib Zorble, reporting for tourism!"],
              'mortimer': ["Good evening. I'm Mortimer Gourd. Shall we take a little drive? [chuckle]", "Ah, a traveler. I'll tell you what grows out there."]},
    'start:morning': {'cornbeard': ["Mornin', crew! Raise the anchor!"], 'al': ["Good morning, folks! Early bird gets the deal!"],
                      'tyler': ["It's so early. Why are we awake?"], 'zib': ["Your sun has risen! Such a small sun. Cute."],
                      'mortimer': ["Morning mist on the fields. Lovely. And a little eerie."]},
    'start:afternoon': {'cornbeard': ["Afternoon, crew! Fair winds today!"], 'al': ["Good afternoon, folks! Let's get bidding!"],
                        'tyler': ["Afternoon road trip. Great. Love it."], 'zib': ["Afternoon on Earth! The best time for sightseeing!"],
                        'mortimer': ["A sunny afternoon. The shadows are just waiting."]},
    'start:evening': {'cornbeard': ["Evening, crew! Red sky at night, sailor's delight!"], 'al': ["Good evening, folks! Prime time auction!"],
                      'tyler': ["Evening drive. Sunset's kinda nice, actually."], 'zib': ["Your sun is setting! It turns orange! Magnificent!"],
                      'mortimer': ["Dusk. My favorite hour. [chuckle] Let's go."]},
    'start:night': {'cornbeard': ["A night voyage! Steer by the stars, matey."], 'al': ["Late night auction, folks! Everything must go!"],
                    'tyler': ["Driving at night? I'm so tired."], 'zib': ["Night! I can see my home from here. That one. No, that one."],
                    'mortimer': ["A night drive. [chuckle] Now we're talking."]},
    'end': {'cornbeard': ["Drop anchor! Good voyage, matey.", "And that's the end of the voyage. Arr!"],
            'al': ["Going once, going twice, that drive is sold! Thank you, folks!", "That's the auction, folks! See you next time!"],
            'tyler': ["We're done? Finally. Okay, that was kind of fun.", "Cool. Bye."],
            'zib': ["Our journey is complete! I will tell my planet everything!", "Farewell, Earthling! Zib Zorble, signing off!"],
            'mortimer': ["And so our tale ends. [chuckle] For now.", "Goodnight, traveler. Sleep well. If you can."]},
    'card': {'cornbeard': ["A new card for the treasure chest!", "New card! Into the chest it goes!"], 'al': ["New card, folks! Sold, to you!"],
             'tyler': ["New card. Okay, that's actually kind of cool."], 'zib': ["A new card! I shall add it to my collection of Earth things!"],
             'mortimer': ["A new card. [chuckle] Your collection grows."]},
    'rare': {'cornbeard': ["A rare treasure! Rarer than gold doubloons!"], 'al': ["A rare one, folks! Collector's item!"],
             'tyler': ["Wait. That's a rare one? Okay, sick."], 'zib': ["A rare specimen! My planet will be so jealous!"],
             'mortimer': ["A rare one. Some say it's cursed. [chuckle] It isn't."]},
    'badge': {'cornbeard': ["A badge! Ye've earned yer stripes, matey!"], 'al': ["A badge, folks! Top bidder!"],
              'tyler': ["A badge. Cool. I'll tell literally no one."], 'zib': ["A badge! On my planet, this makes you royalty!"],
              'mortimer': ["A badge. Well done, traveler."]},
    'bingo:square': {'cornbeard': ["A bingo square! Mark it on the map!"], 'al': ["Bingo square, folks!"], 'tyler': ["Bingo square. Yay."],
                     'zib': ["A bingo square! I do not understand this game, but yay!"], 'mortimer': ["A bingo square. One step closer."]},
    'bingo': {'cornbeard': ["Bingo! Arr, we found the treasure!"], 'al': ["Bingo! Sold! We have a winner, folks!"], 'tyler': ["Bingo. Okay. That was actually fun."],
              'zib': ["Bingo! I have won the Earth game!"], 'mortimer': ["Bingo. [chuckle] Just as I predicted."]},
    'gps:lost': {'cornbeard': ["We've lost our bearings! Hold fast, crew!"], 'al': ["Lost the signal, folks! Stand by!"],
                 'tyler': ["No signal. This is literally the worst."], 'zib': ["My scanners are offline! Do not panic, Earthling!"],
                 'mortimer': ["The signal's gone dark. [chuckle] How fitting."]},
    'gps:back': {'cornbeard': ["Back on course, matey!"], 'al': ["And we're back, folks!"], 'tyler': ["Signal's back. Thank goodness."],
                 'zib': ["Scanners online! We are found!"], 'mortimer': ["And we're back. Nothing to fear."]},
    'streak': {'cornbeard': ["Same crop for leagues and leagues!", "Still the same, crew. Steady as she goes."],
               'al': ["Same lot, folks! Still on the block!", "Still the same, folks! Big inventory!"],
               'tyler': ["It's been the same crop for like an hour.", "Still the same. I'm dying of boredom."],
               'zib': ["The same plant, still! Your planet repeats itself!", "Still the same. Is this a loop? Are we in a simulation?"],
               'mortimer': ["The same crop, mile after mile. [chuckle] It's as if we're going in circles.", "Still the same. Endless. Like a curse."]},
}
STREAK_CROP = {
    1: {'cornbeard': ["Still corn! A whole ocean of it!"], 'al': ["Still corn, folks! The supply never ends!"], 'tyler': ["Still corn. I can't."],
        'zib': ["Still corn. Earth must really love corn."], 'mortimer': ["Still corn. Row after row. They all look the same. [chuckle]"]},
    5: {'cornbeard': ["Still soybeans! Beans to the horizon!"], 'al': ["Still soybeans, folks! Bulk lot!"], 'tyler': ["Soybeans. Still. Help."],
        'zib': ["The soybeans continue. They are very committed."], 'mortimer': ["Still soybeans. They never end."]},
    24: {'cornbeard': ["Still wheat! Golden as treasure!"], 'al': ["Still wheat, folks! Wheat by the bushel!"], 'tyler': ["Wheat. Still. Cool."],
         'zib': ["Still wheat. It waves at me. I wave back."], 'mortimer': ["Still wheat. Swaying. Whispering."]},
    2: {'cornbeard': ["Still cotton! Like sailing through clouds!"], 'al': ["Still cotton, folks! Bales and bales!"], 'tyler': ["Still cotton. Fluffy. Whatever."],
        'zib': ["Still cotton. So many little clouds."], 'mortimer': ["Still cotton. Pale as a ghost."]},
}
JOKE_T = {'cornbeard': "Here be a joke, matey. {J} Arr!", 'al': "Joke time, folks, free of charge! {J}", 'tyler': "Okay, this is dumb, but. {J}",
          'zib': "I learned an Earth joke! {J} I do not understand it.", 'mortimer': "A little joke, from beyond. {J} [chuckle]"}
MILES_T = {'cornbeard': "{M} A fine voyage!", 'al': "{M} Sold!", 'tyler': "{M} Are we there yet?",
           'zib': "{M} Your miles are very small. But still!", 'mortimer': "{M} And still, the road goes on."}
AHEAD_T = {'cornbeard': "Up ahead, matey, lots of {x}!", 'al': "Coming up next on the block, folks, {x}!", 'tyler': "Up ahead, it's {x}. Yay.",
           'zib': "My scanners detect {x} ahead!", 'mortimer': "Up ahead... {x}. [chuckle]"}
RECAP_T = {'cornbeard': "Today's treasure: {x}!", 'al': "Top seller today, folks: {x}!", 'tyler': "It was mostly {x}. Shocking.",
           'zib': "Today, I saw mostly {x}. My planet will be amazed.", 'mortimer': "Tonight's tale was mostly {x}."}
HARVEST = {
    'start': {'cornbeard': "The harvest has begun, crew!", 'al': "Harvest is starting, folks!", 'tyler': "Harvest is starting. Okay.",
              'zib': "The humans are starting the great gathering!", 'mortimer': "The harvest begins. [chuckle] At last."},
    'quarter': {'cornbeard': "A quarter of the harvest be in!", 'al': "A quarter harvested, folks!", 'tyler': "Like a quarter is harvested.",
                'zib': "One quarter of the gathering is done!", 'mortimer': "A quarter of the harvest is in."},
    'half': {'cornbeard': "Half the harvest be in the hold!", 'al': "Halfway harvested, folks!", 'tyler': "Harvest is half done.",
             'zib': "The gathering is half complete!", 'mortimer': "Half the harvest is in. Half remains."},
    'most': {'cornbeard': "Most of the harvest be in!", 'al': "Most of it's harvested, folks!", 'tyler': "Most of it's harvested.",
             'zib': "The gathering is nearly complete!", 'mortimer': "Most of the harvest is in. The fields grow quiet."},
    'done': {'cornbeard': "The harvest is done! Arr!", 'al': "Harvest's done, folks! Sold out!", 'tyler': "Harvest's done. Good for them.",
             'zib': "The great gathering is complete!", 'mortimer': "The harvest is done. The fields sleep now."},
}
BANTER = {
    'cornbeard': ["A pirate's life for me. Well, a farm pirate.", "If ye see a scarecrow with an eye patch, that's me cousin.", "Arr, these roads be calmer than the open sea."],
    'al': ["Folks, every barn we pass, I wanna sell it.", "I once sold a tractor in four seconds flat.", "Who'll give me a snack? Anybody? Snack, snack, snack?"],
    'tyler': ["Are we there yet? Seriously.", "My phone's on two percent.", "This is fine. Totally fine. I'm having fun.", "Can we listen to my music next?"],
    'zib': ["Your roads are very long. On my planet, we teleport.", "I like your cows. Can I take one home?", "Earth is my favorite planet. Don't tell Mars."],
    'mortimer': ["Did you hear that? No? Good.", "Every old barn has a story. [chuckle]", "The scarecrows are friendly. Mostly."],
}

# Meme nods for the new five (merged like lines_memes.EXTRA).
EXTRA = {
    'cornbeard': {'meme': ["Arr, the treasure was the friends we made along the way.", "Cap'n Cornbeard has main character energy, matey.",
                           "Hold me grog. [laugh]", "This crew has rizz. Arr."],
                  'gps:lost': ["Lost the signal! This is fine. Arr, this is fine."], 'spot:pasture': ["Grass! The crew should touch some."]},
    'al': {'meme': ["Folks, let him cook! Let him cook!", "No cap, best auction ever.", "Sheesh! What a lot!", "That's bussin', folks! Sold!"],
           'gps:lost': ["Signal's gone, folks! This is fine!"], 'spot:pasture': ["Pasture! Touch grass, folks! Sold!"]},
    'tyler': {'meme': ["It's giving... farm.", "Very demure. Very corn.", "This road trip is mid. Okay, not mid. It's fine.",
                       "Lowkey, the cows are kind of slay.", "Touch grass, they said. Well, here's grass."],
              'gps:lost': ["No signal. This is fine. I'm fine."], 'card': ["New card. Okay, that's actually fire."]},
    'zib': {'meme': ["My planet also has the juice. But less corn.", "Is this a crop? Yes. Yes it is.", "We come in peace. And for snacks.",
                     "Earthlings say 'no cap.' I have no cap. I have antennae."],
            'gps:lost': ["My signal is lost. This is fine, as the dog says."], 'spot:pasture': ["The humans touch grass to calm down. I will try it."]},
    'mortimer': {'meme': ["It's spooky season. It's always spooky season.", "The scarecrow knows something. And so do I. [chuckle]",
                          "Some say the corn has the juice. I say it has secrets.", "Very demure. Very mindful. Very spooky."],
                 'gps:lost': ["The signal is lost. This is fine. [chuckle] Probably."], 'spot:pasture': ["Pasture. Go ahead. Touch the grass. If you dare."]},
}

# ---------------------------------------------------------------- new moments for everyone
# Extra crop calls for the crops people hear most, with templates the earlier rounds didn't use.
TOP = [1, 5, 37, 24, 36, 2, 23, 4, 3, 21]
T_MORE = {
    'earl': {'left': ["Yonder on the left, that's {x}.", "Off to your left, a whole mess of {x}.", "Left side, partner. {X}."],
             'right': ["Yonder on the right, that's {x}.", "Off to your right, a whole mess of {x}.", "Right side, partner. {X}."]},
    'dot': {'left': ["Ooh, {x} on the left, sweetheart.", "Over on the left, dear, {x}.", "Left side, honey. {X}!"],
            'right': ["Ooh, {x} on the right, sweetheart.", "Over on the right, dear, {x}.", "Right side, honey. {X}!"]},
    'buck': {'left': ["Folks, on the left, give it up for {x}!", "Left side, it's {x}, and the crowd goes wild!", "Here comes {x}, on the left!"],
             'right': ["Folks, on the right, give it up for {x}!", "Right side, it's {x}, and the crowd goes wild!", "Here comes {x}, on the right!"]},
    'penny': {'left': ["Ooh la la, {x} on the left!", "Left side! {X}! We love to see it!", "Psst. {X}. On the left."],
              'right': ["Ooh la la, {x} on the right!", "Right side! {X}! We love to see it!", "Psst. {X}. On the right."]},
    'kernel': {'left': ["{X}! {X}! On the left!", "Look, look! {X}, on the left!", "Left side! I see {x}!"],
               'right': ["{X}! {X}! On the right!", "Look, look! {X}, on the right!", "Right side! I see {x}!"]},
    'sam': {'left': ["There's {x} on your left.", "{X}, on the left side."], 'right': ["There's {x} on your right.", "{X}, on the right side."]},
    'nigel': {'left': ["Observe, on the left, {x}.", "To our left, {x}, quite undisturbed.", "And there, on the left, {x}. Splendid."],
              'right': ["Observe, on the right, {x}.", "To our right, {x}, quite undisturbed.", "And there, on the right, {x}. Splendid."]},
    'brody': {'left': ["Yo, {x}, left side!", "Left side, dude. {X}. Stoked.", "Bro, look left. {X}!"],
              'right': ["Yo, {x}, right side!", "Right side, dude. {X}. Stoked.", "Bro, look right. {X}!"]},
    'hank': {'left': ["Left side! {X}! Big play!", "{X} on the left! Way to show up!", "Look left! {X}! Hustle!"],
             'right': ["Right side! {X}! Big play!", "{X} on the right! Way to show up!", "Look right! {X}! Hustle!"]},
    'rye': {'left': ["Left side. {X}. Write it down.", "{X} on the left. Same as last time.", "On the left, {x}. Nobody talks."],
            'right': ["Right side. {X}. Write it down.", "{X} on the right. Same as last time.", "On the right, {x}. Nobody talks."]},
    'delphine': {'left': ["On the left, darling! {X}!", "{X}, on the left. [sigh] Exquisite.", "Look left! {X}! The elegance!"],
                 'right': ["On the right, darling! {X}!", "{X}, on the right. [sigh] Exquisite.", "Look right! {X}! The elegance!"]},
}

BRIDGE = {   # water on both sides at once: a bridge or a causeway
    'earl': ["Crossin' the water. Hope this bridge was built by somebody sober. [chuckle]", "Water on both sides. Good fishin' down there, I bet."],
    'dot': ["Oh, a bridge! Hold the wheel steady, dear.", "Water on both sides! Isn't that pretty?"],
    'buck': ["We are crossing the water, folks! What a bridge!", "Water on both sides! The fish are watching!"],
    'penny': ["Bridge! Over troubled water? No, it's pretty calm actually.", "Water on both sides! Water you doing? Driving!"],
    'kernel': ["A bridge! We're flying over the water!", "Water on both sides! Hi, fish!"],
    'sam': ["Crossing water.", "Bridge ahead. Water on both sides."],
    'nigel': ["We cross the water now. Below us, unseen, the fish go about their business.", "Water on both sides. A rare glimpse of the river in its habitat."],
    'brody': ["Water on both sides, dude! Wish I had my board.", "Bridge, bro! Gnarly view!"],
    'hank': ["Bridge! Stay in your lane! Good form!", "Water on both sides! Eyes forward!"],
    'rye': ["A bridge. Lot of secrets get dropped off bridges.", "Water on both sides. Deep. Cold. Quiet."],
    'delphine': ["A bridge! [gasp] How romantic, darling!", "Water on both sides! I feel like I'm in a movie."],
    'cornbeard': ["Water! On both sides! Now this is proper sailing!", "Arr, a bridge. Pirates prefer to go under, not over."],
    'al': ["Waterfront on both sides, folks! Double the view, double the price!", "A bridge, folks! Not for sale!"],
    'tyler': ["A bridge. Okay, that's a nice view, I'll give it that.", "Water on both sides. Neat."],
    'zib': ["We are flying over liquid! Your cars can almost fly!", "A bridge! Earth engineering is adorable."],
    'mortimer': ["A bridge. Don't look down. [chuckle]", "Dark water on both sides. Who knows what lives down there."],
}

SPEED = {    # fast: over about 80 mph for a while (gentle nudge, never a cheer); slow: crawling in traffic
    'fast': {
        'earl': ["Easy there, partner. The corn ain't goin' anywhere.", "Whoa there. Slow down a hair, I can't read the fields that fast."],
        'dot': ["Slow down, dear, I'd like to get there in one piece.", "Honey, ease up a little. The crops will wait."],
        'buck': ["Whoa, folks, the crops are a blur! Let's ease off the gas!", "Slow it down a touch! Safety first in this arena!"],
        'penny': ["Whoa, the corn's a blur! Slow down so I can make puns!", "Speedy! Let's ease up, okay?"],
        'kernel': ["Too fast! The corn is all blurry! Slow down, please!", "Whoa, slow down! My husk is flapping!"],
        'sam': ["You're moving fast. Easy does it.", "Consider slowing down a little."],
        'nigel': ["The fields rush past at alarming speed. Perhaps we might ease off.", "Even the cheetah slows down eventually."],
        'brody': ["Whoa, dude, slow your roll. Chill.", "Easy, bro. Cruise speed, not race speed."],
        'hank': ["Slow it down! Control the tempo! Smart drivers win!", "Ease off! Pace yourself! Long game!"],
        'rye': ["Ease up, kid. Nobody's chasing us.", "Slow down. Fast drivers end up in my case files."],
        'delphine': ["Darling, slow down! My hair!", "Slower, please. I'd like to arrive glamorous, not flustered."],
        'cornbeard': ["Easy on the sails, matey! Slow 'er down!", "Too fast, crew! Reef the sails!"],
        'al': ["Whoa, slow it down! That's the one thing I don't do fast!", "Easy, folks! No rush on this lot!"],
        'tyler': ["Okay, slow down. I'd like to live.", "Dude, ease up. Seriously."],
        'zib': ["Too fast for my scanners! Please slow down, Earthling!", "Your vehicle is very fast. Please make it less fast."],
        'mortimer': ["Slow down. [chuckle] We'll get there. Everyone gets there eventually.", "Easy now. No need to hurry."],
    },
    'slow': {
        'earl': ["Slow goin'. Gives ya time to admire the scenery.", "Bit of traffic. Corn's not goin' anywhere either."],
        'dot': ["A little traffic, dear. Deep breaths.", "Slow going. Good time for a snack, honey."],
        'buck': ["Traffic, folks! A slow-motion replay of the fields!", "We're crawling, folks! More time to enjoy the show!"],
        'penny': ["Traffic! More time for puns! Lucky you!", "Slow lane! Time to stop and smell the soybeans!"],
        'kernel': ["We're going so slow! I can count the corn!", "Traffic! Are we there yet? We're not anywhere!"],
        'sam': ["Slow traffic. Plenty of time to look around.", "Moving slowly for now."],
        'nigel': ["Traffic. The herd of cars moves slowly, as one.", "We creep forward. Patience, as in nature, is rewarded."],
        'brody': ["Traffic, dude. Just float with it.", "Slow, man. Good vibes only."],
        'hank': ["Traffic! Stay patient! Patience is a skill!", "Slow going! Mental toughness!"],
        'rye': ["Traffic. Everybody's going nowhere fast.", "Slow. Gives a guy time to think."],
        'delphine': ["Traffic! [sigh] The suspense is unbearable!", "Slow going, darling. At least the view is lovely."],
        'cornbeard': ["Becalmed, matey! No wind in the sails!", "Traffic. Slow as a ship in the doldrums."],
        'al': ["Slow traffic, folks. Only thing in my life that's slow!", "Traffic! Going nowhere, going nowhere!"],
        'tyler': ["Traffic. Perfect. Love this.", "We're barely moving. Cool."],
        'zib': ["Your vehicles have stopped. Is this a festival?", "Traffic! The humans gather to sit very still."],
        'mortimer': ["Traffic. Creeping along. Like fog.", "We crawl forward. [chuckle] How suspenseful."],
    },
}

SEASON = {   # said now and then on quiet stretches, by month
    'fall': {
        'earl': ["Harvest time. Best time of year, if ya ask me.", "Fall. Combines are rollin' and the leaves are turnin'."],
        'dot': ["Oh, fall is my favorite, dear. Apple cider and sweaters.", "The leaves are turning, honey. So pretty."],
        'buck': ["It's harvest season, folks! The playoffs of farming!", "Fall is here! The combines are taking the field!"],
        'penny': ["It's fall! Pumpkin spice everything!", "Harvest season! Time to turnip the fun!"],
        'kernel': ["It's fall! This is when they harvest my cousins!", "Leaves are falling! Can we jump in a leaf pile?"],
        'sam': ["It's harvest season. Watch for slow farm equipment.", "Fall harvest is underway."],
        'nigel': ["Autumn. The great harvest migration begins.", "The fields turn gold, then brown. The cycle is complete."],
        'brody': ["Fall, dude! Hoodie season!", "Harvest season, bro. The combines are shredding."],
        'hank': ["Harvest season! This is the championship!", "Fall! Combines are on the field! Let's go!"],
        'rye': ["Fall. The leaves drop. So do the alibis.", "Harvest season. Everybody's busy. Good time to hide something."],
        'delphine': ["Autumn, darling! Cozy sweaters and heartbreak!", "Fall! [sigh] Everything is golden and fleeting."],
        'cornbeard': ["Harvest season! The farmers be hauling in their treasure!", "Fall, matey! The best time to plunder an orchard."],
        'al': ["Harvest season, folks! Busiest time of year!", "Fall! Everything's coming in, everything's selling!"],
        'tyler': ["It's fall. Okay, I do like fall.", "Harvest season, I guess. Whatever. Pumpkin spice is good."],
        'zib': ["The trees are changing colors! Are they sick? No? Beautiful!", "The humans call this fall. Nothing has fallen. Except leaves."],
        'mortimer': ["Fall. When the days grow short, and the nights grow long. [chuckle]", "Harvest season. My favorite time of year."],
    },
    'winter': {
        'earl': ["Winter. Fields are restin', and so's the farmer.", "Cold out. Hope those fields got a blanket of snow."],
        'dot': ["It's chilly, dear. Do you have your coat?", "Winter fields, honey. They're sleeping till spring."],
        'buck': ["It's the off-season, folks! The fields are resting up!", "Winter! The fields are in training camp!"],
        'penny': ["Winter! Snow much fun!", "It's cold! Ice to meet you!"],
        'kernel': ["It's winter! The fields are sleeping. Shh!", "Brr! Is it snowing? Can we build a snow-corn?"],
        'sam': ["Winter. Most fields are resting.", "Winter wheat is growing under there."],
        'nigel': ["Winter. The fields lie dormant, waiting.", "Under the frost, the winter wheat endures."],
        'brody': ["Winter, dude. Snowboard season!", "Cold out, bro. Fields are chilling. Literally."],
        'hank': ["Winter! Off-season training! No excuses!", "Cold weather builds character!"],
        'rye': ["Winter. Cold trail. Cold coffee.", "Snow covers everything. Even the truth."],
        'delphine': ["Winter, darling! Hot cocoa and drama!", "So cold! [sigh] Hold me."],
        'cornbeard': ["Winter! Even the sea freezes, matey.", "Cold as a sea chest at the bottom of the ocean!"],
        'al': ["Winter, folks! Equipment auction season!", "Cold out there, folks, but the deals are hot!"],
        'tyler': ["It's freezing. Can we turn up the heat?", "Winter. Nothing's growing. So, like, why are we here?"],
        'zib': ["Frozen water falls from the sky! Your planet is magical!", "Winter! The fields are taking a long nap."],
        'mortimer': ["Winter. Bare trees and empty fields. [chuckle] How lovely.", "The cold months. When the fields go quiet."],
    },
    'spring': {
        'earl': ["Spring. Plantin' time. Farmers are up before the sun.", "Spring's here. Watch for tractors on the road."],
        'dot': ["Spring, dear! Everything's coming up green!", "Planting season, honey. Oh, I love spring."],
        'buck': ["It's opening day, folks! Planting season!", "Spring has sprung, folks! The season begins!"],
        'penny': ["Spring! Everything's bloomin' great!", "Planting season! Seed you later!"],
        'kernel': ["It's spring! Baby corn time!", "Spring! Everything is so green!"],
        'sam': ["It's planting season. Watch for tractors.", "Spring planting is underway."],
        'nigel': ["Spring. The fields awaken from their long sleep.", "New shoots emerge. The cycle begins once more."],
        'brody': ["Spring, dude! Everything's growing!", "Planting season, bro. Fresh starts."],
        'hank': ["Spring training! Planting season! Let's go!", "Opening day for the fields!"],
        'rye': ["Spring. Fresh start. Same old secrets.", "Planting season. Everybody's burying something."],
        'delphine': ["Spring, darling! Love is in the air!", "Everything's blooming! [gasp] Just like me!"],
        'cornbeard': ["Spring! Time to plant the seeds of adventure!", "Fair spring winds, matey!"],
        'al': ["Spring, folks! Planting season! Seed's selling fast!", "Spring has sprung! Bid on it!"],
        'tyler': ["It's spring. Allergies. Great.", "Spring. Everything's green. Cool, I guess."],
        'zib': ["Spring! The plants are being born! Beautiful!", "The humans put seeds in the dirt and wait. Brilliant."],
        'mortimer': ["Spring. Even I find it rather pleasant.", "New life in the fields. How charming. [chuckle]"],
    },
    'summer': {
        'earl': ["Summer. Corn's growin' so fast you can hear it.", "Hot one today. Good for the crops."],
        'dot': ["It's hot, dear. Drink some water!", "Summer! Corn on the cob season, honey!"],
        'buck': ["Summer, folks! The fields are in their prime!", "It's hot out there, folks! Peak season!"],
        'penny': ["Summer! Hot hot hot! Like a jalapeño!", "Sunny days! Sweet corn season!"],
        'kernel': ["It's summer! I'm growing so tall!", "Summer! It's so hot! Am I popcorn yet?"],
        'sam': ["Summer. The crops are growing fast.", "It's growing season."],
        'nigel': ["Summer. The fields at the height of their glory.", "The sun is high. The crops reach for it."],
        'brody': ["Summer, dude! Best season!", "Hot out, bro. Perfect beach weather. Or corn weather."],
        'hank': ["Summer! Two-a-days for the crops!", "It's hot! Hydrate! Hydrate!"],
        'rye': ["Summer. Hot. Sticky. Suspicious.", "The heat makes people do crazy things."],
        'delphine': ["Summer, darling! Sunglasses on!", "It's so hot! [sigh] I'm melting!"],
        'cornbeard': ["Summer! Sun on the sails!", "Hot as a cannon, matey!"],
        'al': ["Summer, folks! Crops growing, prices rising!", "Hot out there, folks! Hot lots!"],
        'tyler': ["It's so hot. Can we get ice cream?", "Summer vacation. Spent in a car. Cool."],
        'zib': ["Your sun is very hot! I am sweating! I did not know I could sweat!", "Summer! The plants are very tall now!"],
        'mortimer': ["Summer. Long days. But the nights still come. [chuckle]", "Even in summer, the corn has its shadows."],
    },
}
HOLIDAY = {  # around the day itself
    'halloween': {
        'earl': ["Halloween's comin'. Them pumpkins are nervous."], 'dot': ["Halloween soon, dear! I'll have candy at the door."],
        'buck': ["It's spooky season, folks!"], 'penny': ["Halloween! I'm dressing up as a corn maze. Amazing, right?"],
        'kernel': ["Halloween! I'm gonna be a popcorn ghost!"], 'sam': ["Halloween is coming up."],
        'nigel': ["Halloween. The pumpkin's season of glory."], 'brody': ["Halloween, dude! Spooky vibes!"],
        'hank': ["Halloween! No candy till practice is over!"], 'rye': ["Halloween. Everybody's wearing a mask. Some all year."],
        'delphine': ["Halloween! [gasp] I'll be something glamorous and terrifying!"], 'cornbeard': ["Halloween! A pirate's favorite night!"],
        'al': ["Halloween, folks! Pumpkins, going fast!"], 'tyler': ["Halloween. I'm too old to trick or treat. I'm still going."],
        'zib': ["Halloween! The humans dress as aliens! I am flattered!"], 'mortimer': ["Halloween. [chuckle] My night of nights."],
    },
    'thanksgiving': {
        'earl': ["Thanksgiving's comin'. Thank a farmer for that dinner."], 'dot': ["Thanksgiving, dear! Save room for pie!"],
        'buck': ["Thanksgiving, folks! The biggest feast of the year!"], 'penny': ["Thanksgiving! I'm so grate-ful! Like cheese!"],
        'kernel': ["Thanksgiving! Is there corn? There better be corn."], 'sam': ["Thanksgiving is coming up."],
        'nigel': ["Thanksgiving. The great feast of the harvest."], 'brody': ["Thanksgiving, dude! Food coma incoming!"],
        'hank': ["Thanksgiving! Carb loading!"], 'rye': ["Thanksgiving. Families. Secrets. Gravy."],
        'delphine': ["Thanksgiving! [sigh] Family drama, my favorite!"], 'cornbeard': ["Thanksgiving! A feast fit for a crew!"],
        'al': ["Thanksgiving, folks! Thankful for every bid!"], 'tyler': ["Thanksgiving. At least there's pie."],
        'zib': ["Thanksgiving! The humans eat a large bird and nap. I approve."], 'mortimer': ["Thanksgiving. A feast, by candlelight."],
    },
    'christmas': {
        'earl': ["Christmas is comin'. Hope Santa brings me a new tractor."], 'dot': ["Merry Christmas, sweetie! I'm baking cookies."],
        'buck': ["Christmas is coming, folks!"], 'penny': ["Christmas! Have a holly jolly drive!"],
        'kernel': ["Christmas! Do reindeer eat corn? I hope so!"], 'sam': ["Merry Christmas."],
        'nigel': ["Christmas. The fir tree's moment in the spotlight."], 'brody': ["Merry Christmas, bro!"],
        'hank': ["Christmas! Best gift? Hustle!"], 'rye': ["Christmas. Even I put up a tree. A small one."],
        'delphine': ["Christmas! [gasp] Mistletoe and drama!"], 'cornbeard': ["Merry Christmas, crew! Arr!"],
        'al': ["Christmas, folks! Everything must go!"], 'tyler': ["Christmas. Okay, I'm actually excited."],
        'zib': ["Christmas! A large man enters homes through the chimney. Your planet is wild."], 'mortimer': ["Christmas. [chuckle] Even I like Christmas."],
    },
    'newyear': {
        'earl': ["Happy New Year, partner."], 'dot': ["Happy New Year, dear!"], 'buck': ["Happy New Year, folks!"],
        'penny': ["Happy New Year! New year, new puns!"], 'kernel': ["Happy New Year! I'm one year older! Am I?"], 'sam': ["Happy New Year."],
        'nigel': ["A new year begins."], 'brody': ["Happy New Year, dude!"], 'hank': ["New year! New goals!"], 'rye': ["New year. Same case."],
        'delphine': ["Happy New Year, darling! [gasp] Kisses!"], 'cornbeard': ["Happy New Year, crew!"], 'al': ["Happy New Year, folks!"],
        'tyler': ["Happy New Year, I guess."], 'zib': ["Happy New Earth Year!"], 'mortimer': ["A new year. [chuckle] Let's see what it brings."],
    },
    'july4': {
        'earl': ["Happy Fourth, partner. Corn should be knee high by now."], 'dot': ["Happy Fourth of July, dear! Fireworks tonight!"],
        'buck': ["Happy Fourth of July, folks!"], 'penny': ["Happy Fourth! Let's make some noise!"],
        'kernel': ["Fourth of July! Fireworks! Pop pop pop! Like popcorn!"], 'sam': ["Happy Fourth of July."],
        'nigel': ["Independence Day. The fireworks are coming."], 'brody': ["Happy Fourth, dude!"], 'hank': ["Happy Fourth! Go team!"],
        'rye': ["Fourth of July. Lots of noise tonight."], 'delphine': ["The Fourth! [gasp] Fireworks!"], 'cornbeard': ["Happy Fourth! Fire the cannons!"],
        'al': ["Happy Fourth, folks!"], 'tyler': ["Happy Fourth. Fireworks are cool."], 'zib': ["Happy Fourth! The sky explosions are beautiful!"],
        'mortimer': ["Fourth of July. Even the night lights up."],
    },
}

MORE_MEMES = {
    'earl': ["Some fella on the internet said 'it's corn.' Well, I been sayin' that for forty years.", "Y'all ever hear of the ick? That's how I feel about weeds.",
             "My nephew says I'm a whole vibe. I said I'm a whole farmer."],
    'dot': ["My granddaughter says I'm the main character. Well, I am the grandma.", "Is it slay or slayed, dear? I'll just say slay.",
            "The kids say no cap. I wear a sun hat, so I guess that's right."],
    'buck': ["And the crowd says... let's go!", "Ladies and gentlemen, this road trip is the goat!", "That's a W, folks! A big W!"],
    'penny': ["It's corn! The kids said it best. I just add puns.", "That's so fetch. Wait, nobody says that anymore.", "Not me getting emotional about soybeans."],
    'kernel': ["I'm the goat! Wait, no, I'm corn!", "Okay, but have you tried being corn? It's lit!", "Corn is so slay!"],
    'sam': ["Some people call corn a vibe. It is a crop.", "The goat of crops, statistically, is corn."],
    'nigel': ["And here, a rare sighting of... the vibe.", "The young humans call this the ick. We shall observe it.", "The corn, it seems, is the goat."],
    'brody': ["Dude, corn is the goat.", "Vibe check, bro. Passed.", "That's a W, dude."],
    'hank': ["That's a W! Take the W!", "You are the goat! Greatest of all time!", "Vibe check! Passed! Let's go!"],
    'rye': ["Vibe check. Something's off. It's the soybeans.", "The goat? There's a goat? Where?", "That's a red flag, kid. A red flag on a tractor."],
    'delphine': ["Darling, the vibes are immaculate.", "Not me crying over a field of sunflowers.", "That tractor is giving main character."],
}

MORE_JOKES = [
    "What do you call a cow with no legs? Ground beef.",
    "Why did the corn go to the party? To get popped.",
    "What does a farmer use to count cows? A cow-culator.",
    "Why are pigs bad drivers? They hog the road.",
    "What kind of music do tractors like? Heavy metal.",
    "Why did the soybean break up with the corn? It needed some space in the rotation.",
    "What do you call a sleeping bull? A bulldozer.",
    "How does a farmer mend his overalls? With cabbage patches.",
    "What did the farmer say when he lost his tractor? Where's my tractor?",
    "Why was the sheep arrested on the freeway? It made a ewe turn.",
]
MORE_FACTS = [
    "Almost every state grows some corn.",
    "A big combine can harvest about a hundred acres of corn in a day.",
    "The average American farmer is about fifty-eight years old.",
    "Most American farms are still family farms.",
]
CROP_FACTS = {
    37: ["A big round hay bale can weigh more than a thousand pounds."],
    229: ["Pumpkins are a fruit, and they're mostly water."],
    6: ["A single sunflower head can hold over a thousand seeds."],
    41: ["Sugarbeets are white, and they can weigh a few pounds each."],
    70: ["Most Christmas trees come from farms, not forests."],
    3: ["Rice fields are flooded to help keep the weeds down."],
}

# Two characters, one little scene, on a quiet stretch in "Take turns" (only when both are downloaded).
# Each step is (character, line). 'crop' means only while that crop is beside the road.
DUOS = [
    {'id': 1, 'crop': 1, 'steps': [('earl', "That's corn."), ('dot', "Earl, you say that every single time."), ('earl', "'Cause it's always corn, Dot.")]},
    {'id': 2, 'steps': [('kernel', "Are we there yet?"), ('dot', "Not yet, sweetie."), ('kernel', "How about now?"), ('dot', "Still not yet, dear.")]},
    {'id': 3, 'crop': 5, 'steps': [('nigel', "And here, the soybean, resting in its natural habitat."), ('brody', "Dude. It's just beans."), ('nigel', "Just beans. [sigh] Remarkable.")]},
    {'id': 4, 'steps': [('hank', "Alright, Tyler! Give me some energy!"), ('tyler', "No."), ('hank', "That's the spirit! Wait, no it isn't!")]},
    {'id': 5, 'steps': [('rye', "Something about this road doesn't add up."), ('delphine', "Darling, it's a road. It goes forward."), ('rye', "That's what they want you to think.")]},
    {'id': 6, 'steps': [('penny', "Sam, tell me a pun."), ('sam', "I don't do puns."), ('penny', "That's okay. Lettuce agree to disagree.")]},
    {'id': 7, 'steps': [('zib', "Captain, why do you call left port?"), ('cornbeard', "Because port and left both have four letters, matey!"), ('zib', "Your planet is very confusing.")]},
    {'id': 8, 'steps': [('al', "Do I hear a bid on that barn?"), ('buck', "Ladies and gentlemen, Al is selling the scenery again!"), ('al', "Going once, going twice!")]},
    {'id': 9, 'steps': [('mortimer', "Did you hear that rustling in the corn?"), ('kernel', "That was me! I'm the corn!"), ('mortimer', "[chuckle] Of course it was.")]},
    {'id': 10, 'steps': [('earl', "In my day, we didn't have phones in the car."), ('tyler', "How did you even survive?"), ('earl', "We talked about corn, son.")]},
    {'id': 11, 'steps': [('dot', "Did everyone use the bathroom before we left?"), ('brody', "Uh... no, dude."), ('dot', "Oh, Brody.")]},
    {'id': 12, 'crop': 1, 'steps': [('zib', "What is this tall plant, Earthling?"), ('kernel', "It's my family!"), ('zib', "You are... related to the plant?"), ('kernel', "I'm corn!")]},
    {'id': 13, 'steps': [('delphine', "I'm simply bored, darling."), ('tyler', "Same."), ('delphine', "Finally. Someone understands me.")]},
    {'id': 14, 'steps': [('hank', "Posture check! Shoulders back!"), ('nigel', "Here we observe the coach in his natural habitat. Shouting."), ('hank', "Thank you, Nigel!")]},
    {'id': 15, 'steps': [('buck', "And the crowd goes wild!"), ('sam', "There is no crowd."), ('buck', "The crowd goes mild!")]},
    {'id': 16, 'steps': [('cornbeard', "Arr, I smell treasure!"), ('rye', "That's a feed store, captain."), ('cornbeard', "Treasure!")]},
    {'id': 17, 'steps': [('penny', "Why did the scarecrow get promoted?"), ('mortimer', "Because he was outstanding in his field. [chuckle] I've heard it."), ('penny', "Aw, man.")]},
    {'id': 18, 'steps': [('al', "Folks, who'll give me a hundred for this view?"), ('dot', "Oh, Al, it's not for sale, dear."), ('al', "Everything's for sale, Dot!")]},
    {'id': 19, 'steps': [('brody', "Dude, what if the cows are, like, watching us?"), ('rye', "They are, kid. They always are.")]},
    {'id': 20, 'steps': [('kernel', "Can I be the driver?"), ('hank', "You're corn, buddy!"), ('kernel', "Corn can dream!")]},
    {'id': 21, 'steps': [('nigel', "The scarecrow. Silent. Vigilant."), ('mortimer', "And absolutely, positively, alive. [chuckle]"), ('nigel', "Please don't.")]},
    {'id': 22, 'steps': [('tyler', "Can we listen to my music?"), ('buck', "Ladies and gentlemen, the youth has spoken!"), ('tyler', "Never mind.")]},
    {'id': 23, 'steps': [('earl', "Nice day for it."), ('sam', "It is a nice day."), ('earl', "Well, Sam, you're easy to talk to.")]},
    {'id': 24, 'steps': [('zib', "Delphine, why are you so dramatic?"), ('delphine', "Darling, why are you so green?"), ('zib', "Touché.")]},
    {'id': 25, 'steps': [('cornbeard', "Port side, crew!"), ('kernel', "Which side is port?"), ('cornbeard', "Left, laddie!"), ('kernel', "Why not just say left?")]},
    {'id': 26, 'steps': [('dot', "Is everyone warm enough?"), ('mortimer', "I'm always a little cold. [chuckle]"), ('dot', "Oh, I'll knit you a scarf, dear.")]},
    {'id': 27, 'steps': [('hank', "What do we never do?"), ('brody', "Quit, dude?"), ('hank', "That's right!"), ('brody', "Except napping. I quit everything for naps.")]},
    {'id': 28, 'steps': [('rye', "Penny. Where were you last night?"), ('penny', "Making puns."), ('rye', "That checks out.")]},
    {'id': 29, 'steps': [('al', "Zib, what do they use for money on your planet?"), ('zib', "Corn."), ('al', "Folks, I'm moving.")]},
    {'id': 30, 'crop': 5, 'steps': [('tyler', "Soybeans again."), ('nigel', "Indeed. The soybean is a creature of habit."), ('tyler', "Same, honestly.")]},
]

def extend(add, char, CROPS, JOKE_T, FACT_T, cap):
    """New moments for every character, added after the earlier rounds (own random seed, so old wording stays put)."""
    rnd = random.Random(f'{char}-r4')
    for code in TOP:
        x = CROPS[code][0]
        for side, temps in T_MORE.get(char, {}).items():
            for t in temps:
                add(char, f'crop:{code}:{side}', t.replace('{X}', cap(x)).replace('{x}', x))
    for line in BRIDGE.get(char, []):
        add(char, 'spot:bridge', line)
    for kind, by in SPEED.items():
        for line in by.get(char, []):
            add(char, f'speed:{kind}', line)
    for s, by in SEASON.items():
        for line in by.get(char, []):
            add(char, f'season:{s}', line)
    for h, by in HOLIDAY.items():
        for line in by.get(char, []):
            add(char, f'holiday:{h}', line)
    for line in MORE_MEMES.get(char, []):
        add(char, 'meme', line)
    for j in MORE_JOKES:
        add(char, 'joke', JOKE_T[char].replace('{J}', j))
    for f in MORE_FACTS:
        add(char, 'fact', rnd.choice(FACT_T[char]).replace('{F}', f))
    for code, facts in CROP_FACTS.items():
        for f in facts:
            add(char, f'fact:{code}', rnd.choice(FACT_T[char]).replace('{F}', f))
    for d in DUOS:
        for i, (who, line) in enumerate(d['steps']):
            if who == char:
                add(char, f"duo:{d['id']}:{i}", line)

def duos_json():
    """What the app needs to stage the duets: who says each step, and any crop it needs."""
    return [{'id': d['id'], 'crop': d.get('crop'), 'steps': [w for w, _ in d['steps']]} for d in DUOS]
