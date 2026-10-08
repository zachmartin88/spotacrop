# Every line the Spot-a-Crop voices can say, per character.
# build() returns [{char, key, text}], where key is what the app asks for (e.g. "crop:1:left"),
# and a key usually has several lines so the app can rotate and rarely repeat itself.
#
# Facts are checked against USDA/industry sources; keep them conservative ("about", "most").
import random

CHARS = ['earl', 'dot', 'buck', 'penny', 'kernel', 'sam']

# ---------------------------------------------------------------- crops
# code: (spoken name used in sentences, short exclamation name, plural-ish "around" phrase or None)
CROPS = {
    1: ('corn', 'Corn'), 5: ('soybeans', 'Soybeans'), 37: ('hay', 'Hay'), 24: ('winter wheat', 'Winter wheat'),
    36: ('alfalfa', 'Alfalfa'), 2: ('cotton', 'Cotton'), 23: ('spring wheat', 'Spring wheat'), 4: ('sorghum', 'Sorghum'),
    26: ('wheat and soybeans', 'Wheat and soybeans'), 59: ('sod farms', 'Sod'), 3: ('rice', 'Rice'),
    21: ('barley', 'Barley'), 74: ('pecan orchards', 'Pecans'), 22: ('durum wheat', 'Durum wheat'), 69: ('vineyards', 'Grapes'),
    42: ('dry beans', 'Dry beans'), 31: ('canola', 'Canola'), 28: ('oats', 'Oats'), 75: ('almond orchards', 'Almonds'),
    68: ('apple orchards', 'Apples'), 27: ('rye', 'Rye'), 10: ('peanuts', 'Peanuts'), 45: ('sugarcane', 'Sugarcane'),
    12: ('sweet corn', 'Sweet corn'), 72: ('citrus groves', 'Citrus'), 43: ('potatoes', 'Potatoes'), 29: ('millet', 'Millet'),
    44: ('a mix of crops', 'A mystery crop'), 70: ('Christmas trees', 'Christmas trees'), 25: ('small grains', 'Small grains'),
    67: ('peach orchards', 'Peaches'), 212: ('orange groves', 'Oranges'), 71: ('an orchard', 'Fruit trees'),
    6: ('sunflowers', 'Sunflowers'), 204: ('pistachio orchards', 'Pistachios'), 66: ('cherry orchards', 'Cherries'),
    53: ('peas', 'Peas'), 76: ('walnut orchards', 'Walnuts'), 242: ('blueberries', 'Blueberries'), 52: ('lentils', 'Lentils'),
    54: ('tomatoes', 'Tomatoes'), 41: ('sugarbeets', 'Sugarbeets'), 47: ('veggies', 'Veggies'), 58: ('clover and wildflowers', 'Wildflowers'),
    211: ('olive groves', 'Olives'), 14: ('mint', 'Mint'), 33: ('safflower', 'Safflower'), 49: ('onions', 'Onions'),
    32: ('flax', 'Flax'), 228: ('triticale and corn', 'Triticale and corn'), 225: ('wheat and corn', 'Wheat and corn'),
    226: ('oats and corn', 'Oats and corn'), 215: ('avocado groves', 'Avocados'), 205: ('triticale', 'Triticale'),
    223: ('apricot orchards', 'Apricots'), 46: ('sweet potatoes', 'Sweet potatoes'), 237: ('barley and corn', 'Barley and corn'),
    217: ('pomegranates', 'Pomegranates'), 48: ('watermelons', 'Watermelons'), 77: ('pear orchards', 'Pears'), 222: ('squash', 'Squash'),
    220: ('plum orchards', 'Plums'), 209: ('cantaloupes', 'Cantaloupes'), 206: ('carrots', 'Carrots'), 208: ('garlic', 'Garlic'),
    51: ('chickpeas', 'Chickpeas'), 210: ('prune orchards', 'Prunes'), 57: ('herbs', 'Herbs'), 240: ('soybeans and oats', 'Soybeans and oats'),
    216: ('peppers', 'Peppers'), 236: ('wheat and sorghum', 'Wheat and sorghum'), 50: ('cucumbers', 'Cucumbers'),
    60: ('switchgrass', 'Switchgrass'), 219: ('greens', 'Greens'), 229: ('pumpkins', 'Pumpkins'), 254: ('barley and soybeans', 'Barley and soybeans'),
    35: ('mustard', 'Mustard'), 238: ('wheat and cotton', 'Wheat and cotton'), 213: ('honeydew melons', 'Honeydew'),
    214: ('broccoli', 'Broccoli'), 11: ('tobacco', 'Tobacco'), 13: ('popcorn', 'Popcorn'), 250: ('cranberry bogs', 'Cranberries'),
    207: ('asparagus', 'Asparagus'), 246: ('radishes', 'Radishes'),
}
DOUBLE = {26, 228, 225, 226, 237, 240, 236, 254, 238}   # "X, with Y planted after" reads oddly in some templates

