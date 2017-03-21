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
    high_cards = sorted(cards, key=lambda card: card[2], reverse=True)
    if len(cards) < 2:
        return cards[0] # speel je enige kaart
    elif not trick: # je komt uit
        trump = player.knowledge[0][1]
        team_mate = player.team.players[1] if player.team.players[0] == player.name else player.team.players[0]


        hut = highest_unplayed_trump(player)
        trump_cards = sorted([card for card in cards if card[0] == trump], key=lambda tup:tup[2], reverse=True)
        #print trump_cards

        if hut != []:  # Still trump cards in play

            if trump_cards != []:

                if trump_cards[0][2] == hut[2]: # player has the highest trump   ( AND KNOWS / POSSIBLE OPPONENTS STILL DO TOO )
                    return high_cards[0]
                elif knows(player, (team_mate, hut, False)): # teammate has the highest trump in game ( AND KNOWS / POSSIBLE OPPONENTS STILL DO TOO )
                    return min(trump_cards, key=lambda card:card[2]) # play lowest trump

            other_team = [other for other in PLAYERS if other not in player.team.players]
            #if high_card[0] != trump and high_card[2] == 'ace':  # if highest point card is not a trump, but an ace!  (What if player has trump ace as well?
            #    for other_player in other_team:
            #        if not_knows_doesnt_have_suit(player, other_player, high_card[0]) or not not_knows_doesnt_have_suit(player, other_player, trump):
            #            return high_card
            #else:
            return high_cards[0]
        else:
            hunt = highest_unplayed_no_trump(player)
            return high_cards[0]
    else:
        hunt = highest_unplayed_no_trump(player)
        return high_cards[0]

def highest_unplayed_trump(player):
    played_trumps = [chunk[1] for chunk in player.knowledge if chunk[1][0] == player.knowledge[0][1] and chunk[2]]
    all_trumps = [chunk for chunk in player.all_cards if chunk[0] == player.knowledge[0][1]]
    unplayed_trumps = sorted([card for card in all_trumps if card not in played_trumps], key=lambda tup: tup[2], reverse=True)
    if len(unplayed_trumps) == 0:
        return []
    else:
        return unplayed_trumps[0]

def highest_unplayed_no_trump(player):
    played_cards = [chunk[1] for chunk in player.knowledge if chunk[1][0] != player.knowledge[0][1] and chunk[2]]
    unplayed_cards = sorted([card for card in player.all_cards if card not in played_cards], key=lambda tup:tup[2], reverse=True)
    return unplayed_cards