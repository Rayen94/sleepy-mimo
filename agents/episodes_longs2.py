"""Saison 1, épisodes 7 à 12 au format long (même structure que episodes_longs.py).
Chaque épisode : 6 chapitres (histoire + chanson), grand final endormi + berceuses, bande-annonce du suivant."""

L, R = 1, -1

# ======================================================================= 7. Pip Can't Sleep
EP7 = dict(id="s1e07", title="Pip Can't Sleep", chapters=[
    dict(label="Wide-Awake Pip", story=[
        dict(decor="bedroom", cast=[("bunny", 640, 640, L)], lines=[
            ("narrator", "In a little burrow under the flower meadow, Pip the bunny was in bed. But Pip was not sleeping."),
            ("bunny", "Hop hop! My eyes are wide open! My feet want to bounce, bounce, bounce!"),
            ("bunny", "I tried closing my eyes. One, two, three... Nope! Still awake!")]),
        dict(decor="bedroom", cast=[("bunny", 860, 860, L), ("mimo", -150, 400, L)], lines=[
            ("mimo", "Pip? I saw your light on from my window. Are you okay?"),
            ("bunny", "Mimo! I can't sleep! Everybody else is sleeping, and I'm the only one awake!"),
            ("mimo", "Don't worry. Let's find a way, together. We can start with a sleepy song."),
            ("bunny", "Okay! But a quiet one, please!")]),
    ], song=dict(name="Are You Sleeping (Frère Jacques)", decor="bedroom", cast=[("mimo", 480, L), ("bunny", 820, R)], voice="box", transpose=0)),

    dict(label="Counting Sheep", story=[
        dict(decor="meadow", cast=[("mimo", -150, 330, L), ("bunny", -330, 140, L), ("lamb", 1450, 820, R)], lines=[
            ("narrator", "Mimo and Pip tiptoed out to the meadow, where the moon was shining on the soft grass."),
            ("lamb", "Baa! Hello, friends. Why are you up so late?"),
            ("bunny", "Wooly! I can't fall asleep. Mimo says maybe counting sheep will help."),
            ("lamb", "Baa! I'm a sheep! I can help! Close your eyes, Pip, and I'll hop over the little gate."),
            ("lamb", "One little lamb... two little lambs... three little lambs..."),
            ("bunny", "Four... five... Wait! I'm too excited. I keep wanting to count faster!")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="meadow", cast=[("bunny", 330, L), ("mimo", 600, L), ("lamb", 900, R)], voice="bell", transpose=0)),

    dict(label="Too Many Hops", story=[
        dict(decor="forest", cast=[("mimo", -150, 300, L), ("bunny", -330, 120, L), ("lamb", -500, 520, L), ("owl", 1450, 880, R)], lines=[
            ("owl", "Hoo hoo. I heard some very busy hops in my forest. Is somebody not sleepy?"),
            ("bunny", "Luna! Counting sheep didn't work. My feet won't stop hopping!"),
            ("owl", "Ah. Tired bodies need quiet bodies. Hopping tells your body it's time to play, not time to sleep."),
            ("owl", "Here is a trick. Breathe in slowly, like smelling a flower. Then breathe out slowly, like blowing out a candle."),
            ("bunny", "In... like a flower. Out... like a candle. Hmm. That feels nice."),
            ("mimo", "Let's all do it together. In, like a flower. Out, like a candle.")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="forest", cast=[("bunny", 260, L), ("lamb", 500, L), ("mimo", 740, R), ("owl", 980, R)], voice="harp", transpose=-2)),

    dict(label="Quiet as the River", story=[
        dict(decor="river", cast=[("mimo", -150, 330, L), ("bunny", -330, 140, L), ("fish", 1450, 920, R)], lines=[
            ("fish", "Blub, blub. Good evening, friends. Shh, listen to the river."),
            ("bunny", "It's so quiet. It just goes... shhhh."),
            ("fish", "The river never rushes at night. It flows slowly, slowly, all the way to the sea."),
            ("fish", "Pretend you are a little boat on the water, Pip. Rocking left... and right... and left..."),
            ("bunny", "Left... and right... I feel a little bit heavy, like a pebble. A sleepy pebble."),
            ("mimo", "That's it, Pip. Let's rock gently, all the way home.")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("bunny", 730, R)], voice="soft", transpose=-2)),

    dict(label="A Great Big Yawn", story=[
        dict(decor="night", cast=[("bunny", 640, 640, L), ("mimo", 380, 380, L), ("lamb", 900, 900, R), ("owl", 1130, 1130, R)], lines=[
            ("narrator", "Back on the lantern hill, something happened to Pip. Something very big, and very sleepy."),
            ("bunny", "Haaaaaa... aaaaah... Oh! Was that a yawn?"),
            ("mimo", "That was the biggest yawn I ever saw!"),
            ("lamb", "Baa... and now I'm yawning too. Haaaah."),
            ("owl", "Hoo hoo. Yawns are contagious. And so is sleepiness."),
            ("bunny", "My feet are quiet. My eyes are heavy. I think... I think I'm ready for bed.")]),
    ], song=dict(name="Are You Sleeping (Frère Jacques)", decor="night", cast=[("mimo", 340, L), ("bunny", 600, L), ("lamb", 860, R), ("owl", 1100, R)], voice="box", transpose=-2)),

    dict(label="Sweet Dreams, Pip", story=[
        dict(decor="bedroom", cast=[("bunny", 700, 700, L), ("mimo", 420, 420, L)], lines=[
            ("narrator", "Mimo walked Pip home, and tucked him into his cozy bed."),
            ("bunny", "Mimo? Thank you for helping me. Tomorrow I'll hop all day. But tonight... I'll rest."),
            ("mimo", "Goodnight, Pip. Even the bounciest bunny needs a good sleep."),
            ("narrator", "And Pip closed his eyes, and dreamed of fields of clover, soft as a cloud.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("lamb", 230, L), ("owl", 440, L), ("bunny", 650, L), ("mimo", 860, R), ("kitten", 1070, R)], minutes=12),
   teaser=dict(decor="clouds", cast=[("mimo", 540, 640, L), ("duck", 900, 900, R)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("duck", "Quack! Mimo, look! Someone left a picnic basket on a cloud!"),
       ("mimo", "A picnic, up in the sky? Let's go!"),
       ("narrator", "Find out in the next episode: A Picnic on the Clouds!")]))

# ======================================================================= 8. A Picnic on the Clouds
EP8 = dict(id="s1e08", title="A Picnic on the Clouds", chapters=[
    dict(label="The Invitation", story=[
        dict(decor="meadow", cast=[("mimo", 640, 640, L), ("duck", 1450, 900, R)], lines=[
            ("narrator", "One sunny evening, Mimo was setting up a little picnic in the meadow."),
            ("duck", "Quack quack! Mimo! Mimo! Luna sent a message! It says, picnic on the clouds, tonight, at sunset!"),
            ("mimo", "On the clouds? That sounds amazing! Dot, will you come?"),
            ("duck", "I... um... the clouds are so high up. I'm not sure."),
            ("mimo", "We'll go together. Let's invite our friends!")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="meadow", cast=[("mimo", 560, L), ("duck", 860, R)], voice="bell", transpose=2)),

    dict(label="Packing the Basket", story=[
        dict(decor="meadow", cast=[("mimo", 560, 560, L), ("duck", 820, 820, R), ("kitten", -150, 330, L), ("bunny", 1450, 1040, R)], lines=[
            ("kitten", "Meow! I baked honey biscuits for the picnic!"),
            ("bunny", "Hop hop! I brought carrot sticks and a big blanket!"),
            ("duck", "And I brought... uh... a little sandwich. For the ground. I mean, for the cloud."),
            ("mimo", "Dot, are you a little nervous about going up high?"),
            ("duck", "A little. My feet like water, not sky. What if I look down and feel wobbly?"),
            ("kitten", "Then we'll hold your wing, and take it slowly.")]),
    ], song=dict(name="London Bridge", decor="meadow", cast=[("bunny", 240, L), ("kitten", 450, L), ("mimo", 660, R), ("duck", 880, R)], voice="soft", transpose=0)),

    dict(label="Up the Rainbow", story=[
        dict(decor="clouds", cast=[("mimo", -150, 330, L), ("kitten", -330, 140, L), ("bunny", -500, 520, L), ("duck", 640, 640, L)], lines=[
            ("narrator", "The friends climbed up the rainbow, one colorful step at a time."),
            ("duck", "Quack... Don't look down, Dot. Don't look down."),
            ("mimo", "You can look at me, Dot. I'm right here."),
            ("bunny", "Boing! The clouds are bouncy, Dot! Try one little bounce!"),
            ("duck", "Just one? Okay. Quack... boing! Oh! It's like a soft pillow!")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="clouds", cast=[("bunny", 260, L), ("kitten", 480, L), ("mimo", 700, R), ("duck", 920, R)], voice="harp", transpose=2)),

    dict(label="The Picnic in the Sky", story=[
        dict(decor="clouds", cast=[("mimo", 320, 320, L), ("kitten", 540, 540, L), ("bunny", 760, 760, R), ("duck", 980, 980, R), ("owl", 1450, 640, R)], lines=[
            ("owl", "Hoo hoo. Welcome to the highest picnic in the land!"),
            ("kitten", "Look, the sun is melting into orange and pink!"),
            ("duck", "It's so beautiful. I'm not scared anymore. I'm having fun!"),
            ("mimo", "You were very brave, Dot."),
            ("duck", "I was scared, but I did it anyway. And my friends helped me."),
            ("owl", "That is what bravery really is, little duck. Being scared, and trying anyway.")]),
    ], song=dict(name="Row Row Row Your Boat", decor="clouds", cast=[("kitten", 260, L), ("mimo", 480, L), ("duck", 700, R), ("owl", 920, R)], voice="bell", transpose=0)),

    dict(label="Stars Come Out", story=[
        dict(decor="night", cast=[("mimo", 330, 330, L), ("duck", 560, 560, L), ("bunny", 790, 790, R), ("star", 1450, 980, R)], lines=[
            ("narrator", "When the sun went down, the first star blinked awake."),
            ("star", "Twinkle, twinkle! Hello, picnic friends! What a cozy cloud!"),
            ("duck", "Twinkle! Look how close the stars are from up here!"),
            ("star", "Want to hear a secret, Dot? I was scared of falling my first night in the sky too."),
            ("duck", "You were? And what did you do?"),
            ("star", "I held on to my friends' light. And now I love it up here.")]),
    ], song=dict(name="Are You Sleeping (Frère Jacques)", decor="night", cast=[("mimo", 330, L), ("duck", 560, L), ("bunny", 790, R), ("star", 1000, R)], voice="box", transpose=-2)),

    dict(label="Sleepy on a Cloud", story=[
        dict(decor="clouds", cast=[("mimo", 520, 520, L), ("duck", 760, 760, L)], lines=[
            ("duck", "Mimo? Thank you for staying close to me."),
            ("mimo", "Always, Dot. That's what friends are for."),
            ("narrator", "The clouds were soft. The stars were bright. And one by one, the picnic friends began to yawn."),
            ("mimo", "Goodnight, Dot. Goodnight, sky. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("kitten", 230, L), ("bunny", 440, L), ("duck", 650, L), ("mimo", 860, R), ("owl", 1070, R)], minutes=12),
   teaser=dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("mimo", "Tonight, I heard about a bridge where hundreds of lanterns glow. The Lantern Bridge!"),
       ("narrator", "But what happens when one little lantern won't light up?"),
       ("narrator", "Find out in the next episode: The Lantern Bridge!")]))

# ======================================================================= 9. The Lantern Bridge
EP9 = dict(id="s1e09", title="The Lantern Bridge", chapters=[
    dict(label="A Bridge of Lights", story=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Mimo had heard of a magic bridge, where lanterns glow every night."),
            ("mimo", "Pink lanterns, yellow lanterns, blue lanterns... I want to see the lantern bridge before I sleep!")]),
        dict(decor="meadow", cast=[("mimo", -150, 450, L), ("fox", 1450, 820, R)], lines=[
            ("fox", "Hey, Mimo! Where are you going so late?"),
            ("mimo", "To the lantern bridge! Do you know the way, Finn?"),
            ("fox", "I do! I helped build the bridge. Follow the river, then turn at the big rainbow."),
            ("mimo", "Let's go together!")]),
    ], song=dict(name="London Bridge", decor="meadow", cast=[("mimo", 480, L), ("fox", 820, R)], voice="soft", transpose=2)),

    dict(label="Lighting the Lanterns", story=[
        dict(decor="night", cast=[("mimo", -150, 330, L), ("fox", -330, 140, L), ("bunny", 1450, 900, R), ("kitten", 1600, 1100, R)], lines=[
            ("narrator", "When the sky turned purple, the friends arrived at the bridge. It was waiting in the dark."),
            ("bunny", "Hop hop! We came early to help! Every night, somebody has to light the lanterns."),
            ("kitten", "Meow! Each friend lights one. Mimo, would you like to try?"),
            ("mimo", "Yes, please! Pink one first!"),
            ("narrator", "One by one, the lanterns began to glow. Pink, yellow, blue, purple. The bridge looked like a rainbow made of stars."),
            ("fox", "It's beautiful. It's even better than when we built it!")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="night", cast=[("fox", 300, L), ("mimo", 520, L), ("bunny", 740, R), ("kitten", 960, R)], voice="bell", transpose=0)),

    dict(label="The Little Lantern", story=[
        dict(decor="night", cast=[("mimo", 330, 330, L), ("kitten", 560, 560, L), ("bunny", 790, 790, R), ("fox", 1020, 1020, R)], lines=[
            ("kitten", "Oh! Look at this one. This little lantern isn't glowing."),
            ("bunny", "I tried my best! I lit it three times, and the light just goes poof."),
            ("fox", "Maybe it's broken. Bridges can have little problems, you know."),
            ("mimo", "Hello, little lantern. Are you sleepy?"),
            ("narrator", "The little lantern gave a tiny sigh, and a very small, wobbly voice came out of it."),
            ("mimo", "Did you hear that? I think the lantern is feeling shy.")]),
    ], song=dict(name="Are You Sleeping (Frère Jacques)", decor="night", cast=[("kitten", 330, L), ("mimo", 560, L), ("bunny", 790, R), ("fox", 1020, R)], voice="box", transpose=0)),

    dict(label="Luna Knows", story=[
        dict(decor="night", cast=[("mimo", 330, 330, L), ("kitten", 540, 540, L), ("fox", 1000, 1000, R), ("owl", 1450, 760, R)], lines=[
            ("owl", "Hoo hoo. What is the matter, little ones?"),
            ("mimo", "Luna! One lantern won't glow. We think it's feeling shy."),
            ("owl", "Ah. A lantern doesn't glow because it's pushed. It glows when it feels safe."),
            ("kitten", "How do we make it feel safe?"),
            ("owl", "Do not rush it. Sit beside it. Tell it that its light is welcome, just the way it is."),
            ("fox", "No pushing. Just sitting nearby. I can do that!")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="night", cast=[("kitten", 300, L), ("mimo", 520, L), ("fox", 740, R), ("owl", 960, R)], voice="harp", transpose=-2)),

    dict(label="Everyone Glows Differently", story=[
        dict(decor="night", cast=[("mimo", 330, 330, L), ("kitten", 540, 540, L), ("bunny", 750, 750, R), ("fox", 960, 960, R)], lines=[
            ("narrator", "So the friends sat down next to the little lantern. And nobody said a word, for a long, quiet moment."),
            ("mimo", "Little lantern, our lights are all different, too. Some are big, some are small."),
            ("bunny", "Mine goes zig-zag. I bounce a lot."),
            ("kitten", "Mine is a soft purr. Sometimes I'm loud, sometimes I'm quiet."),
            ("fox", "And mine is... a very busy light. With lots of plans!"),
            ("narrator", "And then, very slowly, the little lantern began to shine. A small, warm, golden glow.")]),
    ], song=dict(name="London Bridge", decor="night", cast=[("bunny", 220, L), ("kitten", 440, L), ("mimo", 660, L), ("fox", 880, R)], voice="bell", transpose=2)),

    dict(label="Goodnight, Lanterns", story=[
        dict(decor="night", cast=[("mimo", 520, 520, L), ("fox", 780, 780, R)], lines=[
            ("fox", "Look, Mimo. The whole bridge is glowing now. Even the little lantern."),
            ("mimo", "It's the most beautiful bridge in the world, because every light is here."),
            ("narrator", "And on the lantern bridge, under a sky full of stars, the friends curled up for a good, long sleep."),
            ("mimo", "Goodnight, little lantern. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("bunny", 230, L), ("kitten", 440, L), ("mimo", 650, L), ("fox", 860, R), ("owl", 1070, R)], minutes=12),
   teaser=dict(decor="river", cast=[("fox", 420, 420, L), ("duck", 820, 820, R)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("fox", "I'm going to row the fastest! Zoom, zoom!"),
       ("duck", "Quack! No way! I'm going to win!"),
       ("narrator", "Who will win the Great Boat Race? Find out in the next episode: The Great Boat Race!")]))

# ======================================================================= 10. The Great Boat Race
EP10 = dict(id="s1e10", title="The Great Boat Race", chapters=[
    dict(label="Ready to Row", story=[
        dict(decor="river", cast=[("fox", 420, 420, L), ("duck", 820, 820, R)], lines=[
            ("narrator", "Today was a big day on the sparkly river. It was the Great Boat Race!"),
            ("fox", "I'm going to row the fastest! Zoom, zoom!"),
            ("duck", "I'm going to win too! Quack! My boat has a flag on it!")]),
        dict(decor="river", cast=[("mimo", -150, 330, L), ("bunny", -330, 140, L), ("fox", 780, 780, R), ("duck", 1010, 1010, R)], lines=[
            ("mimo", "Hello, racers! Can Pip and I race too?"),
            ("bunny", "Hop hop! I never raced a boat before. Will it be hard?"),
            ("fox", "Just row, row, row! Winner gets the golden paddle!"),
            ("mimo", "Whatever happens, let's have fun, and sing our rowing song.")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("bunny", 730, R)], voice="harp", transpose=2)),

    dict(label="On Your Marks", story=[
        dict(decor="river", cast=[("owl", 640, 640, L), ("fox", 330, 330, L), ("duck", 960, 960, R), ("mimo", 1130, 1130, R)], lines=[
            ("owl", "Hoo hoo. I am the judge of the Great Boat Race. The rules are simple."),
            ("owl", "Go down the river, turn at the big rock, and come back to the bridge. Row kindly, and have fun."),
            ("fox", "Ready? Set?"),
            ("duck", "Quack! Go!")]),
    ], song=dict(name="London Bridge", decor="river", boat=True, cast=[("fox", 560, L), ("duck", 730, R)], voice="bell", transpose=2)),

    dict(label="Splish, Splash!", story=[
        dict(decor="river", cast=[("mimo", 330, 330, L), ("bunny", 520, 520, L), ("fox", 900, 900, R)], lines=[
            ("narrator", "The boats splashed down the river. Whoosh! Splash! Zoom!"),
            ("bunny", "Mimo, are we going to win?"),
            ("mimo", "Maybe, maybe not. But we're rowing together, and that's wonderful!"),
            ("fox", "I'm in front! I'm winning! Look at me! Zoom, zoom!"),
            ("narrator", "But the river grew narrow, and Finn was rowing so fast that he did not see the big rock.")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="river", cast=[("mimo", 330, L), ("bunny", 560, L), ("fox", 880, R)], voice="box", transpose=0)),

    dict(label="Stuck!", story=[
        dict(decor="river", cast=[("fox", 560, 560, L), ("duck", 960, 960, R), ("mimo", -150, 780, L)], lines=[
            ("narrator", "Bump! Finn's boat stopped, right on top of the rock."),
            ("fox", "Help! My boat won't move! I'm stuck!"),
            ("duck", "Quack! Finn! Oh no. But if I stop, I'll lose the race."),
            ("mimo", "Dot, Finn needs us. A race is only a game. A friend is a friend!"),
            ("duck", "You're right. Quack! I'm coming!")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("duck", 730, R)], voice="soft", transpose=0)),

    dict(label="Push, Push, Push!", story=[
        dict(decor="river", cast=[("mimo", 330, 330, L), ("bunny", 520, 520, L), ("fox", 900, 900, R), ("duck", 1100, 1100, R)], lines=[
            ("fox", "Thank you for stopping! But now nobody will win the race."),
            ("mimo", "That's okay. Helping a friend is better than winning."),
            ("duck", "Push, push, push! One, two, three!"),
            ("bunny", "Hop hop! It's moving! Finn's boat is free!"),
            ("fox", "I'm sorry I rowed so fast, and didn't look. I only wanted to win."),
            ("mimo", "It's okay, Finn. Let's all row home together, singing our song!")]),
    ], song=dict(name="Row Row Row Your Boat", decor="river", boat=True, cast=[("mimo", 560, L), ("fox", 730, R)], voice="harp", transpose=2)),

    dict(label="The Golden Paddle", story=[
        dict(decor="night", cast=[("owl", 640, 640, L), ("mimo", 330, 330, L), ("fox", 960, 960, R), ("duck", 1130, 1130, R)], lines=[
            ("owl", "Hoo hoo. I have watched every boat today. And I have decided who gets the golden paddle."),
            ("fox", "Whoever came first, right?"),
            ("owl", "No one came first. The golden paddle goes to all of you, for the kindest race on the river."),
            ("duck", "We all win! Quack quack!"),
            ("mimo", "And now, goodnight, racers. Goodnight, river. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("duck", 230, L), ("fox", 440, L), ("mimo", 650, L), ("bunny", 860, R), ("owl", 1070, R)], minutes=12),
   teaser=dict(decor="bedroom", cast=[("mimo", 640, 640, L), ("kitten", -150, 400, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("kitten", "Meow! Mimo, the wind is so loud tonight. I can't sleep!"),
       ("mimo", "Maybe Luna knows a secret that can help us."),
       ("narrator", "Find out in the next episode: Luna's Secret Lullaby!")]))

# ======================================================================= 11. Luna's Secret Lullaby
EP11 = dict(id="s1e11", title="Luna's Secret Lullaby", chapters=[
    dict(label="The Windy Night", story=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "It was a windy night, and Mimo could not fall asleep."),
            ("mimo", "The wind is so loud tonight. Whoosh, whoosh, whoosh!"),
            ("mimo", "Maybe my friends are awake too. Let's see.")]),
        dict(decor="forest", cast=[("mimo", -150, 470, L), ("kitten", 1450, 820, R)], lines=[
            ("kitten", "Meow! Mimo, you can't sleep either? The wind is too noisy!"),
            ("mimo", "Let's ask Luna. She's the wisest owl in the forest."),
            ("kitten", "Good idea! She always knows what to do.")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="forest", cast=[("mimo", 480, L), ("kitten", 820, R)], voice="box", transpose=0)),

    dict(label="Friends Gather", story=[
        dict(decor="forest", cast=[("mimo", 330, 330, L), ("kitten", 540, 540, L), ("bunny", 1450, 780, R), ("lamb", 1600, 1000, R)], lines=[
            ("bunny", "Hop hop! Mimo! Mia! Is the wind keeping you awake too?"),
            ("lamb", "Baa! The wind blew my blanket away! It went whoosh!"),
            ("mimo", "We're all going to see Luna. Come with us!"),
            ("bunny", "Yes! The more friends, the less scary the wind is."),
            ("kitten", "Let's walk together, and sing a little song to keep our paws brave.")]),
    ], song=dict(name="London Bridge", decor="forest", cast=[("kitten", 260, L), ("mimo", 480, L), ("bunny", 700, R), ("lamb", 920, R)], voice="soft", transpose=0)),

    dict(label="Luna's Secret", story=[
        dict(decor="night", cast=[("mimo", 360, 360, L), ("kitten", 560, 560, L), ("bunny", 760, 760, L), ("owl", 1450, 960, R)], lines=[
            ("narrator", "They found Luna at the very top of the lantern hill."),
            ("owl", "Hoo hoo. I heard you can't sleep, little ones."),
            ("kitten", "The wind is so loud, Luna."),
            ("owl", "Listen carefully. The wind is not angry. It is only a big, sleepy sigh from the sky."),
            ("mimo", "A sigh? Like when we say aaaah, at the end of a long day?"),
            ("owl", "Exactly. Tonight, I'll share my secret lullaby. It's very old, and very gentle.")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="night", cast=[("mimo", 330, L), ("kitten", 560, L), ("bunny", 790, R), ("owl", 1020, R)], voice="harp", transpose=-2)),

    dict(label="Learning the Lullaby", story=[
        dict(decor="night", cast=[("owl", 640, 640, L), ("mimo", 330, 330, L), ("kitten", 880, 880, R), ("lamb", 1100, 1100, R)], lines=[
            ("owl", "A lullaby has three secrets. First, sing it very slowly."),
            ("owl", "Second, sing it very softly, like a whisper."),
            ("owl", "Third, sing it for someone you love. Even if that someone is yourself."),
            ("lamb", "Baa. Slowly, softly, with love. I can do that."),
            ("kitten", "Do we sing it all together, Luna?"),
            ("owl", "Yes. Close your eyes, and listen to the music first.")]),
    ], song=dict(name="Brahms' Lullaby", decor="night", cast=[("mimo", 330, L), ("kitten", 540, L), ("owl", 750, R), ("lamb", 960, R)], voice="soft", transpose=0)),

    dict(label="The Wind Sings Too", story=[
        dict(decor="night", cast=[("mimo", 330, 330, L), ("kitten", 540, 540, L), ("bunny", 750, 750, R), ("lamb", 960, 960, R)], lines=[
            ("narrator", "And as the friends hummed the lullaby, a funny thing happened. The wind grew softer."),
            ("bunny", "Listen! The wind is humming along with us."),
            ("kitten", "It's not whoosh, whoosh anymore. It's more like shhh, shhh."),
            ("lamb", "Baa... Now it sounds like a blanket."),
            ("mimo", "Luna was right. The wind was only singing a lullaby too.")]),
    ], song=dict(name="Are You Sleeping (Frère Jacques)", decor="night", cast=[("kitten", 300, L), ("mimo", 520, L), ("bunny", 740, R), ("lamb", 960, R)], voice="bell", transpose=-2)),

    dict(label="Goodnight, Wind", story=[
        dict(decor="night", cast=[("mimo", 520, 520, L), ("owl", 780, 780, R)], lines=[
            ("mimo", "Thank you, Luna. I'm so sleepy now, and the wind feels like a hug."),
            ("owl", "Hoo hoo. Sleep well, Mimo. The sky is watching over all of you."),
            ("narrator", "And on the lantern hill, under a quiet wind and a sky of stars, all the friends fell fast asleep."),
            ("mimo", "Goodnight, Luna. Goodnight, wind. Goodnight, everyone.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("lamb", 230, L), ("kitten", 440, L), ("mimo", 650, L), ("bunny", 860, R), ("owl", 1070, R)], minutes=12),
   teaser=dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
       ("narrator", "Next time, on Sleepy Mimo..."),
       ("mimo", "I made a big pillow fort, and I have honey cookies for everyone!"),
       ("narrator", "It's a very special night. It's the season finale, and Mimo is having a sleepover!"),
       ("narrator", "Find out in the next episode: Goodnight, Everyone!")]))

# ======================================================================= 12. Goodnight, Everyone!
EP12 = dict(id="s1e12", title="Goodnight, Everyone!", chapters=[
    dict(label="The Pillow Fort", story=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
            ("narrator", "Tonight is a very special night. Mimo is having a sleepover!"),
            ("mimo", "I made a big pillow fort. And I have honey cookies for everyone!"),
            ("mimo", "I hope my friends like it. I'll sing a little song while I wait.")]),
    ], song=dict(name="Twinkle Twinkle Little Star", decor="bedroom", cast=[("mimo", 640, L)], voice="box", transpose=0)),

    dict(label="Friends Arrive", story=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L), ("bunny", 1450, 860, R), ("duck", 1600, 1060, R), ("kitten", -150, 380, L)], lines=[
            ("bunny", "Hop hop! We're here! I brought my blanket!"),
            ("duck", "Quack! I brought my rubber ducky!"),
            ("kitten", "Meow! And I brought a story book!"),
            ("mimo", "Welcome, friends! Come into the pillow fort!")]),
    ], song=dict(name="London Bridge", decor="bedroom", cast=[("kitten", 300, L), ("mimo", 520, L), ("bunny", 740, R), ("duck", 960, R)], voice="soft", transpose=0)),

    dict(label="More Friends!", story=[
        dict(decor="bedroom", cast=[("mimo", 640, 640, L), ("kitten", 380, 380, L), ("fox", 1450, 880, R), ("lamb", 1600, 1080, R)], lines=[
            ("fox", "Knock knock! Can Wooly and I join the sleepover?"),
            ("lamb", "Baa! I'm soft, so I can be everyone's pillow!"),
            ("mimo", "Yes! The more friends, the cozier it is."),
            ("kitten", "Meow! There's room for everybody.")]),
    ], song=dict(name="Mary Had a Little Lamb", decor="bedroom", cast=[("kitten", 260, L), ("mimo", 480, L), ("fox", 700, R), ("lamb", 920, R)], voice="bell", transpose=2)),

    dict(label="Cookies and Stories", story=[
        dict(decor="bedroom", cast=[("mimo", 330, 330, L), ("kitten", 540, 540, L), ("fox", 750, 750, R), ("bunny", 960, 960, R)], lines=[
            ("narrator", "They shared honey cookies, and read stories, and giggled until their eyes grew heavy."),
            ("kitten", "My story is about a little bear who loves the stars."),
            ("fox", "Is the little bear Mimo?"),
            ("mimo", "Maybe! And in my story, the little bear has the best friends in the whole world."),
            ("bunny", "Aww. Hop hop. That's us.")]),
    ], song=dict(name="Row Row Row Your Boat", decor="bedroom", cast=[("kitten", 260, L), ("mimo", 480, L), ("fox", 700, R), ("bunny", 920, R)], voice="harp", transpose=0)),

    dict(label="Luna and Twinkle Visit", story=[
        dict(decor="bedroom", cast=[("mimo", 330, 330, L), ("duck", 560, 560, L), ("owl", 1450, 760, R), ("star", 1600, 1000, R)], lines=[
            ("owl", "Hoo hoo. We heard happy giggles from the whole forest."),
            ("star", "Twinkle, twinkle! A sleepover! Can we say goodnight to everyone?"),
            ("duck", "Quack! Yes! We love you, Luna and Twinkle!"),
            ("mimo", "Thank you for watching over us every night. You are our best friends too."),
            ("owl", "Then let's sing them our sleepy song, very softly.")]),
    ], song=dict(name="Are You Sleeping (Frère Jacques)", decor="bedroom", cast=[("mimo", 330, L), ("duck", 560, L), ("owl", 790, R), ("star", 1000, R)], voice="box", transpose=-2)),

    dict(label="Goodnight, Everyone", story=[
        dict(decor="bedroom", sleeping=True, cast=[("owl", 1450, 760, R), ("star", 1600, 1000, R)], lines=[
            ("narrator", "Later, Luna and Twinkle peeked in. Everyone was fast asleep."),
            ("star", "Look, Luna. They all fell asleep together."),
            ("owl", "Hoo hoo. Friends make the best dreams."),
            ("star", "Goodnight, Mimo. Goodnight, everyone."),
            ("owl", "Goodnight, little friends. Sleep tight.")]),
    ], song=None),
], finale=dict(decor="night", cast=[("duck", 150, L), ("fox", 330, L), ("kitten", 510, L), ("mimo", 690, R), ("bunny", 870, R), ("lamb", 1040, R)], minutes=14),
   teaser=dict(decor="bedroom", cast=[("mimo", 640, 640, L)], lines=[
       ("narrator", "That was the end of Season 1 of Sleepy Mimo."),
       ("mimo", "Thank you for sleeping, singing and dreaming with us. We'll see you soon for more adventures!"),
       ("narrator", "Goodnight, everyone.")]))
