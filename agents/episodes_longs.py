"""Épisodes « longs » : l'histoire dure toute la vidéo.
Chaque chapitre = une partie de l'histoire, puis une chanson chantée et dansée par les personnages dans le décor.
Le dernier chapitre mène au grand final, puis aux berceuses pendant que tout le monde dort.

song : name (comptine), decor, cast = [(personnage, x, sens)], voice (instrument principal), transpose, boat (barque)
finale : decor, cast (personnages endormis), minutes de berceuses."""

L, R = 1, -1

EP1 = dict(id="s1e01", title="Hello, Mimo!", chapters=[
    # ---------------------------------------------------------------- 1. La mission de Twinkle
    dict(story=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Far away, in a land of soft hills and sparkly rivers, lives a little bear called Mimo."),
            ("mimo", "Hello! I'm Mimo! I love honey, stars, and my cozy sleepy hat."),
            ("mimo", "It's almost bedtime. Pajamas on, teeth brushed... and now, my favorite part!"),
            ("mimo", "Looking at the stars from my window!")]),
        dict(decor="bedroom", cast=[("mimo", 640, 860, L), ("star", 1450, 1040, R)], lines=[
            ("narrator", "But tonight, one little star came down, all the way to Mimo's window."),
            ("star", "Twinkle, twinkle! Hello, Mimo! I'm Twinkle, the littlest star."),
            ("mimo", "Twinkle! A real star, in my bedroom? Wow!"),
            ("star", "I have a very important mission for you. Tonight is the Big Goodnight Song!"),
            ("mimo", "The Big Goodnight Song? What's that?"),
            ("star", "Once a year, all the friends meet on the lantern hill and sing together, so the whole sky can sleep."),
            ("star", "Can you invite everyone? Pip, Dot, Mia, Finn, Wooly and Luna?"),
            ("mimo", "Yes! I'll invite all my friends! But first... can we sing your song?"),
            ("star", "Of course! Sing with me, Mimo!")]),
    ], label="Twinkle's Mission", song=dict(name="Twinkle Twinkle Little Star", decor="bedroom", cast=[("mimo", 560, L), ("star", 900, R)], voice="box", transpose=0)),

    # ---------------------------------------------------------------- 2. Pip, Dot et la barque
    dict(story=[
        dict(decor="meadow", cast=[("mimo", -150, 380, L), ("bunny", 1450, 760, R), ("duck", 1600, 980, R)], lines=[
            ("narrator", "Mimo tiptoed outside, and hopped down to the flower meadow."),
            ("bunny", "Hop hop! Hi, Mimo! I'm Pip, the bounciest bunny in the whole meadow!"),
            ("duck", "Quack quack! And I'm Dot! I'm a little duckling, and I love puddles!"),
            ("mimo", "Pip! Dot! Tonight is the Big Goodnight Song on the lantern hill. Will you come?"),
            ("bunny", "Yes, yes, yes! I love singing! Hop hop!"),
            ("duck", "But the lantern hill is far away, on the other side of the river."),
            ("mimo", "Hmm. How can we cross the river?"),
            ("duck", "I know! My grandma's little boat! It's waiting by the water!")]),
        dict(decor="river", boat=True, cast=[("mimo", 560, 560, L), ("bunny", 730, 730, R), ("duck", 1450, 1000, R)], lines=[
            ("narrator", "So the three friends climbed into the little boat."),
            ("duck", "Quack! I'll swim next to you. Ducks don't need boats!"),
            ("bunny", "Mimo, how do we make the boat go?"),
            ("mimo", "We row gently, gently, all together. And when we row, we sing!")]),
    ], label="The Little Boat", song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("bunny", 730, R)], voice="harp", transpose=2)),

    # ---------------------------------------------------------------- 3. Le pont de Finn
    dict(story=[
        dict(decor="forest", cast=[("mimo", -150, 330, L), ("bunny", -330, 140, L), ("kitten", 1450, 760, R), ("fox", 1600, 1000, R)], lines=[
            ("narrator", "On the other side of the river, the friends walked into the rainbow forest."),
            ("kitten", "Meow! Hello, Mimo! I'm Mia. Do you like my pink ribbon?"),
            ("mimo", "It's beautiful, Mia! Tonight is the Big Goodnight Song. Will you come?"),
            ("kitten", "Oh, I'd love to! But there's a little stream, and I don't like getting my paws wet."),
            ("fox", "Hey, everyone! I'm Finn the fox. Don't worry, Mia. I'm a super builder!"),
            ("fox", "I'll build a bridge over the stream, with sticks and stones!"),
            ("bunny", "Can we help you, Finn?"),
            ("fox", "Yes! Building is better with friends. Let's build it together!")]),
    ], label="Finn's Bridge", song=dict(name="London Bridge", decor="forest", cast=[("fox", 380, L), ("kitten", 600, L), ("mimo", 820, R), ("bunny", 1040, R)], voice="soft", transpose=0)),

    # ---------------------------------------------------------------- 4. Wooly dort dans la prairie
    dict(story=[
        dict(decor="meadow", cast=[("mimo", -150, 320, L), ("kitten", -330, 150, L), ("lamb", 900, 900, R)], lines=[
            ("narrator", "Across the bridge, the friends found a soft, fluffy cloud... lying in the grass."),
            ("kitten", "Look! A little cloud fell from the sky!"),
            ("mimo", "That's not a cloud. That's Wooly the lamb! He's fast asleep."),
            ("narrator", "Wooly was snoring. Baa-zzz. Baa-zzz."),
            ("kitten", "We have to wake him up, or he'll miss the Big Goodnight Song!"),
            ("mimo", "Let's wake him up very gently, with a song.")]),
    ], label="Sleepy Wooly", song=dict(name="Are You Sleeping (Frère Jacques)", decor="meadow", cast=[("mimo", 330, L), ("kitten", 540, L), ("fox", 750, R), ("lamb", 1000, R)], voice="bell", transpose=0, sleepy="lamb")),

    # ---------------------------------------------------------------- 5. La cloche de Luna
    dict(story=[
        dict(decor="meadow", cast=[("lamb", 900, 900, R), ("mimo", 330, 330, L)], lines=[
            ("lamb", "Baa! Oh, hello, friends! I was dreaming of clover cookies."),
            ("mimo", "Wooly, come with us! It's the Big Goodnight Song tonight!"),
            ("lamb", "The Big Goodnight Song? Baa, I almost forgot! Let's go!")]),
        dict(decor="night", cast=[("mimo", -150, 330, L), ("lamb", -330, 150, L), ("owl", 1450, 960, R)], lines=[
            ("narrator", "At last, the friends climbed up the lantern hill, where the lanterns glow pink, yellow and blue."),
            ("owl", "Hoo hoo. Welcome, little ones. I am Luna. I keep the bedtime bell."),
            ("owl", "Ding, dang, dong! The Big Goodnight Song is about to begin."),
            ("mimo", "Luna, is everybody here?"),
            ("owl", "Pip, Dot, Mia, Finn, Wooly... Yes, everyone is here. Well done, Mimo."),
            ("lamb", "Before the big song, may I sing my favorite song? It's about a little lamb, like me!"),
            ("owl", "Hoo hoo. Of course, Wooly. Everybody, sing along!")]),
    ], label="Luna's Bell", song=dict(name="Mary Had a Little Lamb", decor="night", cast=[("bunny", 220, L), ("lamb", 440, L), ("mimo", 660, L), ("duck", 870, R), ("owl", 1080, R)], voice="bell", transpose=0)),

    # ---------------------------------------------------------------- 6. Le grand final
    dict(story=[
        dict(decor="night", cast=[("mimo", 420, 420, L), ("owl", 960, 960, R), ("star", 1450, 700, R)], lines=[
            ("narrator", "Then, something magical happened. Twinkle floated down from the sky."),
            ("star", "Mimo, you did it! All your friends are here!"),
            ("mimo", "Everybody came, Twinkle! Pip, Dot, Mia, Finn, Wooly and Luna!"),
            ("star", "Then it's time. Let's sing the Big Goodnight Song, so the whole sky can sleep."),
            ("owl", "Everybody, take a deep breath. One, two, three!")]),
    ], label="The Big Goodnight Song", song=dict(name="Twinkle Twinkle Little Star", decor="clouds", cast=[("bunny", 160, L), ("kitten", 360, L), ("mimo", 560, L), ("star", 760, R), ("fox", 960, R), ("duck", 1150, R)], voice="bell", transpose=2)),

    # ---------------------------------------------------------------- 7. Tout le monde s'endort
    dict(story=[
        dict(decor="night", cast=[("mimo", 420, 420, L), ("owl", 860, 860, R)], lines=[
            ("narrator", "The stars sparkled brighter than ever. The Big Goodnight Song had worked!"),
            ("mimo", "Luna... I'm so sleepy now."),
            ("owl", "Hoo hoo. Then lie down, little ones, on the soft grass. I'll play you my lullaby."),
            ("mimo", "Goodnight, Luna. Goodnight, Twinkle. Goodnight, everyone."),
            ("narrator", "And one by one, all the friends closed their eyes, and fell asleep under the stars.")]),
    ], label="Everyone Falls Asleep", song=None),
], finale=dict(decor="night", cast=[("bunny", 220, L), ("lamb", 420, L), ("mimo", 640, L), ("kitten", 860, R), ("duck", 1060, R)], minutes=12),
   teaser=dict(decor="river", cast=[("duck", -150, 560, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("duck", "The big river? Me? Swimming all by myself? Quack... I'm a little bit scared."),
       ("narrator", "And who is making that big, mysterious splash under the water?"),
       ("duck", "Mimo! Something is down there! Something big!"),
       ("narrator", "Find out in the next episode: Dot's First Swim!")]))


