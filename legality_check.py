import numpy as np
zeros=np.zeros((4,4,4),dtype='str')                                                             #initializes the board state
board=np.array((('b','b','b','b'),(' ',' ',' ',' '),(' ',' ',' ',' '),('w','w','w','w')))
board=np.core.defchararray.add(zeros, board)

unit_vectors=np.array([[0,1, 0], [0,0, 1], [0,1, 1], [0,1,-1], [0,-1,1], [0,-1, 0], [0,0, -1], [0,-1, -1]])         #defines the legal vectors for stone movement up to two spaces
viable_vectors=np.concatenate((unit_vectors,unit_vectors*2))


def obtain_board_pos(stone):
    out_of_bounds=False
    if stone[1] or stone[2] not in (0,1,2,3):
        out_of_bounds==True
    return board[stone[0]][stone[1]][stone[2]]

def check_if_pushes(board,stone,vector):                                       #checks if there is a stone in the vector path of the aggressive move
    if board[stone[0]][stone[1]+vector[1]][stone[2]+vector[2]]!=' 'or\
                board[stone[0]][stone[1]+int(round(vector[1]/2+0.1))][stone[2]+int(round(vector[2]/2+0.1))]!=' ':
        return True
    else:
        return False

def passive_move(color,stone_coordinate,move_coordinate):
    legal = True
    vector = (0,move_coordinate[1] - stone_coordinate[1], move_coordinate[2] - stone_coordinate[2])
    if color == "b":
        homeboard = ('0', '1')
    if color == "w":
        homeboard = ('2', '3')
    while True:
        if str(stone_coordinate[0]) not in homeboard:                          #checks if passive move is on homeboard
            print("Error: Board selected is not a homeboard")
            legal=False
            pass
        if obtain_board_pos(stone_coordinate)!=color:                          #checks if you're selecting your own stone
            print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate))
            legal = False
            pass
        if stone_coordinate[0]!=move_coordinate[0]:
            print("Error: Stone coordinate and Move coordinate not on same board")
            legal = False
            pass
        if vector not in viable_vectors:                                        #checks if stone movement is legal
            print('Error: Movement not orthogonally or diagonally adjacent with a scale up to two.')
            legal = False
            pass
        if check_if_pushes(board,stone_coordinate,vector):
            print("Error: Cannot push a stone on a passive move.")
            legal = False
            pass
        return legal, vector, stone_coordinate[0]
def aggressive_move(color, passive_board, stone_coordinate, vector):
    legal=True
    players=['b','w']
    players.remove(color)        #returns w if color is b, b if color is w
    opponent=players[0]
    while True:
        move_position=np.array(stone_coordinate)+np.array(vector)
        unit_vector=np.int_(np.round(np.array(vector)/2 + 0.01))
        if move_position[1] not in [0,1,2,3] or move_position[2] not in [0,1,2,3]:
            print('Error: Aggressive move out of 4x4 bounds')
            legal = False
            return legal
        if stone_coordinate[0] % 2 == passive_board % 2:
            print('error: stone must be played on opposite colored board as your passive move')                 #must play on boards of opposite parity
            legal = False
            pass
        if board[stone_coordinate[0]][stone_coordinate[1]][stone_coordinate[2]]!=color:                         #checks if you're selecting your own stone
            print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate))
            legal = False
            pass
        if obtain_board_pos(move_position)==color or obtain_board_pos(np.array(stone_coordinate)+np.array(unit_vector))==color:
            print('Error: Cannot push your own stones')         #if vector length = 2, checks both spots. if length = 1, only checks destination
            legal = False
        if str(obtain_board_pos(move_position))==opponent and (str(obtain_board_pos(move_position+unit_vector))!= ' ' or str(obtain_board_pos(move_position-unit_vector))== opponent):
            print('Error: Cannot push more than one stone (Case 1)')
            legal = False               #if moved onto opponent stone, checks if there is an opponent stone 1 unit ahead or behind of stone
            pass
        if str(obtain_board_pos(move_position))==' ' and str(obtain_board_pos(move_position-unit_vector))==opponent and str(obtain_board_pos(move_position+unit_vector))!=' ':
            print('Error: Cannot push more than one stone (Case 2)')
            legal= False                #if moved onto empty space, checks if there is an opponent stone both 1 unit behind and ahead of stone
            pass
        return legal
def passive_aggressive(color,init_stone,init_move,aggro_stone):
    legal=False
    passive_legal, vector, sub_board = passive_move(color, init_stone, init_move)       #determines if passive move is legal, records the vector of the move
    aggro_legal=aggressive_move(color, sub_board, aggro_stone, vector)                  #using the vector from passive move, applies to aggressive stone and determines if legal
    aggressive_moved=(aggro_stone[0],aggro_stone[1]+vector[1],aggro_stone[2]+vector[2]) #records position of newly moved aggressive stone
    print('stone selected: '+str([obtain_board_pos(init_stone)])+ ' at ' + str(init_stone))
    print('move position: '+str([obtain_board_pos(init_move)]) + ' at ' +str(init_move))
    print('aggressive stone selected: '+str([obtain_board_pos(aggro_stone)]) + ' at ' +str(aggro_stone))
    print('aggressive stone moved to: ' + str([obtain_board_pos(aggressive_moved)])+' at ' + str(aggressive_moved))
    if aggro_legal==True and passive_legal==True:
        legal = True
    return legal
legality=passive_aggressive('b',(1,0,0),(1,2,0),(2,0,1))
print(legality)