PUNS = {
    1: ['A-maize-ing!', 'Ear-resistible!', 'Shucks!'], 5: ['Bean there, done that!', 'Full of beans!'], 37: ['Hay there!', 'Hay, look at that!'],
    24: ['Wheat dreams!', 'Grain-tastic!'], 23: ['Wheat-ly done!', 'Grain-tastic!'], 36: ['Alfalfa-bulous!'], 2: ['Cotton to like it!', 'So fluffy!'],
    4: ['Sorghum-thing special!'], 3: ['Rice to meet you!', 'Rice and shine!'], 21: ['Barley believable!'], 28: ['Oat of this world!'],
    27: ['Rye not?'], 43: ['Spud-tacular!', 'Tater-ific!'], 54: ['Ketchup with you later!'], 229: ['Oh my gourd!'], 222: ['Gourd job!'],
    68: ['Apple-solutely!'], 69: ['Grape expectations!', "That's grape!"], 66: ['Cherry on top!'], 242: ['Berry nice!'], 250: ['Berry bog-tastic!'],
    67: ['Peachy keen!'], 77: ['Pear-fect!'], 220: ['Plum good!'], 72: ['Orange you glad?'], 212: ['Orange you glad?'], 49: ['This one makes me tear up!'],
    208: ['Clove it!'], 206: ['Carrot top!'], 216: ['Hot stuff!'], 48: ['One in a melon!'], 209: ['One in a melon!'], 213: ['One in a melon!'],
    50: ['Kind of a big dill!'], 6: ['Bright idea!'], 10: ['Nuts about it!'], 75: ['Totally nuts!'], 74: ['Nuts about it!'], 76: ['Totally nuts!'],
    204: ['Nuts about it!'], 211: ['Olive it!'], 215: ['Holy guacamole!'], 70: ['Fir real!', 'Tree-mendous!'], 214: ['Tree-mendous!'],
    246: ['Rad-ish!'], 207: ['Spear-tacular!'], 14: ['Mint condition!'], 57: ['Thyme flies!'], 31: ['Canola-la!'], 32: ['Just the flax!'],
    41: ['How sweet!'], 45: ['Sugar rush!'], 12: ['Sweet!'], 13: ['Pop-ular choice!'], 46: ['Yam-tastic!'], 52: ['Lentil we meet again!'],
    51: ['Chick it out!'], 53: ['Give peas a chance!'], 219: ['Lettuce celebrate!'],
}
GENERIC_PUNS = ['Field good!', 'Un-be-leaf-able!', 'Grow for it!']

# ---------------------------------------------------------------- crop lines, per character
# {x} = spoken name, {X} = capitalized. Templates are rotated per crop so wording varies.
T = {
    'earl': {
        'left': ["{X} on your left.", "Got {x} off to the left there.", "Left side, that's {x}.", "Well now, {x} on the left.",
                 "Lookee there, {x} on your left.", "That's {x} off to the left, partner.", "Over on the left, {x}.", "Some good-lookin' {x} on the left."],
        'right': ["{X} on your right.", "Got {x} off to the right there.", "Right side, that's {x}.", "Well now, {x} on the right.",
                  "Lookee there, {x} on your right.", "That's {x} off to the right, partner.", "Over on the right, {x}.", "Some good-lookin' {x} on the right."],
        'around': ["{X} all around ya.", "We're plumb surrounded by {x}.", "Nothin' but {x} far as you can see.", "{X} everywhere you look, partner."],
        'both': ["{X} on both sides.", "{X} left and right. Can't miss it."],
    },
    'dot': {
        'left': ["Oh, look, {x} on your left, dear.", "{X} on the left, honey.", "There's {x} on your left, sweetie.", "On the left, {x}. Isn't that nice?",
                 "Look at that {x} on the left!", "Left side, dear, that's {x}.", "Oh, {x} on the left. How lovely."],
        'right': ["Oh, look, {x} on your right, dear.", "{X} on the right, honey.", "There's {x} on your right, sweetie.", "On the right, {x}. Isn't that nice?",
                  "Look at that {x} on the right!", "Right side, dear, that's {x}.", "Oh, {x} on the right. How lovely."],
        'around': ["We're right in the middle of {x}, honey.", "{X} everywhere you look, dear.", "Oh my, {x} all around us."],
        'both': ["{X} on both sides, dear.", "Oh, {x} on both sides of the road!"],
    },
    'buck': {
        'left': ["On the left, it's {x}!", "And on the left side... {x}!", "Coming up on the left, {x}, folks!", "Left side, ladies and gentlemen, {x}!",
                 "Look at that {x} on the left!", "Let's hear it for the {x} on the left!"],
        'right': ["On the right, it's {x}!", "And on the right side... {x}!", "Coming up on the right, {x}, folks!", "Right side, ladies and gentlemen, {x}!",
                  "Look at that {x} on the right!", "Let's hear it for the {x} on the right!"],
        'around': ["We are surrounded by {x}, folks!", "{X} as far as the eye can see!", "It's {x} on every side!"],
        'both': ["{X} on both sides! What a matchup!", "{X} left and right, folks! A clean sweep!"],
    },
    'penny': {
        'left': ["{X} on your left! {pun}", "Ooh, {x} on the left!", "Left side, {x}! Love it!", "{X} on the left! Woo!", "Hello, {x}, on the left!"],
        'right': ["{X} on your right! {pun}", "Ooh, {x} on the right!", "Right side, {x}! Love it!", "{X} on the right! Woo!", "Hello, {x}, on the right!"],
        'around': ["{X} everywhere! {pun}", "We're surrounded by {x}! Best. Day. Ever."],
        'both': ["{X} on both sides! Double the fun!", "{X} left and right! {pun}"],
    },
    'kernel': {
        'left': ["Whoa, {x} on the left!", "Look look look, {x} on the left!", "Left side! It's {x}!", "Ooh, {x}! On the left!", "Hey, {x} on the left! Hi, {x}!"],
        'right': ["Whoa, {x} on the right!", "Look look look, {x} on the right!", "Right side! It's {x}!", "Ooh, {x}! On the right!", "Hey, {x} on the right! Hi, {x}!"],
        'around': ["{X} everywhere! So cool!", "We're totally surrounded by {x}!"],
        'both': ["{X} on both sides! Double cool!", "{X} on the left and the right!"],
    },
    'sam': {
        'left': ["{X} on your left.", "On your left, {x}.", "Left: {x}."],
        'right': ["{X} on your right.", "On your right, {x}.", "Right: {x}."],
        'around': ["{X} all around you.", "Surrounded by {x}."],
        'both': ["{X} on both sides."],
    },
}
# How many lines per crop and side (more for the crops you hear most).
BIG = {1, 5, 37, 24, 36, 2, 23, 4, 26, 3, 21, 31, 28, 6, 43, 69, 75, 68, 72, 212}
PER = {'left': 3, 'right': 3, 'around': 2, 'both': 1}

