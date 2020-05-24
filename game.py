
CardType = {
    "SPADES": 0,
    "CLUBS": 1,
    "HEARTS": 2,
    "DIAMONDS": 3
}


CardColor = {
    "BLACK": [0, 1], # Spades and Clubs are black
    "RED": [2, 3] # Hearts and diamonds are white
}


def find_type_of_card(card):
    letter = card[0]

    if letter == 'H' or letter == 'h':
        return CardType["HEARTS"]
    elif letter == 'C' or letter == 'c':
        return CardType["CLUBS"]
    elif letter == 'D' or letter == 'd':
        return CardType["DIAMONDS"]
    elif letter == 'S' or letter == 's':
        return CardType["SPADES"]
    else:
        return None

def find_value_of_card(card):
    initial_value = int(card[1:])

    if type(initial_value) != int:
        return None
    return initial_value

def find_color_of_card(card):
    for key in CardColor.keys():
        if find_type_of_card(card) in CardColor[key]:
            return key
    return None

def is_opposite_color(cardA, cardB):
    if find_color_of_card(cardA) != find_color_of_card(cardB):
        return True
    return False

# Checks if the CardA could be put above the cardB in a Stack and the opposite
def stacks_rule(cardA, cardB):
    if is_opposite_color(cardA, cardB):
        valueBetweenCards = find_value_of_card(cardA) - find_value_of_card(cardB)
        if valueBetweenCards is 1:
            return 1 # cardB will be moved below cardA
        elif valueBetweenCards is -1:
            return -1 # cardA will be moved below cardB
        else:
            return 0 # The move between cards is not allowed

# Checks whether a card can be put in the foundation list
def foundationRule(value_of_card, foundationList):
    if not foundationList:
        foundationValue = -1
    else:
        foundationValue = find_value_of_card(foundationList[-1])
    return value_of_card == foundationValue + 1






