def init():
	global GAME_BOARD
	GAME_BOARD = []
	global CELL_SIZE
	CELL_SIZE = 32
	global BOARD_ROWS
	BOARD_ROWS = 16
	global BOARD_COLUMNS
	BOARD_COLUMNS = 24
	global APPLE_TIMEOUT # Tidsfrist for at spise æble
	APPLE_TIMEOUT = 10000  # millisekunder (10 sekunder)
	global FIXED_SIZE
	FIXED_SIZE = (20, 32)  # (width, height) in pixels
	# Uge 4, Opgave 2 - Lav GAME OVER tekst
	global LARGE_SIZE
	LARGE_SIZE = (40, 64)  # Dobbelt så stor tekst, som vores score
	global font_img
	font_img = {
		'0': 'Resources/font/Individual/0.png',
		'1': 'Resources/font/Individual/1.png',
		'2': 'Resources/font/Individual/2.png',
		'3': 'Resources/font/Individual/3.png',
		'4': 'Resources/font/Individual/4.png',
		'5': 'Resources/font/Individual/5.png',
		'6': 'Resources/font/Individual/6.png',
		'7': 'Resources/font/Individual/7.png',
		'8': 'Resources/font/Individual/8.png',
		'9': 'Resources/font/Individual/9.png',
		'A': 'Resources/font/Individual/Upper_A.png',
		'B': 'Resources/font/Individual/Upper_B.png',
		'C': 'Resources/font/Individual/Upper_C.png',
		'D': 'Resources/font/Individual/Upper_D.png',
		'E': 'Resources/font/Individual/Upper_E.png',
		'F': 'Resources/font/Individual/Upper_F.png',
		'G': 'Resources/font/Individual/Upper_G.png',
		'H': 'Resources/font/Individual/Upper_H.png',
		'I': 'Resources/font/Individual/Upper_I.png',
		'J': 'Resources/font/Individual/Upper_J.png',
		'K': 'Resources/font/Individual/Upper_K.png',
		'L': 'Resources/font/Individual/Upper_L.png',
		'M': 'Resources/font/Individual/Upper_M.png',
		'N': 'Resources/font/Individual/Upper_N.png',
		'O': 'Resources/font/Individual/Upper_O.png',
		'P': 'Resources/font/Individual/Upper_P.png',
		'Q': 'Resources/font/Individual/Upper_Q.png',
		'R': 'Resources/font/Individual/Upper_R.png',
		'S': 'Resources/font/Individual/Upper_S.png',
		'T': 'Resources/font/Individual/Upper_T.png',
		'U': 'Resources/font/Individual/Upper_U.png',
		'V': 'Resources/font/Individual/Upper_V.png',
		'W': 'Resources/font/Individual/Upper_W.png',
		'<': 'Resources/font/Individual/_LeftChevron.png',
		'>': 'Resources/font/Individual/_RightChevron.png',
		}