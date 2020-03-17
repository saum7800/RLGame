
import chess
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
import chess.svg
from IPython.display import SVG, display
from IPython.display import clear_output


def getBoardState():
    for i in range(64):
        if(board.piece_type_at(i) is not None):
            if(board.color_at(i) is True):
                board_state[i]=board.piece_type_at(i)
            else:
                board_state[i]=-1*board.piece_type_at(i)
        else:
            board_state[i]=0
    if board.turn :
        board_state[64]=10
    else :
        board_state[64]=-10





def evaluation():
        input_state=board_state.reshape(1,65)
        prediction=model.predict(input_state)
        return np.sum(prediction)



def getBBestMove(epsilon) :
    bestmove=0
    minval=1
    allMoves=list(board.legal_moves)
    if random.random() < epsilon:
        return allMoves[random.randint(0,len(allMoves)-1)]
    
    for move in allMoves :
        board.push(move)
        getBoardState()
        currval = evaluation()
        if currval < minval :
            bestmove = move
            minval = currval
        board.pop()
    return bestmove

def getWBestMove(epsilon) :
    bestmove=0
    maxval=0
    allMoves=list(board.legal_moves)
    if random.random() < epsilon:
        return allMoves[random.randint(0,len(allMoves)-1)]
    
    for move in allMoves :
        board.push(move)
        getBoardState()
        currval = evaluation()
        if currval > maxval :
            bestmove = move
            maxval = currval
        board.pop()
    return bestmove

def playGame():
    board=chess.Board()
    board_state=np.zeros(65)
    while not(board.is_game_over()) :
        if board.turn :
            a=input()
            #a=getWBestMove(0.5)
            #board.push(a)
            playerMove=board.parse_san(a)
            board.push(playerMove)
            #train_states=np.vstack((train_states,board_state))
        else :
            b=getBBestMove(-1)
            print(b)
            board.push(b)
            #train_states=np.vstack((train_states,board_state))

model = keras.Sequential([
keras.Input(shape=(65,)),
keras.layers.Dense(units=128, activation='sigmoid'),
keras.layers.Dense(units=128, activation='sigmoid'),
keras.layers.Dense(units=64, activation='sigmoid'),
keras.layers.Dense(units=64, activation='sigmoid'),
keras.layers.Dense(units=32, activation='sigmoid'),
keras.layers.Dense(units=32, activation='sigmoid'),
keras.layers.Dense(units=16, activation='sigmoid'),
keras.layers.Dense(units=1, activation='sigmoid')
])

model.compile(optimizer='SGD',
          loss='mean_squared_error',
          metrics=['accuracy'])


epsilon=0.5
for k in range(500):
    epsilon=epsilon - 0.0008
    board=chess.Board()
    board_state=np.zeros(65)
    getBoardState()
    train_states=board_state
    while not(board.is_game_over()) :
        if board.turn :
            #a=input()
            a=getWBestMove(0.5)
            board.push(a)
            #playerMove=board.parse_san(a)
            #board.push(playerMove)
            train_states=np.vstack((train_states,board_state))
        else :
            b=getBBestMove(0.5)
            board.push(b)
            train_states=np.vstack((train_states,board_state))
    if(board.result() is "1-0"):
        train_results=np.ones(len(train_states))
    elif(board.result() is "0-1"):
        train_results=np.zeros(len(train_states))
    else:
        train_results=(np.ones(len(train_states)))*0.5
    combined = list(zip(train_states, train_results))
    random.shuffle(combined)
    train_states[:], train_results[:]=zip(*combined)
    model.fit(train_states, train_results, epochs=10)
    print(k)
playGame()