# Extra crop-specific lines for the crops people pass most. Side-free, said after a crop change.
FLAVOR = {
    'earl': {
        1: ["Corn. The backbone of the whole Midwest, right there.", "That corn's about knee high to a giraffe."],
        5: ["Beans. Corn's best friend. They take turns, year to year."],
        2: ["Cotton. Like a field full of clouds."],
        70: ["Christmas trees! Don't see many of those out here. That's a rare one."],
        6: ["Sunflowers. Now that'll put a smile on your face."],
    },
    'dot': {
        1: ["Corn! Your grandpa loved corn on the cob. Butter and salt, every time."],
        5: ["Soybeans, dear. They make tofu out of those, you know."],
        229: ["Pumpkins! Oh, I'm thinking pie already."],
        68: ["Apples! I'll make a crisp when we get home."],
    },
    'buck': {
        1: ["Corn! The heavyweight champion of the Midwest!"],
        5: ["Soybeans! The number two contender, and they are hungry!"],
        70: ["A Christmas tree farm! You do not see that every day, folks!"],
    },
    'penny': {
        1: ["Corn! Sorry, I know, that's a little corny."],
        229: ["Pumpkins! Oh my gourd, this is the best day ever!"],
        6: ["Sunflowers! They look so happy. I'm happy. Everyone's happy!"],
    },
    'kernel': {
        1: ["Corn on the left! That's my family! Hi, Grandma!", "Corn! Those are my cousins. I have a lot of cousins."],
        5: ["Soybeans! They're my buddies."],
        13: ["Popcorn! That's my cousin who gets really excited when it's hot."],
    },
    'sam': {},
}

# ---------------------------------------------------------------- not crops
SPOTS = {
    'town': {
        'earl': ["Bit of town here. Houses ain't a crop, last I checked.", "Town comin' up. Not much growin' but lawns."],
        'dot': ["A little town, dear. I wonder if they have a bakery.", "Houses, honey. I bet somebody's baking something."],
        'buck': ["We've got houses, folks! Not a crop, but we respect it!", "Entering town! Crops will return after these messages!"],
        'penny': ["Houses! Not a crop. I checked. Twice.", "Town! Fun fact: lawns are not a crop. Sad."],
        'kernel': ["Houses! Do people live there? Do they like corn?", "A town! Can we get snacks?"],
        'sam': ["Passing through town.", "Town for a bit. No crops here."],
    },
    'water': {
        'earl': ["Little water there. The ducks are happy.", "Water. Good for the crops, good for the fish."],
        'dot': ["Oh, look at the water. So peaceful.", "A pond! Your grandpa used to fish in one like that."],
        'buck': ["Water on deck! Splash zone, folks!", "That's water! The fish are cheering!"],
        'penny': ["Water! Wet. Very wet.", "Ooh, water! Fish puns incoming. Just kidding. Or am I?"],
        'kernel': ["Water! Do fish like corn? I hope fish like corn.", "Ooh, a lake! Can I swim? I can't swim. I'm corn."],
        'sam': ["Water nearby.", "Passing some water."],
    },
    'woods': {
        'earl': ["Trees there. The woods don't need much farmin'.", "Bit of woods. Good shade for the deer."],
        'dot': ["Oh, the trees are lovely this time of year.", "Woods, dear. Watch for deer."],
        'buck': ["Trees! Doing tree things, folks!", "A forest appears! The crowd is stunned!"],
        'penny': ["Trees! Doing tree things. I love that for them.", "Woods! Wood you believe it?"],
        'kernel': ["Trees! They're so tall. I wanna be tall.", "A forest! Is it spooky? It's a little spooky."],
        'sam': ["Woods along here.", "Passing some forest."],
    },
    'wetland': {
        'earl': ["Wetlands. Birds love it, tractors don't.", "Marshy ground there. Leave it to the cranes."],
        'dot': ["A marsh, dear. Listen for the frogs.", "Wetlands. Oh, the birds must love it."],
        'buck': ["Wetlands, folks! The frogs are going wild!"],
        'penny': ["Swampy! Toad-ally awesome."],
        'kernel': ["A swamp! Are there frogs? I bet there are frogs."],
        'sam': ["Wetlands along here."],
    },
    'pasture': {
        'earl': ["Pasture. That's the cow buffet.", "Grass for the cattle there. All you can eat."],
        'dot': ["Grassland, dear. Watch for the cows!", "Pasture. Oh, I hope we see some horses."],
        'buck': ["Pasture! The all-you-can-eat cow buffet is open!"],
        'penny': ["Pasture! Moo-velous.", "Grass! The cow buffet. Udderly delicious."],
        'kernel': ["Grass! For cows! Moo! Did I do a good moo?"],
        'sam': ["Pasture and grassland.", "Grassland along here."],
    },
    'fallow': {
        'earl': ["That field's restin' this year. Takin' a nap.", "Fallow ground there. Gets a year off."],
        'dot': ["That field's taking a little rest, dear. Good for it."],
        'buck': ["That field is sitting this season out, folks!"],
        'penny': ["That field is taking a nap. Relatable."],
        'kernel': ["That field is sleeping! Shh!"],
        'sam': ["A resting field. Nothing planted this year."],
    },
    'scrub': {
        'earl': ["Scrubland. Too dry for much but tumbleweeds.", "Open country. Not much farmin' out here."],
        'dot': ["Oh, it's so wide open out here, dear."],
        'buck': ["Wide open country, folks! Tumbleweed territory!"],
        'penny': ["Scrubland! Very scrubby. Ten out of ten scrub."],
        'kernel': ["It's all bushes! Where did all the farms go?"],
        'sam': ["Open scrubland.", "Desert scrub along here."],
    },
}

