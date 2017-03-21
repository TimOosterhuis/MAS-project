import random
from knowledge import *
from rules_config_big import *

#-----------------------------------------------------------------------------------------------------------------------
# Tactics section, currently has function find best card, which determines the best card to play for a player given its
# playable cards, its knowledge and what it holds for possible, calls on the inference rules in knowledge.py
#
# not fully implemented yet
#-----------------------------------------------------------------------------------------------------------------------


def find_best_card(cards, player, trick):  # Find optimal card to return
    if len(cards) < 2:
        return cards[0] # speel je enige kaart
    elif not trick: # je komt uit
        trump = player.knowledge[0][1]
        team_mate = player.team.players[1] if player.team.players[0] == player.name else player.team.players[0]

        high_cards = sorted(cards, key=lambda card:card[2], reverse=True)
        hut = highest_unplayed_trump(player)
        trump_cards = sorted([card for card in cards if card[0] == trump], key=lambda tup:tup[2], reverse=True)
        print trump_cards

        if hut != []:  # Still trump cards in play

            if trump_cards[0][2] == hut[2]: # player has the highest trump   (( AND KNOWS / POSSIBLE OPPONENTS STILL DO TOO )
                return high_cards[0]

            if trump_cards != [] and knows(player, (team_mate, hut, False)): # teammate has the trump jack (( Rewrite to > highest trump in game ))
                return min(trump_cards, key=lambda card:card[2]) # play lowest trump

            other_team = [other for other in PLAYERS if other not in player.team.players]
            #if high_card[0] != trump and high_card[2] == 'ace':  # if highest point card is not a trump, but an ace!  (What if player has trump ace as well?
            #    for other_player in other_team:
            #        if not_knows_doesnt_have_suit(player, other_player, high_card[0]) or not not_knows_doesnt_have_suit(player, other_player, trump):
            #            return high_card
            #else:
            return cards[random.randint(0, len(cards) - 1)]
        else:
            return cards[random.randint(0, len(cards) - 1)]
    else:
        return cards[random.randint(0, len(cards) - 1)]

def highest_unplayed_trump(player):
    played_trumps = [chunk[1] for chunk in player.knowledge if chunk[1][0] == player.knowledge[0][1] and chunk[2]]
    all_trumps =[chunk for chunk in player.all_cards if chunk[0] == player.knowledge[0][1]]
    unplayed_trumps = sorted([card for card in all_trumps if card not in played_trumps], key=lambda tup: tup[2], reverse=True)
    if len(unplayed_trumps) == 0:
        return []
    else:
        return unplayed_trumps[0]
