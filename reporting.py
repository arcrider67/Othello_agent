from client import BoardState
from client import Player

#special class of boardstate that can perform moves and modify the board
class ReportingBoard(BoardState):
    def place_piece(self, player, move):
        board = self.board
        board[move[0]][move[1]] = player
        for offset in offsets:
            check = [move[0]+offset[0], move[1]+offset[1]]
            while 0<=check[0]<board_size and 0<=check[1]<board_size:
                if board[check[0]][check[1]] is EMPTY: break
                if board[check[0]][check[1]] is piece:
                    self.flip( player, move, offset)
                    break
                check[0] += offset[0]
                check[1] += offset[1]

    def flip(self, piece, move, offset):
        board = self.board
        check = [move[0]+offset[0], move[1]+offset[1]]
        while(board[check[0]][check[1]] is self.inverse(piece)):
            board[check[0]][check[1]] = piece
            check[0] += offset[0]
            check[1] += offset[1]

    def inverse(self, piece):
        if(piece == 2):
            return 1
        else:
            return 2



def final_score(board, last_known_move, player):


    complexBoard = ReportingBoard()
    final_player = Player(complexBoard)

    board[last_known_move[0]][last_known_move[1]] = player
    complexBoard.update(board)

    empty_squares = complexBoard.get_empty_count()

    #assume there was 1 empty square
    if(empty_squares == 1):
        final_player.update(2, board)

        space = empty_squares[0]
        

