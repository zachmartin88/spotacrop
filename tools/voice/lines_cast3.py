# Round 3: five new characters (Nigel, Brody, Coach Hank, Detective Rye, Delphine), and more personality
# for the originals. Imported by lines.py, which merges these into its tables before building.
# Tags in [brackets] are acted by Chatterbox Turbo: [laugh] [chuckle] [sigh] [gasp]. Use them sparingly.

NEW = ['nigel', 'brody', 'hank', 'rye', 'delphine']

T = {
    'earl': {   # more Southern, more porch
        'left': ["{X} on your left.", "Got {x} off to the left there.", "Left side, that there's {x}.", "Well now, {x} on the left.",
                 "Lookee yonder, {x} on your left.", "That's {x} off to the left, partner.", "Y'all see that {x} on the left?",
                 "Some mighty fine {x} on the left.", "Well, I'll be. {X} on the left."],
        'right': ["{X} on your right.", "Got {x} off to the right there.", "Right side, that there's {x}.", "Well now, {x} on the right.",
                  "Lookee yonder, {x} on your right.", "That's {x} off to the right, partner.", "Y'all see that {x} on the right?",
                  "Some mighty fine {x} on the right.", "Well, I'll be. {X} on the right."],
        'around': ["{X} all around us, partner.", "We're plumb surrounded by {x}.", "Nothing but {x} far as the eye can see.",
                   "{X} every which way. [chuckle]"],
        'both': ["{X} on both sides, partner.", "{X} left and right. Can't hardly miss it."],
    },
    'nigel': {
        'left': ["And here, on the left... {x}. Magnificent.", "On the left, {x}. Observe it in its natural habitat.",
                 "To our left, a fine example of {x}.", "Look closely. On the left... {x}.", "On the left, {x}. Truly remarkable."],
        'right': ["And here, on the right... {x}. Magnificent.", "On the right, {x}. Observe it in its natural habitat.",
                  "To our right, a fine example of {x}.", "Look closely. On the right... {x}.", "On the right, {x}. Truly remarkable."],
        'around': ["We find ourselves entirely surrounded by {x}. Remarkable.", "{X}, as far as the eye can see. Nature is extraordinary."],
        'both': ["{X} on both sides. A rare symmetry.", "{X}, to the left and to the right. Splendid."],
    },
    'brody': {
        'left': ["Duuude, {x} on the left.", "Whoa, {x} on the left, bro.", "Left side, {x}. Gnarly.", "Check it, {x} on the left, man.",
                 "{X} on the left. So chill."],
        'right': ["Duuude, {x} on the right.", "Whoa, {x} on the right, bro.", "Right side, {x}. Gnarly.", "Check it, {x} on the right, man.",
                  "{X} on the right. So chill."],
        'around': ["Dude, it's {x} everywhere. Like a {x} ocean.", "Total {x} vibes all around, man."],
        'both': ["{X} on both sides, bro! Double gnarly!", "{X} left and right. Radical."],
    },
    'hank': {
        'left': ["{X} on the left! Look at that form!", "Left side! {X}! Textbook!", "{X} on the left! That's what I'm talking about!",
                 "Eyes left! {X}! Let's go!", "{X}, left side! Great hustle!"],
        'right': ["{X} on the right! Look at that form!", "Right side! {X}! Textbook!", "{X} on the right! That's what I'm talking about!",
                  "Eyes right! {X}! Let's go!", "{X}, right side! Great hustle!"],
        'around': ["{X} on every side! Full team effort!", "We are surrounded by {x}! Nobody quits!"],
        'both': ["{X} on both sides! That's teamwork!", "{X} left and right! Huddle up!"],
    },
    'rye': {
        'left': ["{X}. On the left. Something's not right about it.", "Left side. {X}. I've seen this before.", "{X} on the left. Keep your eyes open, kid.",
                 "On the left... {x}. Nobody ever suspects the {x}.", "{X}, left side. It's always the quiet ones."],
        'right': ["{X}. On the right. Something's not right about it.", "Right side. {X}. I've seen this before.", "{X} on the right. Keep your eyes open, kid.",
                  "On the right... {x}. Nobody ever suspects the {x}.", "{X}, right side. It's always the quiet ones."],
        'around': ["{X}, everywhere I look. [sigh] This town's got a {x} problem.", "We're surrounded by {x}. No way out, kid."],
        'both': ["{X} on both sides. They've got us cornered.", "{X} left and right. Classic setup."],
    },
    'delphine': {
        'left': ["{X}! On the left! [gasp] I simply can't!", "On the left... {x}. How dare it be so lovely.", "Darling, look, {x} on the left!",
                 "{X} on the left. [sigh] It's all so beautiful.", "The left! {X}! I'm overcome!"],
        'right': ["{X}! On the right! [gasp] I simply can't!", "On the right... {x}. How dare it be so lovely.", "Darling, look, {x} on the right!",
                  "{X} on the right. [sigh] It's all so beautiful.", "The right! {X}! I'm overcome!"],
        'around': ["{X} everywhere, darling! [gasp] It's all too much!", "Surrounded by {x}. [sigh] Story of my life."],
        'both': ["{X} on both sides! [gasp] Oh, the drama!", "{X} to the left, {x} to the right. I need to sit down."],
    },
}

