import random
from knowledge import *

def find_best_Card(cards, player, trick):
    if len(cards) < 2:
        return cards[0] # speel je enige kaar
    elif not trick: # je komt uit
        high_card = max(cards, key=lambda card:card[2])
        if high_card[2] == 26: # player has the trump jack
            return high_card
        team_mate = player.team#[1] if player.team[0] == player.name else player.team[0]
        trump_cards = [card for card in cards if card[1] == trick.trump]
        if trump_cards != [0] and knows((team_mate, (trick.trump, 26, 'jack'), False), player): # teammate has the trump jack
            return min(trump_cards, key=lambda card:card[2]) # play lowest trump
        other_team = [player for player in ['East', 'South', 'West', 'North'] if player not in player.team]
        for other_player in other_team:
            if knows(player, ())

    else:
        return cards[random.randint(0, len(cards) - 1)]