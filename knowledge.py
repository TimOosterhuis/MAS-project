

#-----------------------------------------------------------------------------------------------------------------------
#knowledge, contains inference rules that can be made using what a player knows and holds for possible
# variable names statement and chunk are used both and mean the same
#-----------------------------------------------------------------------------------------------------------------------


def knows(player, statement):
    return True if statement in player.knowledge else False

def holds_for_possible(player, statement):
    return True if statement in player.possibles else False

def not_knows_doesnt_have_suit(player, other, suit):
    other_cards = [statement[1] for statement in player.knowledge if statement[0] == other]
    other_cards.extend([statement[1] for statement in player.possibles if statement[0] == other])
    return len([card for card in other_cards if card[0] == suit] > 0)