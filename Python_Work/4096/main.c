#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <windows.h>

#define SIZE 4
long score=0;


void setColor(int ForgC, int BackC)
{
    WORD wColor = ((BackC & 0x0F) << 4) + (ForgC & 0x0F);
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), wColor);
}

void drawBoard(int board[SIZE][SIZE])
{
    int x, y;
    int color;

	printf("4096 game %11ld points\n\n", score);

	for(y=0; y<SIZE; y++)
    {

        for(x=0; x<SIZE; x++)
        {
            color = log2(board[x][y]);
			setColor(255, color + 216);
			printf("       ");
			setColor(255, 0);
		}

		printf("\n");

		for(x=0; x<SIZE; x++)
        {
            color = log2(board[x][y]);
			setColor(0, color + 216);

			if(board[x][y]!=0)
            {
				char s[8];

				sprintf(s, "%d", board[x][y]);
				int t = 7 - strlen(s);

				printf("%*s%s%*s",t-t/2,"",s,t/2,"");
			}
			else
            {
				printf("   .   ");
			}

            setColor(255, 0);
		}

		printf("\n");

		for(x=0; x<SIZE; x++)
        {
			color = log2(board[x][y]);
			setColor(255, color + 216);
			printf("       ");
			setColor(255, 0);
		}

		printf("\n");
	}

    setColor(255, 0);
	printf("\n");
	printf("     <4 ^8 >6 |2 or q     \n\n");
}

int findTarget(int array[SIZE],int x,int stop) {
	int t;
	// if the position is already on the first, don't evaluate
	if (x==0) {
		return x;
	}
	for(t=x-1;t>=0;t--) {
		if (array[t]!=0) {
			if (array[t]!=array[x]) {
				// merge is not possible, take next position
				return t+1;
			}
			return t;
		} else {
			// we should not slide further, return this one
			if (t==stop) {
				return t;
			}
		}
	}
	// we did not find a
	return x;
}

bool slideArray(int array[SIZE]) {
	bool success = false;
	int x,t,stop=0;

	for (x=0;x<SIZE;x++) {
		if (array[x]!=0) {
			t = findTarget(array,x,stop);
			// if target is not original position, then move or merge
			if (t!=x) {
				// if target is not zero, set stop to avoid double merge
				if (array[t]!=0) {
					score+=array[t]+array[x];
					stop = t+1;
				}
				array[t]+=array[x];
				array[x]=0;
				success = true;
			}
		}
	}
	return success;
}

void rotateBoard(int board[SIZE][SIZE]) {
	int i,j,n=SIZE;
	int tmp;
	for (i=0; i<n/2; i++){
		for (j=i; j<n-i-1; j++){
			tmp = board[i][j];
			board[i][j] = board[j][n-i-1];
			board[j][n-i-1] = board[n-i-1][n-j-1];
			board[n-i-1][n-j-1] = board[n-j-1][i];
			board[n-j-1][i] = tmp;
		}
	}
}

bool moveUp(int board[SIZE][SIZE]) {
	bool success = false;
	int x;
	for (x=0;x<SIZE;x++) {
		success |= slideArray(board[x]);
	}
	return success;
}

bool moveLeft(int board[SIZE][SIZE]) {
	bool success;
	rotateBoard(board);
	success = moveUp(board);
	rotateBoard(board);
	rotateBoard(board);
	rotateBoard(board);
	return success;
}

bool moveDown(int board[SIZE][SIZE]) {
	bool success;
	rotateBoard(board);
	rotateBoard(board);
	success = moveUp(board);
	rotateBoard(board);
	rotateBoard(board);
	return success;
}

bool moveRight(int board[SIZE][SIZE]) {
	bool success;
	rotateBoard(board);
	rotateBoard(board);
	rotateBoard(board);
	success = moveUp(board);
	rotateBoard(board);
	return success;
}

bool findPairDown(int board[SIZE][SIZE]) {
	bool success = false;
	int x,y;
	for (x=0;x<SIZE;x++) {
		for (y=0;y<SIZE-1;y++) {
			if (board[x][y]==board[x][y+1]) return true;
		}
	}
	return success;
}