FLAVOR = {
    'earl': {1: ["Corn. The good Lord's favorite crop, I reckon.", "That corn's taller than my brother-in-law, and twice as useful. [chuckle]"],
             5: ["Beans. Corn's best friend. They take turns, year to year, just like me and my wife with the remote."],
             2: ["Cotton. Like a field full of little clouds."], 10: ["Peanuts. Boiled peanuts, now that's living."]},
    'dot': {1: ["Corn! Your grandpa loved corn on the cob. Butter and salt, every single time."], 229: ["Pumpkins! Oh, I'm already thinking pie."],
            68: ["Apples! I'll make you a crisp when we get home, sweetie."]},
    'nigel': {1: ["The corn. It neither hunts nor flees. It simply... stands.", "Here, the corn grows in vast colonies, numbering in the millions."],
              5: ["The soybean, shy and unassuming, rarely ventures far from its row."], 37: ["Hay. The cattle's preferred delicacy."]},
    'brody': {1: ["Corn, dude. Corn chips, corn dogs, cornbread. Corn's, like, the ultimate."], 6: ["Sunflowers, bro. They're just, like, vibing with the sun."]},
    'hank': {1: ["Corn! Six feet tall and never takes a day off! Be the corn!"], 5: ["Soybeans! Underrated! Underdog! I love an underdog!"]},
    'rye': {1: ["Corn. Tall. Golden. Lots of ears... always listening."], 5: ["Soybeans. Quiet. Too quiet."]},
    'delphine': {1: ["Corn! It reminds me of a summer romance. [sigh] Gone too soon."], 229: ["Pumpkins! [gasp] Autumn is here, darling, and I am not ready!"]},
}

