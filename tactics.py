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
    thoughts = []
    trump = player.knowledge[0][1]
    high_cards = sorted(cards, key=lambda card: card[2], reverse=True)
    other_team = [other for other in PLAYERS if other not in player.team.players]
    team_mate = player.team.players[1] if player.team.players[0] == player.name else player.team.players[0]
    if len(cards) < 2:
        thought = player.name + ' can only play one card'
        thoughts.append(thought)
        if explain:
            print(thoughts)
        return cards[0], thoughts # speel je enige kaart
    elif not trick: # je komt uit

        ut = unplayed_trumps(player)
        trump_cards = sorted([card for card in cards if card[0] == trump], key=lambda tup:tup[2], reverse=True)

        if ut != []:  # Still trump cards in play
            thought = player.name + ' knows there are still trump cards in play'
            thoughts.append(thought)
            if explain:
                print(thought)
            high_cards_no_trump = [card for card in high_cards if card[0] != trump]

            opt = KM_suit(player, other_team[0], trump)
            op2 = KM_suit(player, other_team[1], trump)
            opt.extend(op2)
            print opt

            if trump_cards != []:   # Player still has trump cards

                if trump_cards[0][2] == ut[0][2] and opt != []: # player has the highest trump and KM(opponent has trump)
                    thought = player.name + ' has highest unplayed trump card and KM opponent at least one trump card left '
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[0], thoughts
                elif knows(player, (team_mate, ut[0], False)) and opt != []: # teammate has the highest trump in game and KM(opponent has trump)
                    thought = player.name + ' knows teammate has highest unplayed trump, has trump himself and KM opponent at lest one trump card left'
                    thoughts.append(thought)
                    if explain:
                        print(thoughts)
                    return min(trump_cards, key=lambda card:card[2]), thoughts # play lowest trump

            for card in high_cards:  # High to low card value
                if card[0] == trump:  # Ignore trump cards
                    pass
                else:
                    KM_opp0 = KM_suit(player, other_team[0], card[0])
                    KM_opp1 = KM_suit(player, other_team[1], card[0])
                    if len(KM_opp0)>=1 and len(KM_opp1)>=1:
                        if card[2] > KM_opp0[0][1][2] and card[2] > KM_opp1[0][1][2]:
                        # Both opponents probably still have suit, and no higher card in that suit
                            thought = player.name + ' thinks ' + str(card) + ' is a better card than his opponents have (and thinks he cannot win with trump)'
                            thoughts.append(thought)
                            if explain:
                                print(thought)
                            return card, thoughts

            # If all tactics fail, just go with the lowest value card (trump or not)
            thought = player.name + ' cannot think of a good card to play, and thus plays his lowest value card'
            thoughts.append(thought)
            if explain:
                print(thought)
            return high_cards[-1], thoughts
        else:
            thought = player.name + ' knows there are no more trump cards in play'
            thoughts.append(thought)
            if explain:
                print(thought)
            for card in high_cards:  # No trumps left, high to low card
                KM_opp0 = KM_suit(player, other_team[0], card[0])
                KM_opp1 = KM_suit(player, other_team[1], card[0])
                if len(KM_opp0) >= 1 and len(KM_opp1) >= 1:
                    if card[2] > KM_opp0[0][1][2] and card[2] > KM_opp1[0][1][2]:
            #        # Both opponents probably still have suit, and no higher card in that suit
                        thought = player.name + ' has checked all cards from high to low value, and thinks the opponents do not have a higher value card than:'
                        thoughts.append(thought)
                        if explain:
                            print(thought)
                        return card, thoughts
                elif len(KM_opp0) >= 0 and len(KM_opp1) == 0:
                    if card[2] > KM_opp0[0][1][2]:
                        thought = player.name + ' has checked all cards from high to low value, and thinks the opponents do not have a higher value card than:'
                        thoughts.append(thought)
                        if explain:
                            print(thought)
                        return card, thoughts
                elif len(KM_opp0) == 0 and len(KM_opp1) >= 1:
                    if card[2] > KM_opp1[0][1][2]:
                        thought = player.name + ' has checked all cards from high to low value, and thinks the opponents do not have a higher value card than:'
                        thoughts.append(thought)
                        if explain:
                            print(thought)
                        return card, thoughts
                elif len(KM_opp0) == 0 and len(KM_opp1) == 0:
                    thought = player.name + ' has checked all cards from high to low value, and thinks the opponents do not have this suit anymore:'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return card, thoughts
            thought = player.name + ' has checked all his cards, and does not think it can win this round, therefor plays his lowest card'
            thoughts.append(thought)
            if explain:
                print(thought)
            return high_cards[-1], thoughts

    elif len(trick.cards) == 1:  # player mag als tweede uitkomen
        opp_left = [name for name in other_team if name != trick.players[0].name]
        KM_opp1_s = KM_suit(player, opp_left[0], trick.cards[0][0])
        if KM_opp1_s == []:
            KM_opp1_t = KM_suit(player, opp_left[0], trump)
        KM_team = KM_suit(player, team_mate, trick.cards[0][0])

        if trick.cards[0][0] == trump and high_cards[0][0] == trump:  #  troef gevraagd en heb nog troef
            thought = player.name + ' has trump and trump is asked'
            thoughts.append(thought)
            if explain:
                print(thought)
            if KM_opp1_s == []:  # Door rules al hogere troef dan uitgekomen (als mogelijk) in lijst. Als tegenstander heen troef meer heeft dan laagste mogeljike opgooien
                thought = player.name + ' has higher trump than played card and knows that the other opponent does not have trump anymore, so he can play the lowest value over the played card'
                thoughts.append(thought)
                if explain:
                    print(thought)
                return high_cards[-1], thoughts
            elif high_cards[0][2] > trick.cards[0][2] and high_cards[0][2] > KM_opp1_s[0][1][2]: # Als mogelijke kaart ook hoger is dan hoogst mogelijke kaart van andere tegenstander
                thought = player.name + ' knows his highest value card is of higher value than the highest possible card that his opponent can have, and thus plays that one'
                thoughts.append(thought)
                if explain:
                    print(player.name + ' knows his highest value card is of higher value than the highest possible card that his opponent can have, and thus plays that one')
                return high_cards[0], thoughts
            else:
                thought = player.name + ' knows he cannot win this round, and thus plays his lowest value card'
                thoughts.append(thought)
                if explain:
                    print(thought)
                return high_cards[-1], thoughts

        if trick.cards[0][0] == trump and high_cards[0][0] != trump:  # troef gevraagd en heb niet meer
            thought = player.name + ' knows trump is called, but he does not have trump anymore. Thus plays lowest value card of other suit'
            thoughts.append(thought)
            if explain:
                print(thought)
            return high_cards[-1], thoughts

        if high_cards[0][0] != trump:  # Player hoeft niet in te troeven
            thought = player.name + ' does not have to play a trump card'
            thoughts.append(thought)
            if explain:
                print(thought)

            if KM_opp1_s == []: # derde speler heeft geen suit meer
                thought = player.name + ' knows third player does not have suit anymore'
                thoughts.append(thought)
                if explain:
                    print(thought)

                if KM_opp1_t != []:  # maar waarschijnlijk nog wel troef
                    thought = player.name + ' suspects third player from still having trump, and thus plays lowest value card'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[-1], thoughts
                elif high_cards[0][2] > trick.cards[0][2]:  # derde speler geen troef, player hoger dan eerste kaart
                    thought = player.name + ' knows third player does not have trump anymore, and has card higher than first card played'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[0], thoughts
                else:
                    thought = player.name + ' knows third player does not have trump anymore, but also does not have a higher card than the first one played himself. So plays lowest possible card'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[-1], thoughts  # Derde speler geen troef, maar geen hogere kaart dan eerste
            elif high_cards[0][2] > trick.cards[0][2] and high_cards[0][2] > KM_opp1_s[0][1][2]:  # Derde speler nog suit, maar kaart hoger dan hoogste daarvan en eerste kaart
                thought = player.name + ' has a higher card than the played one, as well as what he thinks the highest suit card of the third player is'
                thoughts.append(thought)
                if explain:
                    print(thought)
                if KM_team != []:  # teamgenoot heeft ook nog suit
                    if high_cards[0][2] < KM_team[0][1][2]: # Hogere suit zelfs
                        thought = player.name + ' knows/thinks that his teammate even has a higher card than his highest, and thus plays a low card'
                        thoughts.append(thought)
                        if explain:
                            print(thought)
                        return high_cards[-1], thoughts
                    else:   # Maar lagere suit
                        thought = player.name + ' knows/thinks that his teammate has a lower card than his highest, and thus plays this highest card'
                        thoughts.append(thought)
                        if explain:
                            print(thought)
                        return high_cards[0], thoughts
                else: # Teamgenoot heeft geen suit meer
                    thought = player.name + ' knows his teammate does not have suit anymore, and thus plays his highest card to win'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[0], thoughts
            else:  # geen troef gespeeld, geen hogere kaart dan opponents
                thought = player.name + ' knows that there has been no trump played, but does not have a higher suit card than what he thinks his opponents have'
                thoughts.append(thought)
                if explain:
                    print(thought)
                return high_cards[-1], thoughts
        else:  # player moet introeven
            thought = player.name + ' has to play a trump card, and plays his lowest option'
            thoughts.append(thought)
            if explain:
                print(thought)
            return high_cards[-1], thoughts

    elif len(trick.cards) == 2:  # Player mag als derde uitkomen
        opp_left = [name for name in other_team if name != trick.players[1].name]
        KM_opp1_s = KM_suit(player, opp_left[0], trick.cards[0][0])
        if KM_opp1_s == []:
            KM_opp1_t = KM_suit(player, opp_left[0], trump)

        if trick.cards[0][0] == trump and high_cards[0][0] == trump:  # troef gevraagd en heb nog troef
            thought = player.name + ' has trump while trump is called'
            thoughts.append(thought)
            if explain:
                print(thought)
            if KM_opp1_s == []:  # Door rules al hogere troef dan uitgekomen (als mogelijk) in lijst. Als tegenstander geen troef meer heeft dan laagste mogeljike opgooien
                thought = player.name + ' has higher trump than played trump and knows that the other opponent does not have trump anymore, so he can play the lowest value over the played card'
                thoughts.append(thought)
                if explain:
                    print(thought)
                return high_cards[-1], thoughts
            elif high_cards[0][2] > KM_opp1_s[0][1][2]:  # Als hoogste kaart hoger is dan waarschijnlijk hoogste kaart van laatste speler
                thought = player.name + ' thinks he has a higher value card than the fourth player'
                thoughts.append(thought)
                if explain:
                    print(thought)
                if trick.cards[1][0] == trick.trump and high_cards[0][2] > trick.cards[1][2]:  # Als tweede kaart ook troef was en hoogste kaart hoger dan die
                    thought = player.name + ' must play the higher trump card'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[0], thoughts
                else:
                    thought = player.name + ' plays his lowest value card, because it is not higher than the already played card'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[-1], thoughts
            else:
                thought = player.name + ' knows he does not have higher value trump cards than the fourth player, and thus plays his lowest possible card'
                thoughts.append(thought)
                if explain:
                    print(thought)
                return high_cards[-1], thoughts

        if trick.cards[0][0] == trump and high_cards[0][0] != trump:  # troef gevraagd en heb niet meer
            thought = player.name + ' knows trump is called, but he does not have trump anymore, and thus plays his lowest possible card'
            thoughts.append(thought)
            if explain:
                print(thought)
            return high_cards[-1], thoughts

        if high_cards[0][0] != trump:  # Player hoeft niet in te troeven
            thought = player.name + ' does not have to play trump'
            thoughts.append(thought)
            if explain:
                print(thought)
            if KM_opp1_s == []: # vierde speler heeft geen suit meer
                thought = player.name + ' thinks the fourth player does not have suit anymore'
                thoughts.append(thought)
                if explain:
                    print(thought)
                if KM_opp1_t != []:  # maar waarschijnlijk nog wel troef
                    thought = player.name + ' suspects the fourth player from still having suit, and therefor plays his lowest card'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[-1], thoughts
                elif high_cards[0][2] > trick.cards[1][2]:  # vierde speler geen troef, player hoger dan tweede kaart
                    thought = player.name + ' thinks the fourth player does not have trump anymore, and himself has a higher card than the second played card. Play the highest card!'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[0], thoughts
                else:
                    thought = player.name + ' thinks the fourth player does not have trump anymore, but himself does not have a higher card than the second played card'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[-1], thoughts  # vierde speler geen troef, maar geen hogere kaart dan tweede
            elif high_cards[0][2] > trick.cards[1][2] and high_cards[0][2] > KM_opp1_s[0][1][2]:  # vierde speler nog suit, maar kaart hoger dan hoogste van suit en tweede kaart
                if high_cards[0][2] < trick.cards[0][2]:
                    thought = player.name + ' thinks he has a higher card than the played one and one his opponent may play, but his teammate has an even higher one. So he plays a low card'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return  high_cards[-1], thoughts
                else: # Teamgenoot heeft geen suit meer
                    thought = player.name + ' thinks he has a higher card than the played one and one his opponent may play, so he plays this'
                    thoughts.append(thought)
                    if explain:
                        print(thought)
                    return high_cards[0], thoughts
            else:  # geen troef gespeeld, geen hogere kaart dan opponents
                thought = player.name + ' know there is no trump played, but cannot win with his own cards, so plays a low value card'
                thoughts.append(thought)
                if explain:
                    print(thought)
                return high_cards[-1], thoughts

        else:  # player moet introeven
            if explain:
                thought = player.name + ' has to play a trump card, and plays his lowest option'
                thoughts.append(thought)
                print(thought)
            return high_cards[-1], thoughts
    else:  # Player mag als vierde uitkomen
        if trick.winner.team != player.team and high_cards[0][0] == trick.high_card[0] and high_cards[0][2] > trick.high_card[2]:
            thought = player.name + ' is on the losing team, but has higher cards than the winning card, and thus plays this'
            thoughts.append(thought)
            if explain:
                print(thought)
            return high_cards[0], thoughts
        else:
            thought = player.name + ' can not win with suit, and thus plays lowest suit card. Or player must trump and thus plays lowest trump'
            thoughts.append(thought)
            if explain:
                print(thought)
            return high_cards[-1], thoughts

def unplayed_trumps(player):
    trump = player.knowledge[0][1]
    played_trumps = [chunk[1] for chunk in player.knowledge if chunk[1][0] == trump and chunk[2]]
    all_trumps = [chunk for chunk in player.all_cards if chunk[0] == trump]
    unplayed_trump = sorted([card for card in all_trumps if card not in played_trumps], key=lambda tup: tup[2], reverse=True)
    return unplayed_trump


def KM_suit(player, other_player, suit):
    K_opp_suit = [chunk for chunk in player.knowledge if chunk[0] == other_player and chunk[1][0] == suit and not chunk[2]]
    M_opp_suit = [chunk for chunk in player.possibles if chunk[0] == other_player and chunk[1][0] == suit and not chunk[2]]
    K_opp_suit.extend(M_opp_suit)
    to_return = sorted(K_opp_suit, key=lambda tup:tup[1][2], reverse=True)
    return to_return



