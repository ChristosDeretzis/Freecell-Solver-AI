import game
import copy
import math

class TreeNode(object):
    def __init__(self, game, parent, move, f, g, h):
        self.game = game
        self.parent = parent
        self.move = move
        self.f = f
        self.h = h
        self.g = g
        self.children = []


    # finds the children of a TreeNode object
    def find_children(self, method):
        moves = self.find_possible_moves()

        for state in moves:
            g = self.g + 1
            if method == 'astar':
                h = self.heuristic()
                f = h + g
                self.children.append(TreeNode(state[0], self, state[1], f=f, g=g, h=h))
            elif method == 'best':
                h = self.heuristic()
                self.children.append(TreeNode(state[0], self, state[1], f=h, g=g, h=h))
            else:
                self.children.append(TreeNode(state[0], self, state[1], f=0, g=g, h=0))


    """ This function finds all the possible moves in the game"""
    def find_possible_moves(self):
        state = []

        emptyFreecellExaminined = False

        # loop for every freecell card
        for i in range(4):
            if self.game["freecell"][i] != None:
                # MOVE CARD FROM FREECELL TO FOUNDATION

                type_of_card = game.find_type_of_card(self.game["freecell"][i])
                value_of_card = game.find_value_of_card(self.game["freecell"][i])
                foundation_list = self.game["foundation"][type_of_card]

                # if the card can be put to the foundation list, then add it
                if game.foundationRule(value_of_card, foundation_list):
                    new_game, move = self.move_from_freecell_to_foundation(i, type_of_card)
                    state.append([new_game, move])
                    continue

                # END MOVE CARD FROM FREECELL TO FOUNDATION

                # MOVE CARD FROM FREECELL TO STACK
                for j in range(1,9):
                    current_stack = self.game["stack"][j]

                    # if the current stack is empty, then put the foundation card to that empty stack
                    # else, check if the card can be put to the stack and add the card to the stack
                    if not current_stack:
                        new_game, move = self.move_from_freecell_to_empty_stack(i, j)
                        state.append([new_game, move])
                        continue
                    elif game.stacks_rule(current_stack[-1], self.game["freecell"][i]) is 1:
                        new_game, move = self.move_from_freecell_to_stack(i,j)
                        state.append([new_game, move])
                        continue
            #     # END MOVE CARD FROM STACK TO STACK

        emptyFreecellExaminined = False
        for i in range(4):
            if self.game["freecell"][i] is None:
                # MOVE CARD FROM STACK TO FREECELL(ONLY 1 CARD)
                if not emptyFreecellExaminined:
                    for j in range(1,9):
                        if not self.game["stack"][j]:
                            continue
                        else:
                            new_game, move = self.move_from_stack_to_freecell(j, i)
                            state.append([new_game, move])
                            emptyFreecellExaminined = True
                #END MOVE CARD FROM FREECELL TO STACK
        # end of loop of freecell cards

        # loop the stacks
        for i in range(1,9):
            if self.game["stack"][i]:
                # MOVE CARD FROM STACK TO FOUNDATION
                last_card_of_stack = self.game["stack"][i][-1]
                value_of_card = game.find_value_of_card(last_card_of_stack)
                type_of_card = game.find_type_of_card(last_card_of_stack)
                if game.foundationRule(value_of_card, self.game["foundation"][type_of_card]):
                    new_game, move = self.move_from_stack_to_foundation(i, type_of_card);
                    state.append([new_game, move])
                    continue
                # END MOVE CARD FROM STACK TO FOUNDATION

            # MOVE CARD FROM STACK TO ANOTHER STACK
            for j in range(i+1, 9):
                sourceStackId = 0
                targetStackId = 0
                if self.game["stack"][i] == [] and self.game["stack"][j] == []:
                    continue
                elif self.game["stack"][i] == [] and self.game["stack"][j] != []:
                    if len(self.game["stack"][j]) == 1:
                        continue
                    else:
                        sourceStackId = j
                        targetStackId = i
                elif self.game["stack"][i] != [] and self.game["stack"][j] == []:
                    if len(self.game["stack"][i]) == 1:
                        continue
                    else:
                        sourceStackId = i
                        targetStackId = j
                elif self.game["stack"][i] != [] and self.game["stack"][j] != []:
                    card_a = self.game["stack"][i][-1]
                    card_b = self.game["stack"][j][-1]
                    if game.stacks_rule(card_a, card_b) == 1:
                        sourceStackId = j
                        targetStackId = i
                    elif game.stacks_rule(card_a, card_b) == -1:
                        sourceStackId = i
                        targetStackId = j
                    else:
                        continue

                new_game, move = self.move_from_stack_to_stack(targetStackId, sourceStackId)
                state.append([new_game, move])
        # end loop of the stacks

        return state




    def move_from_freecell_to_foundation(self,freecell_position, foundation_stack):
        copy_game = copy.deepcopy(self.game)

        card = copy_game["freecell"][freecell_position]

        # Remove the Card from Freecell
        copy_game["freecell"][freecell_position] = None

        # Put the card of the freecell to the foundation it belongs
        copy_game["foundation"][foundation_stack].append(card)

        return copy_game, ("foundation", card)

    def move_from_freecell_to_empty_stack(self, freecell_position, stack_number):
        copy_game = copy.deepcopy(self.game)

        freecell_card = copy_game["freecell"][freecell_position]
        copy_game["freecell"][freecell_position] = None;

        copy_game["stack"][stack_number].append(freecell_card);

        return copy_game, ("source", freecell_card)

    def move_from_freecell_to_stack(self, freecell_position, numberOfStack):
        copy_game = copy.deepcopy(self.game)

        freecell_card = copy_game["freecell"][freecell_position]

        if copy_game["stack"][numberOfStack] is []:
            copy_game["freecell"][freecell_position] = None

            copy_game["stack"][numberOfStack].append(freecell_card)

            return copy_game, ("source", freecell_card)
        else:
            lastCardOfStack = copy_game["stack"][numberOfStack][-1] #Get last element from stack

            if game.stacks_rule(lastCardOfStack, freecell_card) == 1:
                copy_game["freecell"][freecell_position] = None

                copy_game["stack"][numberOfStack].append(freecell_card)

                return copy_game, ("stack", freecell_card, lastCardOfStack)
        return None

    def move_from_stack_to_stack(self, source_stack, target_stack):
        copy_game = copy.deepcopy(self.game)

        last_target_stack = copy_game["stack"][target_stack].pop()


        if not copy_game["stack"][source_stack]:
            copy_game["stack"][source_stack].append(last_target_stack)
            move = ('source', last_target_stack)
        else:
            last_source_stack = copy_game["stack"][source_stack][-1]
            copy_game["stack"][source_stack].append(last_target_stack)
            move = ('stack', last_target_stack, last_source_stack)

        return copy_game, move

    def move_from_stack_to_freecell(self, stackNumber, freecell_number):
        copyGame = copy.deepcopy(self.game)

        card = copyGame["stack"][stackNumber].pop()

        copyGame["freecell"][freecell_number] = card

        return copyGame, ("freecell", card)

    def move_from_stack_to_foundation(self, stackNumber, foundation_list):
        copyGame = copy.deepcopy(self.game)

        card = copyGame["stack"][stackNumber].pop()

        copyGame["foundation"][foundation_list].append(card)

        return copyGame, ("foundation", card)

    def is_goal(self):
        # A game is a goal if all of the cards have been put in the foundations

        for i in range(4):
            if len(self.game["foundation"][i]) < 13:
                return False
        return True

    # this functions finds all the steps that need to be done in order to find the solution
    def extract_solution(self):

        path = []
        temp_node = copy.copy(self)
        while temp_node is not None:
            if temp_node.move is not None:
                path.append(temp_node.move)
            temp_node = temp_node.parent

        return path

    """ The heuristic function gives more emphasis to the cards that are not in the foundation and less to the cards that are not in the correct order"""
    def heuristic(self):
        copy_game = copy.deepcopy(self.game)

        # The higher the value of a card in the freecell or any stack that is not in the foundation
        # the lower the penalty it gets
        cards_not_in_foundation_penalty = 0
        for card in copy_game["freecell"]:
            if card is not None:
                value_of_card = game.find_value_of_card(card)
                cards_not_in_foundation_penalty += abs(13 - value_of_card)

        for stackNum in copy_game["stack"]:
            for card in copy_game["stack"][stackNum]:
                if card is not None:
                    value_of_card = game.find_value_of_card(card)
                    cards_not_in_foundation_penalty += abs(13 - value_of_card)

        # Penalty for cards in the stack that are not in order
        cards_order_penalty = 0
        for key in copy_game["stack"]:
            cards_order_penalty += self.ordering_penalty(copy_game["stack"][key])

        return int(0.75*cards_not_in_foundation_penalty + 0.25*cards_order_penalty )

    # This functions calculates the penalty
    # for the for 2 cards in the stack. If 2 consecutive cards do not follow the stack rule, then add 1 to the penalty
    def ordering_penalty(self, stack):
        penalty = 0;

        for i in range(len(stack) - 1):
            card_a = stack[i]
            card_b = stack[i+1]
            if game.stacks_rule(card_a, card_b) != 1:
                penalty += 1

        return penalty

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        if other is not None:
            return self.game == other.game















