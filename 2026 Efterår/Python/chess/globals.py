def init():
    global CELL_SIZE
    CELL_SIZE = 64
    global BOARD_ROWS
    BOARD_ROWS = 8
    global BOARD_COLUMNS
    BOARD_COLUMNS = 8
    global PIECES_WHITE
    PIECES_WHITE = []
    global PIECES_BLACK
    PIECES_BLACK = []
    global pieces_img
    pieces_img = {
		'white_pawn': 'Resources/gfx/pawn-w.svg',
		'black_pawn': 'Resources/gfx/pawn-b.svg',
		'white_rook': 'Resources/gfx/rook-w.svg',
		'black_rook': 'Resources/gfx/rook-b.svg',
		'white_bishop': 'Resources/gfx/bishop-w.svg',
		'black_bishop': 'Resources/gfx/bishop-b.svg',
		'white_knight': 'Resources/gfx/knight-w.svg',
		'black_knight': 'Resources/gfx/knight-b.svg',
		'white_queen': 'Resources/gfx/queen-w.svg',
		'black_queen': 'Resources/gfx/queen-b.svg',
		'white_king': 'Resources/gfx/king-w.svg',
		'black_king': 'Resources/gfx/king-b.svg',
		}