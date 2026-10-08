# The Spot-a-Crop voice cast (round 3).
# Each character starts from a reference clip read in character by a natural base voice:
#   orpheus: Orpheus TTS (Apache-2.0, Llama 3.2 base) voices tara/leah/jess/mia/zoe/leo/dan/zac, with <laugh>-style tags
#   kokoro:  Kokoro (Apache-2.0) stock voices; hammed up by original Chatterbox's exaggeration dial first
# Lines are then performed by Chatterbox Turbo (MIT) cloning that reference, with [laugh]-style tags.
# pitch > 1 raises the reference (kept small: big shifts sound robotic).

CAST = {
    'earl': {
        # Orpheus "dan" came out British; am_santa is an older, warm American voice.
        'name': 'Earl', 'emoji': '🤠', 'blurb': 'Southern farmer', 'base': 'kokoro', 'voice': 'am_santa', 'speed': 0.9, 'pitch': 0.98, 'exag': 0.9,
        'ref': "Well, I'll be. <chuckle> Y'all come on in, sit a spell. I been farming this ground for forty-some years, "
               "corn, beans, a little hay for the cows. Ain't nothing fancy, no sir. But I reckon there ain't a prettier sight "
               "in this whole world than a field of corn at sundown.",
    },
    'dot': {
        'name': 'Dot', 'emoji': '👵', 'blurb': 'Sweet grandma', 'base': 'orpheus', 'voice': 'leah', 'pitch': 0.97,
        'ref': "Oh, honey! Come here, come here, sit down. <laugh> I just made a pie, rhubarb, your favorite! "
               "Oh, I'm so happy you're here. Now tell me everything. Did you see the sunflowers? Oh, I just love the sunflowers.",
    },
    'buck': {
        'name': 'Buck', 'emoji': '📣', 'blurb': 'Rodeo announcer', 'base': 'kokoro', 'voice': 'am_fenrir', 'speed': 1.08, 'pitch': 1.0, 'exag': 1.35,
        'ref': "Ladies and gentlemen! Boys and girls! Welcome... to the biggest! Show! In the whole entire county! Are you ready?! "
               "I can't hear you! Let's make some noise for our next rider, coming out of chute number three! Yeehaw!",
    },
    'penny': {
        'name': 'Penny', 'emoji': '🤪', 'blurb': 'Bubbly pun machine', 'base': 'orpheus', 'voice': 'jess', 'pitch': 1.0,
        'ref': "Oh my gosh, okay, okay, okay, I have the best joke ever, you're gonna love this. <laugh> "
               "Why did the tomato blush? Because it saw the salad dressing! Get it? I'm hilarious. I know, I know!",
    },
    'kernel': {
        'name': 'Kernel', 'emoji': '🌽', 'blurb': 'The mascot, a corn kid', 'base': 'orpheus', 'voice': 'mia', 'pitch': 1.08,
        'ref': "Hi hi hi! I'm Kernel! Are we going on a road trip? Can I sit in the front? <laugh> Ooh, ooh, look, a tractor! "
               "I love tractors so, so much! Are we there yet? Just kidding! But... are we?",
    },
    'sam': {
        'name': 'Sam', 'emoji': '🎧', 'blurb': 'Calm and clear', 'base': 'orpheus', 'voice': 'tara', 'pitch': 1.0,
        'ref': "Hi there. I'll keep it simple. I'll tell you what's growing on each side of the road as we drive, "
               "and let you know when something interesting is coming up. Enjoy the ride.",
    },
    'nigel': {
        'name': 'Nigel', 'emoji': '🎩', 'blurb': 'Nature documentary narrator', 'base': 'kokoro', 'voice': 'bm_george', 'speed': 0.9, 'pitch': 1.0, 'exag': 0.7,
        'ref': "And here, in the quiet of the early morning, we find a remarkable sight. The field awakens. "
               "Slowly, patiently, the young shoots reach for the light. Truly... one of nature's great wonders.",
    },
    'brody': {
        'name': 'Brody', 'emoji': '🏄', 'blurb': 'Surfer dude', 'base': 'orpheus', 'voice': 'zac', 'pitch': 1.0,
        'ref': "Duuude. <laugh> Okay, so, like, I was out on the waves this morning, right? And it was totally gnarly, bro. "
               "Like, the sun was coming up, and I was just like, whoa. Life is good, man. Life is so good.",
    },
    'hank': {
        'name': 'Coach Hank', 'emoji': '🧢', 'blurb': 'Hype coach', 'base': 'kokoro', 'voice': 'am_michael', 'speed': 1.05, 'pitch': 0.98, 'exag': 1.3,
        'ref': "Alright, listen up! I want hustle! I want heart! Nobody quits on my watch! "
               "You think the corn quits? No! The corn does not quit! Now get out there and give me everything you got!",
    },
    'rye': {
        'name': 'Detective Rye', 'emoji': '🕵️', 'blurb': 'Film-noir detective', 'base': 'orpheus', 'voice': 'leo', 'pitch': 0.96,
        'ref': "The rain hadn't stopped in three days. <sigh> I lit a match and watched it burn down to my fingers. "
               "She walked in like trouble in a red dress, and said she had a case for me. They always do.",
    },
    'delphine': {
        'name': 'Delphine', 'emoji': '💅', 'blurb': 'Soap-opera drama queen', 'base': 'orpheus', 'voice': 'zoe', 'pitch': 1.0,
        'ref': "Darling, <gasp> you will not believe what happened! He said he loved me, and then he left! Just like that! "
               "<sigh> Oh, it's all too much. Pour me a glass of something, I simply must sit down.",
    },
    'cole': {
        'name': 'Cole', 'emoji': '🎸', 'blurb': 'Sings every call', 'base': 'kokoro', 'voice': 'am_puck', 'speed': 0.95, 'pitch': 1.0, 'exag': 0.8,
        'sing': True,   # lines are sung: spoken take -> songify.py (Auto-Tune style, banjo backing)
        'ref': "Well howdy, folks, pull up a hay bale. I'm gonna sing you a little song about the open road, "
               "the big blue sky, and a field of corn that goes on forever. Here we go now, one, two, three!",
    },
}
