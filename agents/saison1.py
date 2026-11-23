"""Saison 1 de la série « Sleepy Mimo » : 12 épisodes écrits, diffusés dans l'ordre.
Chaque épisode : une vraie histoire (début, problème, aventure, fin douce) puis la comptine qui va avec.
Personnages : mimo, owl (Luna), bunny (Pip), star (Twinkle), lamb (Wooly), kitten (Mia), duck (Dot), fox (Finn).
cast : (personnage, x de départ, x d'arrivée, sens) — x entre 150 et 1130, hors écran = -150 ou 1450."""

L, R = 1, -1

EPISODES = [
    dict(id="s1e01", title="Hello, Mimo!", song="Twinkle Twinkle Little Star", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Far away, in a land of soft hills and sparkly rivers, lives a little bear called Mimo."),
            ("mimo", "Hello! I'm Mimo! I love honey, stars, and my sleepy hat."),
            ("mimo", "Every evening, before bed, I go and say goodnight to all my friends."),
            ("mimo", "Do you want to come with me? Let's go!")]),
        dict(decor="meadow", cast=[("mimo", -150, 380, L), ("bunny", 1450, 760, R), ("duck", 1600, 960, R)], lines=[
            ("narrator", "First, Mimo hopped down to the flower meadow."),
            ("bunny", "Hop hop! Hi, Mimo! I'm Pip, the bounciest bunny in the meadow!"),
            ("duck", "Quack quack! And I'm Dot! I'm a little duckling, and I love puddles!"),
            ("mimo", "Goodnight, Pip! Goodnight, Dot! Sleep tight!"),
            ("bunny", "Goodnight, Mimo! Don't forget to visit Mia and Finn!")]),
        dict(decor="forest", cast=[("mimo", -150, 360, L), ("kitten", 1450, 720, R), ("fox", 1600, 960, R)], lines=[
            ("narrator", "Next, Mimo walked into the rainbow forest."),
            ("kitten", "Meow! Hello, Mimo! I'm Mia. Do you like my pink ribbon?"),
            ("mimo", "It's beautiful, Mia!"),
            ("fox", "Hey, Mimo! I'm Finn the fox. I'm building a tower with pinecones!"),
            ("mimo", "Wow, Finn! Goodnight, Mia! Goodnight, Finn!")]),
        dict(decor="night", cast=[("mimo", -150, 330, L), ("lamb", 1450, 640, R), ("owl", 1600, 940, R)], lines=[
            ("narrator", "Last of all, Mimo climbed the lantern hill."),
            ("lamb", "Baa! Hello, Mimo! I'm Wooly. My wool is soft like a cloud."),
            ("owl", "Hoo hoo. And I am Luna, the wise owl. I watch over everyone at night."),
            ("mimo", "Goodnight, Wooly! Goodnight, Luna!"),
            ("owl", "Look up, Mimo. Someone else wants to say goodnight.")]),
        dict(decor="clouds", cast=[("mimo", 420, 420, L), ("star", 900, 900, R)], lines=[
            ("star", "Twinkle, twinkle! Hello, Mimo! I'm Twinkle, the littlest star."),
            ("mimo", "Hello, Twinkle! Will you shine for me while I sleep?"),
            ("star", "I will! But first, will you sing my song with me?"),
            ("mimo", "Yes! Everybody, sing along with us!")]),
    ]),

    dict(id="s1e02", title="Dot's First Swim", song="Row Row Row Your Boat", shots=[
        dict(decor="meadow", cast=[("duck", 640, 640, L)], lines=[
            ("narrator", "Dot the duckling loved puddles. Big puddles, small puddles, muddy puddles."),
            ("duck", "Splash! Splash! Puddles are the best!"),
            ("duck", "But today, my mommy says I can swim in the river. The big, big river!")]),
        dict(decor="river", cast=[("duck", -150, 520, L), ("mimo", 1450, 820, R)], lines=[
            ("narrator", "But when Dot saw the river, she stopped."),
            ("duck", "Oh. The river is so big. What if I sink?"),
            ("mimo", "Hi, Dot! Are you okay? You look a little worried."),
            ("duck", "I want to swim, Mimo. But I'm scared."),
            ("mimo", "It's okay to be scared. Being brave means trying, even a tiny bit.")]),
        dict(decor="river", boat=True, cast=[("mimo", 560, 560, L), ("duck", 730, 730, R)], lines=[
            ("mimo", "I have an idea! Let's go in my little boat first."),
            ("duck", "A boat? Okay! I can see the water from here."),
            ("narrator", "They rowed gently, gently, down the sparkly river."),
            ("duck", "The water looks friendly. And the fish are waving at me!"),
            ("mimo", "Do you want to try? I'll stay right here, next to you.")]),
        dict(decor="river", cast=[("mimo", 420, 420, L), ("duck", 800, 800, R), ("bunny", 1450, 1060, R)], lines=[
            ("narrator", "Dot took a big breath. One, two, three... splash!"),
            ("duck", "I'm floating! I'm swimming! Look at me, Mimo!"),
            ("bunny", "Hop hop! Go, Dot, go! You're a super swimmer!"),
            ("mimo", "You did it, Dot! You were so brave!"),
            ("duck", "Thank you, Mimo! Now let's sing the rowing song, all together!")]),
    ]),

    dict(id="s1e03", title="Mia's Missing Ribbon", song="Mary Had a Little Lamb", shots=[
        dict(decor="forest", cast=[("kitten", 640, 640, L)], lines=[
            ("narrator", "One windy evening, Mia the kitten was playing in the rainbow forest."),
            ("kitten", "Whoosh! The wind is so strong today!"),
            ("kitten", "Oh no! My pink ribbon! It flew away!")]),
        dict(decor="forest", cast=[("kitten", 420, 420, L), ("mimo", 1450, 760, R), ("fox", 1600, 1000, R)], lines=[
            ("mimo", "Mia, why are you sad?"),
            ("kitten", "The wind took my ribbon, Mimo. It's my favorite."),
            ("fox", "Don't worry, Mia. I have a super fox nose. Sniff, sniff!"),
            ("mimo", "Let's look everywhere. Under the leaves, behind the trees!"),
            ("kitten", "Thank you, friends. Let's go!")]),
        dict(decor="meadow", cast=[("mimo", -150, 300, L), ("kitten", -300, 500, L), ("fox", -450, 700, L)], lines=[
            ("narrator", "They searched the whole meadow, from the flowers to the rainbow."),
            ("fox", "Not under the daisies."),
            ("mimo", "Not behind the butterflies."),
            ("kitten", "Maybe it's gone forever."),
            ("fox", "Wait! I can hear someone giggling over there!")]),
        dict(decor="night", cast=[("mimo", 300, 300, L), ("kitten", 500, 500, L), ("lamb", 1450, 860, R)], lines=[
            ("lamb", "Baa! Hello, friends! Look what I found tangled in my wool!"),
            ("kitten", "My ribbon! Wooly, you found it!"),
            ("lamb", "It landed right on my back. Now I look very fancy!"),
            ("kitten", "You can wear it tonight, Wooly. Sharing makes me happy too."),
            ("mimo", "Hooray! Let's sing Wooly's favorite song about a little lamb!")]),
    ]),

    dict(id="s1e04", title="The Bedtime Bell", song="Are You Sleeping (Frère Jacques)", shots=[
        dict(decor="forest", cast=[("owl", 640, 640, L)], lines=[
            ("narrator", "In the rainbow forest lives Luna, the owl who keeps the bedtime bell."),
            ("owl", "Hoo hoo! Every night, I ring the bedtime bell."),
            ("owl", "Ding, dang, dong! It means: time to sleep, everyone!")]),
        dict(decor="night", cast=[("owl", -200, 380, L), ("bunny", 1450, 760, R), ("duck", 1600, 980, R)], lines=[
            ("bunny", "Luna! Luna! Where is Mimo? We wanted to play hide and seek!"),
            ("duck", "We looked everywhere. Even inside the big puddle!"),
            ("owl", "Hoo hoo! I think Mimo is already in bed."),
            ("bunny", "Already? Let's go and see!")]),
        dict(decor="forest", cast=[("owl", -200, 380, L), ("bunny", -380, 620, L), ("duck", -520, 840, L)], lines=[
            ("narrator", "They tiptoed through the forest, past the sleepy mushrooms."),
            ("duck", "Luna, why do owls stay awake at night?"),
            ("owl", "Because someone has to watch over the stars, little one."),
            ("bunny", "Wow! You're a night-time guardian!"),
            ("owl", "Hoo hoo! That's right. Now, shhh. We're almost there.")]),
        dict(decor="bedroom", sleeping=True, cast=[("owl", 1450, 700, R), ("bunny", 1600, 880, R), ("duck", 1750, 1060, R)], lines=[
            ("narrator", "They peeked into Mimo's room. Mimo was snoring softly, hugging his pillow."),
            ("bunny", "Shhh. He's fast asleep."),
            ("owl", "He must be dreaming of honey and stars."),
            ("duck", "Can we sing him a little song? Very, very softly?"),
            ("owl", "Yes. Our bell song. Are you sleeping, Mimo?")]),
    ]),

    dict(id="s1e05", title="Finn Learns to Share", song="London Bridge", shots=[
        dict(decor="meadow", cast=[("fox", 640, 640, L)], lines=[
            ("narrator", "Finn the fox loved to build things. Towers, houses, and bridges."),
            ("fox", "Today, I'm building the biggest bridge ever. All by myself!")]),
        dict(decor="meadow", cast=[("fox", 640, 640, L), ("mimo", 1450, 920, R), ("kitten", -150, 330, L)], lines=[
            ("mimo", "Wow, Finn! Can we help you build it?"),
            ("fox", "No! It's my bridge. I want to do it alone."),
            ("kitten", "Oh. Okay, Finn."),
            ("narrator", "So Finn built and built. But the bridge kept falling down."),
            ("fox", "Oh no! It fell down again! This is too hard.")]),
        dict(decor="meadow", cast=[("fox", 640, 640, L), ("mimo", 920, 920, R), ("kitten", 330, 330, L)], lines=[
            ("mimo", "Finn, building is easier with friends. I can hold the sticks."),
            ("kitten", "And I can find the flat stones!"),
            ("fox", "Really? You still want to help me?"),
            ("mimo", "Of course! That's what friends do."),
            ("fox", "I'm sorry I said no. Let's build it together!")]),
        dict(decor="night", cast=[("fox", 640, 640, L), ("mimo", 900, 900, R), ("kitten", 380, 380, L)], lines=[
            ("narrator", "Together, they built a beautiful bridge, all the way to the lantern hill."),
            ("fox", "Look! It's standing strong! Our bridge!"),
            ("kitten", "Our bridge. I like how that sounds."),
            ("mimo", "Let's sing a bridge song to celebrate!")]),
    ]),

    dict(id="s1e06", title="Mimo and the Lost Star", song="Twinkle Twinkle Little Star", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 860, L)], lines=[
            ("narrator", "One night, as Mimo was getting ready for bed, he counted the stars from his window."),
            ("mimo", "One, two, three, four... Oh no! One little star is missing!"),
            ("mimo", "It's Twinkle! I have to find her. A star can't sleep all alone!")]),
        dict(decor="forest", cast=[("mimo", -150, 420, L), ("owl", 1450, 820, R)], lines=[
            ("mimo", "Luna, have you seen Twinkle? She's not in the sky!"),
            ("owl", "Hoo hoo. I saw a tiny light fall behind the clouds."),
            ("mimo", "Will you help me find her?"),
            ("owl", "Of course. Friends always help each other.")]),
        dict(decor="clouds", cast=[("mimo", -150, 460, L), ("owl", -330, 760, L)], lines=[
            ("narrator", "They climbed up, up, up, to the land of soft clouds."),
            ("owl", "Twinkle! Are you here?"),
            ("mimo", "Not here. Only fluffy clouds and a rainbow."),
            ("owl", "Let's look on the lantern hill.")]),
        dict(decor="night", cast=[("mimo", -150, 470, L), ("owl", -330, 230, L), ("star", 960, 960, R)], lines=[
            ("star", "Here I am! I fell asleep and slipped out of the sky."),
            ("mimo", "We found you! Are you okay, Twinkle?"),
            ("star", "I'm okay. But I'm too sleepy to fly home."),
            ("owl", "A song will give you sparkles, little star."),
            ("mimo", "Yes! Let's sing you back home. One, two, three!")]),
    ]),

    dict(id="s1e07", title="Pip Can't Sleep", song="Mary Had a Little Lamb", shots=[
        dict(decor="bedroom", cast=[("mimo", 420, 420, L), ("bunny", 1450, 820, R)], lines=[
            ("narrator", "It was bedtime, and Mimo was all ready to sleep."),
            ("bunny", "Mimo? Mimo? I can't fall asleep!"),
            ("mimo", "Oh, Pip! Why not?"),
            ("bunny", "My eyes are wide open, and my feet want to hop, hop, hop!"),
            ("mimo", "I know a trick. Let's count sheep together!"),
            ("bunny", "Okay! One sheep, two sheep, three sheep...")]),
        dict(decor="meadow", cast=[("mimo", 330, 330, L), ("bunny", 540, 540, L), ("lamb", 1450, 920, R)], lines=[
            ("narrator", "And then, a real little lamb came hopping by!"),
            ("lamb", "Baa! Hello, friends! I heard someone counting sheep!"),
            ("bunny", "That was me, Wooly! I can't sleep."),
            ("lamb", "Don't worry. When I can't sleep, I hum a gentle song."),
            ("mimo", "Can you teach us, Wooly?"),
            ("lamb", "Yes! It's a song about a little lamb, just like me. Let's sing it softly!")]),
    ]),

    dict(id="s1e08", title="A Picnic on the Clouds", song="Brahms' Lullaby", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "One night, Mimo found a little note on his pillow."),
            ("mimo", "It says: Come to a picnic on the clouds! Love, Twinkle."),
            ("mimo", "A picnic in the sky? Hooray!")]),
        dict(decor="night", cast=[("mimo", -150, 420, L), ("duck", 1450, 820, R)], lines=[
            ("duck", "Quack! Mimo, I got a note too! But how do we get up there?"),
            ("narrator", "Just then, a soft rainbow slid down from the sky, like a slide."),
            ("mimo", "A rainbow slide! Hold my paw, Dot, and let's climb up!"),
            ("duck", "Wheee! This is fun!")]),
        dict(decor="clouds", cast=[("mimo", -150, 380, L), ("duck", -330, 220, L), ("star", 950, 950, R), ("kitten", 1450, 700, R)], lines=[
            ("star", "Welcome to my cloud picnic! I made moon cookies."),
            ("kitten", "Meow! And I brought starberry juice. It sparkles!"),
            ("duck", "Mmm! It tastes like sunshine and sleepy dreams."),
            ("mimo", "Thank you, Twinkle. This is the best picnic ever."),
            ("star", "Now lie down on the soft clouds, and listen. I'll play you a lullaby.")]),
    ]),

    dict(id="s1e09", title="The Lantern Bridge", song="London Bridge", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Mimo had heard about a magic bridge, where lanterns glow every night."),
            ("mimo", "I want to see the lantern bridge before I sleep!")]),
        dict(decor="meadow", cast=[("mimo", -150, 450, L), ("fox", 1450, 820, R)], lines=[
            ("fox", "Hey, Mimo! Where are you going?"),
            ("mimo", "To the lantern bridge! Do you know the way, Finn?"),
            ("fox", "Yes! Follow the river, then turn at the big rainbow."),
            ("mimo", "Let's go together!")]),
        dict(decor="night", cast=[("mimo", -150, 470, L), ("fox", -330, 260, L), ("bunny", 1450, 900, R)], lines=[
            ("narrator", "When the sky turned purple, the lanterns began to glow."),
            ("bunny", "Look, Mimo! Pink, yellow, blue and purple lights!"),
            ("mimo", "It's so pretty! The bridge looks like it's dancing."),
            ("fox", "People say the bridge loves a song. Shall we sing it one?"),
            ("mimo", "Yes! Let's sing the bridge song!")]),
    ]),

    dict(id="s1e10", title="The Great Boat Race", song="Row Row Row Your Boat", shots=[
        dict(decor="river", cast=[("fox", 420, 420, L), ("duck", 820, 820, R)], lines=[
            ("narrator", "Today was a big day on the sparkly river. It was the Great Boat Race!"),
            ("fox", "I'm going to row the fastest! Zoom, zoom!"),
            ("duck", "I'm going to win too! Quack!")]),
        dict(decor="river", boat=True, cast=[("mimo", 560, 560, L), ("bunny", 730, 730, R)], lines=[
            ("bunny", "Mimo, are we going to win?"),
            ("mimo", "Maybe, maybe not. But we'll have fun rowing together!"),
            ("narrator", "Ready, set, go! The boats splashed down the river."),
            ("bunny", "Oh! Look! Finn's boat is stuck on a rock!")]),
        dict(decor="river", cast=[("mimo", 330, 330, L), ("bunny", 520, 520, L), ("fox", 900, 900, R), ("duck", 1100, 1100, R)], lines=[
            ("fox", "Help! My boat won't move!"),
            ("mimo", "Let's stop and help Finn!"),
            ("duck", "I'll help too! Push, push, push!"),
            ("fox", "Thank you, friends! But now nobody will win the race."),
            ("mimo", "That's okay. Helping a friend is better than winning."),
            ("bunny", "Let's all row home together, singing our song!")]),
    ]),

    dict(id="s1e11", title="Luna's Secret Lullaby", song="Brahms' Lullaby", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "It was a windy night, and Mimo could not fall asleep."),
            ("mimo", "The wind is so loud. Whoosh, whoosh!"),
            ("mimo", "Maybe Luna knows a way to help me sleep.")]),
        dict(decor="forest", cast=[("mimo", -150, 470, L), ("kitten", 1450, 820, R)], lines=[
            ("kitten", "Meow! Mimo, you can't sleep either? The wind is too noisy!"),
            ("mimo", "Let's ask Luna. She's the wisest owl in the forest."),
            ("kitten", "Good idea! She always knows what to do.")]),
        dict(decor="night", cast=[("mimo", 360, 360, L), ("kitten", 560, 560, L), ("owl", 1450, 900, R)], lines=[
            ("narrator", "They found Luna on the lantern hill."),
            ("owl", "Hoo hoo. I heard you can't sleep, little ones."),
            ("kitten", "The wind is so loud, Luna."),
            ("owl", "Tonight, I'll share my secret lullaby. It's very old, and very gentle."),
            ("owl", "Close your eyes, and listen to the music."),
            ("mimo", "Goodnight, Luna. Goodnight, everyone.")]),
    ]),

    dict(id="s1e12", title="Goodnight, Everyone!", song="Are You Sleeping (Frère Jacques)", shots=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Tonight is a very special night. Mimo is having a sleepover!"),
            ("mimo", "I made a big pillow fort. And I have honey cookies for everyone!")]),
        dict(decor="bedroom", cast=[("mimo", 640, 640, L), ("bunny", 1450, 860, R), ("duck", 1600, 1060, R), ("kitten", -150, 380, L)], lines=[
            ("bunny", "Hop hop! We're here! I brought my blanket!"),
            ("duck", "Quack! I brought my rubber ducky!"),
            ("kitten", "Meow! And I brought a story book!"),
            ("mimo", "Welcome, friends! Come into the pillow fort!")]),
        dict(decor="bedroom", cast=[("mimo", 640, 640, L), ("kitten", 380, 380, L), ("fox", 1450, 880, R), ("lamb", 1600, 1080, R)], lines=[
            ("fox", "Knock knock! Can Wooly and I join the sleepover?"),
            ("lamb", "Baa! I'm soft, so I can be everyone's pillow!"),
            ("mimo", "Yes! The more friends, the cozier it is."),
            ("narrator", "They shared cookies, read stories, and giggled until their eyes grew heavy.")]),
        dict(decor="bedroom", sleeping=True, cast=[("owl", 1450, 760, R), ("star", 1600, 1000, R)], lines=[
            ("narrator", "Later, Luna and Twinkle peeked in. Everyone was fast asleep."),
            ("star", "Look, Luna. They all fell asleep together."),
            ("owl", "Hoo hoo. Friends make the best dreams."),
            ("star", "Let's sing them our sleepy song, very softly."),
            ("owl", "Are you sleeping, little friends? Goodnight, everyone.")]),
    ]),
]
