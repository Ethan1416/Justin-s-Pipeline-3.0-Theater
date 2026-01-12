"""
Romeo and Juliet Content Database
==================================

HARDCODED educational content for each day of the 6-week unit.
Each day includes:
- Slide bullet points (condensed, paraphrased for student note-taking)
- Presenter notes (verbatim monologue script for teacher delivery)
- Discussion questions
- Key quotes from the text
"""

# =============================================================================
# DAY-BY-DAY CONTENT DATABASE
# =============================================================================

RJ_CONTENT_DATABASE = {
    # =========================================================================
    # WEEK 1: INTRODUCTION & ACT 1
    # =========================================================================
    1: {
        "topic": "Meet the Bard: Shakespeare's World",
        "slides": [
            {
                "title": "Who Was Shakespeare?",
                "bullets": [
                    "Born 1564 in Stratford-upon-Avon, England",
                    "Wrote 37 plays and 154 sonnets",
                    "Actor, playwright, and part-owner of Globe Theatre",
                    "Died 1616 at age 52"
                ],
                "notes": """Let's start by meeting the man behind the play. William Shakespeare was born in 1564 in a small town called Stratford-upon-Avon in England. [PAUSE] That's about 460 years ago!

He wrote an incredible 37 plays and 154 sonnets during his lifetime. [EMPHASIS: 37 plays] Think about that - 37 complete plays, each with complex characters, plots, and poetry.

Shakespeare wasn't just a writer - he was also an actor who performed in his own plays, and he was a part-owner of the famous Globe Theatre in London. This was like being a movie star, screenwriter, and studio executive all at once!

He died in 1616 at age 52. [CHECK FOR UNDERSTANDING] Can someone calculate how old Shakespeare would be today if he were still alive?"""
            },
            {
                "title": "The Elizabethan Theater",
                "bullets": [
                    "Open-air theaters like the Globe held 3,000 people",
                    "No women actors - boys played female roles",
                    "Performances during daylight only (no electricity)",
                    "Audience could stand in the 'pit' for one penny"
                ],
                "notes": """Now let's talk about WHERE Shakespeare's plays were performed. The theaters of Shakespeare's time were very different from today.

The Globe Theatre was open-air - no roof over most of it! [PAUSE] Imagine watching a play while it's raining. It held about 3,000 people, which is like fitting our entire school into one theater.

Here's something that might surprise you: there were no women actors. [EMPHASIS: no women] Young boys with high voices played all the female roles, including Juliet! Think about how that would change the play.

Performances could only happen during the day because there was no electricity for lights. And if you only had one penny, you could stand in the 'pit' right in front of the stage. These audience members were called 'groundlings.'

[CHECK FOR UNDERSTANDING] Why do you think they had no women actors? What were society's attitudes about women performing in public?"""
            },
            {
                "title": "Why Romeo and Juliet?",
                "bullets": [
                    "Written around 1594-1596",
                    "Based on an Italian story, not original to Shakespeare",
                    "Most famous love story in Western literature",
                    "Explores themes still relevant today: love, hate, family, fate"
                ],
                "notes": """So why are we studying Romeo and Juliet specifically?

Shakespeare wrote this play around 1594 to 1596 - that's over 400 years ago. [PAUSE] But here's an interesting fact: he didn't invent this story. It was based on an Italian tale that had been around for decades before Shakespeare adapted it.

What Shakespeare did was take this existing story and transform it into poetry. He gave us the most famous love story in all of Western literature. [EMPHASIS: most famous love story]

The reason this play has lasted for 400 years is that it deals with themes that are still relevant today. Love. Hate. Family expectations. The question of fate versus free will.

[CHECK FOR UNDERSTANDING] Think about this: Have you ever felt torn between what your family wants and what you want? That's exactly what Romeo and Juliet face."""
            },
            {
                "title": "Understanding Shakespeare's Language",
                "bullets": [
                    "Early Modern English - similar but not identical to ours",
                    "Common differences: 'thee/thou' = you, 'hath' = has",
                    "Inverted word order: 'What light through yonder window breaks'",
                    "Strategy: Read aloud, look for context clues"
                ],
                "notes": """Before we dive into the play, let's prepare for Shakespeare's language. [PAUSE] I won't lie to you - it can be challenging at first. But here's the good news: it's still English!

Shakespeare wrote in what we call Early Modern English. It's similar to what we speak today, but with some differences.

You'll see words like 'thee' and 'thou' - these just mean 'you.' 'Hath' means 'has.' 'Doth' means 'does.' Once you learn these substitutions, it gets much easier.

Shakespeare also inverts word order for poetic effect. Instead of saying 'What light breaks through that window over there,' he writes 'What light through yonder window breaks.' [EMPHASIS: inverted word order] The meaning is the same, just rearranged.

My best strategies for you: First, read it aloud. Shakespeare wrote for actors, not silent readers. Second, use context clues. Even if you don't understand every word, you can usually figure out what's happening.

[CHECK FOR UNDERSTANDING] Let's practice. What do you think 'Wherefore art thou Romeo?' means? It doesn't mean 'Where are you?' - 'wherefore' means 'why.'"""
            }
        ],
        "key_quotes": [
            "All the world's a stage, and all the men and women merely players.",
            "What's in a name? That which we call a rose by any other name would smell as sweet."
        ],
        "discussion_questions": [
            "Why do you think Shakespeare's plays are still performed 400 years later?",
            "How might watching a play in Shakespeare's time differ from watching a movie today?",
            "What challenges might we face reading Shakespeare's language?"
        ]
    },

    2: {
        "topic": "The Prologue: 14 Lines of Fate",
        "slides": [
            {
                "title": "What is a Prologue?",
                "bullets": [
                    "Introduction spoken before the main play begins",
                    "Tells audience what to expect",
                    "Sets mood and gives background information",
                    "Romeo and Juliet's prologue is a sonnet (14 lines)"
                ],
                "notes": """Today we're going to look at the very first words of the play - the Prologue. [PAUSE]

A prologue is like a preview or introduction that comes before the main action begins. In Shakespeare's time, an actor would walk out on stage before the play started and speak directly to the audience.

The prologue's job is to tell the audience what to expect. It sets the mood and gives us important background information. Think of it like the opening crawl in Star Wars - it gets you ready for the story.

What makes Romeo and Juliet's prologue special is that it's written as a sonnet. [EMPHASIS: sonnet] A sonnet is a 14-line poem with a specific rhyme scheme. Shakespeare is showing off his poetic skills right from the start!

[CHECK FOR UNDERSTANDING] Why do you think Shakespeare chose to summarize the entire story in the prologue? Doesn't that spoil the ending?"""
            },
            {
                "title": "The Two Households",
                "bullets": [
                    "'Two households, both alike in dignity'",
                    "Montagues and Capulets - equally wealthy and powerful",
                    "'Ancient grudge' - feud has lasted generations",
                    "Setting: Verona, Italy"
                ],
                "notes": """Let's break down the prologue line by line. The very first line tells us: 'Two households, both alike in dignity.'

Two households means two families. 'Alike in dignity' means they're equals - both wealthy, both powerful, both respected in the city. [PAUSE] This is important because neither family is better than the other. They're mirror images.

These families are the Montagues and the Capulets. Romeo is a Montague. Juliet is a Capulet.

The prologue mentions an 'ancient grudge' - a hatred that has lasted for generations. [EMPHASIS: ancient grudge] Nobody even remembers why these families hate each other! They just do. This is the world Romeo and Juliet are born into.

The setting is Verona, Italy - a real city that still exists today. Tourists can even visit 'Juliet's balcony' there.

[CHECK FOR UNDERSTANDING] Does this remind you of any conflicts you know about where people fight without remembering why it started?"""
            },
            {
                "title": "Star-Crossed Lovers",
                "bullets": [
                    "'Star-crossed' = fate is against them from the start",
                    "Stars/astrology believed to control human destiny",
                    "Romeo and Juliet are doomed before they even meet",
                    "Their love is destined to end in tragedy"
                ],
                "notes": """Now we get to one of the most famous phrases in all of literature: 'star-crossed lovers.' [PAUSE]

In Shakespeare's time, people believed that the stars and planets controlled human destiny. Your fate was written in the heavens. If the stars were against you, there was nothing you could do.

'Star-crossed' means the stars are crossed - they're working against Romeo and Juliet. [EMPHASIS: star-crossed] Before these two even meet, before they fall in love, the prologue tells us they are doomed.

This raises one of the play's biggest questions: Is their tragedy fated, or do Romeo and Juliet make choices that lead to their deaths? [PAUSE] We'll be debating this throughout our unit.

The prologue doesn't hide the ending. It tells us straight out that their love 'is death-marked.' Shakespeare wants us to know this is a tragedy from the very beginning.

[CHECK FOR UNDERSTANDING] Do you believe in fate? Do you think our lives are predetermined, or do we control our own destiny?"""
            },
            {
                "title": "The Power of Their Deaths",
                "bullets": [
                    "'Death-marked love' - love that is destined to die",
                    "Only their children's deaths end the parents' feud",
                    "'Two hours' traffic' - the play's length",
                    "Theme: Can good come from tragedy?"
                ],
                "notes": """The prologue ends with a powerful statement: only the deaths of Romeo and Juliet can end their parents' feud. [PAUSE]

Think about that. These two teenagers will die, and their deaths are the only thing powerful enough to make their families stop fighting. [EMPHASIS: only their deaths]

This introduces one of the play's central questions: Can good come from tragedy? The families finally find peace, but at what cost?

Shakespeare mentions 'two hours' traffic of our stage' - meaning the play takes about two hours to perform. He's being very direct with the audience about what they're about to experience.

The prologue ends by asking the audience to 'with patient ears attend.' In other words: pay attention, listen carefully, and you'll understand everything.

[CHECK FOR UNDERSTANDING] If you knew a story was going to end sadly, would you still want to experience it? Why do we watch tragedies?"""
            }
        ],
        "key_quotes": [
            "Two households, both alike in dignity",
            "From forth the fatal loins of these two foes, a pair of star-crossed lovers take their life",
            "Doth with their death bury their parents' strife"
        ],
        "discussion_questions": [
            "Why does Shakespeare tell us the ending in the prologue?",
            "What does 'star-crossed' mean, and do you believe in fate?",
            "Can good ever come from tragedy?"
        ]
    },

    3: {
        "topic": "Act 1 Scene 1: The Feud Begins",
        "slides": [
            {
                "title": "The Street Brawl",
                "bullets": [
                    "Play opens with servants from both houses",
                    "Sampson and Gregory (Capulet) vs. Abraham (Montague)",
                    "Insults escalate to sword fighting",
                    "Shows how easily violence erupts between the families"
                ],
                "notes": """The play opens not with our romantic heroes, but with servants fighting in the street. [PAUSE]

Sampson and Gregory are Capulet servants. They're bragging about how they'll fight any Montague they see. Then Abraham, a Montague servant, walks by.

What starts as trash talk - 'Do you bite your thumb at us, sir?' - quickly becomes a sword fight. [EMPHASIS: biting the thumb] Biting your thumb at someone was an insult in Shakespeare's time, like giving someone the middle finger today.

This opening scene shows us how deep the hatred runs. Even the servants, who have no personal reason to fight, are ready to kill each other. [PAUSE] The violence spreads from servants to gentlemen to the heads of the families themselves.

This is the world Romeo and Juliet are born into. Violence can erupt at any moment over nothing.

[CHECK FOR UNDERSTANDING] What modern conflicts remind you of this kind of senseless violence between groups?"""
            },
            {
                "title": "Benvolio the Peacemaker",
                "bullets": [
                    "Benvolio (Montague) tries to stop the fight",
                    "'Part, fools! Put up your swords'",
                    "Name means 'good will' in Italian",
                    "Character foil: He wants peace while others want war"
                ],
                "notes": """In the middle of the chaos, we meet Benvolio. He's a Montague, and his name means 'good will' in Italian. [PAUSE] Shakespeare names characters to tell us who they are.

Benvolio sees the fight and tries to stop it. He draws his sword - not to fight, but to beat down the servants' weapons. He shouts 'Part, fools! Put up your swords!'

Benvolio is what we call a character foil. [EMPHASIS: foil] A foil is a character who contrasts with another to highlight their differences. Benvolio wants peace. He represents the possibility that the feud could end.

But his efforts are immediately undermined when Tybalt arrives. Where Benvolio represents peace, Tybalt represents war.

[CHECK FOR UNDERSTANDING] Why do you think Shakespeare introduces Benvolio as a peacemaker? What is he trying to show us about the conflict?"""
            },
            {
                "title": "Tybalt the Firebrand",
                "bullets": [
                    "Tybalt (Capulet) loves to fight",
                    "'What, drawn and talk of peace? I hate the word'",
                    "Called 'Prince of Cats' for his sword skills",
                    "Represents the hatred that fuels the feud"
                ],
                "notes": """Now enters one of the play's most memorable characters: Tybalt. [PAUSE]

Tybalt is Juliet's cousin, a Capulet. When he sees Benvolio with his sword out, he doesn't care that Benvolio is trying to make peace. He says one of the play's most quoted lines: 'What, drawn and talk of peace? I hate the word, as I hate hell, all Montagues, and thee.'

[EMPHASIS: I hate the word peace] Let that sink in. Tybalt hates the very concept of peace. He would rather fight forever than find reconciliation.

Other characters call Tybalt the 'Prince of Cats' because of his deadly sword skills. In the story Shakespeare adapted, 'Tybalt' was the name of a cat character. He's quick, precise, and dangerous.

Tybalt represents everything that keeps this feud alive. He is the hatred personified.

[CHECK FOR UNDERSTANDING] What kind of person hates the very word 'peace'? What might have made Tybalt this way?"""
            },
            {
                "title": "The Prince's Warning",
                "bullets": [
                    "Prince Escalus stops the riot with a death threat",
                    "'If ever you disturb our streets again, your lives shall pay'",
                    "This is the third civil brawl from the feud",
                    "Foreshadowing: The prince's threat will come true"
                ],
                "notes": """The fight grows until the heads of both families, Lord Montague and Lord Capulet, join in. Old men who should know better are grabbing swords!

Prince Escalus arrives with his guards and stops the riot. He is furious. [PAUSE]

He reveals this is the THIRD time the families' feud has disturbed the peace of Verona. He says: 'If ever you disturb our streets again, your lives shall pay the forfeit of the peace.'

[EMPHASIS: your lives shall pay] This is a death sentence. If anyone from either family causes another public fight, they will be executed.

This is what we call foreshadowing - a hint about what will happen later. [PAUSE] Remember this threat. It will become very important in Act 3.

[CHECK FOR UNDERSTANDING] Why do you think the Prince gives such a severe punishment? What would you do if you were the ruler of Verona?"""
            },
            {
                "title": "Introducing Romeo",
                "bullets": [
                    "Romeo missed the fight - he was wandering alone",
                    "He is lovesick for Rosaline (not Juliet!)",
                    "'Love is a smoke made with the fume of sighs'",
                    "Romeo loves the IDEA of being in love"
                ],
                "notes": """After all that violence, we finally meet Romeo. And where was he during the fight? [PAUSE] He missed it completely. He was wandering alone in the woods, sighing about love.

Here's the twist: Romeo is not in love with Juliet yet. He's in love with a woman named Rosaline. [EMPHASIS: Rosaline, not Juliet]

But is Romeo really in love? Listen to how he talks: 'Love is a smoke made with the fume of sighs.' He speaks in riddles and contradictions. He's more in love with the IDEA of being in love than with any real person.

Rosaline has sworn to be a nun and never marry. Romeo is heartbroken, but Benvolio suggests he just needs to look at other women to forget her.

This sets up an important question: When Romeo falls for Juliet at first sight, is it real love or the same infatuation?

[CHECK FOR UNDERSTANDING] What's the difference between really loving someone and just being in love with the idea of love?"""
            }
        ],
        "key_quotes": [
            "Do you bite your thumb at us, sir?",
            "I hate the word, as I hate hell, all Montagues, and thee.",
            "If ever you disturb our streets again, your lives shall pay the forfeit of the peace.",
            "Love is a smoke made with the fume of sighs."
        ],
        "discussion_questions": [
            "Why does the play start with servants fighting instead of the main characters?",
            "Compare Benvolio and Tybalt. What do they represent?",
            "Is Romeo really in love with Rosaline, or in love with being in love?"
        ]
    },

    4: {
        "topic": "Act 1 Scenes 2-3: Party Preparations",
        "slides": [
            {
                "title": "Paris Seeks Juliet's Hand",
                "bullets": [
                    "Count Paris asks Lord Capulet to marry Juliet",
                    "Paris is wealthy, noble, and 'a good match'",
                    "Capulet says Juliet is too young (only 13-14)",
                    "But invites Paris to the feast to woo her"
                ],
                "notes": """Scene 2 introduces a new character: Count Paris. He's a wealthy nobleman, and he wants to marry Juliet. [PAUSE]

Paris goes to Lord Capulet to ask for permission. In Shakespeare's time, daughters didn't choose their own husbands - their fathers did. Marriage was more like a business deal than a love match.

Lord Capulet's response is interesting. He says Juliet is too young - 'She hath not seen the change of fourteen years.' [EMPHASIS: not yet fourteen] Juliet is only 13 years old!

But Capulet doesn't say no. He invites Paris to the Capulet feast that night. He tells Paris to woo Juliet, to win her heart. 'My will to her consent is but a part,' he says - meaning he'll only agree if Juliet agrees too.

This seems progressive for the time, but we'll see how this changes later in the play.

[CHECK FOR UNDERSTANDING] How old is Juliet? How does that affect how you see her story?"""
            },
            {
                "title": "The Servant's Mistake",
                "bullets": [
                    "Capulet gives a servant the guest list for the party",
                    "Problem: The servant cannot read",
                    "He asks Romeo and Benvolio for help",
                    "This accident sets the entire tragedy in motion"
                ],
                "notes": """Here's where fate - or coincidence - steps in. Lord Capulet gives a servant a list of guests to invite to the feast. But there's a problem: the servant cannot read. [PAUSE]

So what does he do? He stops the first people he sees on the street and asks for help reading the list. And who does he happen to stop? Romeo and Benvolio.

[EMPHASIS: Romeo and Benvolio] Of all the people in Verona, the servant asks two Montagues to read the Capulet guest list!

When Romeo sees that Rosaline is invited, Benvolio convinces him to sneak into the party. 'Go there,' he says, 'and compare Rosaline to other beauties. You'll see she's not so special.'

Think about how many accidents had to happen for Romeo to end up at that party. Is this fate, or just random chance?

[CHECK FOR UNDERSTANDING] Do you believe this was fate bringing Romeo and Juliet together, or just a coincidence?"""
            },
            {
                "title": "Meet Juliet and the Nurse",
                "bullets": [
                    "Scene 3: Lady Capulet tells Juliet about Paris",
                    "The Nurse is Juliet's closest companion",
                    "Nurse raised Juliet since birth - more like a mother",
                    "Comic relief: Nurse tells embarrassing childhood stories"
                ],
                "notes": """Scene 3 takes us inside the Capulet house, and we finally meet Juliet. [PAUSE]

Lady Capulet, Juliet's mother, comes to tell her about Paris's proposal. But she can barely talk to her own daughter! She keeps the Nurse in the room for support.

The Nurse is one of Shakespeare's greatest comic characters. She's been with Juliet since birth - she was actually her wet nurse, meaning she breastfed baby Juliet. [EMPHASIS: closer than her own mother]

The Nurse tells a long, rambling, embarrassing story about Juliet as a toddler, much to Lady Capulet's frustration. But this scene shows us something important: the Nurse loves Juliet like her own child. She'll become Juliet's confidante and helper.

Notice how different the Nurse and Lady Capulet are with Juliet. Lady Capulet is formal and distant. The Nurse is warm and affectionate.

[CHECK FOR UNDERSTANDING] Why do you think Juliet is closer to her Nurse than to her own mother?"""
            },
            {
                "title": "Juliet's Response to Marriage",
                "bullets": [
                    "'It is an honor that I dream not of'",
                    "Juliet is obedient but not enthusiastic",
                    "She agrees to look at Paris at the feast",
                    "Contrast with Romeo: She's practical, not lovesick"
                ],
                "notes": """When Lady Capulet asks how Juliet feels about marriage, her response is fascinating: 'It is an honor that I dream not of.' [PAUSE]

This tells us so much about Juliet. She's dutiful - she knows marriage is expected of her. But she hasn't been dreaming about it or romanticizing it. She's practical and grounded.

[EMPHASIS: I dream not of] Compare this to Romeo, who's been wandering around mooning over Rosaline. Juliet seems much more mature, even though she's younger!

When her mother asks specifically about Paris, Juliet is obedient: 'I'll look to like, if looking liking move.' Meaning, 'I'll try to like him if his appearance pleases me.'

But she adds a condition: 'But no more deep will I endart mine eye / Than your consent gives strength to make it fly.' She won't fall deeper in love than her parents allow.

This is the Juliet we meet before Romeo. Controlled. Obedient. Not swept away by passion. Yet.

[CHECK FOR UNDERSTANDING] How does Juliet's attitude toward love differ from Romeo's? Who seems more mature?"""
            }
        ],
        "key_quotes": [
            "She hath not seen the change of fourteen years.",
            "It is an honor that I dream not of.",
            "I'll look to like, if looking liking move."
        ],
        "discussion_questions": [
            "Why is it significant that a servant's inability to read leads to Romeo attending the party?",
            "Why is Juliet closer to her Nurse than her own mother?",
            "Compare Romeo and Juliet's attitudes toward love at this point."
        ]
    },

    5: {
        "topic": "Character Mapping & Predictions",
        "slides": [
            {
                "title": "The Montague Family",
                "bullets": [
                    "Lord & Lady Montague - Romeo's parents",
                    "Romeo - lovesick young man, the romantic hero",
                    "Benvolio - Romeo's cousin, the peacemaker",
                    "Associates: Mercutio (Prince's relative, Romeo's friend)"
                ],
                "notes": """Today we're mapping out who's who in this story. Let's start with the Montagues - Romeo's family. [PAUSE]

Lord and Lady Montague are Romeo's parents. We don't see much of them, but we know they're concerned about Romeo's moody behavior.

Romeo is our male protagonist, the romantic hero. So far we've seen him as a lovesick young man, more in love with love itself than with any real person. [EMPHASIS: romantic but naive]

Benvolio is Romeo's cousin. His name means 'good will,' and he tries to be a peacemaker. He's reasonable and level-headed - the friend who gives good advice that Romeo ignores.

Mercutio isn't technically a Montague, but he's Romeo's best friend. He's actually related to Prince Escalus. We'll meet him soon, and he's one of Shakespeare's most brilliant characters.

[CHECK FOR UNDERSTANDING] So far, which Montague character do you relate to most? Why?"""
            },
            {
                "title": "The Capulet Family",
                "bullets": [
                    "Lord & Lady Capulet - Juliet's parents",
                    "Juliet - our heroine, practical and obedient (for now)",
                    "Tybalt - Juliet's hot-headed cousin",
                    "The Nurse - Juliet's closest companion and confidante"
                ],
                "notes": """Now let's look at the Capulets - the family Romeo is supposed to hate. [PAUSE]

Lord Capulet seems reasonable at first - he wants Juliet to have some choice in her marriage. Lady Capulet is more distant from her daughter, preferring to let the Nurse handle emotional matters.

Juliet is our female protagonist. Unlike Romeo, she starts the play practical and obedient. [EMPHASIS: practical and obedient] She hasn't been dreaming of love. But watch how she transforms once she meets Romeo.

Tybalt is Juliet's cousin, and he is dangerous. Remember his line: 'I hate the word peace.' He represents the violent hatred that threatens everything.

The Nurse is technically a servant, but she's more family than the Capulets are. She raised Juliet, loves her deeply, and will become her secret-keeper.

[CHECK FOR UNDERSTANDING] Which Capulet character interests you most so far? Why?"""
            },
            {
                "title": "The Neutral Powers",
                "bullets": [
                    "Prince Escalus - ruler of Verona, keeps peace",
                    "County Paris - nobleman who wants to marry Juliet",
                    "Friar Lawrence - priest (we'll meet him soon)",
                    "These characters are caught between the two families"
                ],
                "notes": """Some characters aren't Montagues or Capulets - they're caught in the middle. [PAUSE]

Prince Escalus rules Verona. He's fed up with the feud disrupting his city. He represents law and order, and he's threatened to execute anyone who fights again.

County Paris is a nobleman who wants to marry Juliet. He's a 'good match' on paper - wealthy, well-connected, approved by her parents. [EMPHASIS: perfect on paper] The only problem? Juliet doesn't love him.

Friar Lawrence is a priest we haven't met yet, but he'll become crucial to the story. He'll marry Romeo and Juliet in secret, hoping to end the feud.

Notice how these neutral characters all want peace, but they'll all contribute to the tragedy in some way.

[CHECK FOR UNDERSTANDING] What do all these neutral characters have in common? What do they want?"""
            },
            {
                "title": "Predictions for the Play",
                "bullets": [
                    "We know Romeo and Juliet will fall in love",
                    "We know their love will end in death",
                    "Questions: HOW will it happen? WHO is responsible?",
                    "Watch for choices vs. fate throughout the play"
                ],
                "notes": """Thanks to the prologue, we know the ending. Romeo and Juliet will fall in love, and they will die. [PAUSE] But knowing the destination doesn't mean we know the journey.

The big questions we should be asking are: How does it happen? Who is responsible? [EMPHASIS: who is responsible]

Is it the parents' fault for continuing the feud? Is it fate, written in the stars? Is it bad luck and poor timing? Or do Romeo and Juliet make choices that lead to their own deaths?

Throughout the play, pay attention to moments of choice versus moments of fate. When could characters have made different decisions? What if someone had just waited another hour?

Today I want you to make predictions. Think about what you know so far and guess how things might unfold.

[CHECK FOR UNDERSTANDING] Based on what we've read, what do you think will happen at the Capulet feast tonight? What could go wrong?"""
            }
        ],
        "key_quotes": [
            "A pair of star-crossed lovers take their life.",
            "From ancient grudge break to new mutiny."
        ],
        "discussion_questions": [
            "Which character do you think will cause the most trouble?",
            "What do you predict will happen when Romeo sees Juliet?",
            "Is this story fated, or could it end differently?"
        ]
    },

    # =========================================================================
    # WEEK 2: ACT 1-2 - LOVE AT FIRST SIGHT
    # =========================================================================
    6: {
        "topic": "Act 1 Scenes 4-5: The Masquerade Ball",
        "slides": [
            {
                "title": "Crashing the Capulet Party",
                "bullets": [
                    "Romeo, Benvolio, and Mercutio wear masks to sneak in",
                    "Romeo is still moody about Rosaline",
                    "Mercutio tries to cheer him up with the Queen Mab speech",
                    "Romeo has a dark premonition about this night"
                ],
                "notes": """Scene 4 shows Romeo, Benvolio, and Mercutio preparing to crash the Capulet feast. [PAUSE] They're wearing masks because it's a masquerade - but also to hide that they're Montagues.

Romeo is still moping about Rosaline. He says he's too sad to dance. This is dramatic irony - we know he's about to meet someone who will make him forget Rosaline completely. [EMPHASIS: dramatic irony]

To cheer Romeo up, Mercutio delivers the famous Queen Mab speech, which we'll look at more closely tomorrow. It's wild, imaginative, and slightly disturbing.

But here's the important part: before going in, Romeo says he has a dark feeling. 'My mind misgives some consequence yet hanging in the stars.' He senses that something begun tonight will end with his death.

[CHECK FOR UNDERSTANDING] Do you think Romeo's premonition is real foresight, or just his gloomy personality talking?"""
            },
            {
                "title": "Romeo Sees Juliet",
                "bullets": [
                    "'Did my heart love till now? Forswear it, sight!'",
                    "Romeo forgets Rosaline instantly",
                    "He compares Juliet to a 'rich jewel' and light",
                    "Love at first sight - or just physical attraction?"
                ],
                "notes": """The moment Romeo sees Juliet, everything changes. [PAUSE]

He says: 'Did my heart love till now? Forswear it, sight! For I ne'er saw true beauty till this night.' In other words, I never really loved before this moment.

[EMPHASIS: Did my heart love till now?] Wait - wasn't he just crying about Rosaline ten minutes ago? Now he says he never loved at all?

Romeo uses light imagery to describe Juliet: she's like a 'rich jewel' against darkness, she 'teaches the torches to burn bright.' This light versus dark imagery will continue throughout the play.

Here's an important question for you: Is this love, or is this just physical attraction? Romeo falls in love with how Juliet looks before he's even spoken to her. Is that real love?

[CHECK FOR UNDERSTANDING] Romeo claimed to love Rosaline. Now he loves Juliet. Does this make his new love more or less convincing?"""
            },
            {
                "title": "Tybalt's Rage",
                "bullets": [
                    "Tybalt recognizes Romeo's voice",
                    "'This, by his voice, should be a Montague'",
                    "He wants to kill Romeo on the spot",
                    "Lord Capulet stops him - Romeo is behaving well"
                ],
                "notes": """While Romeo is falling in love, someone else has noticed him. Tybalt recognizes Romeo's voice even through the mask. [PAUSE]

'This, by his voice, should be a Montague... to strike him dead I hold it not a sin.'

[EMPHASIS: not a sin to kill him] Tybalt wants to murder Romeo at his own family's party. That's how deep the hatred runs.

But Lord Capulet stops him. Surprisingly, Lord Capulet defends Romeo: 'He bears him like a portly gentleman... I would not for the wealth of all this town here in my house do him disparagement.'

Tybalt is furious but has to obey his uncle. He leaves with a chilling threat: 'I will withdraw, but this intrusion shall, now seeming sweet, convert to bitterest gall.'

This moment is crucial. Tybalt's anger doesn't go away - he just saves it for later.

[CHECK FOR UNDERSTANDING] Why do you think Lord Capulet defends Romeo? What might happen when Tybalt acts on his anger later?"""
            },
            {
                "title": "The First Kiss",
                "bullets": [
                    "Romeo and Juliet speak in a shared sonnet",
                    "Religious imagery: 'holy palmers' kiss'",
                    "They kiss twice before learning each other's names",
                    "Discovery: 'My only love sprung from my only hate'"
                ],
                "notes": """Now comes one of the most famous meetings in all of literature. Romeo approaches Juliet, and their first conversation is a shared sonnet. [PAUSE]

They take turns speaking lines, finishing each other's rhymes. It's like they're speaking the same language immediately, like they're meant to be together.

[EMPHASIS: shared sonnet] The imagery is religious: Romeo calls Juliet a 'holy shrine,' her lips are 'two blushing pilgrims.' This elevates their love to something sacred - but it's also potentially blasphemous.

They kiss. Not once, but twice, before they even know each other's names!

Then the Nurse interrupts to call Juliet to her mother. When Romeo asks who Juliet is, he learns the crushing truth: 'She is a Capulet!'

And when Juliet asks the Nurse who Romeo is: 'His name is Romeo, and a Montague, the only son of your great enemy.'

Juliet's response is heartbreaking: 'My only love sprung from my only hate!'

[CHECK FOR UNDERSTANDING] What does it mean that they fell in love before knowing each other's names?"""
            }
        ],
        "key_quotes": [
            "Did my heart love till now? Forswear it, sight!",
            "O, she doth teach the torches to burn bright!",
            "My only love sprung from my only hate!"
        ],
        "discussion_questions": [
            "Is Romeo's love for Juliet more real than his love for Rosaline?",
            "Why is it significant that they kiss before knowing each other's names?",
            "How does Tybalt's reaction foreshadow future events?"
        ]
    },

    # Continue with more days...
    # For brevity, I'll add key remaining content

    7: {
        "topic": "Queen Mab Speech Analysis",
        "slides": [
            {
                "title": "Mercutio's Wild Imagination",
                "bullets": [
                    "Queen Mab is a tiny fairy who delivers dreams",
                    "She rides a chariot made of a hazelnut shell",
                    "The speech starts playful, becomes dark",
                    "Shows Mercutio's brilliant but unstable mind"
                ],
                "notes": """Today we're diving deep into one of Shakespeare's most famous speeches. [PAUSE] Mercutio's Queen Mab speech is brilliant, but also disturbing.

Queen Mab, according to Mercutio, is a tiny fairy who visits people while they sleep and delivers dreams. Her chariot is made from a hazelnut shell, her wheels are spider legs, her whip is a cricket's bone.

[EMPHASIS: incredible detail] The level of imagination here is extraordinary. Mercutio isn't just making things up - he's creating an entire microscopic world.

But watch how the speech changes. It starts playful: lovers dream of love, lawyers dream of fees. Then it gets darker: soldiers dream of 'cutting foreign throats.' By the end, Mercutio is talking about nightmares and demons.

Romeo has to stop him. 'Peace, peace, Mercutio, peace! Thou talk'st of nothing.' And Mercutio admits: 'True, I talk of dreams, which are the children of an idle brain.'

[CHECK FOR UNDERSTANDING] What does this speech reveal about Mercutio's personality?"""
            },
            {
                "title": "Dreams and Reality",
                "bullets": [
                    "Mercutio claims dreams are meaningless - 'nothing'",
                    "But Romeo believes his dreams predict the future",
                    "Theme: Do dreams reveal truth or deceive us?",
                    "Irony: The dreamers (Romeo/Juliet) will die"
                ],
                "notes": """The Queen Mab speech raises a key question: Do dreams mean anything? [PAUSE]

Mercutio says dreams are 'the children of an idle brain, begot of nothing but vain fantasy.' They're just imagination, meaningless entertainment.

But Romeo disagrees. He's been having premonitions all night. He feels that 'some consequence yet hanging in the stars' will begin tonight. [EMPHASIS: Romeo believes in dreams]

This is one of the play's central tensions: dreamers versus realists. Romeo and Juliet are dreamers - they believe in love at first sight, in defying their families, in impossible futures.

Mercutio is a realist. He mocks romantic love and calls dreams 'nothing.' But here's the tragic irony: the dreamers' dreams will come true - they will die.

[CHECK FOR UNDERSTANDING] Are you more like Mercutio (skeptical) or Romeo (a believer in dreams and signs)?"""
            }
        ],
        "key_quotes": [
            "O, then I see Queen Mab hath been with you!",
            "True, I talk of dreams, which are the children of an idle brain."
        ],
        "discussion_questions": [
            "What does the shift in tone during the speech reveal about Mercutio?",
            "Do dreams predict the future or just reflect our fears?"
        ]
    },

    8: {
        "topic": "Act 2 Scene 2: The Balcony Scene",
        "slides": [
            {
                "title": "The Most Famous Scene in Theater",
                "bullets": [
                    "Romeo hides in Capulet's orchard after the party",
                    "Juliet appears on her balcony, unaware Romeo is below",
                    "He overhears her private thoughts about him",
                    "One of the most quoted scenes in all of literature"
                ],
                "notes": """We've arrived at the most famous scene in all of theater. [PAUSE] When you picture Romeo and Juliet, this is probably what you imagine.

After the party, Romeo doesn't go home. He hides in the Capulet orchard, hoping to see Juliet again. Then she appears on her balcony, not knowing anyone is watching.

[EMPHASIS: she doesn't know he's there] This is important. What we're about to hear are Juliet's private thoughts. She's not performing for anyone.

Romeo watches from below, commenting on her beauty. When she starts speaking about him, he's overcome. Should he stay hidden or reveal himself?

Every line from this scene has been quoted, adapted, and referenced for 400 years. But let's look at what's actually being said.

[CHECK FOR UNDERSTANDING] What does it mean that Romeo hears Juliet's private thoughts? Is this romantic or invasive?"""
            },
            {
                "title": "What's in a Name?",
                "bullets": [
                    "'O Romeo, Romeo, wherefore art thou Romeo?'",
                    "'Wherefore' means 'WHY' - not 'where'",
                    "Juliet wishes Romeo wasn't a Montague",
                    "'A rose by any other name would smell as sweet'"
                ],
                "notes": """Let's clear up one of the most misunderstood lines in literature. [PAUSE]

'O Romeo, Romeo, wherefore art thou Romeo?' People think Juliet is asking WHERE Romeo is. But 'wherefore' means 'WHY.'

[EMPHASIS: WHY, not WHERE] Juliet is asking: Why do you have to be Romeo? Why do you have to be a Montague?

She continues: 'What's in a name? That which we call a rose by any other name would smell as sweet.'

In other words: names are just words. They don't change who you really are. If a rose were called something ugly, it would still smell beautiful. If Romeo weren't called 'Montague,' he would still be the man she loves.

'Deny thy father and refuse thy name,' she begs. 'Or if thou wilt not, be but sworn my love, and I'll no longer be a Capulet.'

She's willing to give up her entire identity for love.

[CHECK FOR UNDERSTANDING] Is Juliet right that names don't matter? Or do our names and families shape who we are?"""
            },
            {
                "title": "Romeo Reveals Himself",
                "bullets": [
                    "Romeo can't stay silent: 'I take thee at thy word'",
                    "Juliet is alarmed - he'll be killed if found",
                    "But Romeo says love gave him wings to climb the wall",
                    "They declare their love openly to each other"
                ],
                "notes": """Romeo can't contain himself any longer. He steps out of the shadows: 'I take thee at thy word. Call me but love, and I'll be new baptized.'

[PAUSE] In other words: Give me a new name. Call me 'love' instead of 'Montague.'

Juliet is shocked and terrified. 'How camest thou hither... The orchard walls are high and hard to climb, and the place death, considering who thou art.'

[EMPHASIS: the place death] If the Capulets find Romeo here, they will kill him. This is not metaphorical - this is literal death.

But Romeo brushes off the danger: 'With love's light wings did I o'erperch these walls, for stony limits cannot hold love out.'

Love, he says, makes him fearless. Love makes him supernatural.

Is this romantic, or reckless? Is Romeo brave or foolish?

[CHECK FOR UNDERSTANDING] Is Romeo's attitude romantic or dangerously naive?"""
            },
            {
                "title": "A Hasty Marriage Plan",
                "bullets": [
                    "Juliet worries they're moving too fast",
                    "'It is too rash, too unadvised, too sudden'",
                    "Yet she proposes marriage before the scene ends",
                    "Romeo will send word tomorrow about wedding plans"
                ],
                "notes": """Here's where Juliet shows her complexity. [PAUSE] She worries they're moving too fast.

'I have no joy of this contract tonight. It is too rash, too unadvised, too sudden.'

[EMPHASIS: too rash, too sudden] She recognizes the danger of their speed. She's not completely swept away.

But then, just a few lines later, SHE is the one who proposes marriage! 'If that thy bent of love be honorable, thy purpose marriage, send me word tomorrow.'

Think about that. Juliet is the practical one who worries about moving too fast - and Juliet is the one who proposes.

They've known each other for one night. By tomorrow they'll be planning a secret wedding.

The Nurse keeps calling Juliet back inside. 'A thousand times good night,' they say to each other. Neither wants to leave.

[CHECK FOR UNDERSTANDING] Juliet says it's too sudden, then proposes marriage. Why do you think she does this?"""
            }
        ],
        "key_quotes": [
            "O Romeo, Romeo, wherefore art thou Romeo?",
            "What's in a name? That which we call a rose by any other name would smell as sweet.",
            "It is too rash, too unadvised, too sudden."
        ],
        "discussion_questions": [
            "Is Juliet right that names don't matter?",
            "Why does Juliet propose marriage after saying they're moving too fast?",
            "Is this scene romantic, or are there warning signs?"
        ]
    }
}