# ---------------------------------------------------------------- states
STATES = {
    'AL': ('Alabama', 'Yellowhammer State', 'Alabama grows a lot of peanuts and cotton.'),
    'AZ': ('Arizona', 'Grand Canyon State', 'Yuma, Arizona grows most of the country\'s winter lettuce.'),
    'AR': ('Arkansas', 'Natural State', 'Arkansas grows more rice than any other state.'),
    'CA': ('California', 'Golden State', 'California grows nearly all of America\'s almonds.'),
    'CO': ('Colorado', 'Centennial State', 'Colorado grows lots of wheat, and famous Rocky Ford melons.'),
    'CT': ('Connecticut', 'Constitution State', 'Connecticut grows special tobacco for cigar wrappers.'),
    'DE': ('Delaware', 'First State', 'Delaware grows a lot of lima beans.'),
    'FL': ('Florida', 'Sunshine State', 'Florida is famous for its oranges.'),
    'GA': ('Georgia', 'Peach State', 'Georgia grows more peanuts than any other state.'),
    'ID': ('Idaho', 'Gem State', 'Idaho grows more potatoes than any other state.'),
    'IL': ('Illinois', 'Prairie State', 'Illinois grows more pumpkins than any other state.'),
    'IN': ('Indiana', 'Hoosier State', 'Indiana grows lots of corn, and lots of popcorn.'),
    'IA': ('Iowa', 'Hawkeye State', 'Iowa grows more corn than any other state.'),
    'KS': ('Kansas', 'Sunflower State', 'Kansas grows more wheat than just about anywhere.'),
    'KY': ('Kentucky', 'Bluegrass State', 'Kentucky grows a lot of tobacco, and raises famous horses.'),
    'LA': ('Louisiana', 'Pelican State', 'Louisiana grows sugarcane and rice, and raises crawfish in the rice fields.'),
    'ME': ('Maine', 'Pine Tree State', 'Maine is famous for wild blueberries and potatoes.'),
    'MD': ('Maryland', 'Old Line State', 'Maryland grows corn and soybeans, and loves its crabs.'),
    'MA': ('Massachusetts', 'Bay State', 'Massachusetts is home to cranberry bogs.'),
    'MI': ('Michigan', 'Great Lakes State', 'Michigan grows more tart cherries than any other state.'),
    'MN': ('Minnesota', 'North Star State', 'Minnesota grows more sugarbeets than any other state.'),
    'MS': ('Mississippi', 'Magnolia State', 'Mississippi grows cotton, soybeans and rice.'),
    'MO': ('Missouri', 'Show-Me State', 'Missouri grows soybeans and corn, and rice down in the Bootheel.'),
    'MT': ('Montana', 'Treasure State', 'Montana grows tons of wheat, and more lentils and dry peas than any other state.'),
    'NE': ('Nebraska', 'Cornhusker State', 'Nebraska grows a ton of corn, and more popcorn than any other state.'),
    'NV': ('Nevada', 'Silver State', 'Nevada\'s biggest crop is alfalfa hay.'),
    'NH': ('New Hampshire', 'Granite State', 'New Hampshire has apple orchards and sweet maple syrup.'),
    'NJ': ('New Jersey', 'Garden State', 'New Jersey grows blueberries and cranberries.'),
    'NM': ('New Mexico', 'Land of Enchantment', 'New Mexico is famous for green chile peppers.'),
    'NY': ('New York', 'Empire State', 'New York grows a lot of apples.'),
    'NC': ('North Carolina', 'Tar Heel State', 'North Carolina grows more sweet potatoes than any other state.'),
    'ND': ('North Dakota', 'Peace Garden State', 'North Dakota grows more sunflowers than any other state.'),
    'OH': ('Ohio', 'Buckeye State', 'Ohio grows lots of corn and soybeans.'),
    'OK': ('Oklahoma', 'Sooner State', 'Oklahoma grows winter wheat, and cattle graze on it.'),
    'OR': ('Oregon', 'Beaver State', 'Oregon grows more Christmas trees than any other state.'),
    'PA': ('Pennsylvania', 'Keystone State', 'Pennsylvania grows more mushrooms than any other state.'),
    'RI': ('Rhode Island', 'Ocean State', 'Rhode Island is tiny, but it\'s got some sweet little farms.'),
    'SC': ('South Carolina', 'Palmetto State', 'South Carolina grows a lot of peaches.'),
    'SD': ('South Dakota', 'Mount Rushmore State', 'South Dakota grows corn, soybeans and sunflowers.'),
    'TN': ('Tennessee', 'Volunteer State', 'Tennessee grows soybeans, corn and cotton.'),
    'TX': ('Texas', 'Lone Star State', 'Texas grows more cotton than any other state.'),
    'UT': ('Utah', 'Beehive State', 'Utah grows hay and tart cherries.'),
    'VT': ('Vermont', 'Green Mountain State', 'Vermont makes more maple syrup than any other state.'),
    'VA': ('Virginia', 'Old Dominion', 'Virginia grows apples, peanuts and tobacco.'),
    'WA': ('Washington', 'Evergreen State', 'Washington grows more apples than any other state.'),
    'WV': ('West Virginia', 'Mountain State', 'West Virginia is where the Golden Delicious apple was born.'),
    'WI': ('Wisconsin', 'Badger State', 'Wisconsin grows more cranberries than any other state.'),
    'WY': ('Wyoming', 'Equality State', 'Wyoming grows hay and sugarbeets.'),
}
STATE_T = {
    'earl': "Welcome to {S}, partner. The {N}. {F}",
    'dot': "Welcome to {S}, honey! {F}",
    'buck': "Ladies and gentlemen, welcome to {S}, the {N}! {F}",
    'penny': "Hello, {S}! The {N}! {F} Fun!",
    'kernel': "We're in {S}! {F} Cool!",
    'sam': "Welcome to {S}, the {N}. {F}",
}