EP2 = dict(id="s1e02", title="Dot's First Swim", chapters=[
    dict(label="Dot's Big Day", story=[
        dict(decor="meadow", cast=[("duck", 640, 640, L)], lines=[
            ("narrator", "In the flower meadow lives Dot, a little yellow duckling who loves puddles."),
            ("duck", "Splash! Splish! Splash! Puddles are the best thing in the whole world!"),
            ("duck", "And guess what? Tonight, before the moon comes up, I'm going to swim in the big river. For the very first time!")]),
        dict(decor="meadow", cast=[("duck", 640, 640, L), ("mimo", -150, 330, L), ("bunny", 1450, 900, R), ("lamb", 1700, 1120, R)], lines=[
            ("mimo", "Dot! We heard the big news! Your first swim!"),
            ("bunny", "Hop hop hooray! We'll come and cheer for you!"),
            ("duck", "Thank you! I'm so excited. And... maybe a tiny bit scared."),
            ("mimo", "That's okay, Dot. Even brave ducks feel a little scared sometimes."),
            ("narrator", "Just then, a fluffy friend came trotting over the hill."),
            ("lamb", "Baa! Wait for me! I want to cheer for Dot too!")]),
        dict(decor="meadow", cast=[("mimo", 330, 330, L), ("duck", 640, 640, L), ("bunny", 940, 940, R), ("lamb", 1450, 1120, R)], lines=[
            ("lamb", "When I feel scared, I sing my favorite song. It makes my wool all warm and cozy."),
            ("duck", "Will you sing it with me, Wooly?"),
            ("lamb", "Of course! Everybody, sing along!")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="meadow", cast=[("mimo", 260, L), ("duck", 500, L), ("lamb", 760, R), ("bunny", 1010, R)], voice="bell", transpose=0)),

    dict(label="The Mysterious Splash", story=[
        dict(decor="river", cast=[("duck", -150, 520, L), ("mimo", -330, 300, L), ("bunny", 1450, 900, R)], lines=[
            ("narrator", "The friends walked down to the sparkly river. The water was wide, and blue, and shiny."),
            ("duck", "Wow. The river is so much bigger than a puddle."),
            ("bunny", "You can do it, Dot! One little step!"),
            ("narrator", "But just as Dot put one foot in the water... SPLASH!"),
            ("duck", "Quack! What was that?"),
            ("mimo", "Something big jumped in the water! Right over there!"),
            ("bunny", "Maybe it's a sea monster! Hop hop, let's hide!")]),
        dict(decor="river", boat=True, cast=[("mimo", 560, 560, L), ("bunny", 730, 730, R)], lines=[
            ("narrator", "But Mimo wanted to find out what it was. So he climbed into the little boat."),
            ("bunny", "Mimo, are you sure? What if it's a big, grumpy monster?"),
            ("mimo", "Maybe it's not grumpy. Maybe it's just... someone we don't know yet."),
            ("mimo", "Let's row very gently, and sing, so it knows we're friendly.")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("bunny", 730, R)], voice="harp", transpose=2)),

    dict(label="Meet Bubbles", story=[
        dict(decor="river", cast=[("mimo", 330, 330, L), ("duck", 560, 560, L), ("fish", 1450, 900, R)], lines=[
            ("narrator", "Then, very slowly, a big round face came up out of the water."),
            ("fish", "Blub, blub... Hello? Please don't run away."),
            ("duck", "Quack! You're... a fish! A big, blue, round fish!"),
            ("fish", "I'm Bubbles. I live in the river. I splash when I'm happy, but everyone gets scared and runs away."),
            ("mimo", "Oh, Bubbles. You just wanted to make friends!"),
            ("fish", "Yes. Blub. It's a little lonely in the river."),
            ("duck", "I was scared of you... but you're not scary at all. You're nice!")]),
        dict(decor="river", cast=[("mimo", 330, 330, L), ("duck", 560, 560, L), ("fish", 900, 900, R), ("fox", -150, 140, L)], lines=[
            ("fish", "Dot, I heard it's your first swim. I'm the best swimmer in the whole river. May I help you?"),
            ("duck", "Really? You'd swim next to me?"),
            ("fox", "Hey, everyone! I'm Finn! I'll build a little wooden dock, so Dot can step into the water slowly!"),
            ("mimo", "Great idea, Finn! Let's all help!"),
            ("fox", "Building song, everybody! One, two, three!")]),
    ], song=dict(name="London Bridge", decor="river", cast=[("fox", 300, L), ("mimo", 520, L), ("duck", 740, R), ("fish", 1000, R)], voice="soft", transpose=0)),

    dict(label="Dot Swims!", story=[
        dict(decor="river", cast=[("duck", 560, 560, L), ("fish", 900, 900, R), ("mimo", 300, 300, L), ("bunny", -150, 120, L)], lines=[
            ("narrator", "The little dock was ready. Dot stood at the very edge."),
            ("fish", "I'm right here, Dot. Just paddle your feet, like this. Blub, blub."),
            ("duck", "One, two, three... SPLASH!"),
            ("narrator", "And Dot... was floating! And paddling! And swimming!"),
            ("duck", "I'm swimming! I'm really swimming! Look at me, everyone!"),
            ("bunny", "Hop hop hooray! Go, Dot, go!"),
            ("mimo", "You did it, Dot! You were so brave!"),
            ("fish", "And now I have new friends. This is the best day ever. Blub!")]),
        dict(decor="night", cast=[("mimo", 300, 300, L), ("duck", 520, 520, L), ("bunny", 740, 740, R), ("owl", 1450, 1000, R)], lines=[
            ("narrator", "Soon, the sky turned purple, and the first stars began to twinkle."),
            ("owl", "Hoo hoo. What a brave day, little Dot. I saw everything from my tree."),
            ("duck", "Luna! I swam in the big river! And I made a new friend!"),
            ("owl", "That deserves a song. Look, the stars are coming out to listen.")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="night", cast=[("mimo", 240, L), ("duck", 460, L), ("owl", 700, R), ("bunny", 940, R), ("star", 1100, R)], voice="box", transpose=0)),

    dict(label="Sleepy Swimmers", story=[
        dict(decor="night", cast=[("duck", 520, 520, L), ("mimo", 300, 300, L), ("owl", 860, 860, R)], lines=[
            ("duck", "Luna... swimming makes you so... sleepy."),
            ("owl", "Hoo hoo. That's because you used all your brave today, little one."),
            ("mimo", "Goodnight, Dot. Goodnight, Bubbles, down in the river."),
            ("narrator", "Far away, in the sparkly river, Bubbles blew one last bubble... and closed his eyes."),
            ("narrator", "And on the lantern hill, all the friends fell asleep, dreaming of splashes and stars.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("bunny", 240, L), ("duck", 450, L), ("mimo", 660, L), ("lamb", 880, R), ("fox", 1080, R)], minutes=12),
   teaser=dict(decor="forest", cast=[("kitten", -150, 600, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("kitten", "Whoosh! The wind is so strong tonight! Oh no... my pink ribbon! It's flying away!"),
       ("narrator", "Where will the wind take Mia's favorite ribbon? And who will find it first?"),
       ("narrator", "Find out in the next episode: Mia's Missing Ribbon!")]))


EP3 = dict(id="s1e03", title="Mia's Missing Ribbon", chapters=[
    dict(label="The Windy Night", story=[
        dict(decor="forest", cast=[("kitten", 640, 640, L)], lines=[
            ("narrator", "It was a windy, whooshy night in the rainbow forest."),
            ("kitten", "Meow! Look at my pink ribbon. It's my very favorite thing in the whole world."),
            ("narrator", "But then, a big gust of wind came rushing through the trees. Whoooosh!"),
            ("kitten", "Oh no! My ribbon! Come back! Come back!")]),
        dict(decor="forest", cast=[("kitten", 420, 420, L), ("mimo", 1450, 760, R), ("bunny", 1600, 980, R)], lines=[
            ("mimo", "Mia! We heard you calling. What happened?"),
            ("kitten", "The wind took my pink ribbon, Mimo. It flew up, up, up, and now it's gone."),
            ("bunny", "Don't cry, Mia. We'll find it! Hop hop, I'm a super finder!"),
            ("mimo", "But it's so dark. How can we see where it went?"),
            ("narrator", "Just then, a soft golden light began to twinkle above the trees."),
            ("star", "Twinkle, twinkle! Did somebody need a little light?")]),
        dict(decor="forest", cast=[("kitten", 420, 420, L), ("mimo", 760, 760, R), ("star", 1450, 1040, R)], lines=[
            ("kitten", "Twinkle! Did you see a pink ribbon flying in the sky?"),
            ("star", "I did! It flew toward the sparkly river. I'll light the way for you."),
            ("mimo", "Thank you, Twinkle! Let's sing your song, so you shine extra bright!")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="forest", cast=[("kitten", 300, L), ("mimo", 520, L), ("bunny", 740, R), ("star", 980, R)], voice="box", transpose=0)),

    dict(label="A Clue in the River", story=[
        dict(decor="river", cast=[("mimo", -150, 320, L), ("kitten", -330, 530, L), ("fish", 1450, 920, R)], lines=[
            ("narrator", "Following Twinkle's light, the friends arrived at the sparkly river."),
            ("fish", "Blub, blub! Hello, friends! What are you doing out so late?"),
            ("mimo", "Bubbles! We're looking for Mia's pink ribbon. Have you seen it?"),
            ("fish", "Yes! A pink ribbon floated over the water, like a little flying fish!"),
            ("fish", "The wind carried it to the other side of the river. Toward the flower meadow."),
            ("kitten", "The other side? But I can't swim! Cats don't like getting wet!"),
            ("mimo", "Don't worry, Mia. We'll take the little boat.")]),
        dict(decor="river", boat=True, cast=[("mimo", 560, 560, L), ("kitten", 730, 730, R)], lines=[
            ("kitten", "Meow... the boat is wobbly. I'm a little nervous."),
            ("mimo", "Hold on tight, Mia. If we row together, and sing together, we'll be across in no time!")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("kitten", 730, R)], voice="harp", transpose=2)),

    dict(label="The Broken Bridge", story=[
        dict(decor="meadow", cast=[("mimo", -150, 330, L), ("kitten", -330, 140, L), ("duck", 1450, 780, R)], lines=[
            ("narrator", "In the flower meadow, they met Dot the duckling."),
            ("duck", "Quack! Look what I found! Is this your ribbon, Mia?"),
            ("kitten", "Hmm... no, Dot. That's a pink flower petal. But thank you for looking!"),
            ("duck", "Oops! Quack, quack. Silly me."),
            ("mimo", "Dot, did you see anything pink flying by?"),
            ("duck", "Yes! Something pink went over the little stream, toward the lantern hill. But the little bridge is broken!")]),
        dict(decor="meadow", cast=[("mimo", 330, 330, L), ("kitten", 140, 140, L), ("duck", 780, 780, R), ("fox", 1450, 1040, R)], lines=[
            ("fox", "Did somebody say broken bridge? Finn the fox, super builder, at your service!"),
            ("mimo", "Finn! Can you help us fix it?"),
            ("fox", "Of course! But it's a big job. I'll need everyone's help."),
            ("kitten", "I'll find the flat stones."),
            ("duck", "I'll carry the little sticks!"),
            ("fox", "Then let's build it together. Everybody, sing the building song!")]),
    ], song=dict(name="London Bridge", decor="meadow", cast=[("fox", 260, L), ("kitten", 480, L), ("mimo", 700, R), ("duck", 920, R)], voice="soft", transpose=0)),

    dict(label="Found It!", story=[
        dict(decor="night", cast=[("mimo", -150, 320, L), ("kitten", -330, 130, L), ("lamb", 900, 900, R)], lines=[
            ("narrator", "Across the new bridge, at the top of the lantern hill, someone was waiting."),
            ("lamb", "Baa! Hello, friends! Look at me! A pink ribbon fell from the sky, right onto my wool!"),
            ("kitten", "My ribbon! Wooly, you found it!"),
            ("lamb", "Oh! It's yours, Mia? I thought it was a present from the wind. Here, you can have it back."),
            ("narrator", "Mia looked at her ribbon. Then she looked at Wooly, who looked so happy and so fancy."),
            ("kitten", "Wooly... you can wear it tonight. It looks lovely on you. Sharing makes me happy too."),
            ("lamb", "Really? Thank you, Mia! You're the kindest kitten ever!"),
            ("mimo", "Hooray! Let's sing Wooly's favorite song, for the fanciest lamb on the hill!")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="night", cast=[("kitten", 240, L), ("lamb", 460, L), ("mimo", 680, R), ("fox", 900, R), ("duck", 1100, R)], voice="bell", transpose=0)),

    dict(label="A Kind Goodnight", story=[
        dict(decor="night", cast=[("mimo", 330, 330, L), ("kitten", 560, 560, L), ("owl", 1450, 900, R)], lines=[
            ("owl", "Hoo hoo. I saw everything from my tree, little Mia. You were very kind tonight."),
            ("kitten", "Thank you, Luna. My ribbon went on a big adventure. And so did I!"),
            ("mimo", "And we did it all together. Friends, Twinkle, Bubbles, the boat and the bridge!"),
            ("owl", "Now, it's time to rest. Lie down on the soft grass, and listen to the wind sing you to sleep."),
            ("narrator", "The wind was gentle now. It whispered through the trees, like a lullaby."),
            ("narrator", "And one by one, the friends closed their eyes. Goodnight, Mia. Goodnight, Wooly. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("bunny", 230, L), ("kitten", 440, L), ("lamb", 650, L), ("mimo", 860, R), ("fox", 1070, R)], minutes=12),
   teaser=dict(decor="forest", cast=[("owl", -150, 600, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("owl", "Hoo hoo! Oh no! My bedtime bell... it won't ring! Not a single ding, not a single dong!"),
       ("narrator", "If the bedtime bell can't ring, how will everyone know it's time to sleep?"),
       ("narrator", "Find out in the next episode: The Bedtime Bell!")]))


EP4 = dict(id="s1e04", title="The Bedtime Bell", chapters=[
    dict(label="The Silent Bell", story=[
        dict(decor="forest", cast=[("owl", 640, 640, L)], lines=[
            ("narrator", "Every night, in the rainbow forest, Luna the owl rings the bedtime bell. Ding, dang, dong!"),
            ("owl", "Hoo hoo! Time to ring the bell. One, two, three..."),
            ("narrator", "But tonight... nothing. Not a single ding. Not a single dong."),
            ("owl", "Oh no! My bell won't ring! How will everyone know it's time to sleep?")]),
        dict(decor="forest", cast=[("owl", 420, 420, L), ("mimo", 1450, 760, R), ("bunny", 1600, 980, R)], lines=[
            ("mimo", "Luna! We were waiting for the bell, but it never rang. Is everything okay?"),
            ("owl", "My bell is silent, Mimo. I don't know why."),
            ("bunny", "Maybe something is stuck inside! Let's take a peek!"),
            ("narrator", "Very carefully, they peeked inside the big golden bell. And there, in a tiny nest of moss..."),
            ("bunny", "Oh! Look! Three teeny, tiny lights! They're baby fireflies, and they're fast asleep!"),
            ("owl", "Hoo hoo. They made their nest inside my bell. If I ring it, I'll wake them up."),
            ("mimo", "Shhh. Let's sing them a soft song, so they keep dreaming.")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="forest", cast=[("bunny", 330, L), ("owl", 600, L), ("mimo", 880, R)], voice="box", transpose=-2)),

    dict(label="Bubble Bells", story=[
        dict(decor="forest", cast=[("owl", 420, 420, L), ("mimo", 760, 760, R), ("bunny", 980, 980, R)], lines=[
            ("owl", "But now we have a problem. Without the bell, nobody will know it's bedtime."),
            ("mimo", "I have an idea! We'll go and tell all our friends, ourselves!"),
            ("bunny", "Yes! We'll be the bedtime bell! Hop hop, let's go!")]),
        dict(decor="river", cast=[("mimo", -150, 330, L), ("bunny", -330, 140, L), ("fish", 1450, 920, R), ("duck", 1600, 640, R)], lines=[
            ("fish", "Blub, blub! Hello, friends! I didn't hear the bedtime bell tonight."),
            ("duck", "Quack! Me neither! Is it still playtime?"),
            ("mimo", "The bell can't ring tonight, so we're telling everyone: it's bedtime!"),
            ("fish", "I can help! Listen. I can make bubble bells. Blub-ding! Blub-dong!"),
            ("duck", "Quack, that's so funny! Bubble bells!"),
            ("bunny", "Let's cross the river and tell the others. Everybody in the boat!")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("bunny", 730, R)], voice="harp", transpose=2)),

    dict(label="Wooly's Idea", story=[
        dict(decor="meadow", cast=[("mimo", -150, 300, L), ("bunny", -330, 120, L), ("lamb", 1450, 760, R), ("kitten", 1600, 980, R)], lines=[
            ("narrator", "In the flower meadow, Wooly and Mia were still playing tag."),
            ("kitten", "Meow! Mimo! We didn't hear the bell. Is it time for bed?"),
            ("mimo", "Yes! The bell is silent tonight, because baby fireflies are sleeping inside."),
            ("lamb", "Baa! Baby fireflies? How cute! But how will the whole land know it's bedtime?"),
            ("lamb", "Oh, I know! When my mommy wants me to come home, she sings my song. Everyone knows it!"),
            ("kitten", "Let's sing it really loud, so all the little ones hear it!")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="meadow", cast=[("bunny", 220, L), ("lamb", 440, L), ("mimo", 660, R), ("kitten", 880, R), ("duck", 1090, R)], voice="bell", transpose=0)),

    dict(label="We Are the Bell!", story=[
        dict(decor="night", cast=[("mimo", -150, 330, L), ("lamb", -330, 140, L), ("owl", 1450, 900, R), ("fox", 1600, 640, R)], lines=[
            ("narrator", "At last, everyone gathered on the lantern hill."),
            ("fox", "Hey, everyone! I heard singing all over the land. What's going on?"),
            ("owl", "Hoo hoo. Tonight, my friends, we will be the bedtime bell. All of us, together."),
            ("mimo", "We'll sing the bell song! The one that goes ding, dang, dong!"),
            ("fox", "Great idea! When we sing together, we're even louder than a bell!"),
            ("owl", "But softly, so we don't wake the baby fireflies. Ready? One, two, three!")]),
    ], song=dict(name="Are You Sleeping (Frère Jacques)", decor="night", cast=[("bunny", 200, L), ("fox", 400, L), ("mimo", 600, L), ("owl", 820, R), ("lamb", 1040, R)], voice="bell", transpose=0)),

    dict(label="Thank You, Fireflies", story=[
        dict(decor="forest", cast=[("owl", 420, 420, L), ("mimo", 760, 760, R)], lines=[
            ("narrator", "Back at the big golden bell, something wonderful was happening."),
            ("narrator", "The three baby fireflies had woken up, and they were glowing brighter than ever."),
            ("owl", "Hoo hoo. Look, Mimo. They heard your song. Now they're ready for their first flight."),
            ("narrator", "And up they flew, like three tiny stars, all the way into the sky."),
            ("mimo", "Goodbye, little fireflies! Now Luna's bell can ring again!"),
            ("owl", "Tomorrow, it will ring. But tonight, your song was the most beautiful bell of all."),
            ("mimo", "Goodnight, Luna. Goodnight, fireflies. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("bunny", 230, L), ("fox", 440, L), ("mimo", 650, L), ("lamb", 860, R), ("kitten", 1070, R)], minutes=12),
   teaser=dict(decor="meadow", cast=[("fox", -150, 600, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("fox", "I'm going to build the biggest bridge ever! All by myself! Nobody can help me!"),
       ("narrator", "But what happens when Finn's bridge keeps falling down?"),
       ("narrator", "Find out in the next episode: Finn Learns to Share!")]))


EP5 = dict(id="s1e05", title="Finn Learns to Share", chapters=[
    dict(label="The Biggest Bridge Ever", story=[
        dict(decor="meadow", cast=[("fox", 640, 640, L)], lines=[
            ("narrator", "Finn the fox loved building things. Towers of pinecones. Houses of leaves. And bridges. Lots of bridges."),
            ("fox", "Today, I'm going to build the biggest bridge ever! All the way across the stream, to the lantern hill!"),
            ("fox", "And I'll build it all by myself. Because I'm the best builder in the whole land!")]),
        dict(decor="meadow", cast=[("fox", 640, 640, L), ("mimo", -150, 330, L), ("kitten", 1450, 960, R)], lines=[
            ("mimo", "Wow, Finn! That's a big pile of sticks! Can we help you build?"),
            ("kitten", "Meow! I'm very good at finding flat stones!"),
            ("fox", "No, thank you. It's my bridge. I want to do it alone."),
            ("kitten", "Oh. Okay, Finn."),
            ("narrator", "So Mimo and Mia sat down on the grass, and watched Finn work."),
            ("mimo", "Let's sing a little song while we wait. Maybe it will help Finn too.")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="meadow", cast=[("mimo", 330, L), ("kitten", 560, L), ("fox", 900, R)], voice="box", transpose=0, sleepy=None)),

    dict(label="Crash!", story=[
        dict(decor="meadow", cast=[("fox", 640, 640, L), ("mimo", 300, 300, L), ("kitten", 980, 980, R)], lines=[
            ("narrator", "Finn built, and built, and built. The bridge grew longer and longer."),
            ("fox", "Almost done! Just one more stick, and..."),
            ("narrator", "CRASH! The whole bridge fell down into the stream."),
            ("fox", "Oh no! My bridge! It fell down!"),
            ("mimo", "Are you okay, Finn?"),
            ("fox", "I'll try again. All by myself."),
            ("narrator", "But it fell down again. And again. And again.")]),
        dict(decor="river", cast=[("fox", 560, 560, L), ("fish", 1450, 920, R)], lines=[
            ("fish", "Blub, blub. Hello, Finn. I keep finding your sticks floating down my river!"),
            ("fox", "Sorry, Bubbles. My bridge keeps falling down. Building is too hard."),
            ("fish", "Hmm. Do you know how the river gets so big and strong, Finn?"),
            ("fox", "How?"),
            ("fish", "Lots of little streams, all coming together. Blub. Together is strong."),
            ("fox", "Together... is strong.")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", cast=[("fox", 420, L), ("fish", 860, R)], voice="harp", transpose=2)),

    dict(label="Building Together", story=[
        dict(decor="meadow", cast=[("fox", -150, 640, L), ("mimo", 300, 300, L), ("kitten", 980, 980, R), ("bunny", 1600, 1170, R), ("duck", -350, 110, L)], lines=[
            ("fox", "Mimo, Mia... I'm sorry I said no. I wanted to do everything alone. But I can't."),
            ("mimo", "That's okay, Finn. Everybody needs help sometimes."),
            ("kitten", "Do you still want to build the bridge? With us?"),
            ("fox", "Yes! Please! Will you help me?"),
            ("mimo", "Of course! That's what friends do."),
            ("narrator", "And soon, more friends came to help."),
            ("bunny", "Hop hop! I can carry the little sticks!"),
            ("duck", "Quack! And I can check the water!"),
            ("fox", "Okay, team! Mimo holds, Mia finds stones, Pip carries, Dot checks. Ready? Let's build!")]),
    ], song=dict(name="London Bridge", decor="meadow", cast=[("bunny", 200, L), ("kitten", 400, L), ("fox", 620, L), ("mimo", 840, R), ("duck", 1060, R)], voice="soft", transpose=0)),

    dict(label="Our Bridge", story=[
        dict(decor="night", cast=[("fox", 640, 640, L), ("mimo", 400, 400, L), ("kitten", 880, 880, R), ("owl", 1450, 1100, R)], lines=[
            ("narrator", "When the sky turned purple, the bridge was finished. And it was strong, and long, and beautiful."),
            ("fox", "Look! It's standing! It's really standing! Our bridge!"),
            ("kitten", "Our bridge. I like how that sounds."),
            ("owl", "Hoo hoo. What a wonderful bridge. Who built it?"),
            ("fox", "We all did, Luna! Together! I learned that sharing the work makes everything better."),
            ("owl", "That is a very wise lesson, little fox. Shall we walk across it, all together?"),
            ("mimo", "Yes! And let's sing the bridge song, so it stays strong forever!")]),
    ], song=dict(name="London Bridge", decor="night", cast=[("bunny", 220, L), ("fox", 440, L), ("mimo", 660, L), ("kitten", 880, R), ("owl", 1090, R)], voice="bell", transpose=2)),

    dict(label="A Proud Fox", story=[
        dict(decor="night", cast=[("fox", 520, 520, L), ("mimo", 760, 760, R)], lines=[
            ("fox", "Mimo... this was the best building day ever. Not because the bridge is big..."),
            ("fox", "But because I built it with my friends."),
            ("mimo", "Me too, Finn. Now let's rest. Builders need lots of sleep!"),
            ("narrator", "And on the lantern hill, next to their beautiful bridge, all the friends curled up and closed their eyes."),
            ("narrator", "Goodnight, Finn. Goodnight, builders. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("duck", 230, L), ("fox", 440, L), ("mimo", 650, L), ("kitten", 860, R), ("bunny", 1070, R)], minutes=12),
   teaser=dict(decor="bedroom", cast=[("mimo", 640, 860, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("mimo", "One, two, three, four... Wait. Where's Twinkle? She's not in the sky!"),
       ("narrator", "Has the littlest star really disappeared? And where could she have gone?"),
       ("narrator", "Find out in the next episode: Mimo and the Lost Star!")]))


EP6 = dict(id="s1e06", title="Mimo and the Lost Star", chapters=[
    dict(label="One Star Is Missing", story=[
        dict(decor="bedroom", cast=[("mimo", 640, 860, L)], lines=[
            ("narrator", "Every night, before bed, Mimo counts the stars from his window."),
            ("mimo", "One, two, three, four, five... and Twinkle! Wait. Where's Twinkle?"),
            ("mimo", "Twinkle is always right there, next to the moon. But tonight, her spot is empty!"),
            ("mimo", "Oh no. A little star can't be lost all alone in the dark. I have to find her!")]),
        dict(decor="forest", cast=[("mimo", -150, 420, L), ("owl", 1450, 860, R)], lines=[
            ("mimo", "Luna! Luna! Have you seen Twinkle? She's not in the sky!"),
            ("owl", "Hoo hoo. I did see something strange tonight. A tiny light, falling down, down, down... behind the clouds."),
            ("mimo", "That must be her! Will you help me find her, Luna?"),
            ("owl", "Of course, Mimo. Friends always help each other. But first, let's sing her song. Maybe she'll hear us and shine back.")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="forest", cast=[("mimo", 420, L), ("owl", 860, R)], voice="box", transpose=-2)),

    dict(label="Up to the Clouds", story=[
        dict(decor="clouds", cast=[("mimo", -150, 420, L), ("owl", -330, 760, L), ("bunny", 1450, 1040, R)], lines=[
            ("narrator", "Mimo and Luna climbed up, up, up the rainbow, to the land of soft clouds."),
            ("bunny", "Hop hop! Mimo! Luna! What are you doing up here so late?"),
            ("mimo", "Pip! We're looking for Twinkle. She fell out of the sky!"),
            ("bunny", "Oh no! I'll help! I'll bounce on the clouds and look everywhere! Boing, boing!"),
            ("narrator", "They looked behind the big clouds, and under the small clouds, and inside the fluffy clouds."),
            ("owl", "Hoo hoo. She isn't here. But look, little sparkles on the rainbow. They go down... toward the river."),
            ("mimo", "Sparkle footprints! Let's follow them!")]),
    ], song=dict(name="London Bridge", decor="clouds", cast=[("mimo", 330, L), ("bunny", 600, L), ("owl", 880, R)], voice="bell", transpose=0)),

    dict(label="Bubbles Knows Something", story=[
        dict(decor="river", cast=[("mimo", -150, 330, L), ("bunny", -330, 140, L), ("fish", 1450, 920, R)], lines=[
            ("fish", "Blub, blub! Hello, friends! Did you lose something shiny?"),
            ("mimo", "Bubbles! Yes! Our friend Twinkle, the littlest star. Did you see her?"),
            ("fish", "I saw a little light bounce on the water, like a skipping stone. Plip, plip, plop!"),
            ("fish", "Then it rolled up the lantern hill. It looked very, very sleepy."),
            ("bunny", "The lantern hill! It's on the other side of the river!"),
            ("mimo", "Let's take the boat. Row, row, as fast as we can... but gently!")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("bunny", 730, R)], voice="harp", transpose=2)),

    dict(label="Found You, Twinkle!", story=[
        dict(decor="night", cast=[("mimo", -150, 420, L), ("bunny", -330, 230, L), ("star", 960, 960, R), ("owl", -500, 640, L)], lines=[
            ("narrator", "At the very top of the lantern hill, behind a pink lantern, something was glowing softly."),
            ("star", "Hmm? Mimo? Is that you?"),
            ("mimo", "Twinkle! We found you! Are you okay?"),
            ("star", "I'm okay. I was so sleepy that I slipped right out of the sky. And now I'm too tired to fly back home."),
            ("bunny", "Oh no! How can we help a star fly?"),
            ("owl", "Hoo hoo. I know. Stars fly on happy music. If everyone sings together, Twinkle will float back up."),
            ("mimo", "Then let's call all our friends! Everybody, to the lantern hill!")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="night", cast=[("bunny", 220, L), ("lamb", 440, L), ("mimo", 660, L), ("kitten", 880, R), ("star", 1080, R)], voice="bell", transpose=0)),

    dict(label="Back to the Sky", story=[
        dict(decor="night", cast=[("mimo", 330, 330, L), ("star", 640, 640, L), ("owl", 950, 950, R)], lines=[
            ("star", "I feel lighter already! One more song, and I'll be back in the sky!"),
            ("mimo", "Ready, everyone? Let's sing Twinkle's very own song, louder and brighter than ever!"),
            ("owl", "One, two, three!")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="clouds", cast=[("bunny", 180, L), ("kitten", 380, L), ("mimo", 580, L), ("star", 780, R), ("lamb", 980, R), ("owl", 1150, R)], voice="bell", transpose=2)),

    dict(label="Goodnight, Twinkle", story=[
        dict(decor="bedroom", cast=[("mimo", 760, 860, L)], lines=[
            ("narrator", "And Twinkle floated up, up, up, all the way back to her spot, next to the moon."),
            ("mimo", "One, two, three, four, five... and Twinkle! Everyone is home."),
            ("narrator", "Far above, the littlest star winked at Mimo. Twinkle, twinkle."),
            ("mimo", "Goodnight, Twinkle. Goodnight, Luna. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("bunny", 230, L), ("owl", 440, L), ("mimo", 650, L), ("kitten", 860, R), ("lamb", 1070, R)], minutes=12),
   teaser=dict(decor="bedroom", cast=[("bunny", -150, 640, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("bunny", "Mimo? Mimo? I can't sleep! My eyes are wide open and my feet want to hop, hop, hop!"),
       ("narrator", "How do you help a bouncy bunny fall asleep? Maybe... by counting sheep?"),
       ("narrator", "Find out in the next episode: Pip Can't Sleep!")]))


from .episodes_longs2 import EP7, EP8, EP9, EP10, EP11, EP12
from .episodes_s2a import S2E01, S2E02, S2E03, S2E04, S2E05, S2E06
from .episodes_s2b import S2E07, S2E08, S2E09, S2E10, S2E11, S2E12

LONG_EPISODES = {"s1e01": EP1, "s1e02": EP2, "s1e03": EP3, "s1e04": EP4, "s1e05": EP5, "s1e06": EP6,
                 "s1e07": EP7, "s1e08": EP8, "s1e09": EP9, "s1e10": EP10, "s1e11": EP11, "s1e12": EP12,
                 "s2e01": S2E01, "s2e02": S2E02, "s2e03": S2E03, "s2e04": S2E04, "s2e05": S2E05, "s2e06": S2E06,
                 "s2e07": S2E07, "s2e08": S2E08, "s2e09": S2E09, "s2e10": S2E10, "s2e11": S2E11, "s2e12": S2E12}
