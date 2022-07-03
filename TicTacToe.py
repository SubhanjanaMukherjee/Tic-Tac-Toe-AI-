import copy
import sys
import pygame
import numpy as np
import random 

from constants import *

#PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC TAC TOE - AI')
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        #print(self.squares)
        #self.mark_sqr(1,1,2)
        #print(self.squares)
        self.empty_sqrs = self.squares #[squares]
        self.marked_sqrs = 0

    def final_state(self,show=False):
        '''
        @return 0 if there is no win yet
        @return 1 if player 1 wins
        @returns 2 if player 2 wins
        '''

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    ipos = (col * SQSIZE + SQSIZE // 2,20 )
                    fpos = (col * SQSIZE + SQSIZE // 2,HEIGHT - 20 )
                    pygame.draw.line(screen,WIN_COLOR,ipos,fpos,LINE_WIDTH)
                return self.squares[0][col]

        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    ipos = (20,row*SQSIZE + SQSIZE //2 )
                    fpos = (WIDTH - 20,row*SQSIZE + SQSIZE //2 )
                    pygame.draw.line(screen,WIN_COLOR,ipos,fpos,LINE_WIDTH)
                return self.squares[row][0]

        #desc diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                ipos = (20,20 )
                fpos = (WIDTH - 20,HEIGHT-20 )
                pygame.draw.line(screen,WIN_COLOR,ipos,fpos,LINE_WIDTH)
            return self.squares[1][1]

        #asc diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                ipos = (20,HEIGHT-20 )
                fpos = (WIDTH - 20,20 )
                pygame.draw.line(screen,WIN_COLOR,ipos,fpos,LINE_WIDTH)
            return self.squares[1][1]

        #no win yet
        return 0

    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs +=1

    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 0

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self,level =1,player=2):
        self.level=level
        self.player=player

    def rnd(self,board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0,len(empty_sqrs))

        return empty_sqrs[idx] #[row,col]

    def minimax(self,board,maximizing):
        #terminal cases
        case = board.final_state()

        #player 1 wins
        if case == 1:
            return 1,None # eval,move
        
        #player 2 wins
        if case == 2 :
            return -1,None

        #draw
        elif board.isfull():
            return 0,None

        
        if maximizing :
            max_eval = -100 #any number greater than 0,1 or -1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for( row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval = self.minimax(temp_board,False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)


            return max_eval,best_move

        elif not maximizing:
            min_eval = 100 #any number greater than 0,1 or -1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for( row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval = self.minimax(temp_board,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)


            return min_eval,best_move



    def eval(self,main_board):
        if self.level == 0:
            #random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            #minimax algorithm choice
            eval,move = self.minimax(main_board , False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')   

        return move #row,col



class Game:
    #will be called each time we create a game object
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 #next player to mark square
        # player 1 - X & player 2 - O
        self.gamemode = 'ai' #pvp or ai mode
        self.running = True #if the game is not over
        self.show_lines()

    def make_move(self,row,col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.next_turn()

    def show_lines(self):
        #fill background
        screen.fill(BG_COLOR)
        #vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE,0),(WIDTH - SQSIZE,HEIGHT),LINE_WIDTH)
        
        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0,SQSIZE),(WIDTH,SQSIZE),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0,HEIGHT - SQSIZE),(WIDTH,HEIGHT - SQSIZE),LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.player == 1:
            #draw cross
            #cross needs an ascending line and descending line  

            #desc line
            start_desc = (col * SQSIZE + OFFSET , row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET , row * SQSIZE + SQSIZE - OFFSET) 
            pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)

            #asc line 
            start_asc = (col * SQSIZE + OFFSET , row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET , row * SQSIZE + OFFSET) 
            pygame.draw.line(screen,CROSS_COLOR,start_asc,end_asc,CROSS_WIDTH)


        elif self.player == 2:
        #draw circle
            center = (col * SQSIZE + SQSIZE //2 , row * SQSIZE + SQSIZE //2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)


    def next_turn(self):
        self.player = self.player % 2 +1 # changing player turns from 1 to 2 and vice versa

    def change_gamemode(self):
        if self.gamemode == 'pvp' :
            self.gamemode = 'ai'
        else:
            self.gamemode = 'pvp'

    def isover(self):
        return self.board.final_state(show=True) !=0 or self.board.isfull()

    def reset(self):
        self.__init__()



def main():
    #object
    game = Game()
    board = game.board
    ai = game.ai

    #main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #g - gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                # 0 - random ai level change
                if event.key == pygame.K_0:
                    ai.level = 0
                # 1 - random ai level change
                if event.key == pygame.K_1:
                    ai.level = 1
                #r - restart
                if event.key == pygame.K_r:
                    game.reset()
                    #reset the board
                    board = game.board
                    ai = game.ai

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                #print(row,col)


                if board.empty_sqr(row,col) and game.running:
                    '''game.board.mark_sqr(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()
                    #print(board.squares)'''
                    game.make_move(row,col)
                    # print(game.board.squares)

                    if game.isover():
                        game.running = False

            

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            #update the screen
            pygame.display.update()

            #ai methods
            row,col = ai.eval(board)

            '''game.board.mark_sqr(row,col,ai.player)
            game.draw_fig(row,col)
            game.next_turn()'''
            game.make_move(row,col)

            if game.isover():
                game.running = False

        pygame.display.update()


main()