int countEmpty(int board[SIZE][SIZE]) {
	int x,y;
	int count=0;

	for (x=0;x<SIZE;x++) {
		for (y=0;y<SIZE;y++) {
			if (board[x][y]==0) {
				count++;
			}
		}
	}
 /*
     if (count == 0)
     {
        board[0][3] = 0;
        count ++;
     }
*/
	return count;
}

bool gameEnded(int board[SIZE][SIZE]) {
	bool ended = true;
	if (countEmpty(board)>0) return false;
	if (findPairDown(board)) return false;
	rotateBoard(board);
	if (findPairDown(board)) ended = false;
	rotateBoard(board);
	rotateBoard(board);
	rotateBoard(board);
	return ended;
}

void addRandom(int board[SIZE][SIZE]) {
	static bool initialized = false;
	int x,y;
	int r,len=0;
	int n,list[SIZE*SIZE][2];

	if (!initialized) {
		srand(time(NULL));
		initialized = true;
	}

	for (x=0;x<SIZE;x++) {
		for (y=0;y<SIZE;y++) {
			if (board[x][y]==0) {
				list[len][0]=x;
				list[len][1]=y;
				len++;
			}
		}
	}

	if (len>0) {
		r = rand()%len;
		x = list[r][0];
		y = list[r][1];
		n = ((rand()%10)/9+1)*2;
		board[x][y]=n;
	}
}

int main(int argc, char *argv[])
{
// my board + initialize of the board
    int board[SIZE][SIZE];
    memset(board, 0, sizeof(board));

    // user char input
    int c;
    char cc;
    int counter = 0;

    // state of the move
    bool success;

    addRandom(board);
    addRandom(board);

    drawBoard(board);

    /*
    int moves[] = {8, 4, 4, 8, 4, 2, 4};
    int nr = 7;
    int i = 0;
    */

    while(true)
    {
        /* player play
        // get the input char
        //c = getch();
        //cc = c - '0';
        */

        /* random play
        cc = ((rand() % 4) + 1 ) * 2;
        */

        /* fixed sequence
        if (i < nr)
        {
            cc = moves[i];
            i++;
        }
        else
         i = 0;
         */

        cc = nextMove(board);

        switch(cc)
        {
			case 4:	// left arrow
				success = moveLeft(board);  break;
			case 6:	// right arrow
				success = moveRight(board); break;
			case 8:	// up arrow
				success = moveUp(board);    break;
			case 2:	// down arrow
				success = moveDown(board);  break;
			default:
			    success = false;
		}

        if (success)
        {
            drawBoard(board);
            counter ++;
            /*
            if (counter % 100 == 0)
                Sleep(3000);
                */
            addRandom(board);
            drawBoard(board);
			if (gameEnded(board))
			{
				printf("         GAME OVER          \n");
				break;
			}
		}

		if (c=='q')
        {
			printf("            QUIT            \n");
			break;
		}
	}

 return 0;
}

long long int evaluate( int a[SIZE][SIZE] )
{
    int x, y;
    long long int score = 0;
    int n = 16;

    for(x=0; x<SIZE; x++)
    {
        if(x%2==0)
        {
            for(y=SIZE-1; y>0; y--)
            {
                n -= 1;
                score += a[x][y] * pow(2, n);
            }
        }
        else
        {
            for(y=0; y<SIZE; y++)
            {
                n -= 1;
                score += a[x][y] * pow(2, n);
            }
        }
    }

    return score;
}


int nextMove(int board[SIZE][SIZE])
{
    int m, i, j;
    int bestMove = 0;
    long long int bestScore = -1;
    long long int score = 0;
    int aux[SIZE][SIZE] = {0};
    bool suc = false;

    for(m=2; m<9; m+=2)
    {
        // copy
        for(i=0; i<SIZE; i++)
            for(j=0; j<SIZE; j++)
                aux[i][j] = board[i][j];

        switch(m)
        {
            case 4:	// left arrow
                    suc = moveLeft(aux);  break;
			case 6:	// right arrow
                    suc = moveRight(aux); break;
			case 8:	// up arrow
                    suc = moveUp(aux);    break;
			case 2:	// down arrow
                    suc = moveDown(aux);  break;
        }

        score = evaluate(aux);

        if ((bestScore < score) && (suc == true))
        {
            bestScore = score;
            bestMove = m;
        }
    }

    return bestMove;
}
