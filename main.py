import pygame as p
from chess import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT// DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
     IMAGES[piece] = p.transform.scale(p.image.load("IMAGES/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMove()
    moveMade = False


    load_images()
    running = True
    sqSelected = ()
    playerClickes = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE

                if sqSelected == (row,col):
                    sqSelected= ()
                    playerClickes= []
                else:
                    sqSelected=(row,col)
                    playerClickes.append((sqSelected))

                if len(playerClickes) == 2:
                    move = chessEngine.Move(playerClickes[0],playerClickes[1],gs.board)
                    print(move.getchessNotation())
                    for i in range(len(validMoves)):
                       if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClickes= []

                    if not moveMade:
                        playerClickes = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade= True

        if moveMade:
            validMoves= gs.getValidMove()
            moveMade = False

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color(" gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
           color = colors[((r+c) % 2)]
           p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))





if __name__ == "__main__":
  main()