SPOTS = {
    'town': {'nigel': ["We now enter a human settlement. The crops, sensibly, keep their distance."],
             'brody': ["Town, dude. Houses aren't crops. Bummer."], 'hank': ["Town! Crops are on the bench! Back in a minute!"],
             'rye': ["Town. Too many houses. Not enough answers."], 'delphine': ["A little town! [gasp] I hope there's a café."]},
    'water': {'nigel': ["Water. Here, the wildlife gathers to drink."], 'brody': ["Water! Surf's up! Kidding. It's like, a pond."],
              'hank': ["Water break! Hydrate! Hydrate!"], 'rye': ["Water. Dark and deep. Like my past."], 'delphine': ["Water! How romantic!"]},
    'woods': {'nigel': ["The woodland. Home to deer, foxes, and absolutely no corn."], 'brody': ["Trees, man. Nature's high fives."],
              'hank': ["Trees! Standing tall! Good posture!"], 'rye': ["The woods. Good place to hide. Or to think."], 'delphine': ["The forest! [sigh] So mysterious."]},
    'wetland': {'nigel': ["A wetland. Listen, and you may hear the frogs."], 'brody': ["Swampy, bro. Frogs are totally partying."],
                'hank': ["Wetlands! Watch your footing!"], 'rye': ["The marsh. Things get lost out there."], 'delphine': ["A swamp! How dreadfully dramatic!"]},
    'pasture': {'nigel': ["Pasture. The cattle graze here, unhurried and content."], 'brody': ["Grass for days. The cows are living their best life."],
                'hank': ["Pasture! The cows are resting up for the big game!"], 'rye': ["Pasture. Cows everywhere. Nobody saw nothing."],
                'delphine': ["The cows! Look at them, darling, so serene."]},
    'fallow': {'nigel': ["A resting field. It too must hibernate."], 'brody': ["That field's taking a nap, man. Respect."],
               'hank': ["That field's on injured reserve this season!"], 'rye': ["Empty field. Nobody's talking."], 'delphine': ["That field is resting. As should I."]},
    'scrub': {'nigel': ["The scrubland. A harsh place. The tumbleweed reigns."], 'brody': ["Desert vibes, dude."],
              'hank': ["Scrubland! Tough terrain! Tough people!"], 'rye': ["Scrubland. Long way from anywhere."], 'delphine': ["Oh, it's so desolate. It suits my mood."]},
}

