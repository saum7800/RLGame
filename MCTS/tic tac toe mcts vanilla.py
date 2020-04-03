import math
import random
import copy
class Node:
    def __init__(self,boardState,turn,parent):
        self.boardState=boardState
        self.totalVal=0
        self.visitCount=0
        self.children=[]
        self.parent=parent
        self.fullyExpanded=False
        self.turn=turn



def evaluate(b):  
   
    # Checking for Rows for X or O victory.  
    for row in range(0, 3):  
       
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:  
           
            if b[row][0] == 'x': 
                return 10 
            elif b[row][0] == 'o':  
                return -10 
  
    # Checking for Columns for X or O victory.  
    for col in range(0, 3):  
       
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:  
           
            if b[0][col]=='x': 
                return 10 
            elif b[0][col] == 'o':  
                return -10 
  
    # Checking for Diagonals for X or O victory.  
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:  
       
        if b[0][0] == 'x':  
            return 10 
        elif b[0][0] == 'o':  
            return -10 
       
    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:  
       
        if b[0][2] == 'x':  
            return 10 
        elif b[0][2] == 'o':  
            return -10 
       
    # Else if none of them have won then return 0  
    return 0 
   
def isGameOver(board):
    if evaluate(board)==10 or evaluate(board)==-10:
        return True
    else:
        flag=0
        for i in range(3):
            for j in range(3):
                if board[i][j]=='_':
                    flag=1
        if flag==1:
            return False
        else:
            return True

def MCTS(root): 
    for i in range(20000): 
        leaf = traverse(root)
        print("leaf state after",i, "iters:")
        print(leaf.boardState)
        rollout_result = rollout(leaf)
        print("result after",i,"iter:",rollout_result)
        backpropogate_results(root,leaf,rollout_result)
    max_visits=-1
    best_state=None
    for child in root.children:
        if child.visitCount>max_visits:
            max_visits=child.visitCount
            best_state=copy.deepcopy(child.boardState)
    return best_state
         

def backpropogate_results(root,leaf,result):
    while leaf is not None:
        leaf.totalVal=leaf.totalVal + result*-1*leaf.turn
        leaf.visitCount=leaf.visitCount+1
        leaf=leaf.parent
    
    

def rollout(node):
    currState=node.boardState
    #print(currState)
    currTurn=node.turn
    while not(isGameOver(currState)):
        currState=makeRandomAction(currState,currTurn)
        #print(currState)
        currTurn=-1*currTurn
    return (evaluate(currState))

def makeRandomAction(board,turn):
    nextBoards=[]
    for i in range(3):
        for j in range(3):
            if board[i][j]=='_':
                if turn==1.0:
                    board[i][j]='x'
                else:
                    board[i][j]='o'
                nextBoards.append(copy.deepcopy(board))
                board[i][j]='_'
    #print(nextBoards)
    return nextBoards[random.randint(0,len(nextBoards)-1)]

def traverse(node): 
    while node.fullyExpanded and not(isGameOver(node.boardState)): 
        node=best_uct(node)
    if node.visitCount==0: 
        return node
    else: 
        node=fullyExpand(node)
        return randomChild(node)

def fullyExpand(node):
    node.fullyExpanded=True
    if evaluate(node.boardState)==10 or evaluate(node.boardState)==-10:
        return node
    else:
        for i in range(3):
            for j in range(3):
                if node.boardState[i][j]=='_':
                    if node.turn==1:
                        node.boardState[i][j]='x'
                    else:
                        node.boardState[i][j]='o'
                    node.children.append(Node(copy.deepcopy(node.boardState),-node.turn,node))
                    node.boardState[i][j]='_'
    return node

def best_uct(node):
    expConst=2
    bestNode=None
    bestVal=-10000
    for child in node.children:
        uctVal=(child.totalVal/(child.visitCount+0.01)) + expConst * math.sqrt((math.log(node.visitCount)+0.1) /(child.visitCount + 0.01) ) 
        if uctVal>bestVal:
            bestVal=uctVal
            bestNode=child
    return bestNode

def randomChild(node):
    
    if len(node.children)==0:
        return node
    else:
        return node.children[random.randint(0,len(node.children)-1)]  

player=1
board = [['_', '_', '_'],  
         ['_', '_', '_'],  
         ['_', '_', '_']]  
while not(isGameOver(board)):
    if player is 1:
        board=MCTS(Node(board,1,None))
        player=-1
    else:
        row_num, col_num = map(int, input().split())
        board[row_num][col_num]='o'
        player=1
    print(board)
    
        
        
  