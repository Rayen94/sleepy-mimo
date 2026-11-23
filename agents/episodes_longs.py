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
        dict(decor="river", boat=True, cast=[("mimo", 560, 560, L), ("bunny", 730, 730, R)], lines=[
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


LONG_EPISODES = {"s1e01": EP1, "s1e02": EP2}
