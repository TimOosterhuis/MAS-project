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
    trump = player.knowledge[0][1]
    high_cards = sorted(cards, key=lambda card: card[2], reverse=True)
    other_team = [other for other in PLAYERS if other not in player.team.players]
    team_mate = player.team.players[1] if player.team.players[0] == player.name else player.team.players[0]
    if len(cards) < 2:
        return cards[0] # speel je enige kaart
    elif not trick: # je komt uit


        ut = unplayed_trumps(player)
        trump_cards = sorted([card for card in cards if card[0] == trump], key=lambda tup:tup[2], reverse=True)

        if ut != []:  # Still trump cards in play
            high_cards_no_trump = [card for card in high_cards if card[0] != trump]

            opt = opponents_KM_trump(player, team_mate)  # K(opponent has trump) and M(opponent has trump)

            if trump_cards != []:   # Player still has trump cards

                if trump_cards[0][2] == ut[0][2] and opt != []: # player has the highest trump and KM(opponent has trump)
                    return high_cards[0]
                elif knows(player, (team_mate, ut[0], False)) and opt != []: # teammate has the highest trump in game and KM(opponent has trump)
                    return min(trump_cards, key=lambda card:card[2]) # play lowest trump

            for card in high_cards:  # High to low card value
                if card[0] == trump:  # Ignore trump cards
                    pass
                else:
                    KM_opp0 = KM_suit(player, other_team[0], card[0])
                    KM_opp1 = KM_suit(player, other_team[1], card[0])
                    if len(KM_opp0)>=1 and len(KM_opp1)>=1:
                        if card[2] > KM_opp0[0][1][2] and card[2] > KM_opp1[0][1][2]:
                        # Both opponents probably still have suit, and no higher card in that suit
                            return card

            # If all tactics fail, just go with the lowest value card (trump or not)
            return high_cards_no_trump[-1]
        else:
            for card in high_cards:  # No trumps left, high to low card
                KM_opp0 = KM_suit(player, other_team[0], card[0])
                KM_opp1 = KM_suit(player, other_team[1], card[0])
                if len(KM_opp0) >= 1 and len(KM_opp1) >= 1:
                    if card[2] > KM_opp0[0][1][2] and card[2] > KM_opp1[0][1][2]:
            #        # Both opponents probably still have suit, and no higher card in that suit
                        return card
            return high_cards[-1]

    elif len(trick.cards) == 1:  # player mag als tweede uitkomen
        opp_left = [name for name in other_team if name != trick.players[0].name]
        KM_opp1_s = KM_suit(player, opp_left[0], trick.cards[0][0])
        if KM_opp1_s == []:
            KM_opp1_t = KM_suit(player, opp_left[0], trump)
        KM_team = KM_suit(player, team_mate, trick.cards[0][0])

        if trick.cards[0][0] == trump and high_cards[0][0] == trump:  #  troef gevraagd en heb nog troef
            if KM_opp1_s == []:  # Door rules al hogere troef dan uitgekomen (als mogelijk) in lijst. Als tegenstander heen troef meer heeft dan laagste mogeljike opgooien
                return high_cards[-1]
            elif high_cards[0][2] > trick.cards[0][2] and high_cards[0][2] > KM_opp1_s[0][2]: # Als mogelijke kaart ook hoger is dan hoogst mogelijke kaart van andere tegenstander
                return high_cards[0]
            else:
                return high_cards[-1]

        if trick.cards[0][0] == trump and high_cards[0][0] != trump:  # troef gevraagd en heb niet meer
            return high_cards[-1]

        if high_cards[0][0] != trump:  # Player hoeft niet in te troeven

            if KM_opp1_s == []: # derde speler heeft geen suit meer

                if KM_opp1_t != []:  # maar waarschijnlijk nog wel troef
                    return high_cards[-1]
                elif high_cards[0][2] > trick.cards[0][2]:  # derde speler geen troef, player hoger dan eerste kaart
                    return high_cards[0]
                else:
                    return high_cards[-1]  # Derde speler geen troef, maar geen hogere kaart dan eerste
            elif high_cards[0][2] > trick.cards[0][2] and high_cards[0][2] > KM_opp1_s[0][2]:  # Derde speler nog suit, maar kaart hoger dan hoogste daarvan en eerste kaart
                if KM_team != []:  # teamgenoot heeft ook nog suit
                    if high_cards[0][2] < KM_team[0][2]: # Hogere suit zelfs
                        return high_cards[-1]
                    else:   # Maar lagere suit
                        return high_cards[0]
                else: # Teamgenoot heeft geen suit meer
                    return high_cards[0]
            else:  # geen troef gespeeld, geen hogere kaart dan opponents
                return high_cards[-1]
        else:  # player moet introeven
            return high_cards[-1]

    elif len(trick.cards) == 2:  # Player mag als derde uitkomen
        opp_left = [name for name in other_team if name != trick.players[1].name]
        KM_opp1_s = KM_suit(player, opp_left[0], trick.cards[0][0])
        if KM_opp1_s == []:
            KM_opp1_t = KM_suit(player, opp_left[0], trump)

        if trick.cards[0][0] == trump and high_cards[0][0] == trump:  # troef gevraagd en heb nog troef
            if KM_opp1_s == []:  # Door rules al hogere troef dan uitgekomen (als mogelijk) in lijst. Als tegenstander geen troef meer heeft dan laagste mogeljike opgooien
                return high_cards[-1]
            elif high_cards[0][2] > KM_opp1_s[0][2]:  # Als hoogste kaart hoger is dan waarschijnlijk hoogste kaart van laatste speler
                if trick.cards[1][0] == trick.trump and high_cards[0][2] > trick.cards[0][2]:  # Als tweede kaart ook troef was en hoogste kaart hoger dan die
                    return high_cards[0]
                else:
                    return high_cards[-1]
            else:
                return high_cards[-1]

        if trick.cards[0][0] == trump and high_cards[0][0] != trump:  # troef gevraagd en heb niet meer
            return high_cards[-1]

        if high_cards[0][0] != trump:  # Player hoeft niet in te troeven ---- ALLEEN DEZE NOG!!!
            return high_cards[0]
        else:  # player moet introeven
            return high_cards[-1]
    else:  # Player mag als vierde uitkomen  - Onderstaande is al compleet
        if trick.winner.team != player.team and high_cards[0][0] == trick.high_card[0] and high_cards[0][2] > trick.high_card[2]:
            return high_cards[0]
        else:
            return high_cards[-1]

