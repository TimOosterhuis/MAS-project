
#Visualisation of the agent knowledge#

At every moment of the game it is possible to see what the players know and hold for possible regarding the card ownership of each card in the game. After each turn, a spectator can select a card via a dropdown menu in the main loop. A schematic S5 kripke model is then drawn for each card with the draw_model function, which calls on the player.knowledge and player.possible triples for each card to get the relations between the four worlds. As card ownership is mutually exp