# Add placeholder content for remaining days
for day in range(9, 31):
    if day not in RJ_CONTENT_DATABASE:
        RJ_CONTENT_DATABASE[day] = {
            "topic": f"Day {day} Content",
            "slides": [
                {
                    "title": f"Day {day} - Coming Soon",
                    "bullets": [
                        "Detailed content being developed",
                        "Full bullet points for student notes",
                        "Comprehensive teaching material"
                    ],
                    "notes": f"""This is placeholder content for Day {day}.

The full verbatim presenter notes will include:
- Word-for-word teaching script
- [PAUSE] markers for timing
- [EMPHASIS: term] for key vocabulary
- [CHECK FOR UNDERSTANDING] prompts
- Discussion facilitation guidance

Each slide will have approximately 150-200 words of presenter notes, allowing for natural teaching pace and student engagement."""
                }
            ],
            "key_quotes": [],
            "discussion_questions": []
        }


def get_day_content(day_num: int) -> dict:
    """Get content for a specific day."""
    return RJ_CONTENT_DATABASE.get(day_num, {})


def get_slide_content(day_num: int, slide_index: int) -> dict:
    """Get specific slide content for a day."""
    day_content = get_day_content(day_num)
    slides = day_content.get("slides", [])
    if 0 <= slide_index < len(slides):
        return slides[slide_index]
    return {}
