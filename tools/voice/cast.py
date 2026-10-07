# The Spot-a-Crop voice cast. Each character is a Kokoro stock voice (Apache-2.0) used as the
# reference for Chatterbox Turbo (MIT), which adds the acting. Sam is plain Kokoro: calm and clean.
#
# ref_text is read in character to make the reference clip, so the cloned voice picks up the energy.
# pitch > 1 raises the reference voice (Kernel), < 1 lowers it; tempo < 1 slows it down.

CAST = {
    'earl': {
        'name': 'Earl', 'emoji': '🤠', 'blurb': 'Laid-back farmer',
        'kokoro': 'am_onyx', 'speed': 0.88, 'pitch': 0.97, 'engine': 'turbo',
        'ref_text': "Well now, I've been farmin' this ground for forty-some years. Corn, beans, a little hay for the cows. "
                    "Ain't nothin' fancy about it, but I tell ya, there's no prettier sight than a field of corn at sunset.",
    },
    'dot': {
        'name': 'Dot', 'emoji': '👵', 'blurb': 'Sweet grandma',
        'kokoro': 'af_sarah', 'speed': 0.86, 'pitch': 0.94, 'engine': 'turbo',
        'ref_text': "Oh, honey, come sit down, I just made a pie. Rhubarb, your favorite. "
                    "Now tell me all about your trip. Did you see the sunflowers? Oh, I just love the sunflowers this time of year.",
    },
    'buck': {
        'name': 'Buck', 'emoji': '📣', 'blurb': 'Rodeo announcer',
        'kokoro': 'am_fenrir', 'speed': 1.08, 'pitch': 1.0, 'engine': 'turbo',
        'ref_text': "Ladies and gentlemen, boys and girls, welcome to the biggest show in the whole entire county! "
                    "Are you ready? I can't hear you! Let's give it up for our next rider, coming out of chute number three!",
    },
    'penny': {
        'name': 'Penny', 'emoji': '🤪', 'blurb': 'Bubbly pun machine',
        'kokoro': 'af_bella', 'speed': 1.08, 'pitch': 1.02, 'engine': 'turbo',
        'ref_text': "Oh my gosh, okay, okay, I have the best joke ever, you are going to love this. "
                    "Why did the tomato blush? Because it saw the salad dressing! Ha! Get it? I'm hilarious, I know.",
    },
    'kernel': {
        'name': 'Kernel', 'emoji': '🌽', 'blurb': 'The mascot, a corn kid',
        'kokoro': 'af_sky', 'speed': 1.1, 'pitch': 1.22, 'engine': 'turbo',
        'ref_text': "Hi hi hi! I'm Kernel! Are we going on a road trip? Can I sit in the front? Ooh, look, a tractor! "
                    "I love tractors so much. Are we there yet? Just kidding! But are we?",
    },
    'sam': {
        'name': 'Sam', 'emoji': '🎧', 'blurb': 'Calm and clear',
        'kokoro': 'af_heart', 'speed': 1.0, 'pitch': 1.0, 'engine': 'kokoro',
        'ref_text': '',
    },
}