STATE_T = {
    'nigel': "We now enter {S}, the {N}. {F}",
    'brody': "Welcome to {S}, dude! {F} Gnarly.",
    'hank': "Welcome to {S}! The {N}! {F} Let's go!",
    'rye': "{S}. The {N}. {F} I've got a feeling about this one.",
    'delphine': "{S}! [gasp] The {N}! {F} Divine, darling.",
}
BELT_T = {
    'earl': ["Well, we just rolled on into {B}. {F}"],
    'nigel': ["We have now entered {B}. {F}"],
    'brody': ["Dude, we're in {B}! {F}"],
    'hank': ["We're in {B}! {F} Game time!"],
    'rye': ["{B}. {F} I've been here before."],
    'delphine': ["{B}! [gasp] {F}"],
}
FACT_T = {
    'nigel': ["Remarkably, {F}", "A curious fact. {F}"],
    'brody': ["Dude, fun fact. {F} Mind blown.", "Okay, so, like... {F}"],
    'hank': ["Fun fact! {F} Write that down!", "Listen up! {F}"],
    'rye': ["Here's something they don't tell you. {F}", "I did some digging. {F}"],
    'delphine': ["Darling, did you know? {F}", "Oh, here's a delicious little fact. {F}"],
}
MOMENTS = {
    'hello': {'nigel': ["Hello. I'll be narrating today's journey through the fields."],
              'brody': ["Yo, dude! Let's spot some crops, bro!"], 'hank': ["Alright, team! Eyes on the fields! Let's go!"],
              'rye': ["The name's Rye. I'll keep an eye on the fields."], 'delphine': ["Hello, darling! Let's make this drive fabulous!"]},
    'start:morning': {'nigel': ["Dawn breaks over the fields. Our journey begins."], 'brody': ["Morning, dude! Dawn patrol!"],
                      'hank': ["Rise and shine! Early practice!"], 'rye': ["Morning. Coffee's cold. Let's go."], 'delphine': ["Good morning, darling! I'm simply not a morning person."]},
    'start:afternoon': {'nigel': ["The afternoon sun warms the fields. We set off."], 'brody': ["Afternoon cruise, bro!"],
                        'hank': ["Afternoon session! Let's get after it!"], 'rye': ["Afternoon. The case is open."], 'delphine': ["An afternoon drive! How delightful!"]},
    'start:evening': {'nigel': ["Evening falls. The fields glow gold."], 'brody': ["Sunset drive, dude. So rad."],
                      'hank': ["Evening run! Finish strong!"], 'rye': ["Evening. Long shadows. My kind of hour."], 'delphine': ["The golden hour, darling! I look marvelous in this light."]},
    'start:night': {'nigel': ["Night. The fields rest, but we press on."], 'brody': ["Night drive, bro. Stars are out."],
                    'hank': ["Night game! Lights on! Stay sharp!"], 'rye': ["Night. When the crops talk. If you listen."], 'delphine': ["A midnight drive! How scandalous!"]},
    'end': {'nigel': ["And so our journey ends. Until next time.", "Thus concludes our expedition."],
            'brody': ["Later, dude! That was epic!", "Peace out, bro!"], 'hank': ["Great game! Hit the showers!", "That's a wrap! Proud of you!"],
            'rye': ["Case closed. For now.", "That's all for tonight, kid."], 'delphine': ["Farewell, darling! [sigh] Until we meet again.", "That was divine. Kisses!"]},
    'card': {'nigel': ["A new specimen for the collection.", "A new card. A splendid find."], 'brody': ["New crop card, dude!", "Card get! Radical!"],
             'hank': ["New card! That's a win!", "Another card! Keep it coming!"], 'rye': ["New card. Add it to the file."], 'delphine': ["A new card! [gasp] For me?"]},
    'rare': {'nigel': ["A rare sighting. Few have witnessed this."], 'brody': ["Whoa, dude, that's a rare one!"], 'hank': ["Rare find! MVP material!"],
             'rye': ["A rare one. Now that's a clue."], 'delphine': ["Something rare! [gasp] Just like me!"]},
    'badge': {'nigel': ["A badge. Well earned."], 'brody': ["Badge unlocked, bro! Sick!"], 'hank': ["Badge! That's a trophy, kid!"],
              'rye': ["A badge. Nice work, kid."], 'delphine': ["A badge! I'm so proud I could cry!"]},
    'bingo:square': {'nigel': ["A bingo square, observed."], 'brody': ["Bingo square, dude!"], 'hank': ["Bingo square! Check it!"],
                     'rye': ["Bingo square. One more clue."], 'delphine': ["A bingo square! Divine!"]},
    'bingo': {'nigel': ["Bingo. Extraordinary."], 'brody': ["Bingo, bro! Radical!"], 'hank': ["Bingo! Victory! Gatorade shower!"],
              'rye': ["Bingo. Case closed."], 'delphine': ["Bingo! [gasp] I've won! We've won!"]},
    'gps:lost': {'nigel': ["We appear to have lost our bearings."], 'brody': ["Lost signal, dude. No worries."], 'hank': ["Lost the signal! Stay calm! Next play!"],
                 'rye': ["Signal's gone dark."], 'delphine': ["The signal's gone! [gasp] Don't leave me!"]},
    'gps:back': {'nigel': ["And we have our bearings once more."], 'brody': ["Back, baby!"], 'hank': ["We're back! Let's go!"],
                 'rye': ["Back on the trail."], 'delphine': ["There you are, darling!"]},
    'streak': {'nigel': ["The same crop, still. The landscape is remarkably committed.", "Still the same. Nature, it seems, has made up its mind."],
               'brody': ["Still the same crop, dude. Consistent vibes.", "Same crop, man. It's like a long wave."],
               'hank': ["Same crop! That's consistency! That wins championships!", "Still going! No quit!"],
               'rye': ["Same crop. Mile after mile. Somebody's hiding something.", "Still the same. I don't buy it."],
               'delphine': ["Still the same crop! [sigh] Will it ever end?", "The same, again! How tragically predictable."]},
}
STREAK_CROP = {
    1: {'nigel': ["Still corn. The corn, it seems, has no natural predators."], 'brody': ["Still corn, man. Riding the corn wave."],
        'hank': ["Still corn! Corn doesn't quit, and neither do you!"], 'rye': ["Still corn. It was always corn. I should've known."],
        'delphine': ["Still corn. It's always corn. Story of my life, darling."]},
    5: {'nigel': ["Still soybeans. A vast, unhurried herd."], 'brody': ["Beans for days, bro."], 'hank': ["Soybeans! Still going! Love the hustle!"],
        'rye': ["Still soybeans. They're stalling."], 'delphine': ["Soybeans, still. [sigh] Such loyalty."]},
    24: {'nigel': ["Still wheat. Golden, endless, entirely unbothered."], 'brody': ["Still wheat, dude. Amber waves, bro."], 'hank': ["Still wheat! Keep rolling!"],
         'rye': ["Still wheat. This trail goes on forever."], 'delphine': ["Wheat, still! So golden, so endless."]},
    2: {'nigel': ["Still cotton. Like snow, in summer."], 'brody': ["Still cotton. So fluffy, man."], 'hank': ["Still cotton! Soft crop, tough team!"],
        'rye': ["Still cotton. Soft on the outside."], 'delphine': ["Still cotton! Like a cloud, darling!"]},
}
JOKE_T = {'nigel': "And now, a joke. {J}", 'brody': "Okay, dude, joke time. {J} [laugh]", 'hank': "Joke break! {J} Ha!",
          'rye': "Heard one down at the precinct. {J}", 'delphine': "Darling, I heard the funniest thing. {J} [laugh]"}
