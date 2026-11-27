"""Saison 2 « Wild Nights » — épisodes 19 à 24 (s2e07 à s2e12) : course contre la lune, traces dans la neige, chasse à la plume,
fausse alerte, radeau sur la rivière, et la plus longue nuit (finale)."""
from .episodes_s2a import song, L, R

# ======================================================================= 19. Race to the Moon Pond  (course contre la montre)
S2E07 = dict(id="s2e07", style="s2", title="Race to the Moon Pond", bye_decor="pond_night",
  blurb="The full moon will sit on the water of the Moon Pond, but only for a little while. Pip zooms ahead, Shelly walks slowly, and a wide stream is in the way.",
  fact="a turtle's shell is part of its body, so it can never take it off. On land turtles are slow, but in water many of them swim fast.",
  chapters=[
    dict(label="The Moon Promise", story=[
        dict(decor="pond_night", cast=[("turtle", 420, 420, L), ("mimo", -150, 880, R)], lines=[
            ("narrator", "Once a year, when the moon is full and round, it sits right on the water of the Moon Pond."),
            ("turtle", "Mimo, I'm Shelly. I want to see the moon on the water tonight. But it only stays for a little while."),
            ("mimo", "Then we'd better start walking, Shelly!"),
            ("turtle", "Slowly, slowly. I'm a turtle, you know. But I'll get there.")]),
    ], song=song("Twinkle Twinkle Little Star", "pond_night", [("turtle", 440, L), ("mimo", 860, R)], "bell", -2)),

    dict(label="Pip Zooms Ahead", story=[
        dict(decor="meadow_night", cast=[("turtle", 330, 330, L), ("mimo", 640, 640, L), ("bunny", 1450, 960, R)], lines=[
            ("bunny", "Hop hop! Moon Pond? I can be there in two minutes! Watch me!"),
            ("turtle", "Pip, wait. We should go together."),
            ("bunny", "Too slow, Shelly! I'm a rabbit. Zoom, zoom, zoom!"),
            ("narrator", "And off went Pip, faster than the wind, leaving a little cloud of dust behind him."),
            ("mimo", "Don't worry, Shelly. I'll walk with you. Every step counts.")]),
    ], song=song("London Bridge", "meadow_night", [("turtle", 330, L), ("mimo", 640, L), ("bunny", 960, R)], "soft", 0)),

    dict(label="Steady Steps", story=[
        dict(decor="forest_night", cast=[("mimo", -150, 330, L), ("turtle", -420, 640, L), ("owl", 1450, 960, R)], lines=[
            ("owl", "Hoo hoo. Where are you two going?"),
            ("mimo", "To the Moon Pond. Shelly can't wait to see the moon on the water."),
            ("owl", "Shelly, aren't you tired? Carrying that big shell?"),
            ("turtle", "It's not heavy, Luna. It's my house, and my back, and my ribs, all in one. I never take it off."),
            ("owl", "Hoo hoo. Then you are always at home, wherever you go.")]),
    ], song=song("Row Row Row Your Boat", "forest_night", [("mimo", 330, L), ("turtle", 640, L), ("owl", 960, R)], "harp", 0)),

    dict(label="The Wide Stream", story=[
        dict(decor="river_night", cast=[("bunny", 420, 420, L), ("mimo", -150, 760, R), ("turtle", -420, 1040, R)], lines=[
            ("bunny", "Oh no. A stream! It's so wide. And cold. And wet. I don't like wet paws."),
            ("mimo", "Pip! You stopped!"),
            ("bunny", "I got here first, but I can't cross. And the moon is rising higher!"),
            ("turtle", "Good evening, Pip. I know a way across. Slowly on land, but quickly in water!")]),
    ], song=None),

    dict(label="Across Together", story=[
        dict(decor="river_night", cast=[("turtle", 420, 420, L), ("bunny", 760, 760, R), ("mimo", 1050, 1050, R)], lines=[
            ("turtle", "Hop on my shell, Pip. It's flat and strong. And Mimo, you can swim next to me."),
            ("bunny", "Really? You'd carry me?"),
            ("turtle", "Of course. You were fast on the land. Now I'll be fast in the water. Everyone is good at something."),
            ("narrator", "And with a splash, Shelly glided across the stream, paddling with her strong flippers, faster than anyone had expected.")]),
    ], song=song("Row Row Row Your Boat", "river_night", [("turtle", 330, L), ("bunny", 640, L), ("mimo", 960, R)], "soft", 2)),

    dict(label="The Moon on the Water", story=[
        dict(decor="pond_night", cast=[("turtle", 330, 330, L), ("bunny", 640, 640, L), ("mimo", 950, 950, R)], lines=[
            ("narrator", "They arrived just in time. The moon was sitting on the pond, round and silver, shimmering on every ripple."),
            ("bunny", "It's the most beautiful thing I've ever seen. And I almost missed it, zooming so fast."),
            ("turtle", "Sometimes the best views are for those who go together."),
            ("mimo", "Goodnight, moon. Goodnight, Shelly. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="pond_night", cast=[("turtle", 230, L), ("bunny", 520, L), ("mimo", 810, R), ("fox", 1090, R)], minutes=12),
  teaser=dict(decor="snow_night", cast=[("otter", 420, 420, L), ("mimo", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("otter", "Mimo, look at all these tracks in the snow! Somebody left a mystery for us."),
      ("narrator", "Find out in the next episode: The Snow Day Surprise!")]))

# ======================================================================= 20. The Snow Day Surprise  (traces, glissade)
S2E08 = dict(id="s2e08", style="s2", title="The Snow Day Surprise", bye_decor="snow_night",
  blurb="Fresh snow covers the woods, and mysterious tracks cross it. Mimo and Finn follow them to a big surprise.",
  fact="every animal leaves its own footprints, and river otters love to slide on their bellies in the snow, to travel fast and to play.",
  chapters=[
    dict(label="Tracks in the Snow", story=[
        dict(decor="snow_night", cast=[("mimo", -150, 420, L), ("fox", 1450, 880, R)], lines=[
            ("narrator", "In the night, the snow had covered the whole forest, soft and white like a blanket."),
            ("mimo", "Finn! Look at all these footprints! Who walked here?"),
            ("fox", "Footprints are a secret code, Mimo. Every animal has its own. Do you want to learn to read them?"),
            ("mimo", "Yes, please!")]),
    ], song=song("Twinkle Twinkle Little Star", "snow_night", [("mimo", 440, L), ("fox", 860, R)], "bell", 2)),

    dict(label="Reading the Code", story=[
        dict(decor="snow_night", cast=[("mimo", 330, 330, L), ("fox", 700, 700, R), ("bunny", 1450, 1040, R)], lines=[
            ("fox", "Look at this one. Two big prints in front, and two small ones behind. Who is that?"),
            ("mimo", "A rabbit! Pip, is that you?"),
            ("bunny", "Hop hop! Yes! When I hop, my big back feet land in front of my little front feet."),
            ("fox", "And my prints are in one neat line, because I place my back paws right where my front paws were."),
            ("mimo", "That's so clever! And what about this long, smooth line, like a ribbon?")]),
    ], song=song("London Bridge", "snow_night", [("mimo", 310, L), ("fox", 650, R), ("bunny", 980, R)], "soft", 0)),

    dict(label="Following the Ribbon", story=[
        dict(decor="snow_night", cast=[("mimo", -150, 330, L), ("fox", -420, 640, L), ("bunny", -700, 950, L)], lines=[
            ("narrator", "The ribbon of snow wound between the pine trees, up a little hill, and then down again."),
            ("mimo", "Whoever made it must have been moving very fast."),
            ("fox", "And no paw prints on the sides. It looks like somebody slid on their belly."),
            ("bunny", "A slide! Who slides in the snow? I'm too curious to wait!")]),
    ], song=None),

    dict(label="Ollie's Slide", story=[
        dict(decor="snow_night", cast=[("mimo", 330, 330, L), ("otter", 700, 700, R), ("fox", 1030, 1030, R)], lines=[
            ("otter", "Wheee! Hi, everybody! Watch this!"),
            ("narrator", "Ollie ran three steps, tucked his front paws, and slid on his belly all the way down the hill."),
            ("mimo", "Ollie! It was you!"),
            ("otter", "Of course! Otters love to slide on snow and ice. It's the fastest way to travel, and it's also the most fun."),
            ("fox", "So that was the surprise. A snow slide party!")]),
    ], song=song("Row Row Row Your Boat", "snow_night", [("mimo", 320, L), ("otter", 650, R), ("fox", 980, R)], "harp", 2)),

    dict(label="Everyone Slides", story=[
        dict(decor="snow_night", cast=[("mimo", 230, 230, L), ("bunny", 500, 500, L), ("otter", 770, 770, R), ("fox", 1040, 1040, R)], lines=[
            ("otter", "Come on, Mimo! Lie on your belly, and push with your back legs!"),
            ("mimo", "Okay! One, two, three... Whee! I'm sliding!"),
            ("bunny", "My turn! Hop, hop, whee! I'm slippery as a snowball!"),
            ("fox", "I'll go last. Fox slide! Woo!"),
            ("narrator", "They slid down the hill again and again, until their fur was covered in snowflakes.")]),
    ], song=song("Mary Had a Little Lamb", "snow_night", [("mimo", 230, L), ("bunny", 500, L), ("otter", 770, R), ("fox", 1040, R)], "bell", 0)),

    dict(label="A Warm Snow Den", story=[
        dict(decor="den", cast=[("mimo", 330, 330, L), ("otter", 660, 660, R), ("fox", 960, 960, R)], lines=[
            ("narrator", "When the friends were tired and chilly, Ollie knew just where to go: a cozy den under the tree roots, warm and quiet."),
            ("otter", "Snow keeps the cold wind out. That's why the den is so warm inside."),
            ("fox", "Thank you for the best snow day, Ollie."),
            ("mimo", "Goodnight, Ollie. Goodnight, Finn. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="snow_night", cast=[("bunny", 230, L), ("mimo", 520, L), ("otter", 810, R), ("fox", 1090, R)], minutes=12),
  teaser=dict(decor="forest_night", cast=[("owl", 420, 420, L), ("mimo", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("owl", "Mimo, one of my feathers has gone missing. And without it, I can't fly silently."),
      ("narrator", "Find out in the next episode: Luna's Silent Feather!")]))

# ======================================================================= 21. Luna's Silent Feather  (chasse au trésor à travers les habitats)
S2E09 = dict(id="s2e09", style="s2", title="Luna's Silent Feather", bye_decor="forest_night",
  blurb="Luna has lost a very special feather, the one that helps her fly in perfect silence. Mimo follows a trail of clues across the whole forest.",
  fact="owls fly almost silently, because the edges of their feathers are soft and fringed, so the air flows by without a whoosh.",
  chapters=[
    dict(label="A Noisy Wing", story=[
        dict(decor="forest_night", cast=[("owl", 420, 420, L), ("mimo", -150, 880, R)], lines=[
            ("narrator", "Luna the owl was perched on a branch, looking worried, and a little bit embarrassed."),
            ("mimo", "Luna, what's wrong?"),
            ("owl", "Hoo hoo. Listen. Whoosh, whoosh. My wing is making a noise when I fly."),
            ("mimo", "I thought owls were always quiet!"),
            ("owl", "We are! Our feathers have soft, fringed edges that hush the air. But one of mine fell out, and now my wing whooshes.")]),
    ], song=song("Twinkle Twinkle Little Star", "forest_night", [("owl", 440, L), ("mimo", 860, R)], "box", 0)),

    dict(label="Clue One: The Pond", story=[
        dict(decor="pond_night", cast=[("mimo", -150, 330, L), ("owl", -420, 640, L), ("turtle", 1450, 960, R)], lines=[
            ("turtle", "Slowly, slowly... Oh, hello, Luna. Hello, Mimo. Are you looking for something?"),
            ("mimo", "A feather. A soft, brown, fringed one."),
            ("turtle", "I saw one floating by this morning, drifting down the stream, toward the big old dam."),
            ("owl", "Thank you, Shelly. To the dam, then!")]),
    ], song=song("London Bridge", "pond_night", [("mimo", 310, L), ("owl", 640, L), ("turtle", 970, R)], "soft", 0)),

    dict(label="Clue Two: The Dam", story=[
        dict(decor="river_night", cast=[("mimo", -150, 330, L), ("owl", -420, 640, L), ("beaver", 1450, 960, R)], lines=[
            ("beaver", "Chip the beaver, at your service! A feather? Yes, I did see one."),
            ("beaver", "It got stuck on my dam, and then a little breeze lifted it up, toward the meadow."),
            ("mimo", "The meadow! Let's go, Luna!"),
            ("beaver", "Good luck! And fly softly!")]),
    ], song=None),

    dict(label="Clue Three: The Meadow", story=[
        dict(decor="meadow_night", cast=[("mimo", 330, 330, L), ("owl", 640, 640, L), ("fawn", 1450, 960, R)], lines=[
            ("fawn", "Hello! I'm Fern. Are you the ones looking for the feather?"),
            ("mimo", "Yes! Have you seen it?"),
            ("fawn", "A fluffy brown feather landed on my back, and then slid off, up there, on the old oak tree."),
            ("owl", "Hoo hoo. My very own oak tree. How funny, it was right next to my nest the whole time!")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "meadow_night", [("mimo", 330, L), ("owl", 640, L), ("fawn", 960, R)], "harp", -2)),

    dict(label="The Feather Found", story=[
        dict(decor="forest_night", cast=[("mimo", 420, 420, L), ("owl", 880, 880, R)], lines=[
            ("narrator", "High in the old oak, tangled in a twig, was a soft, brown feather with a fringed edge."),
            ("mimo", "There it is! I can reach it!"),
            ("narrator", "Mimo climbed up carefully, picked it up with two paws, and brought it back down."),
            ("owl", "Thank you, Mimo. Now watch. And, more importantly, listen.")]),
    ], song=song("Mary Had a Little Lamb", "forest_night", [("mimo", 440, L), ("owl", 860, R)], "bell", 0)),

    dict(label="The Silent Flight", story=[
        dict(decor="forest_night", cast=[("mimo", 420, 420, L), ("owl", 880, 880, R)], lines=[
            ("narrator", "Luna spread her wings and glided over the treetops. Not a sound. Not a whisper. Only the moonlight."),
            ("mimo", "I can't hear her at all! It's like watching a shadow float."),
            ("owl", "Hoo hoo. Silent as the night. Thank you, Mimo. Sleep well."),
            ("mimo", "Goodnight, Luna. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="forest_night", cast=[("fawn", 230, L), ("mimo", 520, L), ("beaver", 810, R), ("turtle", 1090, R)], minutes=12),
  teaser=dict(decor="meadow_night", cast=[("bunny", 420, 420, L), ("mimo", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("bunny", "Mimo! Thump, thump! I saw a big shadow in the meadow! Everybody hide!"),
      ("narrator", "Find out in the next episode: Pip Thumps Twice!")]))

# ======================================================================= 22. Pip Thumps Twice  (fausse alerte)
S2E10 = dict(id="s2e10", style="s2", title="Pip Thumps Twice", bye_decor="meadow_night",
  blurb="Pip thumps his foot to warn everyone about a big scary shadow. But was it really danger? A gentle story about brave warnings and kind friends.",
  fact="rabbits thump their strong back feet on the ground to warn others of danger, and they are most active at dusk and dawn.",
  chapters=[
    dict(label="Thump, Thump!", story=[
        dict(decor="meadow_night", cast=[("bunny", 330, 330, L), ("mimo", 640, 640, R), ("fawn", 950, 950, R)], lines=[
            ("narrator", "In the silver meadow, Mimo and Fern were nibbling clover, when suddenly..."),
            ("bunny", "Thump! Thump! Everybody freeze! There's a big shadow in the grass!"),
            ("fawn", "A shadow? Where?"),
            ("bunny", "Over there, wide and dark, and it's moving!"),
            ("mimo", "Let's all stay very still and quiet.")]),
    ], song=None),

    dict(label="Everybody Hides", story=[
        dict(decor="meadow_night", cast=[("mimo", 330, 330, L), ("fawn", 640, 640, L), ("bunny", 950, 950, R)], lines=[
            ("narrator", "The whole meadow went still. Fern lay down in the grass. Mimo hid behind a bush. Pip's ears stood up, tall and straight."),
            ("bunny", "My ears can turn all around. I hear something. Rustle, rustle..."),
            ("mimo", "Is it close?"),
            ("bunny", "It's... coming... closer...")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "meadow_night", [("mimo", 330, L), ("fawn", 640, L), ("bunny", 950, R)], "box", -2)),

    dict(label="The Shadow", story=[
        dict(decor="meadow_night", cast=[("bunny", 330, 330, L), ("mimo", 640, 640, L), ("owl", 1450, 960, R)], lines=[
            ("owl", "Hoo hoo. Good evening, my friends. Why are you all hiding?"),
            ("bunny", "Luna! There's a big shadow in the meadow. Thump, thump! I warned everyone."),
            ("owl", "Ah. A big shadow. Look up, Pip."),
            ("narrator", "High above them, a huge, fluffy moth was flying past the moon, and its giant shadow was sliding across the grass."),
            ("bunny", "Oh! It was only a moth. A moth with a very big shadow.")]),
    ], song=None),

    dict(label="Was Pip Wrong?", story=[
        dict(decor="meadow_night", cast=[("bunny", 330, 330, L), ("mimo", 640, 640, L), ("fawn", 950, 950, R)], lines=[
            ("bunny", "I'm sorry, everybody. I scared you for nothing. I feel silly."),
            ("mimo", "Pip, you didn't do anything wrong. You thought someone might be in danger, and you told us."),
            ("fawn", "That's what a good friend does. I'd rather hear a thump, than not hear one."),
            ("bunny", "Really? Even if it's a false alarm?"),
            ("mimo", "Always. Better safe than sorry.")]),
    ], song=song("London Bridge", "meadow_night", [("bunny", 330, L), ("mimo", 640, L), ("fawn", 950, R)], "soft", 0)),

    dict(label="Thump Number Two", story=[
        dict(decor="forest_night", cast=[("fawn", 330, 330, L), ("bunny", 640, 640, L), ("mimo", 950, 950, R)], lines=[
            ("narrator", "Later, as the friends walked home through the forest, Pip stopped, and his ears went up again."),
            ("bunny", "Thump! Thump! Fern, jump away from that tree. Now!"),
            ("narrator", "Fern leaped to the side. And with a loud crack, a heavy branch fell on the very spot where she had been standing."),
            ("fawn", "Oh! If you hadn't warned me, Pip, that would have been so close!"),
            ("mimo", "See? This time the thump was exactly right.")]),
    ], song=song("Row Row Row Your Boat", "forest_night", [("fawn", 330, L), ("bunny", 640, L), ("mimo", 950, R)], "harp", 2)),

    dict(label="The Brave Little Rabbit", story=[
        dict(decor="forest_night", cast=[("bunny", 420, 420, L), ("mimo", 880, 880, R)], lines=[
            ("mimo", "You were brave twice today, Pip. Once when it was a moth, and once when it was a real branch."),
            ("bunny", "And both times, my friends listened."),
            ("narrator", "And the little rabbit hopped home, with his ears down, and his heart light."),
            ("mimo", "Goodnight, Pip. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="forest_night", cast=[("bunny", 230, L), ("fawn", 520, L), ("mimo", 810, R), ("owl", 1090, R)], minutes=12),
  teaser=dict(decor="river_night", cast=[("otter", 420, 420, L), ("beaver", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("beaver", "Ollie, I built a raft from my best sticks. Do you want to see where the river goes?"),
      ("otter", "Yes! Let's go on an adventure!"),
      ("narrator", "Find out in the next episode: The Raft Down the Silver River!")]))

# ======================================================================= 23. The Raft Down the Silver River  (voyage)
S2E11 = dict(id="s2e11", style="s2", title="The Raft Down the Silver River", bye_decor="river_night",
  blurb="Chip builds a raft, and Mimo, Ollie and Echo float down the silver river to reach a party under the old willow before the moon sets.",
  fact="otters have thick, waterproof fur that traps a layer of air, and a river's gentle current has carried travelers and seeds for thousands of years.",
  chapters=[
    dict(label="Chip's Raft", story=[
        dict(decor="river_night", cast=[("beaver", 330, 330, L), ("mimo", 640, 640, R), ("otter", 950, 950, R)], lines=[
            ("beaver", "Ta-da! My raft. Sticks tied with reeds, and a little mud to keep it tight."),
            ("mimo", "It's wonderful, Chip! Can it carry all of us?"),
            ("beaver", "Of course. Ollie will swim alongside, and steer."),
            ("otter", "I love steering! Where are we going?"),
            ("beaver", "Echo invited us to a party under the old willow tree, down the river. It starts when the moon is high.")]),
    ], song=song("Row Row Row Your Boat", "river_night", [("beaver", 300, L), ("mimo", 640, L), ("otter", 980, R)], "harp", 0)),

    dict(label="Pushing Off", story=[
        dict(decor="river_night", cast=[("mimo", 420, 420, L), ("otter", 880, 880, R)], lines=[
            ("narrator", "Mimo sat on the raft, and Ollie gave it a push. The raft began to glide."),
            ("mimo", "We're moving! The water is so smooth and shiny."),
            ("otter", "It's carrying us all the way, and we don't even need to row. The river knows the way."),
            ("mimo", "I can see the stars in the water!")]),
    ], song=song("Twinkle Twinkle Little Star", "river_night", [("mimo", 440, L), ("otter", 860, R)], "box", 0)),

    dict(label="The Fast Part", story=[
        dict(decor="rain_night", cast=[("mimo", 420, 420, L), ("otter", 880, 880, R)], lines=[
            ("narrator", "Further down, the river narrowed, and the water began to bubble and rush."),
            ("mimo", "Ollie! The raft is spinning!"),
            ("otter", "Hold on tight! Lean to the left! Now to the right! Don't worry, I've done this a hundred times."),
            ("mimo", "Whoa! Whee! This is the best ride I've ever had!"),
            ("otter", "See? The trick is to go with the river, not against it.")]),
    ], song=None),

    dict(label="The Low Branch", story=[
        dict(decor="river_night", cast=[("mimo", 330, 330, L), ("otter", 700, 700, R), ("bat", 1450, 1030, R)], lines=[
            ("bat", "Eeek! Mimo! Ollie! Duck! There's a low branch right ahead!"),
            ("mimo", "Echo! You came to find us!"),
            ("bat", "My echo says the branch is two paws above your heads. Get down, everybody!"),
            ("otter", "Everyone flat! Now we're under it. Phew!"),
            ("bat", "Follow me! The party is just around the bend.")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "river_night", [("mimo", 330, L), ("otter", 660, R), ("bat", 990, R)], "bell", 2)),

    dict(label="Under the Old Willow", story=[
        dict(decor="meadow_night", cast=[("mimo", 230, 230, L), ("otter", 500, 500, L), ("bat", 770, 770, R), ("owl", 1450, 1040, R)], lines=[
            ("owl", "Hoo hoo. Welcome, travelers! Everyone has been waiting for you."),
            ("bat", "Surprise! It's a moonlight party for the whole river."),
            ("narrator", "Under the old willow, a hundred fireflies were glowing, and all the animals of the river were there."),
            ("otter", "Thank you for inviting us, Echo."),
            ("mimo", "We came all this way on a raft, and it was worth every bump.")]),
    ], song=song("Mary Had a Little Lamb", "meadow_night", [("mimo", 230, L), ("otter", 500, L), ("bat", 770, R), ("owl", 1040, R)], "bell", 2)),

    dict(label="Floating Home", story=[
        dict(decor="river_night", cast=[("mimo", 420, 420, L), ("otter", 880, 880, R)], lines=[
            ("narrator", "When the party was over, the river carried them gently home, as the moon sank lower and the stars grew soft."),
            ("mimo", "Ollie, thank you for the best adventure."),
            ("otter", "Rivers are made for adventures, Mimo. Now it's time for them to be quiet."),
            ("mimo", "Goodnight, river. Goodnight, Ollie. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="river_night", cast=[("beaver", 230, L), ("mimo", 520, L), ("otter", 810, R), ("bunny", 1090, R)], minutes=12),
  teaser=dict(decor="dawn_hills", cast=[("owl", 420, 420, L), ("mimo", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("owl", "Mimo, tonight is the longest night of the year. We must wait for the very first sunrise."),
      ("narrator", "It's the season finale! Find out in the next episode: The Longest Night!")]))

# ======================================================================= 24. The Longest Night  (finale : l'aube)
S2E12 = dict(id="s2e12", style="s2", title="The Longest Night", bye_decor="dawn_hills",
  blurb="It's the longest night of the year! All of Mimo's forest friends gather on the hill to wait for the first sunrise, and say goodnight as the day begins.",
  fact="at sunrise, the forest changes shifts: birds begin their dawn chorus while many night animals, like owls, hedgehogs and bats, go to sleep.",
  chapters=[
    dict(label="The Longest Night", story=[
        dict(decor="snow_night", cast=[("owl", 420, 420, L), ("mimo", -150, 880, R)], lines=[
            ("owl", "Hoo hoo. Mimo, tonight is a special night. It is the longest night of the whole year."),
            ("mimo", "The longest? So we have lots of time to play!"),
            ("owl", "And lots of time to wait for the sunrise. After the longest night, the days start growing longer again."),
            ("mimo", "Then let's invite all our friends to wait for the sun together!")]),
    ], song=song("Twinkle Twinkle Little Star", "snow_night", [("owl", 440, L), ("mimo", 860, R)], "bell", 2)),

    dict(label="Everyone Gathers", story=[
        dict(decor="forest_night", cast=[("mimo", 230, 230, L), ("fox", 500, 500, L), ("otter", 1450, 770, R), ("bunny", 1450, 1040, R)], lines=[
            ("fox", "Finn the fox, here and ready. I brought warm leaves for everybody."),
            ("otter", "Ollie the otter! I came as fast as I could, sliding all the way!"),
            ("bunny", "Hop hop! Me too! I'm so excited I can't stop wiggling my ears."),
            ("mimo", "Let's go up the hill. The best view is at the top.")]),
    ], song=song("London Bridge", "forest_night", [("mimo", 230, L), ("fox", 500, L), ("otter", 770, R), ("bunny", 1040, R)], "soft", 2)),

    dict(label="Night Stories", story=[
        dict(decor="snow_night", cast=[("mimo", 230, 230, L), ("fawn", 500, 500, L), ("beaver", 770, 770, R), ("turtle", 1450, 1040, R)], lines=[
            ("beaver", "Chip the beaver! And look who I met on the way up."),
            ("turtle", "Slowly, slowly. Shelly the turtle. I'm here, at last."),
            ("fawn", "I'm Fern. I wasn't lost this time. I came with my mama, and she's resting over there."),
            ("mimo", "All my friends are here. The whole forest!"),
            ("turtle", "Let's tell each other our favorite night memory.")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "snow_night", [("mimo", 230, L), ("fawn", 500, L), ("beaver", 770, R), ("turtle", 1040, R)], "harp", -2)),

    dict(label="Hazel Wakes Up", story=[
        dict(decor="den", cast=[("mimo", 420, 420, L), ("hedgehog", 880, 880, R)], lines=[
            ("narrator", "On the way, Mimo passed a leafy nest. Inside, a tiny hedgehog rolled over, and opened one eye."),
            ("hedgehog", "Yawn. Mimo? Is it spring already?"),
            ("mimo", "Not yet, Hazel. It's the longest night. Go back to sleep, and dream about beetles."),
            ("hedgehog", "Mmm. Beetles. Goodnight, Mimo.")]),
    ], song=None),

    dict(label="The First Light", story=[
        dict(decor="dawn_hills", cast=[("mimo", 230, 230, L), ("owl", 500, 500, L), ("fox", 770, 770, R), ("bat", 1450, 1040, R)], lines=[
            ("narrator", "And then, at the top of the hill, the sky began to blush. First pink, then orange, then gold."),
            ("mimo", "Look! The sun is coming!"),
            ("bat", "Eeek! My night is over. It's time for me to sleep."),
            ("owl", "Hoo hoo. Mine too. At sunrise, the night animals say goodnight, and the day animals say good morning."),
            ("fox", "It's a change of shifts. Listen. Do you hear the birds?")]),
    ], song=song("Row Row Row Your Boat", "dawn_hills", [("mimo", 230, L), ("owl", 500, L), ("fox", 770, R), ("bat", 1040, R)], "bell", 0)),

    dict(label="Goodnight, Everyone", story=[
        dict(decor="dawn_hills", cast=[("mimo", 420, 420, L), ("owl", 880, 880, R)], lines=[
            ("mimo", "Luna, this was the most beautiful night of my life."),
            ("owl", "Hoo hoo. It was beautiful because you shared it with friends."),
            ("narrator", "And as the sun rose over the hills, one by one the friends curled up, and closed their eyes."),
            ("mimo", "Goodnight, sun. Goodnight, stars. Goodnight, everyone. Thank you for the Wild Nights.")]),
    ], song=None),
  ],
  finale=dict(decor="dawn_hills", cast=[("owl", 230, L), ("mimo", 520, L), ("fox", 810, R), ("otter", 1090, R)], minutes=14),
  teaser=dict(decor="dawn_hills", cast=[("mimo", 420, 420, L), ("owl", 880, 880, R)], lines=[
      ("narrator", "That was the end of Season 2, Wild Nights."),
      ("mimo", "Thank you for sleeping, listening and dreaming with us under the stars."),
      ("owl", "Hoo hoo. Sleep well, little ones. See you soon."),
      ("narrator", "Goodnight, everyone.")]))
