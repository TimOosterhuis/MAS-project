

def knows(statement, player):
    return True if statement in player.knowledge else False

def holds_for_possible(statement, player):
    return True if statement in player.knowledge else False