def unplayed_trumps(player):
    trump = player.knowledge[0][1]
    played_trumps = [chunk[1] for chunk in player.knowledge if chunk[1][0] == trump and chunk[2]]
    all_trumps = [chunk for chunk in player.all_cards if chunk[0] == trump]
    unplayed_trump = sorted([card for card in all_trumps if card not in played_trumps], key=lambda tup: tup[2], reverse=True)
    return unplayed_trump

def opponents_KM_trump(player, team_mate):
    trump = player.knowledge[0][1]
    opponent_M_trumps = [chunk for chunk in player.possibles if chunk[0] != player.name and chunk[0] != team_mate and chunk[1][0] == trump]
    opponent_K_trumps = [chunk for chunk in player.knowledge if chunk[0] != player.name and chunk[0] != team_mate and chunk[1][0] == trump and not chunk[2]]
    opponent_K_trumps.extend(opponent_M_trumps)
    #print(player.name + ' holds for possible (opponent trumps): ' + str(opponent_K_trumps))
    return opponent_K_trumps

def KM_suit(player, other_player, suit):
    K_opp_suit = [chunk for chunk in player.knowledge if chunk[0] == other_player and chunk[1][0] == suit]
    M_opp_suit = [chunk for chunk in player.possibles if chunk[0] == other_player and chunk[1][0] == suit]
    K_opp_suit.extend(M_opp_suit)
    to_return = sorted(K_opp_suit, key=lambda tup:tup[1][2], reverse=True)
    return to_return



