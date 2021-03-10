import numpy as np
import time
zeros=np.zeros((4,4,4),dtype='str')
board=np.array((('b','b','b','b'),(' ',' ',' ',' '),(' ',' ',' ',' '),('w','w','w','w')))
board=np.core.defchararray.add(zeros, board)
unit_vectors=np.array([[0,1, 0], [0,0, 1], [0,1, 1], [0,-1, 0], [0,0, -1], [0,-1, -1]])
viable_vectors=np.concatenate((unit_vectors,unit_vectors*2))                #defines the legal vectors for stone movement up to two spaces


def check_if_pushes(board,stone,vector):
    if board[stone[0]][stone[1]+vector[1]][stone[2]+vector[2]]!=' 'or\
                board[stone[0]][stone[1]+int(round(vector[1]/2+0.1))][stone[2]+int(round(vector[2]/2+0.1))]!=' ':
        return True
    else:
        return False
def passive_move(color,stone_coordinate,move_coordinate):
    legal = True
    sub_board=(stone_coordinate[0])
    vector = (0,move_coordinate[1] - stone_coordinate[1], move_coordinate[2] - stone_coordinate[2])
    if color == "b":
        homeboard = ('0', '1')
    if color == "w":
        homeboard = ('2', '3')
    while True:
        if str(sub_board) not in homeboard:                          #checks if passive move is on homeboard
            print("Error: Board selected is not a homeboard")
            legal=False
            pass
        if board[stone_coordinate[0]][stone_coordinate[1]][stone_coordinate[2]]!=color:                          #checks if you're selecting your own stone
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
            #(x,y) notation i.e.(3,2)
            #if board[move_coordinate]-board[stone_coordinate]:
def aggressive_move(color, passive_board, stone_coordinate, vector):
    legal=True
    opponent=['b','w']
    opponent.remove(color)             #returns w if color is b, b if color is w
    while True:
        move_position=np.array(stone_coordinate)+np.array(vector)
        unit_vector=np.array(vector)//2
        if stone_coordinate[0] % 2 == passive_board % 2:
            print('error: stone must be played on opposite colored board as your passive move')                 #must play on boards of opposite parity
            legal = False
            pass
        if board[stone_coordinate[0]][stone_coordinate[1]][stone_coordinate[2]]!=color:                         #checks if you're selecting your own stone
            print("Error: no '"+ str(color)+"' stone at "+ str(stone_coordinate))
            legal = False
            pass
        try:
            #if board[stone_coordinate[0]][stone_coordinate[1] + vector[1]][stone_coordinate[2] + vector[2]] == color \
            #    or board[stone_coordinate[0]][stone_coordinate[1]+int(round(((vector[1])/2)+0.1))][stone_coordinate[2]+int(round((vector[2])/2)+0.1)]==color:
            if board[move_position[0]][move_position[1]][move_position[2]]==color or board[stone_coordinate[0]][stone_coordinate[1]+unit_vector[1]][stone_coordinate[2]+unit_vector[2]]==color:
                legal = False
                print('Error: Cannot push your own stones')         #if vector length = 2, checks both spots. if length = 1, only checks destination
        except IndexError:
            legal = False
            print('Error: Aggressive move out of 4x4 bounds ')
            pass
            if board[move_position[0]][move_position[1]][move_position[2]]==opponent and board[move_position[0]][move_position+unit_vector[1]][move_position+unit_vector[2]]!= ' ':
                    print('Error: Cannot push more than one stone')
                    legal = False
                    pass
        return legal
def passive_aggressive(color,init_stone,init_move,aggro_stone):
    legal=False
    passive_legal, vector, sub_board = passive_move(color, init_stone, init_move)
    aggro_legal=aggressive_move(color, sub_board, aggro_stone, vector)
    aggressive_moved=(aggro_stone[0],aggro_stone[1]+vector[1],aggro_stone[2]+vector[2])
    print('stone selected: '+str([board[init_stone[0]][init_stone[1]][init_stone[2]]])+ ' at ' + str(init_stone))
    print('move position: '+str([board[init_move[0]][init_move[1]][init_move[2]]]) + ' at ' +str(init_move))
    print('aggressive stone selected: '+str([board[aggro_stone[0]][aggro_stone[1]][aggro_stone[2]]]) + ' at ' +str(aggro_stone))
    print('aggressive stone moved to: ' + str([board[aggro_stone[0]][aggro_stone[1]+vector[1]][aggro_stone[2]+vector[2]]])+' at ' + str(aggressive_moved))
    if aggro_legal==True and passive_legal==True:
        legal = True
    return legal
legality=passive_aggressive('b',(1,0,0),(1,2,0),(2,0,1))
print(legality)