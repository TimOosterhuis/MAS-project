![Model beginning game](/site_images/model.png)

# Object Oriented View of logical Klaverjas playing
Cards are modeled like a tuple holding the suit, the name of the card and the point value. For example: (‘hearts’, ‘king’, 4) is the tuple representing the king of hearts cards which is worth 4 points.

Classes and functions:

## Team Class:
This is a data class holding only the number of the team (1 or 2) and the names of the players in it.

## Trick Class:
This class holds multiple attributes for each round, which include: each played cards, score of the round, the winning player, the highest card, what is trump and which players played a card in a certain order.
It also holds a function that handles the adding of a new card to the round. The card and player are added to the attributes, the value of the new card is added to the score and if the card trumps the others or is of higher value the winner and high card attributes are also updated.
The last functions check the bonus that might be provided at the end of the round, and adds these to the score.

## Player Class:
Variables for this class are:
-	team, a Team class instance
-	closed_cards, a list holding the closed cards as tuples
-	open_cards, a list holding the open cards as tuples
-	own_cards, the combination of open_cards and closed_cards
-	turn, a integer representing the turn order in a trick
-	name, self-explanatory
-	all_cards, list of tuples holding all cards in the game
-	knowledge, a list holding tuples of the form (name, card, played), where name are the names of the other players, card can be any tuple representing a card and played is a Boolean representing if a card is played or not. This list holds all items a players knows for certain
-	possibles, a list of the same form as the knowledge list. But this list holds all the cards the player is uncertain about. This means that if a player (South) does not know whether the ace of spades is held by West, North or East, than this card is represented thrice in the list, as (‘West’, ( ‘Spades’, ‘Ace’, 11), False), (‘North, ( ‘Spades’, ‘Ace’, 11), False) and (‘East, ( ‘Spades’, ‘Ace’, 11), False)

Functions for this class are:
Play_card() is the function called when a player needs to play a card. It receives the trump and the trick if there is any yet. It will then first select the playable cards of the player by calling playable() from the rules_config_big.py file, after that it will select the best card from this list by calling find_best_card() from the tactics.py file (both these functions are explained later). Play_card() will then remove the found card from the open_cards or closed_cards list, depending on in which it was in, and then returns that card and the thoughts as found by the tactics.py function

Create_possibles() creates the possibles list. It looks at all the cards that are in the all_cards list and not in the knowledge list and creates three instances (for all the other players) in the possibles list for each card. Update_possibles() is a more interesting function, this function looks at the played cards in a trick and makes inferences based on that cards:
-	When a card is played, it is not possible anymore, so all instances in the possibles list holding that card are removed.
-	Next, when a player has played a card that is not of the same suit as the first played card, that player does not have that suit anymore, so all instances holding that players name and that suit in the card tuple are removed from the possibles list.
-	If the last played card is from a player that is not on the winning team and he played a non-trump card other options arise: If in the trick trump cards have been played this means that the last playing player doesn’t have a higher trump than the already played trump left. If there were no trump cards played and the player still didn’t play a trump card, this means he/she has no trump left at all. All suitable combinations are removed from the possibles list
-	If a player played a card that in rank is one lower than the highest already played card, this means that he/she cannot play a lower value card (in our setting of the game, this is not true in real life), so the player does not have any other cards of that suit left, and the suitable combinations are removed from the possibles list. For example: South starts with the ace of spades and West follows with the ten of spades. This means he has no other spades cards, and all combinations of West and spades are removed from the possibles list
-	Finally, when a card is only found once in the possibles list it is not possible anymore, but sure knowledge. The card is then removed from the possibles list and added to the knowledge list. For example, South has two trump cards left, and because East and West have not responded with trump cards when these were played the remaining trump cards are all in North’s possession.

