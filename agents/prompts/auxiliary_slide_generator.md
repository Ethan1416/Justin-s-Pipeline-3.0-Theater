# Auxiliary Slide Generator

## Purpose
Generate the 4 auxiliary slides (Agenda, Warmup, Activity, Journal/Exit) that frame each theater lesson. These slides provide structure and transitions for the 56-minute class period.

## HARDCODED SKILLS
```yaml
skills:
  - warmup_bank_selector
  - activity_type_selector
  - word_count_analyzer
```

## Input Schema
```json
{
  "unit": {
    "number": 1,
    "name": "Greek Theater",
    "day": 5,
    "total_days": 20
  },
  "lesson_topic": "The Theatron and Orchestra",
  "learning_objectives": [
    "Identify the parts of a Greek theater",
    "Explain the function of the orchestra"
  ],
  "warmup": {
    "name": "Greek Chorus Walk",
    "type": "physical",
    "duration": 5,
    "instructions": [
      "Stand in a circle",
      "Walk as a unified group",
      "Match the rhythm of the leader"
    ],
    "connection_to_lesson": "Prepares bodies for understanding how performers used the orchestra space"
  },
  "activity": {
    "name": "Theater Blueprint Analysis",
    "type": "gallery_walk",
    "duration": 15,
    "setup_instructions": "Post diagrams around room",
    "main_instructions": "Rotate through stations analyzing Greek theater components",
    "sharing_format": "Whole class discussion"
  },
  "journal_prompt": "How might the design of the Greek theater have affected the performance style of actors?",
  "exit_ticket": "Label the three main parts of a Greek theater on a blank diagram."
}
```

## Output Schema
```json
{
  "auxiliary_slides": [
    {
      "slide_number": 1,
      "type": "auxiliary",
      "subtype": "agenda",
      "header": "Today's Agenda",
      "body": "1. Warmup: Greek Chorus Walk (5 min)\n2. Lecture: The Theatron and Orchestra (15 min)\n3. Activity: Theater Blueprint Analysis (15 min)\n4. Reflection: Journal + Exit Ticket (10 min)",
      "presenter_notes": "...",
      "performance_tip": "Review each agenda item while making eye contact with different sections of the room."
    },
    {
      "slide_number": 2,
      "type": "auxiliary",
      "subtype": "warmup",
      "header": "Warmup: Greek Chorus Walk",
      "body": "...",
      "presenter_notes": "...",
      "performance_tip": "..."
    },
    {
      "slide_number": 3,
      "type": "auxiliary",
      "subtype": "activity",
      "header": "Activity: Theater Blueprint Analysis",
      "body": "...",
      "presenter_notes": "...",
      "performance_tip": "..."
    },
    {
      "slide_number": 4,
      "type": "auxiliary",
      "subtype": "journal_exit",
      "header": "Reflection Time",
      "body": "...",
      "presenter_notes": "...",
      "performance_tip": "..."
    }
  ]
}
```

## Slide 1: Agenda

### Header
`Today's Agenda`

### Body Format
```
1. Warmup: [Name] (5 min)
2. Lecture: [Topic] (15 min)
3. Activity: [Name] (15 min)
4. Reflection: Journal + Exit Ticket (10 min)
```

### Presenter Notes Template (75-100 words)
```
Good [morning/afternoon] everyone! [PAUSE]

As you can see, we have an exciting class today. Let me walk you through our agenda.

We'll start with our warmup, [Warmup Name], which connects to today's topic by [connection]. [PAUSE]

Then we'll dive into our lecture on [Topic]. [EMPHASIS: key term]

After that, you'll apply what you've learned in [Activity Name].

We'll wrap up with reflection time for journaling and your exit ticket.

Any questions before we begin? [CHECK FOR UNDERSTANDING]
```

### Performance Tip
`Review each agenda item while making eye contact with different sections of the room.`

## Slide 2: Warmup

### Header
`Warmup: [Name]`

### Body Format
```
Purpose: [Connection to lesson]

Instructions:
- [Step 1]
- [Step 2]
- [Step 3]

Time: 5 minutes
```