# ---------------------------------------------------------------- farm belts
BELTS = {
    'corn': ('the Corn Belt', 'Buckle up, it\'s a whole lot of corn.'),
    'wheat': ('the Wheat Belt', 'Amber waves of grain, here we come.'),
    'spring': ('Spring Wheat Country', 'Wheat as far as the eye can see.'),
    'cotton': ('Cotton Country', 'Fluffy fields ahead.'),
    'rice': ('the Rice Bowl', 'Rice fields, flooded and shiny.'),
    'fruit': ("America's Fruit Basket", 'Fruits and nuts and all the good stuff.'),
    'citrus': ('the Citrus Belt', 'Oranges and grapefruit ahead.'),
    'potato': ('Potato Country', 'Spud country.'),
    'palouse': ('the Palouse', 'Rolling hills of wheat. Gorgeous.'),
    'beets': ('Sugarbeet Valley', 'Sweet country ahead.'),
}
BELT_T = {
    'earl': ["Well, we just rolled into {B}. {F}"],
    'dot': ["Oh, honey, we're in {B} now. {F}"],
    'buck': ["Ladies and gentlemen, we have officially entered {B}! {F}"],
    'penny': ["We're in {B}! {F} Woo!"],
    'kernel': ["We're in {B}! {F} Yay!"],
    'sam': ["Entering {B}. {F}"],
}

# ---------------------------------------------------------------- facts (true, kept conservative)
FACTS = {
    1: ["An acre of corn grows about twenty-five million kernels.", "Most corn grown out here feeds livestock or becomes ethanol, not corn on the cob.",
        "An ear of corn almost always has an even number of rows."],
    5: ["Soybeans make their own fertilizer, with help from tiny bacteria on their roots.", "A bushel of soybeans makes about eleven pounds of oil."],
    24: ["A bushel of wheat makes about forty-two loaves of bread."], 23: ["A bushel of wheat makes about forty-two loaves of bread."],
    2: ["One bale of cotton can make about two hundred pairs of jeans."],
    36: ["Alfalfa roots can reach twenty feet deep."],
    3: ["Arkansas grows almost half of America's rice."],
    4: ["Sorghum handles drought better than corn does."],
    6: ["Young sunflowers turn to follow the sun across the sky."],
    43: ["Idaho grows about a third of America's potatoes."],
    75: ["California grows about eighty percent of the world's almonds."],
    69: ["A ton of grapes makes about seven hundred bottles of wine."],
    68: ["Thousands of apple varieties are grown in the United States."],
    229: ["Illinois grows more pumpkins than any other state."],
    250: ["Cranberries don't grow underwater. The bogs are flooded at harvest, so the berries float."],
    70: ["A Christmas tree takes about seven years to grow."],
    10: ["Peanuts aren't really nuts. They're legumes that grow underground."],
    212: ["Most Florida oranges become orange juice."], 72: ["Most Florida oranges become orange juice."],
    41: ["About half of America's sugar comes from sugarbeets."],
    45: ["Sugarcane is a giant grass that can grow over twelve feet tall."],
    31: ["Canola got its name from Canada, oil, and low acid."],
    74: ["Pecans are the only major tree nut native to North America."],
    242: ["Blueberries are native to North America."],
    54: ["Botanically speaking, a tomato is a fruit."],
    21: ["A lot of barley ends up as malt, for brewing."],
    28: ["Oats like it cool and wet."],
}
GENERAL_FACTS = ["There are about two million farms in the United States.", "Farmland covers about forty percent of the United States.",
                 "One American farmer feeds about a hundred and sixty people."]
FACT_T = {
    'earl': ["Here's somethin' for ya. {F}", "Fun fact, partner. {F}"],
    'dot': ["Did you know, dear? {F}", "Here's a little something, honey. {F}"],
    'buck': ["Fun fact, folks! {F}", "Ladies and gentlemen, did you know? {F}"],
    'penny': ["Fun fact time! {F}", "Ooh, fun fact! {F}"],
    'kernel': ["Did you know? {F} Whoa!", "Fun fact! {F} So cool!"],
    'sam': ["Did you know? {F}", "Here's a fact. {F}"],
}

