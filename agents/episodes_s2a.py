"""Saison 2 « Wild Nights » — épisodes 13 à 18 (s2e01 à s2e06).
De vrais animaux de la nuit, des aventures qui changent d'un épisode à l'autre (visite guidée, enquête, orage, recherche, hibernation, grotte),
et un vrai fait sur la nature dans chaque épisode. Écartement des animaux : au moins 250 à l'écran (ce sont des quadrupèdes)."""

L, R = 1, -1


def song(name, decor, cast, voice="box", transpose=0, **kw):
    return dict(name=name, decor=decor, cast=cast, voice=voice, transpose=transpose, **kw)


# ======================================================================= 13. The Night Safari
S2E01 = dict(id="s2e01", style="s2", title="The Night Safari", bye_decor="forest_night",
  blurb="Mimo can't sleep, so wise Luna the owl takes him on a night safari to meet the animals that wake up when the moon comes out.",
  fact="hedgehogs are nocturnal: they sniff out beetles and worms in the dark, and curl into a spiky ball when they feel scared.",
  chapters=[
    dict(label="Mimo Can't Sleep", story=[
        dict(decor="den", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Deep in the old forest, inside a hollow tree, a little bear cub named Mimo was trying to sleep."),
            ("mimo", "One, two, three... Hmm. I hear rustling outside. And tiny footsteps."),
            ("mimo", "Everybody should be asleep. So who is making all that noise?")]),
        dict(decor="den", cast=[("mimo", 420, 420, L), ("owl", 1450, 900, R)], lines=[
            ("owl", "Hoo hoo. Good evening, Mimo. I'm Luna. I saw your little light from the sky."),
            ("mimo", "Luna! Everyone in the forest is sleeping, but I can still hear noises!"),
            ("owl", "Not everyone sleeps at night, little bear. Night is when many animals wake up."),
            ("mimo", "Really? What do they do?"),
            ("owl", "Come with me on a night safari, and I'll show you. Bring your sleepy hat!")]),
    ], song=song("Twinkle Twinkle Little Star", "den", [("mimo", 440, L), ("owl", 860, R)], "box", 0)),

    dict(label="Hazel the Hedgehog", story=[
        dict(decor="forest_night", cast=[("mimo", -150, 640, L), ("owl", -400, 330, L), ("hedgehog", 1450, 960, R)], lines=[
            ("narrator", "Mimo and Luna walked under the tall trees. The moon made silver stripes on the ground."),
            ("mimo", "Look, Luna! Something small is snuffling in the leaves!"),
            ("hedgehog", "Sniff, sniff. Oh! Visitors! Please don't be scared. I'm Hazel the hedgehog."),
            ("mimo", "Hello, Hazel! Why are you awake at night?"),
            ("hedgehog", "Because that's when my dinner comes out! Beetles, worms, and juicy little slugs.")]),
        dict(decor="forest_night", cast=[("mimo", 330, 330, L), ("hedgehog", 700, 700, R), ("owl", 1000, 1000, R)], lines=[
            ("hedgehog", "I can't see very well, but I have a super nose. Sniff, sniff! It tells me where to dig."),
            ("mimo", "What if you get scared?"),
            ("hedgehog", "Then I roll into a ball, and my spines stand up. Thousands of them!"),
            ("owl", "Hoo hoo. A very clever way to stay safe, Hazel."),
            ("mimo", "Can you teach us a night song?")]),
    ], song=song("London Bridge", "forest_night", [("mimo", 320, L), ("hedgehog", 650, R), ("owl", 980, R)], "soft", 0)),

    dict(label="Finn Listens", story=[
        dict(decor="meadow_night", cast=[("mimo", -150, 640, L), ("hedgehog", -420, 330, L), ("fox", 1450, 960, R)], lines=[
            ("narrator", "Next, they crossed the silver meadow. In the tall grass, two pointy ears were standing up."),
            ("fox", "Shh! Don't move. I hear something."),
            ("mimo", "What is it, Finn?"),
            ("fox", "A little mouse, far across the meadow. Squeak, squeak. Can you hear it?"),
            ("mimo", "I can't hear anything at all!"),
            ("fox", "Foxes have very big ears. We hear tiny sounds from very far away. Try closing your eyes.")]),
        dict(decor="meadow_night", cast=[("mimo", 330, 330, L), ("fox", 700, 700, R), ("hedgehog", 1030, 1030, R)], lines=[
            ("mimo", "Okay. Eyes closed. I hear crickets. And the wind in the grass."),
            ("fox", "Good listening! What else?"),
            ("mimo", "A tiny squeak, far away! I heard it, Finn! I really did!"),
            ("fox", "See? The night isn't quiet. It's full of soft little sounds."),
            ("hedgehog", "Let's sing a sleepy song, very softly, so we don't scare the mouse.")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "meadow_night", [("mimo", 330, L), ("fox", 700, R), ("hedgehog", 1030, R)], "harp", -2)),

    dict(label="Echo Flies By", story=[
        dict(decor="forest_night", cast=[("mimo", 330, 330, L), ("owl", 700, 700, R), ("bat", 1450, 960, R)], lines=[
            ("narrator", "Suddenly, something fluttered over their heads. Flap, flap, whoosh!"),
            ("bat", "Eeek! Sorry! I'm Echo the bat. I'm on my way to catch some moths!"),
            ("mimo", "Wow, you fly so fast! Can you even see in the dark?"),
            ("bat", "I'm not blind, Mimo! But at night I use my voice. I squeak, and the sound bounces back from everything."),
            ("bat", "That tells me where the trees are, and where the moths are. It's called an echo."),
            ("owl", "Hoo hoo. Every night animal has its own special trick.")]),
    ], song=None),

    dict(label="The Night Journal", story=[
        dict(decor="meadow_night", cast=[("mimo", 330, 330, L), ("owl", 700, 700, R), ("fox", 1030, 1030, R)], lines=[
            ("narrator", "Back on the hill, Mimo took out a little notebook, and began to draw."),
            ("mimo", "Hazel has a super nose. Finn has super ears. And Echo has a voice that bounces."),
            ("owl", "And what about me?"),
            ("mimo", "You have the biggest eyes in the forest, Luna!"),
            ("owl", "Hoo hoo. That's right. Owls have huge eyes that catch even the tiniest bit of moonlight."),
            ("fox", "Everybody has a night job, Mimo. Even you.")]),
    ], song=song("Mary Had a Little Lamb", "meadow_night", [("mimo", 330, L), ("owl", 700, R), ("fox", 1030, R)], "bell", 2)),

    dict(label="Time for Bed", story=[
        dict(decor="forest_night", cast=[("mimo", 420, 420, L), ("owl", 860, 860, R)], lines=[
            ("mimo", "Luna, what's my night job?"),
            ("owl", "Yours is a very important one. You rest, so you can have a big adventure tomorrow."),
            ("mimo", "Oh! That's a job I like. And now I know the noises are only friends, waking up for their work."),
            ("narrator", "So Mimo curled up in his hollow tree, while Hazel snuffled, and Finn listened, and Echo flew under the stars."),
            ("mimo", "Goodnight, Luna. Goodnight, night animals. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="forest_night", cast=[("hedgehog", 260, L), ("mimo", 640, L), ("fox", 1010, R)], minutes=12),
  teaser=dict(decor="meadow_night", cast=[("mimo", 420, 420, L), ("owl", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("owl", "Mimo, look at the meadow. The fireflies have stopped glowing!"),
      ("mimo", "What? That's strange. We have to find out why!"),
      ("narrator", "Find out in the next episode: The Missing Fireflies!")]))

# ======================================================================= 14. The Missing Fireflies  (enquête)
S2E02 = dict(id="s2e02", style="s2", title="The Missing Fireflies", bye_decor="meadow_night",
  blurb="The fireflies of the meadow have stopped glowing! Mimo and his friends follow the clues to solve the mystery.",
  fact="fireflies are beetles. They flash a cool light to find one another, and they stay hidden when the night is cold and windy.",
  chapters=[
    dict(label="The Dark Meadow", story=[
        dict(decor="meadow_night", cast=[("mimo", -150, 420, L), ("owl", 1450, 880, R)], lines=[
            ("narrator", "Every night, the meadow twinkled with a thousand tiny lights. But tonight, it was dark."),
            ("mimo", "Luna, where are the fireflies? The meadow is so quiet and so dark."),
            ("owl", "Hoo hoo. I don't know, Mimo. Something is wrong. I think we have a mystery to solve."),
            ("mimo", "A mystery! Where do we start?"),
            ("owl", "A good detective always starts with a clue. Let's look around carefully.")]),
    ], song=song("Twinkle Twinkle Little Star", "meadow_night", [("mimo", 440, L), ("owl", 860, R)], "box", -2)),

    dict(label="Clue Number One", story=[
        dict(decor="meadow_night", cast=[("mimo", 330, 330, L), ("owl", 700, 700, R), ("bunny", 1450, 980, R)], lines=[
            ("bunny", "Hop hop! Mimo! Luna! Did you notice? There's a cold wind tonight!"),
            ("mimo", "Pip! You're shivering. Yes, it's much colder than yesterday."),
            ("bunny", "My ears are freezing! And look, all the grass is bending over."),
            ("mimo", "Clue number one: a cold, windy night."),
            ("owl", "Hoo hoo. Write that in your notebook, detective.")]),
    ], song=song("London Bridge", "meadow_night", [("mimo", 330, L), ("owl", 700, R), ("bunny", 1030, R)], "soft", 0)),

    dict(label="Clue Number Two", story=[
        dict(decor="meadow_night", cast=[("mimo", -150, 640, L), ("bunny", -420, 330, L), ("fox", 1450, 960, R)], lines=[
            ("fox", "Psst, over here! I found something, but be very quiet."),
            ("mimo", "What is it, Finn?"),
            ("fox", "Look at the bottom of the grass. Tiny, tiny lights. They are on, but so, so faint."),
            ("bunny", "They're hiding! Why would fireflies hide?"),
            ("mimo", "Clue number two: the fireflies are still here. They're just not glowing.")]),
    ], song=None),

    dict(label="The Firefly Secret", story=[
        dict(decor="meadow_night", cast=[("mimo", 330, 330, L), ("owl", 700, 700, R), ("fox", 1030, 1030, R)], lines=[
            ("owl", "Hoo hoo. I think I know the answer. Fireflies are little beetles."),
            ("owl", "They glow to talk to each other, flashing a special light, like a secret code."),
            ("mimo", "But why did they stop?"),
            ("owl", "On cold, windy nights, fireflies stay low, and cuddle in the grass to keep warm."),
            ("mimo", "So they aren't gone. They're cold! We have to help them!")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "meadow_night", [("mimo", 330, L), ("owl", 700, R), ("fox", 1030, R)], "harp", -2)),

    dict(label="A Wall Against the Wind", story=[
        dict(decor="meadow_night", cast=[("mimo", 230, 230, L), ("fox", 500, 500, L), ("bunny", 770, 770, R), ("turtle", 1450, 1040, R)], lines=[
            ("mimo", "Friends, we can block the wind! If we make a wall, the grass will be warm again."),
            ("turtle", "Slowly... slowly... I'm Shelly. I'm very good at being a wall."),
            ("fox", "Then I'll curl my big fluffy tail on this side, to block the breeze."),
            ("bunny", "And I'll thump the ground to tell the grass to stand up straight. Thump, thump!"),
            ("mimo", "And I'll stand right here. A bear is a very good wall too!"),
            ("narrator", "And so the friends lined up, side by side, and the cold wind slid right over them.")]),
    ], song=song("Row Row Row Your Boat", "meadow_night", [("mimo", 300, L), ("fox", 570, L), ("bunny", 840, R), ("turtle", 1110, R)], "bell", 0)),

    dict(label="The Meadow Lights Up", story=[
        dict(decor="meadow_night", cast=[("mimo", 420, 420, L), ("owl", 880, 880, R)], lines=[
            ("narrator", "Slowly, the grass grew warmer. And then, one tiny light blinked. Then another. Then ten. Then a thousand."),
            ("mimo", "They're glowing! Luna, they're all glowing again!"),
            ("owl", "Hoo hoo. Well done, detective. Mystery solved."),
            ("mimo", "It's like the stars came down to say thank you."),
            ("narrator", "And in the warm, twinkling meadow, the friends settled down to sleep."),
            ("mimo", "Goodnight, fireflies. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="meadow_night", cast=[("fox", 220, L), ("mimo", 520, L), ("bunny", 820, R), ("turtle", 1080, R)], minutes=12),
  teaser=dict(decor="rain_night", cast=[("beaver", 420, 420, L), ("otter", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("beaver", "Ollie! The river is rising! My dam is going to break!"),
      ("otter", "Don't worry, Chip. We'll fix it together!"),
      ("narrator", "Find out in the next episode: The Storm at Chip's Dam!")]))

# ======================================================================= 15. The Storm at Chip's Dam  (orage, sauvetage)
S2E03 = dict(id="s2e03", style="s2", title="The Storm at Chip's Dam", bye_decor="river_night",
  blurb="A big storm makes the river rise. Can Mimo, Ollie the otter and Chip the beaver save the dam before the water breaks through?",
  fact="beavers build dams from sticks and mud to make a calm pond, and they slap their flat tails on the water to warn their family.",
  chapters=[
    dict(label="Rain on the River", story=[
        dict(decor="rain_night", cast=[("mimo", -150, 420, L), ("otter", 1450, 880, R)], lines=[
            ("narrator", "It had been raining all night. Pitter, patter, pitter, patter. The river was getting bigger and bigger."),
            ("otter", "Mimo! Over here! I'm Ollie the otter. I came to find you!"),
            ("mimo", "Ollie! You're soaking wet!"),
            ("otter", "That's okay, my fur keeps me warm and dry underneath. But I'm worried about Chip's dam."),
            ("mimo", "Who is Chip?"),
            ("otter", "My beaver friend. Come on, there's no time to lose!")]),
    ], song=song("Row Row Row Your Boat", "rain_night", [("mimo", 440, L), ("otter", 860, R)], "harp", 0)),

    dict(label="Chip's Big Dam", story=[
        dict(decor="river_night", cast=[("mimo", -150, 640, L), ("otter", -420, 330, L), ("beaver", 1450, 960, R)], lines=[
            ("beaver", "Oh, Ollie! Oh, Mimo! Thank goodness you came. I'm Chip."),
            ("mimo", "Is this your dam, Chip? It's amazing!"),
            ("beaver", "I built it with sticks, mud, and stones. It keeps the pond calm and gives my family a safe home."),
            ("beaver", "But the rain is pushing so hard. Look! The water is starting to leak through!")]),
    ], song=song("London Bridge", "river_night", [("otter", 300, L), ("mimo", 620, L), ("beaver", 950, R)], "soft", 2)),

    dict(label="Splash! Warning!", story=[
        dict(decor="river_night", cast=[("beaver", 420, 420, L), ("mimo", 760, 760, R), ("otter", 1050, 1050, R)], lines=[
            ("beaver", "I'll warn everyone. Watch this!"),
            ("narrator", "Chip lifted his flat tail and slapped the water. SPLASH! A big sound rolled across the river."),
            ("mimo", "Wow! That was so loud!"),
            ("beaver", "That's how beavers say, danger, come quickly! Everyone nearby will hear it."),
            ("otter", "And look, here come the helpers!")]),
    ], song=None),

    dict(label="A Team of Builders", story=[
        dict(decor="river_night", cast=[("mimo", 230, 230, L), ("fox", 500, 500, L), ("beaver", 770, 770, R), ("otter", 1040, 1040, R)], lines=[
            ("fox", "Finn the fox reporting! I heard the splash. What can I carry?"),
            ("beaver", "Sticks! Lots of sticks, and big flat stones."),
            ("otter", "I'll swim out and push the heavy logs. Otters are great in the water!"),
            ("mimo", "And I'll carry stones. Bears are very strong!"),
            ("fox", "Then let's go. One, two, three!")]),
    ], song=song("Mary Had a Little Lamb", "river_night", [("fox", 290, L), ("mimo", 560, L), ("beaver", 840, R), ("otter", 1110, R)], "bell", 0)),

    dict(label="The Last Gap", story=[
        dict(decor="rain_night", cast=[("beaver", 420, 420, L), ("otter", 760, 760, R), ("mimo", 1080, 1080, R)], lines=[
            ("narrator", "They worked and worked, while the rain fell. But one big hole in the dam was still gushing water."),
            ("beaver", "It's too big! My sticks are not enough!"),
            ("otter", "Wait. What if we all push the big log together? Mimo, you push from the top. Chip, from the side. I'll dive and push from below."),
            ("mimo", "On three! One... two... three!"),
            ("narrator", "Together, they pushed the big log, right into the gap. And the water stopped.")]),
    ], song=song("Row Row Row Your Boat", "rain_night", [("beaver", 300, L), ("mimo", 620, L), ("otter", 950, R)], "harp", 2)),

    dict(label="A Calm Pond", story=[
        dict(decor="river_night", cast=[("beaver", 420, 420, L), ("mimo", 760, 760, R), ("otter", 1050, 1050, R)], lines=[
            ("narrator", "The rain slowly stopped. Above the clouds, the moon peeked out, and the river went quiet."),
            ("beaver", "The dam held. Thank you, friends. I could never have done it alone."),
            ("otter", "That's the best part of a team, Chip. Everyone brings something different."),
            ("mimo", "I'm so sleepy, but I'm so happy. Goodnight, Chip. Goodnight, Ollie. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="river_night", cast=[("beaver", 220, L), ("mimo", 520, L), ("otter", 810, R), ("fox", 1090, R)], minutes=12),
  teaser=dict(decor="meadow_night", cast=[("fawn", 420, 420, L), ("mimo", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("mimo", "Luna says a little fawn is lost in the meadow. We have to find her!"),
      ("narrator", "Find out in the next episode: The Quiet Fawn!")]))

# ======================================================================= 16. The Quiet Fawn  (recherche, calme)
S2E04 = dict(id="s2e04", style="s2", title="The Quiet Fawn", bye_decor="meadow_night",
  blurb="Fern the fawn has disappeared in the tall grass. Mimo learns that the best way to find someone is to be very, very quiet.",
  fact="newborn fawns have white spots that hide them in the light and shadows, almost no scent, and they stay completely still while their mother is away.",
  chapters=[
    dict(label="Where Is Fern?", story=[
        dict(decor="meadow_night", cast=[("mimo", -150, 420, L), ("bunny", 1450, 880, R)], lines=[
            ("bunny", "Hop hop! Mimo! Fern the little fawn was right here a minute ago, and now she's gone!"),
            ("mimo", "Oh no. Fern is only a few days old. She must be so scared."),
            ("bunny", "I looked behind the log, and under the bush, and in the clover. Nothing!"),
            ("mimo", "Don't worry, Pip. We'll find her. Let's call Finn. He's the best tracker in the forest.")]),
    ], song=song("Twinkle Twinkle Little Star", "meadow_night", [("mimo", 440, L), ("bunny", 860, R)], "bell", 0)),

    dict(label="Tracks in the Grass", story=[
        dict(decor="meadow_night", cast=[("mimo", 330, 330, L), ("bunny", 600, 600, L), ("fox", 1450, 960, R)], lines=[
            ("fox", "Finn the fox, at your service. Show me where you last saw her."),
            ("bunny", "Right here, in the clover."),
            ("fox", "I see tiny hoof prints. Little ones, like this. And they lead toward the old birch trees."),
            ("mimo", "You can read footprints?"),
            ("fox", "Sure. Every animal leaves its own story on the ground. Follow me, quietly.")]),
    ], song=song("London Bridge", "meadow_night", [("mimo", 300, L), ("bunny", 570, L), ("fox", 850, R)], "soft", 0)),

    dict(label="Shh, Be Still", story=[
        dict(decor="forest_night", cast=[("mimo", 330, 330, L), ("fox", 640, 640, L), ("owl", 1450, 960, R)], lines=[
            ("owl", "Hoo hoo. I've been watching from above. I think I know where she is."),
            ("mimo", "Where, Luna?"),
            ("owl", "Fawns are very special. When mama is away, they curl up and stay completely still. They don't even make a sound."),
            ("owl", "They have almost no smell, and their spots look like little patches of moonlight in the leaves."),
            ("mimo", "So Fern isn't lost. She's hiding on purpose. That's why we can't see her!"),
            ("owl", "Exactly. To find her, we must be as quiet as she is.")]),
    ], song=None),

    dict(label="The Quietest Walk", story=[
        dict(decor="forest_night", cast=[("mimo", -150, 330, L), ("fox", -420, 640, L), ("bunny", -700, 950, L)], lines=[
            ("narrator", "So the friends walked on the tips of their paws. Not a leaf crunched. Not a twig snapped."),
            ("mimo", "I can hear my own heart. Thump, thump."),
            ("fox", "Now listen. Very carefully. Do you hear her breathing?"),
            ("bunny", "My long ears hear something, over there, by the big ferns!")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "forest_night", [("mimo", 330, L), ("fox", 650, L), ("bunny", 970, R)], "harp", -2)),

    dict(label="Found You, Fern", story=[
        dict(decor="forest_night", cast=[("mimo", 330, 330, L), ("fawn", 760, 760, R), ("bunny", 1060, 1060, R)], lines=[
            ("narrator", "And there, curled in the ferns, with moon spots on her back, was a tiny fawn."),
            ("fawn", "Oh! You found me. I was being very still, just like my mama told me."),
            ("mimo", "You did it perfectly, Fern. We only found you because we were quiet too."),
            ("fawn", "My mama said she'd come back soon. She just went to eat. I wasn't lost, I was waiting."),
            ("mimo", "Then we'll wait with you, so you're not alone.")]),
    ], song=song("Mary Had a Little Lamb", "forest_night", [("mimo", 330, L), ("fawn", 700, R), ("bunny", 1030, R)], "box", 2)),

    dict(label="Mama Comes Home", story=[
        dict(decor="forest_night", cast=[("mimo", 420, 420, L), ("fawn", 880, 880, R)], lines=[
            ("narrator", "After a little while, a soft whistle came from between the trees. Mama deer was back."),
            ("fawn", "That's her! Thank you, Mimo. Thank you for waiting with me."),
            ("mimo", "Sleep well, Fern. You're so brave."),
            ("narrator", "And in the quiet forest, the little bear tiptoed home, and slid into bed without making a sound."),
            ("mimo", "Goodnight, Fern. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="forest_night", cast=[("bunny", 230, L), ("mimo", 520, L), ("fawn", 810, R), ("fox", 1090, R)], minutes=12),
  teaser=dict(decor="autumn_dusk", cast=[("hedgehog", 420, 420, L), ("mimo", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("hedgehog", "Mimo, the leaves are turning gold, and I'm getting very, very sleepy. Winter is coming!"),
      ("narrator", "Find out in the next episode: Hazel's Long Sleep!")]))

# ======================================================================= 17. Hazel's Long Sleep  (saison, hibernation)
S2E05 = dict(id="s2e05", style="s2", title="Hazel's Long Sleep", bye_decor="autumn_dusk",
  blurb="Autumn leaves are falling and Hazel the hedgehog is getting ready for her long winter sleep. Mimo and his friends help her build the coziest nest.",
  fact="hedgehogs hibernate in winter. They eat a lot in autumn, then sleep in a nest of leaves while their body slows down to save energy.",
  chapters=[
    dict(label="Golden Leaves", story=[
        dict(decor="autumn_dusk", cast=[("mimo", -150, 420, L), ("hedgehog", 1450, 880, R)], lines=[
            ("narrator", "In the golden woods, the leaves were falling, one by one, like slow, red and yellow rain."),
            ("hedgehog", "Yawn. Hello, Mimo. I'm sorry, I'm sleepy all the time lately."),
            ("mimo", "Hazel, are you okay? You look so round!"),
            ("hedgehog", "Haha, I've been eating lots of beetles. I need to get big and cozy, because soon I'll sleep all winter long."),
            ("mimo", "All winter? For months?"),
            ("hedgehog", "Yes. It's called hibernating. My body slows down, and I rest until spring.")]),
    ], song=song("Twinkle Twinkle Little Star", "autumn_dusk", [("mimo", 440, L), ("hedgehog", 860, R)], "bell", 2)),

    dict(label="A Nest of Leaves", story=[
        dict(decor="autumn_dusk", cast=[("mimo", 330, 330, L), ("hedgehog", 700, 700, R), ("bunny", 1450, 980, R)], lines=[
            ("hedgehog", "I need a nest. A thick, soft, warm one, made of dry leaves, under a bush."),
            ("bunny", "Hop hop! I can help! I'm very good at jumping into leaf piles!"),
            ("mimo", "Pip, we need to carry the leaves, not just jump in them."),
            ("bunny", "Oops. Okay, okay. Carry first, jump later!"),
            ("hedgehog", "Dry leaves only, please. Wet ones get cold.")]),
    ], song=song("London Bridge", "autumn_dusk", [("mimo", 310, L), ("hedgehog", 640, R), ("bunny", 970, R)], "soft", 0)),

    dict(label="The Leaf Parade", story=[
        dict(decor="autumn_dusk", cast=[("mimo", -150, 640, L), ("bunny", -420, 330, L), ("fox", 1450, 960, R)], lines=[
            ("narrator", "Mimo and Pip carried armfuls of golden leaves, and made a long, rustling parade."),
            ("fox", "Finn the fox, joining the parade! I have a very fluffy tail. It carries lots of leaves."),
            ("mimo", "Thank you, Finn! Every leaf will make the nest softer."),
            ("bunny", "Look at this beautiful red one. It looks like a little fire!")]),
    ], song=song("Row Row Row Your Boat", "autumn_dusk", [("mimo", 310, L), ("fox", 640, R), ("bunny", 970, R)], "harp", 2)),

    dict(label="Tucking In", story=[
        dict(decor="den", cast=[("hedgehog", 640, 640, L), ("mimo", 340, 340, L), ("fox", 960, 960, R)], lines=[
            ("hedgehog", "It's perfect. Warm, soft, and a little bit crunchy."),
            ("mimo", "Are you sure you'll be okay for so many months?"),
            ("hedgehog", "I'll be fine. My heart goes very slow, and I'll breathe very softly. I won't even feel the cold."),
            ("fox", "And we'll visit your nest, and stay quiet, so we don't wake you."),
            ("hedgehog", "Thank you, my friends. Now, I'm going to curl up. Yawn.")]),
    ], song=song("Brahms' Lullaby", "den", [("mimo", 340, L), ("hedgehog", 640, L), ("fox", 960, R)], "soft", 0)),

    dict(label="The First Snow", story=[
        dict(decor="snow_night", cast=[("mimo", 420, 420, L), ("fox", 880, 880, R)], lines=[
            ("narrator", "That night, the very first snowflakes came floating down, one by one, onto the quiet woods."),
            ("mimo", "Look, Finn! It's snowing!"),
            ("fox", "Right on time. Hazel is already asleep, snug as can be."),
            ("mimo", "I'll see you in the spring, Hazel. Sleep well.")]),
    ], song=None),

    dict(label="Goodnight, Hazel", story=[
        dict(decor="den", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Mimo went home through the snow, past the sleepy nest, where a little hedgehog was dreaming of spring."),
            ("mimo", "Goodnight, Hazel. Goodnight, leaves. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="snow_night", cast=[("bunny", 230, L), ("mimo", 520, L), ("fox", 820, R), ("fawn", 1100, R)], minutes=12),
  teaser=dict(decor="cave", cast=[("bat", 420, 420, L), ("mimo", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("bat", "Mimo, I'm lost! I flew into a cave, and my echoes don't know where the door is!"),
      ("narrator", "Find out in the next episode: Echo and the Crystal Cave!")]))

# ======================================================================= 18. Echo and the Crystal Cave  (grotte, jeu de sons)
S2E06 = dict(id="s2e06", style="s2", title="Echo and the Crystal Cave", bye_decor="cave",
  blurb="Echo the little bat is lost in a glowing crystal cave. Mimo discovers how a bat sees with sound, and how to follow an echo all the way home.",
  fact="bats are not blind. They make high squeaks, and the echoes that bounce back tell them where everything is, even in total darkness.",
  chapters=[
    dict(label="Echo Is Lost", story=[
        dict(decor="forest_night", cast=[("mimo", -150, 420, L), ("bat", 1450, 900, R)], lines=[
            ("bat", "Mimo! Mimo! Help! I flew into a big cave, and now I can't find the way out!"),
            ("mimo", "Echo? But you never get lost. You have the best echoes in the forest!"),
            ("bat", "I know! But inside the cave, there are so many echoes bouncing everywhere, that I got all mixed up."),
            ("mimo", "Don't worry. I'll come with you. Together, we'll find the way.")]),
    ], song=song("Twinkle Twinkle Little Star", "forest_night", [("mimo", 440, L), ("bat", 860, R)], "box", 0)),

    dict(label="Into the Cave", story=[
        dict(decor="cave", cast=[("mimo", -150, 420, L), ("bat", 1450, 880, R)], lines=[
            ("narrator", "Inside the cave, it was dark and cool. But the walls were dotted with tiny glowing crystals."),
            ("mimo", "Wow. It's like a night sky, but under the ground."),
            ("bat", "It's beautiful. But it's also confusing. Every wall answers back, and every answer is different."),
            ("mimo", "Hello! Hello! Hello!"),
            ("bat", "See? That's an echo. Your voice goes out, hits the wall, and comes back.")]),
    ], song=song("Are You Sleeping (Frère Jacques)", "cave", [("mimo", 440, L), ("bat", 860, R)], "bell", 2)),

    dict(label="Mimo Calls Out", story=[
        dict(decor="cave", cast=[("mimo", 420, 420, L), ("bat", 880, 880, R)], lines=[
            ("bat", "I have an idea. Do what I do, Mimo. Call out, and then listen very carefully."),
            ("mimo", "Hoooo! Okay. I hear it coming back quickly from the left."),
            ("bat", "A quick echo means a wall that's very close."),
            ("mimo", "Hoooo! This one is slow. It takes a long time to come back from the right."),
            ("bat", "A slow echo means a wide open space. Maybe a tunnel! That's what we need.")]),
    ], song=None),

    dict(label="A Friend in the Dark", story=[
        dict(decor="cave", cast=[("mimo", -150, 640, L), ("bat", -420, 330, L), ("owl", 1450, 960, R)], lines=[
            ("owl", "Hoo hoo. Is somebody calling in my cave?"),
            ("mimo", "Luna! You're here too!"),
            ("owl", "I like to rest here in the daytime. Echo, why are you flying so low?"),
            ("bat", "I'm lost. I can't find the way out through all the echoes."),
            ("owl", "Hoo hoo. Then let's sing a song. A big, clear melody makes a very clean echo, and the echo always knows the door.")]),
    ], song=song("Mary Had a Little Lamb", "cave", [("mimo", 330, L), ("bat", 640, L), ("owl", 960, R)], "harp", 0)),

    dict(label="Follow the Echo", story=[
        dict(decor="cave", cast=[("mimo", 330, 330, L), ("owl", 640, 640, L), ("bat", 960, 960, R)], lines=[
            ("narrator", "The friends followed the sound through the tunnel. Left, then right, then straight ahead."),
            ("bat", "I hear it! The song is coming back from outside! The echo is open and wide!"),
            ("mimo", "That's the way out, Echo! The night air is blowing in."),
            ("owl", "Hoo hoo. You did it, little bat. You never lost your echo. You only needed a bit of company.")]),
    ], song=song("Row Row Row Your Boat", "cave", [("mimo", 330, L), ("owl", 640, L), ("bat", 960, R)], "soft", 2)),

    dict(label="Out Under the Stars", story=[
        dict(decor="forest_night", cast=[("mimo", 420, 420, L), ("bat", 880, 880, R)], lines=[
            ("narrator", "They stepped out of the cave, and the moon was waiting for them, big and round."),
            ("bat", "Thank you, Mimo. Now I'll always remember that even a lost bat can find the way, with a good friend."),
            ("mimo", "And I learned that listening is a kind of seeing. Goodnight, Echo. Goodnight, everyone.")]),
    ], song=None),
  ],
  finale=dict(decor="forest_night", cast=[("owl", 230, L), ("mimo", 530, L), ("fox", 830, R), ("hedgehog", 1110, R)], minutes=12),
  teaser=dict(decor="pond_night", cast=[("turtle", 420, 420, L), ("bunny", 880, 880, R)], lines=[
      ("narrator", "Next time, on Sleepy Mimo: Wild Nights..."),
      ("turtle", "Pip, tonight the full moon will sit on the water, but only for a little while. We have to hurry!"),
      ("bunny", "Hurry? I love to hurry! But what about you, Shelly?"),
      ("narrator", "Find out in the next episode: Race to the Moon Pond!")]))