MILES_T = {'nigel': "{M} A considerable journey.", 'brody': "{M} Stoked, bro!", 'hank': "{M} Personal best! Keep pushing!",
           'rye': "{M} Long road.", 'delphine': "{M} We've come so far together, darling!"}
AHEAD_T = {'nigel': "Up ahead, we expect {x}.", 'brody': "Up ahead, dude, lots of {x}.", 'hank': "Coming up! {X}! Get ready!",
           'rye': "Up ahead, {x}. Stay sharp.", 'delphine': "Coming up, darling, {x}! I can hardly wait!"}
RECAP_T = {'nigel': "Today's dominant species: {x}.", 'brody': "Mostly {x} today, dude. Epic.", 'hank': "Today's MVP: {x}!",
           'rye': "Today it was mostly {x}. Figures.", 'delphine': "Today was all about {x}, darling!"}
HARVEST = {
    'start': {'nigel': "The harvest has just begun.", 'brody': "Harvest is starting, dude!", 'hank': "Harvest kickoff!", 'rye': "Harvest is starting. The machines are out.", 'delphine': "The harvest begins! [gasp]"},
    'quarter': {'nigel': "About a quarter of the harvest is in.", 'brody': "Quarter harvested, bro.", 'hank': "First quarter of the harvest is done!", 'rye': "A quarter of it's harvested.", 'delphine': "A quarter harvested already!"},
    'half': {'nigel': "The harvest is about halfway done.", 'brody': "Halfway harvested, dude.", 'hank': "Halftime! Harvest is half done!", 'rye': "Halfway through the harvest.", 'delphine': "Halfway harvested! The suspense!"},
    'most': {'nigel': "Most of the harvest is now in.", 'brody': "Almost all harvested, man.", 'hank': "Fourth quarter! Almost there!", 'rye': "Most of it's in. Nearly over.", 'delphine': "Almost all harvested! I'm emotional."},
    'done': {'nigel': "The harvest is essentially complete.", 'brody': "Harvest is done, bro!", 'hank': "Final whistle! Harvest complete!", 'rye': "Harvest's done. Case closed.", 'delphine': "The harvest is over! [sigh] Bittersweet."},
}
BANTER = {
    'nigel': ["We continue our slow journey through the farmland.", "Note the fence posts. Each one... a fence post.", "Somewhere out there, a cow ponders its existence."],
    'brody': ["Dude, road trips are, like, the best.", "Snack check, bro. Corn chips?", "This drive is so mellow, man.", "Is that cow surfing? No? Bummer."],
    'hank': ["Water break! Hydrate!", "Posture check! Shoulders back!", "You're doing great! Keep those eyes on the road!", "Who's the best driver? You are!"],
    'rye': ["The road's long. The answers are longer.", "I don't trust that scarecrow.", "Every barn's got a story. Most of them are boring."],
    'delphine': ["Darling, are we there yet? I'm parched.", "This drive is simply divine.", "Do you think the cows have secrets? I do."],
}