# ---------------------------------------------------------------- one-off moments
MOMENTS = {
    'hello': {
        'earl': ["Howdy. I'll holler out the crops as we go.", "Alright, partner. I'll keep an eye on the fields."],
        'dot': ["Hello, sweetie! I'll tell you what's growing as we go.", "Oh, a drive! I'll keep you company, dear."],
        'buck': ["Ladies and gentlemen, it's crop time!", "Welcome, folks, to the greatest show on dirt!"],
        'penny': ["Hiii! Lettuce begin!", "Okay, I'm so ready. Let's spot some crops!"],
        'kernel': ["Hi! It's me, Kernel! Let's find crops!", "Road trip! Road trip! I'll call out the crops!"],
        'sam': ["Voice on. I'll name the crops as we go.", "Ready. I'll call out the fields."],
    },
    'start:morning': {
        'earl': ["Mornin'. Good day for a drive.", "Early bird gets the corn. Let's go."],
        'dot': ["Good morning, dear! Did you eat breakfast?", "Morning, sweetie. Coffee in hand? Let's go."],
        'buck': ["Good morning, folks! The fields are wide awake!"],
        'penny': ["Good morning, sunshine! Rise and grind! Get it? Grain?"],
        'kernel': ["Good morning! I'm awake! Are you awake?"],
        'sam': ["Good morning. Let's see what's growing."],
    },
    'start:afternoon': {
        'earl': ["Afternoon. Let's see what's growin'.", "Good afternoon for it. Let's roll."],
        'dot': ["Good afternoon, honey. Drive safe now."],
        'buck': ["Good afternoon, folks! Let's get this show on the road!"],
        'penny': ["Afternoon road trip! Best kind of trip!"],
        'kernel': ["Afternoon adventure! Let's go!"],
        'sam': ["Good afternoon. Let's see what's growing."],
    },
    'start:evening': {
        'earl': ["Evenin'. Fields look their best this time of day.", "Golden hour. Prettiest time for a drive."],
        'dot': ["Good evening, dear. Isn't the light pretty?"],
        'buck': ["Good evening, folks! Prime time on the farm!"],
        'penny': ["Evening drive! Sunset vibes!"],
        'kernel': ["It's evening! Is it almost bedtime? Not yet!"],
        'sam': ["Good evening. Let's see what's growing."],
    },
    'start:night': {
        'earl': ["Night drive, huh. I'll keep talkin' so you stay awake.", "Dark out. The crops are still there, promise."],
        'dot': ["Oh, it's late, honey. Drive careful."],
        'buck': ["A night drive, folks! The crops never sleep!"],
        'penny': ["Night owl mode! Hoo hoo!"],
        'kernel': ["It's so dark! The corn is sleeping. Shh."],
        'sam': ["Night drive. Stay alert."],
    },
    'end': {
        'earl': ["Good drive, partner. See ya next time.", "That's a wrap. Fields'll be here when ya get back."],
        'dot': ["Oh, that was a lovely drive, dear. Get some rest.", "Bye, sweetie! Call me when you get home."],
        'buck': ["And that's the show, folks! Goodnight, and drive safe!", "What a drive! Thank you, and goodnight!"],
        'penny': ["Peas out! Thanks for the ride!", "That was a-maize-ing! Bye!"],
        'kernel': ["That was the best drive ever! Bye bye!", "Aww, done already? Okay, bye!"],
        'sam': ["Drive ended.", "That's the end of the drive."],
    },
    'card': {
        'earl': ["New crop card for the collection.", "Well, there's a new card."],
        'dot': ["Oh, a new card, dear! How exciting!", "You got a new card, sweetie!"],
        'buck': ["New crop card! The crowd goes wild!", "Ladies and gentlemen, a brand new card!"],
        'penny': ["New crop card! Lettuce celebrate!", "Ooh, new card! Yay!"],
        'kernel': ["New crop card! New crop card!", "Yay! A new card! Can I hold it?"],
        'sam': ["New crop card.", "Added a new crop card."],
    },
    'rare': {
        'earl': ["Well, I'll be. That's a rare one.", "Don't see that every day."],
        'dot': ["Oh my, that's a rare one, dear!"],
        'buck': ["A rare sighting, folks! Rare!"],
        'penny': ["Ooh, a rare one! Rare-ly do we see that! Get it?"],
        'kernel': ["Whoa! A rare one! A really rare one!"],
        'sam': ["That's a rare one."],
    },
    'badge': {
        'earl': ["You earned yourself a badge.", "New badge. Not bad, partner."],
        'dot': ["A badge! I'm so proud of you, dear."],
        'buck': ["A new badge, folks! What a champion!"],
        'penny': ["Badge unlocked! You're on fire!"],
        'kernel': ["You got a badge! You're the best!"],
        'sam': ["New badge earned."],
    },
    'bingo:square': {
        'earl': ["That's a bingo square.", "Check that one off the bingo card."],
        'dot': ["Ooh, a bingo square, dear!"],
        'buck': ["Bingo square! Mark it down!"],
        'penny': ["Bingo square! Check!"],
        'kernel': ["Bingo square! Yay!"],
        'sam': ["Bingo square."],
    },
    'bingo': {
        'earl': ["Bingo! Well, how about that.", "Bingo, partner!"],
        'dot': ["Bingo! Oh, I just love bingo!"],
        'buck': ["Bingo! Bingo! Bingo! We have a winner!"],
        'penny': ["Bingo! Bing-oh-my-gosh!"],
        'kernel': ["Bingo! I love bingo! We won!"],
        'sam': ["Bingo."],
    },
    'gps:lost': {
        'earl': ["Lost the signal there. Hang tight.", "Signal's gone quiet. It'll come back."],
        'dot': ["Oh, I lost you for a second, dear."],
        'buck': ["We've lost the signal, folks! Stand by!"],
        'penny': ["Uh oh, no signal! Don't panic. I'm panicking."],
        'kernel': ["Where are we? I can't tell! Hang on!"],
        'sam': ["GPS signal lost."],
    },
    'gps:back': {
        'earl': ["There we go. Back on track.", "Signal's back."],
        'dot': ["There you are, dear!"],
        'buck': ["And we're back, folks!"],
        'penny': ["We're back! Phew!"],
        'kernel': ["Found us! Yay!"],
        'sam': ["GPS signal back."],
    },
    'streak': {
        'earl': ["Same crop for a while now. Consistent.", "Long stretch of the same. Farmers like what works.", "Still more of the same. Good thing it's pretty."],
        'dot': ["My, there's a lot of it out here, isn't there?", "Still more of the same, dear. Want to play a game?"],
        'buck': ["The same crop is defending its title, folks!", "What a streak! Nobody can stop it!"],
        'penny': ["Still the same crop! Consistency is key!", "Same crop! Again! I love commitment."],
        'kernel': ["It's still the same! Are we going in circles?", "Same crop again! Are we there yet?"],
        'sam': ["Same crop for a while now.", "Still the same crop."],
    },
}
STREAK_CROP = {
    1: {'earl': ["Still corn. I'd act surprised, but I'd be lyin'."], 'dot': ["Corn again. Well, it's good for you, so I won't complain."],
        'buck': ["Corn is still the champion, folks! Undefeated!"], 'penny': ["Still corn! Shocking, I know."],
        'kernel': ["Still corn! My family is huge!"], 'sam': ["Still corn."]},
    5: {'earl': ["Still beans. Lotta beans."], 'dot': ["Still soybeans, dear. That's a lot of tofu."],
        'buck': ["Soybeans keep rolling, folks!"], 'penny': ["Still soybeans! Bean there, still doing that!"],
        'kernel': ["Still soybeans! Hi again, buddies!"], 'sam': ["Still soybeans."]},
    24: {'earl': ["Still wheat. Amber waves and all that."], 'dot': ["Still wheat, honey. That's a lot of bread."],
         'buck': ["Wheat is holding the lead, folks!"], 'penny': ["Still wheat! Wheat-ly consistent!"],
         'kernel': ["Still wheat! It's so wavy!"], 'sam': ["Still wheat."]},
    2: {'earl': ["Still cotton. Lotta T-shirts out there."], 'dot': ["Still cotton, dear. So many fluffy clouds."],
        'buck': ["Cotton keeps on coming, folks!"], 'penny': ["Still cotton! So fluffy!"],
        'kernel': ["Still cotton! Can I jump in it?"], 'sam': ["Still cotton."]},
}

