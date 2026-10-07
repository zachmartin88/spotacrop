// Crop puns and jokes. Used by the punny voice style now, and by badges and toasts later.
import { prettyName } from './data.js';

const pick = (a) => a[Math.floor(Math.random() * a.length)];

// Matched against the crop's name, first hit wins (so "sweet potatoes" beats "potatoes").
const PUNS = [
  [/sweet potato/, ['Sweet!', 'Yam-tastic!']],
  [/sweet corn|pop or orn/, ['Pop-ular choice!', 'Sweet!']],
  [/corn/, ['Ear-resistible!', 'A-maize-ing!', 'Sorry, that was corny.', 'Shucks!']],
  [/soybean|dry bean|bean/, ['Bean there, done that.', 'Full of beans!', 'Un-bean-lievable!']],
  [/wheat|durum|triticale/, ['Wheat-ly done!', 'Wheat dreams!', 'Grain-tastic!']],
  [/alfalfa/, ['Alfalfa-bulous!', 'Hay, nice!']],
  [/hay/, ['Hay there!', 'Hay, look!', 'Hay is for horses!']],
  [/oat/, ['Oat of this world!', 'Oat-standing!']],
  [/rye/, ['Rye not?', 'Rye-t on!']],
  [/barley/, ['Barley made it!', 'Barley believable!']],
  [/sorghum/, ['Sorghum-thing special!', 'Sorghum fun!']],
  [/millet/, ['Millet-ary precision!']],
  [/cotton/, ['Cotton to like it!', 'Soft spot for this one.']],
  [/rice/, ['Rice to meet you!', 'Rice and shine!']],
  [/potato/, ['Spud-tacular!', 'Tater-ific!', 'Po-tay-to, po-tah-to.']],
  [/tomato/, ['Ketchup later!', 'Tom-ah-to!']],
  [/greens|lettuce/, ['Lettuce celebrate!', 'Lettuce turnip the beet!']],
  [/chick pea/, ['Chick it out!']],
  [/pea/, ['Peas and love!', 'Give peas a chance!']],
  [/lentil/, ['Lentil we meet again!']],
  [/pumpkin/, ['Oh my gourd!', 'Gourd-geous!']],
  [/squash/, ['Squash goals!', 'Gourd job!']],
  [/apple/, ['Apple-solutely!', 'Core-rect!']],
  [/grape/, ['Grape expectations!', 'That\'s grape!']],
  [/cherr/, ['Cherry on top!', 'Cherry-ish this!']],
  [/cranberr/, ['Berry bog-tastic!', 'Berry nice!']],
  [/blueberr|berr/, ['Berry nice!', 'Berry impressive!']],
  [/peach/, ['Peachy keen!', 'Life\'s a peach!']],
  [/pear/, ['Pear-fect!', 'Ap-pear-ing now!']],
  [/plum|prune/, ['Plum good!', 'Plum-believable!']],
  [/apricot/, ['Apri-cool!']],
  [/citrus|orange/, ['Orange you glad?', 'Zest of luck!']],
  [/onion/, ['This one makes me tear up.', 'Onion rings a bell!']],
  [/garlic/, ['Garlic? Clove it!', 'Breath of fresh air. Not.']],
  [/carrot/, ['Carrot top!', 'What\'s up, doc?']],
  [/pepper/, ['Hot stuff!', 'Pepper-oni? Close!']],
  [/watermelon|cantaloupe|honeydew|melon/, ['One in a melon!', 'Melon-choly no more!']],
  [/cucumber/, ['Cool as a cucumber!', 'Kind of a big dill.']],
  [/sunflower/, ['Bright idea!', 'Look on the sunny side!']],
  [/peanut|almond|pecan|walnut|pistachio/, ['Nuts about it!', 'Totally nuts!']],
  [/olive/, ['Olive it!', 'Olive you!']],
  [/avocado/, ['Holy guacamole!', 'Avo-good day!']],
  [/christmas/, ['Fir real!', 'Tree-mendous!']],
  [/broccoli/, ['Tree-mendous!']],
  [/radish/, ['Rad-ish!']],
  [/asparagus/, ['Spear-tacular!']],
  [/mint/, ['Mint condition!']],
  [/herb/, ['Thyme flies!']],
  [/canola/, ['Canola-la!']],
  [/flax/, ['Just the flax!']],
  [/sugar/, ['Sweet!', 'Sugar rush!']],
  [/clover/, ['Feeling lucky!']],
  [/grass|pasture/, ['Cow buffet!', 'Moo-velous!']],
  [/fallow|idle/, ['This field is taking a nap.']],
];
const GENERIC = ['Field good!', 'Un-be-leaf-able!', 'Crop of the morning!', 'Grow for it!'];

/** A pun for this crop (a random one when it has a few). */
export function cropPun(code) {
  const name = prettyName(code).toLowerCase();
  for (const [re, list] of PUNS) if (re.test(name)) return pick(list);
  return pick(GENERIC);
}

// Kernel's corniest jokes, for when you tap him.
export const JOKES = [
  'Why did the tomato blush? It saw the salad dressing.',
  'What do you call a sad strawberry? A blueberry.',
  'Why do potatoes make good detectives? They keep their eyes peeled.',
  'What did the corn say when it got complimented? Aw, shucks.',
  'Why did the scarecrow win an award? He was outstanding in his field.',
  'What do you call a stolen yam? A hot potato.',
  'How do you fix a broken pumpkin? With a pumpkin patch.',
  'What\'s a farmer\'s favorite kind of music? Anything with a good beet.',
  'Why did the farmer ride his horse to town? It was too heavy to carry.',
  'What did the big flower say to the little flower? Hi, bud!',
  'Why are peppers good at archery? They habanero.',
  'What do you call a cow with no legs? Ground beef.',
];
export const joke = () => pick(JOKES);
