import random
from knowledge import *
from rules_config_big import *

PLAYERS = ['East', 'South', 'West', 'North']

def find_best_Card(cards, player, trick):
    if len(cards) < 2:
        return cards[0] # speel je enige kaar
    elif not trick: # je komt uit
        trump = player.knowledge[0][1]
        print('player knows trump: ' + str(trump))
        high_card = max(cards, key=lambda card:card[1])

        if high_card[1] == TRUMP_POINTS['jack']: # player has the trump jack
            return high_card

        team_mate = player.team.players[1] if player.team.players[0] == player.name else player.team.players[0]
        trump_cards = [card for card in cards if card[1] == trump]

        if trump_cards != [0] and knows((team_mate, (trump, TRUMP_POINTS['jack'], 'jack'), False), player): # teammate has the trump jack
            return min(trump_cards, key=lambda card:card[2]) # play lowest trump

        other_team = [player for player in PLAYERS if player not in player.team.players]
        if high_card[0] != trump and high_card[2] == 'ace':
            for other_player in other_team:
                if not_knows_doesnt_have_suit(other_player, high_card[0], player) or not not_knows_doesnt_have_suit(other_player, trump, player):
                    return high_card

    else:
        return cards[random.randint(0, len(cards) - 1)]