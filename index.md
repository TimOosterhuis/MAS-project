
## Visualisation of the agent knowledge

At every moment of the game it is possible to see what the players know and hold for possible regarding the card ownership of each card in the game. After each turn, a spectator can select a card via a dropdown menu in the main loop. A schematic S5 kripke model is then drawn for each card with the draw_model function, which calls on the player.knowledge and player.possible triples for each card to get the relations between the worlds. As card ownership is mutually exclusive in 'klaverjassen' (every card in the game is dealt to exactly one player), players never hold any worlds for possible where this is not the case, so for any card C with the corresponding propositional atoms (p1: south owns C, p2: west owns C, p3: north owns C, p4: east owns C) the S5 model includes only the the states (p1 = T, p2 = F, p3 = F, p4 = F), (p1 = F, p2 = T, p3 = F, p4 = F), (p1 = F, p2 = F, p3 = T, p4 = F) and (p1 = F, p2 = F, p3 = F, p4 = T).


