# Meme references, family-friendly, in each character's own voice. Merged into the matching moments
# by lines.py (EXTRA[char][key] -> more lines for that key), plus a 'meme' pool for quiet stretches.
# Keep quotes to a few words; these are nods, not reproductions.

EXTRA = {
    'earl': {
        'spot:pasture': ["Pasture. Y'all young folks keep sayin' 'touch grass.' Well, there it is."],
        'flavor:1': ["Corn. Now, there was a little fella online said it's got the juice. He ain't wrong."],
        'gps:lost': ["Lost the signal. This is fine. [chuckle] Everything's fine."],
        'end': ["Well, I reckon I'm gonna head out."],
        'card': ["New card. Stonks, as the kids say. Whatever that means."],
        'meme': ["My grandson says I've got main character energy. I told him I've got tractor energy.",
                 "Hold my sweet tea. [chuckle]", "They tell me corn's a whole meme now. Well, it was a meme before memes, son.",
                 "Somebody told me 'no cap.' I said I've got three caps, they're all John Deere."],
    },
    'dot': {
        'spot:pasture': ["Grass, dear. The kids keep telling each other to go touch it. Here's your chance!"],
        'flavor:1': ["Corn! My grandson showed me a video of a little boy who loves corn. Oh, it was precious."],
        'gps:lost': ["Oh, the signal's gone. Well, this is fine. That's what the dog in the cartoon says, isn't it?"],
        'card': ["A new card! Oh, what do the kids say? Sheesh?"],
        'meme': ["My granddaughter says I'm 'slaying.' I think that's good?", "Is that what they call a vibe, dear? It's a lovely vibe.",
                 "Oh, I saw a video of a cat playing the piano. Can you imagine?", "The kids say 'it's giving.' Giving what, I asked. They just laughed."],
    },
    'buck': {
        'card': ["New card! Achievement unlocked, folks!"], 'rare': ["A rare one! The power level is over nine thousand!"],
        'gps:lost': ["We've lost the signal, folks! This is fine! Everything is fine!"],
        'end': ["And that's the show, folks! Mission accomplished! We'll get 'em next time!"],
        'spot:pasture': ["Pasture! Ladies and gentlemen, we have officially touched grass!"],
        'meme': ["Let's go! Let's go! Let him cook!", "This crowd has the rizz, folks!", "And the crowd says... sheesh!",
                 "What a play! Somebody clip that!"],
    },
    'penny': {
        'flavor:1': ["It's corn! I can't imagine a more beautiful thing! [laugh]", "Corn! A big lump with knobs! It has the juice!"],
        'card': ["New card! Stonks! Crop stonks!"], 'gps:lost': ["No signal! This is fine. [laugh] I'm fine. We're all fine."],
        'spot:pasture': ["Grass! We are literally touching grass right now! Well, driving by it."],
        'streak:1': ["Corn again! It's giving... corn."],
        'meme': ["Very demure. Very mindful. Very corn.", "Main character energy, and the main character is soybeans.",
                 "No cap, this is the best road trip ever.", "Crop bestie check! Are you having fun?", "It's the farmland for me."],
    },
    'kernel': {
        'flavor:1': ["It's corn! A big lump with knobs! It has the juice!", "It's corn! I can't imagine a more beautiful thing!"],
        'card': ["New card! Stonks!"], 'gps:lost': ["Uh oh. This is fine. This is fine!"],
        'spot:pasture': ["Grass! Can we touch it? Everyone says touch grass!"],
        'meme': ["Are we there yet? [laugh] Skibidi corn!", "Sheesh! That's a lot of farm!", "I have the juice. Because I'm corn.",
                 "Is this a cow? It's a cow!"],
    },
    'sam': {
        'spot:pasture': ["Pasture. Good place to touch grass, as they say."],
        'gps:lost': ["Signal lost. This is fine."],
        'meme': ["Fun fact: corn became a meme in twenty twenty-two. It still has the juice.", "Touching grass is recommended on long drives."],
    },
    'nigel': {
        'spot:pasture': ["Here we observe the elusive behavior known as... touching grass."],
        'gps:lost': ["The signal has vanished. And yet... this is fine."],
        'flavor:1': ["The corn. A big lump, with knobs. Observers report... it has the juice."],
        'card': ["A new specimen. One might say... stonks."],
        'meme': ["Here, the young human scrolls endlessly. We shall not disturb it.", "The rare main character, in its natural habitat.",
                 "Remarkable. The cow does not know it is a meme. And yet... it is."],
    },
    'brody': {
        'card': ["New card, bro! No cap!"], 'rare': ["Sheesh! That's a rare one, dude!"], 'gps:lost': ["Lost signal, bro. This is fine. Totally fine."],
        'spot:pasture': ["Grass, dude! We're basically touching grass!"],
        'flavor:1': ["Corn, dude. It's got the juice."],
        'end': ["Ight, imma head out. Later, dude!"],
        'meme': ["That's bussin', bro.", "Dude, these fields have serious rizz.", "Bro, no cap, best drive ever.", "Sheesh. Farmland is lowkey beautiful, man.",
                 "It's giving... chill vibes."],
    },
    'hank': {
        'card': ["New card! Let him cook!"], 'rare': ["Rare find! That's big brain energy!"], 'gps:lost': ["Lost the signal! This is fine! Next play!"],
        'spot:pasture': ["Pasture! Go touch some grass! Not now, you're driving!"],
        'end': ["Mission failed successfully! Just kidding, great drive!"],
        'meme': ["Let him cook! Let him cook!", "No days off! Not even corn days!", "That's big brain farming right there!", "Who's got main character energy? You do!"],
    },
    'rye': {
        'gps:lost': ["Signal's dead. This is fine. I've been in worse."],
        'spot:pasture': ["Pasture. Folks say 'touch grass.' I touched it once. Never again."],
        'flavor:1': ["Corn. Big lumps with knobs. They say it has the juice. I say it has secrets."],
        'meme': ["We live in a society. A farming society.", "It's always the soybeans, kid. Many such cases.",
                 "I'm in this field and I don't like it.", "The scarecrow knows something. Is this a clue? Yes."],
    },
    'delphine': {
        'card': ["A new card! [gasp] The audacity! The glamour!"], 'gps:lost': ["The signal is gone! This is fine. [sigh] I'm being brave."],
        'spot:pasture': ["Grass! Darling, we're touching grass! How very wholesome."],
        'flavor:1': ["Corn! [gasp] It has the juice, darling!"],
        'streak:1': ["Still corn. Very demure, very mindful, very... corn."],
        'meme': ["Darling, I'm simply living my main character moment.", "The audacity of these soybeans to be this gorgeous.",
                 "Very demure. Very mindful. Very farm.", "It's giving... harvest season."],
    },
}
