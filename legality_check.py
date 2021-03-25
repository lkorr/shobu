import numpy as np
import colorama
from colorama import Fore
from colorama import Style

colorama.init()

zeros = np.zeros((4, 4, 4), dtype='str')  # initializes the board state
board = np.array((('b', 'b', 'b', 'b'), (' ', ' ', 'w', ' '), (' ', ' ', ' ', ' '), ('w', 'w', 'w', 'w')))
board = np.core.defchararray.add(zeros, board)

unit_vectors = np.array([[0, 1, 0], [0, 0, 1], [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, 0], [0, 0, -1],
                         [0, -1, -1]])  # defines the legal vectors for stone movement up to two spaces
viable_vectors = np.concatenate((unit_vectors, unit_vectors * 2))


def obtain_board_pos(stone,board=board):
    if stone[1] not in [0, 1, 2, 3] or stone[2] not in [0, 1, 2,
                                                        3]:  # checks if position is out of bounds and returns ' '
        position = ' '
    else:
        position = board[stone[0]][stone[1]][stone[2]]
    return position

def update_board_pos(stone,input,board_update):
    out_of_bounds=False
    if stone[1] not in [0, 1, 2, 3] or stone[2] not in [0, 1, 2,
                                                        3]:  # checks if position is out of bounds
        out_of_bounds = True
        return out_of_bounds
    board_update[stone[0]][stone[1]][stone[2]]=input
    return out_of_bounds

def generate_unit_vector(vector):
    unit_vector = [0, 0, 0]
    for i in (1, 2):
        if vector[i] in (1, 2):
            unit_vector[i] = 1
        if vector[i] in (-1, -2):
            unit_vector[i] = -1
        if vector[i] == 0:
            unit_vector[i] = 0
    return unit_vector


def check_if_pushes(board, stone, vector):  # checks if there is a stone in the vector path of the aggressive move
    if board[stone[0]][stone[1] + vector[1]][stone[2] + vector[2]] != ' ' or \
            board[stone[0]][stone[1] + int(round(vector[1] / 2 + 0.1))][
                stone[2] + int(round(vector[2] / 2 + 0.1))] != ' ':
        return True
    else:
        return False


def get_vector(stone_coordinate, move_coordinate):
    return (0, move_coordinate[1] - stone_coordinate[1], move_coordinate[2] - stone_coordinate[2])


def passive_move(color, stone_coordinate, move_coordinate, vector):
    if color == "b":
        homeboard = ('0', '1')
    if color == "w":
        homeboard = ('2', '3')

    if str(stone_coordinate[0]) not in homeboard:  # checks if passive move is on homeboard
        print("Error: Board selected is not a homeboard")
        return False

    if obtain_board_pos(stone_coordinate) != color:  # checks if you're selecting your own stone
        print("Error: no '" + str(color) + "' stone at " + str(stone_coordinate))
        return False

    if stone_coordinate[0] != move_coordinate[0]:
        print("Error: Stone coordinate and Move coordinate not on same board")
        return False

    if vector not in viable_vectors:  # checks if stone movement is legal
        print('Error: Movement not orthogonally or diagonally adjacent with a scale up to two.')
        return False

    if check_if_pushes(board, stone_coordinate, vector):
        print("Error: Cannot push a stone on a passive move.")
        return False

    return True  # , vector, stone_coordinate[0]


def aggressive_move(color, opponent, passive_board, stone_coordinate, vector, unit_vector):
    move_position = np.array(stone_coordinate) + np.array(vector)

    if move_position[1] not in [0, 1, 2, 3] or move_position[2] not in [0, 1, 2, 3]:
        print('Error: Aggressive move out of 4x4 bounds')
        return False

    if obtain_board_pos(stone_coordinate) != color:  # checks if you're selecting your own stone
        print("Error: no '" + str(color) + "' stone at " + str(stone_coordinate) + '  (aggressive move)')
        return False

    if stone_coordinate[0] % 2 == passive_board % 2:
        print(
            'error: stone must be played on opposite colored board as your passive move')  # must play on boards of opposite parity
        return False

    if board[stone_coordinate[0]][stone_coordinate[1]][
        stone_coordinate[2]] != color:  # checks if you're selecting your own stone
        print("Error: no '" + str(color) + "' stone at " + str(stone_coordinate))
        return False

    if obtain_board_pos(move_position) == color or obtain_board_pos(
            np.array(stone_coordinate) + np.array(unit_vector)) == color:
        print(
            'Error: Cannot push your own stones')  # if vector length = 2, checks both spots. if length = 1, only checks destination
        return False

    if obtain_board_pos(move_position) == opponent and (
            obtain_board_pos(move_position + unit_vector) != ' ' or obtain_board_pos(
            move_position - unit_vector) == opponent):
        print('Error: Cannot push more than one stone (Case 1)')
        return False  # if moved onto opponent stone, checks if there is an opponent stone 1 unit ahead or behind of stone

    if obtain_board_pos(move_position) == ' ' and obtain_board_pos(
            move_position - unit_vector) == opponent and obtain_board_pos(move_position + unit_vector) != ' ':
        print('Error: Cannot push more than one stone (Case 2)')
        return False  # if moved onto empty space, checks if there is an opponent stone both 1 unit behind and ahead of stone

    return True


