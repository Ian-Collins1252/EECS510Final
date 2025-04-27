# EECS510 Final
Createing a formal language for EECS 510 Theory of Computing

## Characters
#### Link
###### States
- Idle
- Dialog
- Eat
- Attack
####### Dialog
Modeled with a pushdown automata where the 2 actors can respond to each other, requiring a response from each other until the interaction is ended with the 'bye' signal.
####### Eat
Both restores Link's health during combat and will open up exclusive dialogue with Zelda about Link's backstory. It is also what brings him most joy in life.
####### Attack
Modeled using a Turing Machine using 2 separate tapes to track each of the inputs
#### Zelda
###### States
- Idle
- Dialog
While Zelda has a more active role within the narrative, such as sealing Ganon's evil, we are focusing on the playable character aspect of the Legend of Zelda franchise. Thus Zelda is filling her role as a non-playable character
####### Dialog
A pushdown automata that interfaces with Link's dialog options. As mentioned above, Zelda can learn about Link's backstory, similar to in Breath of the Wild, after getting him to warm up to her. What makes Link the happiest is food.
#### Impa
###### States
- Idle
- Dialog
####### Dialog
Again modeled with a pushdown automata, Impa can issue quests to Link to protect the land of Hyrule and defeat Ganon and his forces.
#### Ganondorf
####### States
- Idle
- Attack
- King
- Dead
######## Attack
Ganondorf can battle Link in a duel for the fate of Hyrule.
######## King
Ganondorf can lie to the King of Hyrule to later betray him and take over his kingdom. Additionally, Ganondorf can defeat Link and either resume or take over the Kingdom of Hyrule.
######## Dead
As most of his stories end, Ganondorf is slain by the Goddess's chosen hero, Link. Until, of course, he is resurrected for the next game.
#### Bokoblin
###### States
- Idle
- Attack
- Dead
####### Attack
Bokoblins can fight Link to prevent him from saving the Kingdom of Hyrule.
####### Dead
Unlike most living things, Bokoblins can be resurrected during the Bloodmoon due to Ganondorf's malice.
