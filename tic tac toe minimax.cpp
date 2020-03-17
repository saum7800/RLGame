#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct Move
{
    int row;
    int col;
};

char maximiser='x',minimizer='o';
int game_status=1,turn=1;
char board[3][3]={{'_','_','_'},{'_','_','_'},{'_','_','_'}};

void updateBoard(Move curr_move)
{
    if(turn==1)
    {
        board[curr_move.row][curr_move.col]=maximiser;
        turn=2;
    }
    else
    {
        board[curr_move.row][curr_move.col]=minimizer;
        turn=1;
    }
    
}
void printBoard()
{
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            cout<<board[i][j];
        }
        cout<<"\n";
    }
}

int isMovesLeft()
{
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            if(board[i][j]=='_')
            return 1;
        }
    }
    return 0;
}

int evaluate(char b[3][3]) 
{ 
    // Checking for Rows for X or O victory. 
    for (int row = 0; row<3; row++) 
    { 
        if (b[row][0]==b[row][1] && 
            b[row][1]==b[row][2]) 
        { 
            if (b[row][0]==maximiser) 
                return +10; 
            else if (b[row][0]==minimizer) 
                return -10; 
        } 
    } 
  
    // Checking for Columns for X or O victory. 
    for (int col = 0; col<3; col++) 
    { 
        if (b[0][col]==b[1][col] && 
            b[1][col]==b[2][col]) 
        { 
            if (b[0][col]==maximiser) 
                return +10; 
  
            else if (b[0][col]==minimizer) 
                return -10; 
        } 
    } 
  
    // Checking for Diagonals for X or O victory. 
    if (b[0][0]==b[1][1] && b[1][1]==b[2][2]) 
    { 
        if (b[0][0]==maximiser) 
            return +10; 
        else if (b[0][0]==minimizer) 
            return -10; 
    } 
  
    if (b[0][2]==b[1][1] && b[1][1]==b[2][0]) 
    { 
        if (b[0][2]==maximiser) 
            return +10; 
        else if (b[0][2]==minimizer) 
            return -10; 
    } 
  
    // Else if none of them have won then return 0 
    return 0; 
} 

int minimax(char board[3][3],int depth, int isMax)
{
    int currVal=evaluate(board);
    if(currVal==10||currVal==-10||isMovesLeft()==0)
    {
        return currVal;
    }
    else
    {
        if(isMax)
        {
            int bestVal=-100;
            for(int i=0;i<3;i++)
            {
                for(int j=0;j<3;j++)
                {
                    if(board[i][j]=='_')
                    {
                        board[i][j]=maximiser;
                        bestVal=max(bestVal,minimax(board,depth+1,0));
                        board[i][j]='_';
                    }
                }
            }
            return bestVal;
        }
        else
        {
            int bestVal=100;
            for(int i=0;i<3;i++)
            {
                for(int j=0;j<3;j++)
                {
                    if(board[i][j]=='_')
                    {
                        board[i][j]=minimizer;
                        bestVal=min(bestVal,minimax(board,depth+1,1));
                        board[i][j]='_';
                    }
                }
            }
            return bestVal;
        }
    }
    
}

Move getBestMove()
{
    int bestVal=100;
    int moveVal;
    Move bestMove;
    for(int i=0;i<3;i++)
    {
        for(int j=0;j<3;j++)
        {
            if(board[i][j]=='_')
            {
                board[i][j]=minimizer;
                moveVal=minimax(board,0,1);
                if(moveVal<bestVal)
                {
                    bestMove.row=i;
                    bestMove.col=j;
                    bestVal=moveVal;
                }                
                board[i][j]='_';
            }
        }
    }
    return bestMove;
}

int main()
{   
    int rno,cno;
    cout<<"welcome";
    int a;
    cin>>a;
    while(game_status==1)
    {
        if(turn==1)
        {
           system("clear");
           printBoard();
           cout<<"enter row and column number for move:";
           cin>>rno>>cno;
           Move player1;
           player1.row=rno;
           player1.col=cno;
           updateBoard(player1);
        }
        else
        {
            system("clear");
            Move best_move = getBestMove();
            updateBoard(best_move);
            printBoard();
        }
        
    }
}
