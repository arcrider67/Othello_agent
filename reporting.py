from client import BoardState
from client import Player



#special class of boardstate that can perform moves and modify the board
class ReportingBoard(BoardState):

    #place a piece of the color player, at the position move 
    def place_piece(self, player, move):
        self.board[move[0]][move[1]] = player

        offsets = self.directions
        board_size = 8

        #check for captures in all directions
        for offset in offsets:
            
            occupied_space = [move[0] + offset[0], move[1]+offset[1]]
            if(self.is_valid_square(occupied_space)):
                if(self.scan_for_cap(occupied_space, offset, player) != False):

                    self.perform_cap(occupied_space, offset, player)

    #updates board values assuming there is a capture that results from the move
    def perform_cap(self, occupied_space, direction, player):
        
        cur_location = occupied_space
        start_value = self.get_board_val(occupied_space) #the piece color that will be flipped
        more_to_search = True #false when the capture has ended

        while(more_to_search):
            piece_val = self.get_board_val(cur_location)
            if(piece_val != start_value):
            #the player value at that location has changed
                if(piece_val != 0):
                    #the space is occupied
                    return True
                else:
                    return False
            else:
                self.set_board_val(cur_location, player)
            cur_location = [cur_location[0]+direction[0], cur_location[1] + direction[1]]
            if(self.is_valid_square(cur_location)):
                more_to_search = True
            else:
            #edge of board hit
                more_to_search = False

    def get_board_val(self,space):
        return self.board[space[0]][space[1]]

    def reverse_board_val(self, space):
        if(self.board[space[0]][space[1]] == 1):
            self.board[space[0]][space[1]] = 2
        else:
            self.board[space[0]][space[1]] = 1

    def set_board_val(self, space, player):
            self.board[space[0]][space[1]] = player


    def scan_for_cap(self,occupied_space, direction, player):

        #determine the direction of the empty space relative to the occupied space

        cur_location = occupied_space
        start_value = self.get_board_val(occupied_space) #the piece color that will be flipped
        more_to_search = True #false when the capture has ended

        #scan the pieces oposite the empty space and determine if a capture can be made in that direction
        #formatted recursively without a recursive call
        while(more_to_search):
            piece_val = self.get_board_val(cur_location)
            if(piece_val != start_value):
            #the player value at that location has changed
                if(piece_val != 0):
                    #the space is occupied
                    if(piece_val == player):
                        return True
                else:
                    return False

            cur_location = [cur_location[0]+direction[0], cur_location[1] + direction[1]]
            if(self.is_valid_square(cur_location)):
                more_to_search = True
            else:
            #edge of board hit
                more_to_search = False

        return False
    def get_winner(self):
        highest_score = max(self.player_scores)
        if(self.player_scores[0] == 0):
            #game is over
            return self.player_scores.index(highest_score)

    def inverse(self, piece):
        if(piece == 2):
            return 1
        else:
            return 2

    def refresh(self):
        self.player_spaces = [[],[],[]]
      
        self.scan_board()

        self.player_scores = [0,0,0]
        self.player_scores[0] = len(self.player_spaces[0])
        self.player_scores[1] = len(self.player_spaces[1])
        self.player_scores[2] = len(self.player_spaces[2])

      
        self.move_number = 64 - len(self.player_spaces[0]) 

        #self.output()

def final_score(board, last_known_move, player):
    
    og_player = player

    complexBoard = ReportingBoard()
    final_player = Player(complexBoard)

    complexBoard.update(board)
    final_player.update(player, board)

   
    complexBoard.place_piece(player, last_known_move)
    complexBoard.refresh()

    empty_spaces = complexBoard.get_empty_spaces()


    #for the remaining spaces play out the game using this agent
    #most common scenario or between 
    for space in empty_spaces:
        
        if(player == 1):
            player = 2
        else:
            player = 1

        final_player.update(player, complexBoard.board)
        move = final_player.get_move()
        complexBoard.place_piece(player, move)
        complexBoard.refresh()
        complexBoard.output()



        
    fs = open("final_scores.csv", "a")
    p1score = complexBoard.get_p1_score()
    p2score = complexBoard.get_p2_score()
    fs.write(str(og_player) + ",")
    fs.write(str(p1score) + ",")
    fs.write(str(p2score) + ",")
    fs.write(str(complexBoard.get_winner()) + "\n")