def print_statements(init_stone, init_move, aggro_stone, aggressive_moved, aggro_legal, passive_legal, unit_vector,
                     opponent):
    print('stone selected: ' + str([obtain_board_pos(init_stone)]) + ' at ' + str(init_stone))
    print('move position: ' + str([obtain_board_pos(init_move)]) + ' at ' + str(init_move))
    print('aggressive stone selected: ' + str([obtain_board_pos(aggro_stone)]) + ' at ' + str(aggro_stone))
    print('aggressive stone moved to: ' + str([obtain_board_pos(aggressive_moved)]) + ' at ' + str(aggressive_moved))

    if aggro_legal == True and passive_legal == True:
        legal = True
    if legal == True and obtain_board_pos(aggressive_moved) == opponent:
        print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(aggressive_moved + unit_vector))
        if -1 in aggressive_moved + unit_vector or 4 in aggressive_moved + unit_vector:
            print(opponent + ' stone removed from the board')
    if legal == True and obtain_board_pos(aggressive_moved) == ' ' and obtain_board_pos(
            aggressive_moved - unit_vector) == opponent:
        print(str([opponent]) + ' stone pushed from ' + str(aggressive_moved - unit_vector) + ' to ' + str(
            aggressive_moved + unit_vector))
        if -1 in aggressive_moved + unit_vector or 4 in aggressive_moved + unit_vector:
            print(opponent + ' stone removed from the board')


def passive_aggressive(color, init_stone, init_move, aggro_stone):
    # this does the same thing as what you had in aggresive_move
    # its called a "ternary operator" all languages have this ability but usually with different syntax
    legality = False
    opponent = 'b' if color == 'w' else 'w'
    vector = get_vector(init_stone, init_move)
    unit_vector = np.array(generate_unit_vector(vector))
    sub_board = init_stone[0]

    passive_legal = passive_move(color, init_stone, init_move, vector)

    if not passive_legal:
        return legality

    aggro_legal = aggressive_move(color, opponent, sub_board, aggro_stone, vector,
                                  unit_vector)  # using the vector from passive move, applies to aggressive stone and determines if legal

    if not aggro_legal:
        return legality

    aggressive_moved = (aggro_stone[0], aggro_stone[1] + vector[1],
                        aggro_stone[2] + vector[2])  # records position of newly moved aggressive stone

    print_statements(init_stone, init_move, aggro_stone, aggressive_moved, aggro_legal, passive_legal, unit_vector,
                     opponent)
    legality=True
    return legality,color,opponent,vector,unit_vector,init_stone,init_move,aggro_stone


def unit_tests():
    # test for legal move
    print(Fore.GREEN + "\ntest for legal move" + Style.RESET_ALL)
    passive_aggressive('b', (1, 0, 3), (1, 2, 1), (2, 0, 2))
    print(Fore.GREEN + "\ntest for legal move white" + Style.RESET_ALL)
    passive_aggressive('w', (2, 3, 0), (2, 1, 2), (1, 3, 1))

    print(Fore.RED + "\ntest for same board passive aggro move" + Style.RESET_ALL)
    passive_aggressive('b', (1, 0, 3), (1, 2, 1), (1, 0, 2))

    print(Fore.RED + "\ntest for illegal board passive move legal board aggro move" + Style.RESET_ALL)
    passive_aggressive('b', (2, 0, 3), (2, 2, 1), (3, 0, 2))

    print(Fore.RED + "\ntest for legal board passive move illegal board aggro move" + Style.RESET_ALL)
    passive_aggressive('b', (0, 0, 3), (0, 2, 1), (2, 0, 2))

    print(Fore.RED + "\ntest for legal boards but illegal move" + Style.RESET_ALL)
    passive_aggressive('b', (1, 0, 3), (1, 3, 0), (2, 0, 2))

    print(Fore.RED + "\ntest for wrong stone" + Style.RESET_ALL)
    passive_aggressive('w', (2, 0, 3), (2, 2, 1), (1, 3, 1))

def update_board(board,color, init_stone, init_move, aggro_stone,board_history):
        updated_board=np.copy(board)
        legal,color,opponent,vector,unit_vector,init_stone,init_move,aggro_stone = passive_aggressive(color,init_stone, init_move,aggro_stone)
        aggressive_moved = (aggro_stone[0], aggro_stone[1] + vector[1], aggro_stone[2] + vector[2])
        if legal==True:
            update_board_pos(init_stone, ' ', updated_board)
            update_board_pos(init_move, color, updated_board)
            update_board_pos(aggro_stone, ' ', updated_board)
            update_board_pos(aggressive_moved, color, updated_board)
            if obtain_board_pos(aggressive_moved) == opponent:
                out_of_bounds=update_board_pos(aggressive_moved+unit_vector, opponent, updated_board)
                if out_of_bounds==True:
                    print(opponent + ' stone removed from the board')
                else:
                    print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(
                    aggressive_moved + unit_vector))
            if obtain_board_pos(aggressive_moved) == ' ' and obtain_board_pos(
                aggressive_moved - unit_vector) == opponent:
                update_board_pos(aggressive_moved-unit_vector,' ', updated_board)
                out_of_bounds=update_board_pos(aggressive_moved+unit_vector,opponent,updated_board)
                if out_of_bounds==True:
                    print(opponent + ' stone removed from the board')
                else:
                    print(opponent + ' stone pushed from ' + str(aggressive_moved) + ' to ' + str(
                    aggressive_moved + unit_vector))
            #board_history+=updated_board
            board_history.append(updated_board)
        else:
            print('illegal move')

        return updated_board,board_history


board_history=[board]
board,board_history=update_board(board,'b',(0,0,0),(0,2,2),(1,0,1),board_history)
print(board)
print(len(board_history))
#unit_tests()
# legality=passive_aggressive('b',(1,0,3),(1,2,1),(2,0,2))
# print(legality)