JOKES = [
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "What did the corn say when it got a compliment? Aw, shucks.",
    "Why did the tomato blush? It saw the salad dressing.",
    "What do you call a sad strawberry? A blueberry.",
    "Why do potatoes make good detectives? They keep their eyes peeled.",
    "How do you fix a broken pumpkin? With a pumpkin patch.",
    "What's a farmer's favorite music? Anything with a good beet.",
    "What did the big flower say to the little flower? Hi, bud!",
    "Why did the farmer ride his horse to town? It was too heavy to carry.",
    "What do you call a stolen yam? A hot potato.",
]
JOKE_T = {'earl': "Here's one for ya. {J}", 'dot': "Oh, I heard a good one, dear. {J}", 'buck': "Joke time, folks! {J}",
          'penny': "Okay okay okay, joke time. {J}", 'kernel': "I know a joke! {J}", 'sam': "Here's a joke. {J}"}

MILES = {
    10: "That's ten miles.", 25: "Twenty-five miles in.", 50: "Fifty miles!", 100: "A hundred miles!", 250: "Two hundred fifty miles!", 500: "Five hundred miles!",
}
MILES_T = {'earl': "{M} Not bad, partner.", 'dot': "{M} Don't forget to stretch, dear.", 'buck': "{M} What a performance, folks!",
           'penny': "{M} We're on a roll! Like a bread roll!", 'kernel': "{M} Are we there yet?", 'sam': "{M}"}

AHEAD = [1, 5, 24, 23, 2, 36, 37, 4, 3, 21, 31, 28, 6, 43, 69, 75, 68, 72, 212, 41, 10, 45, 74, 70, 229]
AHEAD_T = {'earl': "Up ahead, mostly {x}.", 'dot': "Coming up, dear, lots of {x}.", 'buck': "Coming up next, folks, it's {x}!",
           'penny': "Up next: {x}! Get excited!", 'kernel': "Ooh, up ahead there's lots of {x}!", 'sam': "Ahead: mostly {x}."}
RECAP_T = {'earl': "Mostly {x} today. Good drive.", 'dot': "Lots of {x} today, dear!", 'buck': "Today's champion: {x}!",
           'penny': "Today was brought to you by {x}!", 'kernel': "We saw so much {x} today!", 'sam': "Today's top crop: {x}."}

HARVEST = {  # bucket -> generic line per character
    'start': {'earl': "Harvest's just gettin' started around here.", 'dot': "They're just starting the harvest, dear.", 'buck': "Harvest season has begun, folks!",
              'penny': "Harvest is starting! Combine time!", 'kernel': "They're starting the harvest! I see combines!", 'sam': "Harvest is just starting here."},
    'quarter': {'earl': "About a quarter of the harvest's in around here.", 'dot': "About a quarter of it's harvested, honey.", 'buck': "A quarter of the harvest is in, folks!",
                'penny': "A quarter harvested! Woo!", 'kernel': "A quarter is harvested! That's a lot!", 'sam': "About a quarter harvested here."},
    'half': {'earl': "Harvest is about half done around here.", 'dot': "They're about halfway through the harvest, dear.", 'buck': "We're at the halfway mark of the harvest, folks!",
             'penny': "Harvest is half done! Half full, not half empty!", 'kernel': "Halfway harvested! Go, combines, go!", 'sam': "Harvest is about halfway done here."},
    'most': {'earl': "Most of the harvest is in around here.", 'dot': "Most of it's harvested now, honey.", 'buck': "The harvest is in the final stretch, folks!",
             'penny': "Almost all harvested! So close!", 'kernel': "Almost done harvesting! Almost!", 'sam': "Most of the harvest is in."},
    'done': {'earl': "Harvest's about wrapped up here.", 'dot': "They're all done harvesting, dear.", 'buck': "And the harvest is complete, folks!",
             'penny': "Harvest is done! Time to celebrate!", 'kernel': "All harvested! Yay, farmers!", 'sam': "Harvest is about done here."},
}

