
## Visualisation 

### card playing gui

### kripke models of the of the agents' card knowledge

At every moment of the game it is possible to see what the players know and hold for possible regarding the card ownership of each card in the game. After each turn, a spectator can select a card via a dropdown menu in the main loop. A schematic S5 kripke model is then drawn for each card with the draw_model function, which calls on the player.knowledge and player.possible triples for each card to get the relations between the worlds. As card ownership is mutually exclusive in 'klaverjassen' (every card in the game is dealt to exactly one player), players never hold any worlds for possible where this is not the case, so for any card C with the corresponding propositional atoms (p1: south owns C, p2: west owns C, p3: north owns C, p4: east owns C) the S5 model includes only the the states (p1 = T, p2 = F, p3 = F, p4 = F), (p1 = F, p2 = T, p3 = F, p4 = F), (p1 = F, p2 = F, p3 = T, p4 = F) and (p1 = F, p2 = F, p3 = F, p4 = T).

![Testing with images](/site_images/select.png)

In the beginning of the game player South plays its lowest card instead of one of its high cards like the 10 of hearts, to understand this choice, let's look at what player South knows or holds for possible about the location of the ace of hearts.

![Model beginning game](/site_images/model.png)

As we can see, player South (who has no information save his own cards, seeing as it's the beginning of the game), still holds it for possible that either East or West has the ace of hearts, and decides to play it safe by not playing its ten of hearts. As a matter of fact, player East is the actual owner of the ace of hearts, and also the only player who currently knows this.

![Public announcement card](/site_images/pub_ann_card.png)

When players play a card they make a public announcement that they were the owner of that card, if we look at the model for seven of clubs after South has played it, we can see that every player now knows that 'South owns seven of clubs'.