## Rules_config_big.py
This file holds all information about the actual game, so the names of the suits are stored here, as well as the names of the players, the ranking and points of non-trump cards as well as the ranking and points of trump cards. The number of players, the number of rounds and the number of open and closed cards are also stored here. The number of closed cards is set manually to 8, but can be reduced so that players have more knowledge about the cards of the other players at the start of the game. The most interesting part of this file is the playable() function, that receives a list of cards, the team and the trick if there is any. If there is no trick, all cards are immediately returned as this means that the first player can play any card from his/her hand. If trump is asked, a list of higher trumps is first returned. If this does not exist a list of lower trump cards is returned. If this also doesn’t exist all cards are returned. When suit is called and the player still has suit left, all suit cards are returned. If the player does not have suit left and is on the losing team, all (higher) trump cards are returned if available, in all other cases all cards are returned.

## Tactics.py
This file holds three functions, the first being unplayed_trumps(), which returns all trump card that can still be played by any of the layers. The second function KM_suit searches for all instances in the knowledge and possibles lists of a player having a certain suit and returns this as a sorted list on the rank. So this function is called like KM_suit(‘South’, ‘West’, ‘hearts’) and will return a sorted list with all instances in the knowledge and possibles lists of South where (‘West’, (‘Hearts’, _, _)False) is true.
The most important and longest function in tactics.py Is find_best_card(), which receives the playable cards of a player, that player instance and the trick instance. This function returns one card if that is the only possible card, otherwise it analyses the turn of the player and goes through some options for each turn; For the first turn:
If there are still trump cards in play, and
-	If the player has the highest ranking trump card and knows or thinks one of the opponents has at least one trump card left, the player will play this highest trump card.
-	If the player knows that his teammate has this highest trump card, one of the opponents has a trump card left and the player himself has a trump card left, he will play this trump card
-	The player thinks both opponents still have a certain suit, and the player thinks they do not have a higher ranked suit card than his, he plays that highest ranked suit card. For example: South has the ten of spades and thinks both East and West still have spades but not higher than the ten, he will play the ten
If there are no trump cards in play anymore, the first player will search for a card that is higher than any cards the opponents can have, and will also play a card of which the opponents do not have suit anymore

For the second player:
If trump is called and the player still has trump cards, multiple options are available. If the second player thinks the third player doesn’t have trump anymore, it will play the lowest trump card that is higher than the one played by the first player (if this is available). If the second player thinks the third player still has trump, it will play a card of which he thinks is higher than what the third player can play. If that is not the case as well, the second player will play his lowest ranked available card.
If trump is called and the second player does not have trump anymore, he will play his lowest ranked available card.
In all other cases trump has not been played. When the second player has to play trump he plays his lowest ranked trump card. When he doesn’t have to play trump he thinks about what his opponent and teammate may have. If he thinks the third player (his opponent) doesn’t have suit anymore, he plays a card that is better than the first one if the also thinks the third player does not have trump. If he thinks the third player still has suit, he plays his best card if he thinks that is higher than the first card played and the highest possible card from the third player. The exception to this last is when he thinks his teammate has an even better card, than he plays his lowest ranked card. In all other situations the second player doesn’t think he or his teammate can win this trick, and thus plays his lowest card.

For the third player:
Again, this player looks at his own cards, the cards played and what he thinks the fourth player still has left. Only if the third player is sure that he can win the trick (so the fourth player will not have a higher suit card, or no suit and trump left) will he play the highest card so far, in all other cases he will play the lowest card playable.

For the fourth player:
This player knows if he can win this trick with his available cards or not, and so will try to win the trick with the highest card capable of that if he is on the losing team. If he cannot win or his team already wins this trick he will play his lowest playable card.

## Main.py
Excluding graphical details in this explanation, this where the match happens by our logical players. Here trump is chosen at random, the player instances are initialized and the cards are shuffled and dealt between the players. When this is done the knowledge of each player is created at the hand of their own cards and the open cards if any. When this is done each player assesses what he thinks is possible, and then South may start the match by playing his first card. In eight rounds, after each card is played the thoughts of the player are shown. After each card each player updates their knowledge and their uncertainty. After each round the winner of the round is shown at the bottom of the text field, and the scores are added to the correct team. After 8 rounds the programs shuts itself down automatically, but first calculates if the first team accumulated more than half of the points in the game. If they did, they keep the points. If they don’t, the other team receives all the points.


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