### Presenter Notes Template (75-100 words)
```
Let's begin with our warmup! [PAUSE]

Today we're doing [Warmup Name]. This warmup connects to our lesson because [detailed connection]. [PAUSE]

Here's how it works:
First, [instruction 1].
Then, [instruction 2]. [PAUSE]
Finally, [instruction 3].

Remember to [safety/engagement note].

I'll give you a signal when we have one minute left. [PAUSE]

Ready? Let's begin!

[After warmup]
Great work, everyone! [PAUSE] Notice how that warmup prepared us for [lesson connection].
```

### Performance Tip
`Participate in the warmup yourself to model engagement and build ensemble.`

## Slide 3: Activity

### Header
`Activity: [Name]`

### Body Format
```
Setup (1.5 min):
[Brief setup instructions]

Work Time (11 min):
[Main activity instructions]

Sharing (2.5 min):
[Share-out format]

Materials: [List]
```

### Presenter Notes Template (75-100 words)
```
Now it's time for your activity! [PAUSE]

Today you'll be doing [Activity Name]. This activity helps you [learning connection]. [PAUSE]

Here's what you need to know:

For setup, [setup instructions]. This should take about 90 seconds.

During work time, [main instructions]. [EMPHASIS: key requirement] [PAUSE]

You'll have 11 minutes to work. I'll give you a 5-minute and 1-minute warning.

For sharing, [sharing format].

Does everyone understand the instructions? [CHECK FOR UNDERSTANDING]

Go ahead and get started!
```

### Performance Tip
`Circulate during work time, asking guiding questions rather than giving answers.`

## Slide 4: Journal/Exit

### Header
`Reflection Time`

### Body Format
```
Journal Prompt (7 min):
[Thought-provoking question]

Exit Ticket (3 min):
[Quick assessment question]

Turn in exit ticket before you leave!
```

### Presenter Notes Template (50-75 words)
```
Let's wrap up with reflection time. [PAUSE]

Take out your journals. Today's prompt is on the screen.

[Read prompt aloud]

Take about 7 minutes to write your response. Think deeply - there's no single right answer. [PAUSE]

[After journal time]
Now, complete your exit ticket. This helps me know what you understood today.

Turn in your exit ticket before you leave. See you [next class]!
```

### Performance Tip
`Circulate quietly while students write to encourage deeper reflection.`

## Text Limits

### Header
- Maximum: 32 characters per line, 2 lines
- Total maximum: 64 characters

### Body
- Maximum: 8 lines
- Maximum: 66 characters per line

### Performance Tip
- Maximum: 132 characters

### Presenter Notes (per auxiliary slide)
- Agenda: 75-100 words
- Warmup: 75-100 words
- Activity: 75-100 words
- Journal/Exit: 50-75 words
- **Total auxiliary notes: 275-375 words**

## Unit-Specific Adaptations

### Unit 1: Greek Theater
- Warmups emphasize chorus movement and collective action
- Activities focus on spatial awareness and architectural analysis
- Journal prompts connect ancient practices to modern theater

### Unit 2: Commedia dell'Arte
- Warmups include character physicality and mask preparation
- Activities focus on improvisation and scenario development
- Journal prompts explore character archetypes

### Unit 3: Shakespeare
- Warmups include verse speaking and breath work
- Activities focus on text analysis and scene work
- Journal prompts connect language to meaning

### Unit 4: Student-Directed One Acts
- Warmups emphasize ensemble building and trust
- Activities focus on directing and collaboration
- Journal prompts develop directorial thinking

## Error Handling
- If warmup connection is missing, generate based on unit context
- If activity timing doesn't match (setup + work + sharing != 15), adjust work time
- If journal prompt is too simple, add "Why?" or "How might this..."

## Validation Checklist
- [ ] Exactly 4 auxiliary slides generated
- [ ] All headers under 64 characters
- [ ] All body text under 8 lines, 66 chars/line
- [ ] Performance tips under 132 characters
- [ ] Total presenter notes: 275-375 words
- [ ] Warmup connection to lesson is explicit
- [ ] Activity timing sums to 15 minutes
- [ ] Journal prompt encourages deep thinking
- [ ] Exit ticket assesses learning objectives