BANTER = {
    'earl': ["Ever notice how the barns are all red? Cheap paint, back in the day.", "Good farm country, this.", "Wonder what the cows are thinkin'.",
             "A farmer's best friend is a good forecast.", "Combines cost more than most houses. True story."],
    'dot': ["Are you staying hydrated, dear?", "Remember to stretch your legs, honey.", "Oh, I love a good road trip.",
            "Your grandpa and I used to drive these roads.", "Did you call your mother?"],
    'buck': ["What a beautiful day for the greatest sport on Earth: farming!", "The fans are on their feet, folks! Well, the cows are.",
             "Keep it rolling, folks! Plenty more fields ahead!", "Is this the best road trip ever? The judges say yes!"],
    'penny': ["Are you having fun? I'm having fun!", "Road trip snacks are mandatory. Corn chips, maybe?", "I wonder if cows like puns. Probably not. Moo-ving on!",
              "Whoever invented road trips deserves a medal."],
    'kernel': ["Are we there yet?", "I'm hungry. Wait, I'm corn. Never mind.", "Can we get a dog?", "I love road trips! This is my favorite thing!",
               "Did you see that cow? I saw that cow!"],
    'sam': ["Plenty of farmland ahead.", "Remember to take breaks on long drives."],
}

# ---------------------------------------------------------------- round 3 cast
import lines_cast3 as r3
import lines_memes
CHARS = CHARS + r3.NEW
T.update(r3.T)
for d, add in ((FLAVOR, r3.FLAVOR), (MOMENTS, r3.MOMENTS), (STREAK_CROP, r3.STREAK_CROP), (HARVEST, r3.HARVEST), (SPOTS, r3.SPOTS)):
    for k, by in add.items():
        d.setdefault(k, {}).update(by)
for ch in r3.NEW:
    FLAVOR.setdefault(ch, {})
for d, add in ((STATE_T, r3.STATE_T), (BELT_T, r3.BELT_T), (FACT_T, r3.FACT_T), (JOKE_T, r3.JOKE_T), (MILES_T, r3.MILES_T),
               (AHEAD_T, r3.AHEAD_T), (RECAP_T, r3.RECAP_T), (BANTER, r3.BANTER)):
    d.update(add)
# Earl's welcome gets more Southern too.
STATE_T['earl'] = "Well, welcome to {S}, partner. The {N}. {F}"

# ---------------------------------------------------------------- build
def cap(s):
    return s[:1].upper() + s[1:]

def build(chars=CHARS):
    out = []
    def add(char, key, text):
        out.append({'char': char, 'key': key, 'text': text})
    for char in chars:
        rnd = random.Random(f'{char}-lines')
        for code, (x, name) in CROPS.items():
            for side, n in PER.items():
                temps = [t for t in T[char][side] if not (code in DOUBLE and ('good-lookin' in t or 'that ' in t))]
                n = n + 1 if code in BIG and side in ('left', 'right') else n
                picks = rnd.sample(temps, min(n, len(temps)))
                for t in picks:
                    pun = rnd.choice(PUNS.get(code, GENERIC_PUNS))
                    add(char, f'crop:{code}:{side}', t.replace('{X}', cap(x)).replace('{x}', x).replace('{pun}', pun))
            for line in FLAVOR.get(char, {}).get(code, []):
                add(char, f'flavor:{code}', line)
            # One-word lines come out garbled, so names are said in a short sentence.
            add(char, f'name:{code}', f"It's {name.lower() if name[:1].isupper() and name not in ('Christmas trees',) else name}{'.' if char == 'sam' else '!'}")
        for spot, by in SPOTS.items():
            for line in by.get(char, []):
                add(char, f'spot:{spot}', line)
        for st, (s, n, f) in STATES.items():
            add(char, f'state:{st}', STATE_T[char].replace('{S}', s).replace('{N}', n).replace('{F}', f))
        for b, (bname, f) in BELTS.items():
            for t in BELT_T[char]:
                add(char, f'belt:{b}', t.replace('{B}', bname).replace('{F}', f))
        for code, facts in FACTS.items():
            for f in facts:
                add(char, f'fact:{code}', rnd.choice(FACT_T[char]).replace('{F}', f))
        for f in GENERAL_FACTS:
            add(char, 'fact', rnd.choice(FACT_T[char]).replace('{F}', f))
        for key, by in MOMENTS.items():
            for line in by.get(char, []):
                add(char, key, line)
        for code, by in STREAK_CROP.items():
            for line in by.get(char, []):
                add(char, f'streak:{code}', line)
        for j in JOKES:
            add(char, 'joke', JOKE_T[char].replace('{J}', j))
        for m, line in MILES.items():
            add(char, f'miles:{m}', MILES_T[char].replace('{M}', line))
        for code in AHEAD:
            x = CROPS[code][0]
            add(char, f'ahead:{code}', AHEAD_T[char].replace('{X}', cap(x)).replace('{x}', x))
            add(char, f'recap:{code}', RECAP_T[char].replace('{x}', x))
        for bucket, by in HARVEST.items():
            if char in by:
                add(char, f'harvest:{bucket}', by[char])
        for line in BANTER[char]:
            add(char, 'banter', line)
        for key, more in lines_memes.EXTRA.get(char, {}).items():
            for line in more:
                add(char, key, line)
    return out

if __name__ == '__main__':
    lines = build()
    from collections import Counter
    by = Counter(l['char'] for l in lines)
    print(len(lines), 'lines', dict(by))
    print(len({l['key'] for l in lines}), 'keys')
    for l in random.Random(1).sample(lines, 25):
        print(l['char'], l['key'], '|', l['text'])
