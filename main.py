from io import BytesIO

import pygame
import requests

pygame.init()

WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess Game')
screen.fill('dark gray')
pygame.display.flip()  # Show the window while the piece images load.

font = pygame.font.Font("freesansbold.ttf", 20)
medium_font = pygame.font.Font("freesansbold.ttf", 40)
big_font = pygame.font.Font("freesansbold.ttf", 50)

timer = pygame.time.Clock()
fps = 60

white_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
white_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                   (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
black_pieces =  ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
black_locations = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                   (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
                   
captured_black_pieces = []
captured_white_pieces = []

# 0 - whites turn no selection: 1 - whites turn piece selected: 2 - black turn no selection: 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
castling_rights = {
    'white': {'king_side': True, 'queen_side': True},
    'black': {'king_side': True, 'queen_side': True},
}

image_urls = ['https://camo.githubusercontent.com/ca0e49b6cf5b66c7ce41dcf4026a3348d50c03668e3377e0fea104d85af73ef4/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f62712e706e67', # Black King
              'https://camo.githubusercontent.com/b907c506ddca33c6dc11154164a7de48a53c7baf0d6bb805dc37d5e9978c02b1/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f626b2e706e67', # Back Queen
              'https://camo.githubusercontent.com/448d4a58577fe92c10b331c8df5854b4084d6ed2d03e8383287b4a8cdb4df63c/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f62722e706e67', # Black Rook
              'https://camo.githubusercontent.com/4473809e32b3cb6b09bdcac0431628f2a6a942da02a3a68ec0937eafd98e40bf/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f62622e706e67', # Black Bishop
              'https://camo.githubusercontent.com/a2d70376f02bc74f286375504683b8d84e52f76411ed0194ce8d5dd030499dab/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f626e2e706e67', # Black Knight
              'https://camo.githubusercontent.com/8f8b708ccc4d3e985da72601429fc78b1fe7d5d237ac1579079a16b5c0b172aa/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f62702e706e67', # Black Pawn
              'https://camo.githubusercontent.com/bc3ff9263bb953970ab361d133fe37f4ea5aa688cd890a47fb533634badb284d/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f77712e706e67', # White King
              'https://camo.githubusercontent.com/4a614e2a993b4aad0f0f993321f98c1e7a27ec65b84a2ad0e9b673e0e391fb21/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f776b2e706e67', # White Queen
              'https://camo.githubusercontent.com/a8f673a9d2c71530da31bd6b999b72f3a13ea6e00bd86005248ab35ef07907bc/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f77722e706e67', # White Rook
              'https://camo.githubusercontent.com/251c69261fd52c7a920c08d187c89b5fb58028d8efe6cdb23b5d5ef2aeb13a41/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f77622e706e67', # White Bishop
              'https://camo.githubusercontent.com/2ca8468715220953278836803744855138aae834fa0dc26320e7ba0fc371fe17/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f776e2e706e67', # White Knight
              'https://camo.githubusercontent.com/36ffbf234a87a099691b0ebe5ba0a0f09eeacb53591336bbe7fc5203db427f80/68747470733a2f2f696d616765732e6368657373636f6d66696c65732e636f6d2f63686573732d7468656d65732f7069656365732f6e656f2f3235362f77702e706e67']# White Pawn

# Load in game piece images              
black_queen = pygame.image.load(BytesIO(requests.get(image_urls[0]).content))
black_queen = pygame.transform.scale(black_queen, (80,80))
black_queen_small = pygame.transform.scale(black_queen, (45,45))

black_king = pygame.image.load(BytesIO(requests.get(image_urls[1]).content))
black_king = pygame.transform.scale(black_king, (80,80))
black_king_small = pygame.transform.scale(black_king, (45,45))

black_rook = pygame.image.load(BytesIO(requests.get(image_urls[2]).content))
black_rook = pygame.transform.scale(black_rook, (80,80))
black_rook_small = pygame.transform.scale(black_rook, (45,45))

black_bishop = pygame.image.load(BytesIO(requests.get(image_urls[3]).content))
black_bishop = pygame.transform.scale(black_bishop, (80,80))
black_bishop_small = pygame.transform.scale(black_bishop, (45,45))

black_knight = pygame.image.load(BytesIO(requests.get(image_urls[4]).content))
black_knight = pygame.transform.scale(black_knight, (80,80))
black_knight_small = pygame.transform.scale(black_knight, (45,45))

black_pawn = pygame.image.load(BytesIO(requests.get(image_urls[5]).content))
black_pawn = pygame.transform.scale(black_pawn, (65,65))
black_pawn_small = pygame.transform.scale(black_pawn, (45,45))

white_queen = pygame.image.load(BytesIO(requests.get(image_urls[6]).content))
white_queen = pygame.transform.scale(white_queen, (80,80))
white_queen_small = pygame.transform.scale(white_queen, (45,45))

white_king = pygame.image.load(BytesIO(requests.get(image_urls[7]).content))
white_king = pygame.transform.scale(white_king, (80,80))
white_king_small = pygame.transform.scale(white_king, (45,45))

white_rook = pygame.image.load(BytesIO(requests.get(image_urls[8]).content))
white_rook = pygame.transform.scale(white_rook, (80,80))
white_rook_small = pygame.transform.scale(white_rook, (45,45))

white_bishop = pygame.image.load(BytesIO(requests.get(image_urls[9]).content))
white_bishop = pygame.transform.scale(white_bishop, (80,80))
white_bishop_small = pygame.transform.scale(white_bishop, (45,45))

white_knight = pygame.image.load(BytesIO(requests.get(image_urls[10]).content))
white_knight = pygame.transform.scale(white_knight, (80,80))
white_knight_small = pygame.transform.scale(white_knight, (45,45))

white_pawn = pygame.image.load(BytesIO(requests.get(image_urls[11]).content))
white_pawn = pygame.transform.scale(white_pawn, (65,65))
white_pawn_small = pygame.transform.scale(white_pawn, (45,45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

counter = 0
winner = ''
game_over = False

def drawBoard():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select A Piece To Move', 'White: Select A Destination',
                       'Black: Select A Piece To Move', 'Black: Select A Destination']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800 * 100, i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('RESIGN', True, 'black'), (810, 830))
        
def drawPieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])

        image = white_images[index]
        square_x, square_y = white_locations[i][0] * 100, white_locations[i][1] * 100
        image_x = square_x + (100 - image.get_width()) // 2
        image_y = square_y + (100 - image.get_height()) // 2
        screen.blit(image, (image_x, image_y))
            
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)
                
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])

        image = black_images[index]
        square_x, square_y = black_locations[i][0] * 100, black_locations[i][1] * 100
        image_x = square_x + (100 - image.get_width()) // 2
        image_y = square_y + (100 - image.get_height()) // 2
        screen.blit(image, (image_x, image_y))
            
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)

def checkOptions(pieces, locations, turn):
    all_moves_list = []
    for index, piece in enumerate(pieces):
        source = locations[index]
        pseudo_moves = pieceMoves(piece, source, turn)
        if piece == 'king':
            pseudo_moves.extend(castlingMoves(turn, source))

        legal_moves = []
        for target in pseudo_moves:
            if isKingCapture(target, turn):
                continue
            if moveLeavesKingSafe(index, source, target, turn):
                legal_moves.append(target)
        all_moves_list.append(legal_moves)
    return all_moves_list

def pieceMoves(piece, position, color):
    move_functions = {
        'pawn': checkPawn,
        'rook': checkRook,
        'knight': checkKnight,
        'bishop': checkBishop,
        'queen': checkQueen,
        'king': checkKing,
    }
    return move_functions[piece](position, color)

def checkKing(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
        
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
               (-1, 1), (-1, -1), (0, 1), (0, -1)]
              
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def checkQueen(position, color):
    moves_list = checkBishop(position, color)
    second_list = checkRook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

def checkBishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
        
    for i in range(4):
        path = True
        chain = 1
        
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
            
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                    
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
                
            else:
                path = False
    return moves_list
    
def checkRook(position, color):
    moves_list = []
    
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
        
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
            
        while path:
        
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
                
            else:
                path = False
    return moves_list
    
def checkKnight(position, color):
    moves_list = []
    
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
        
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
               
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

def checkPawn(position, color):
    moves_list = []
    
    if color == 'white':
    
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if position[1] == 1 and \
                (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and \
                (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
            
    else:
    
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if position[1] == 6 and \
                (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and \
                (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

def sideState(color, white_piece_list, white_location_list, black_piece_list, black_location_list):
    if color == 'white':
        return white_piece_list, white_location_list, black_piece_list, black_location_list
    return black_piece_list, black_location_list, white_piece_list, white_location_list

def squareAttacked(square, by_color, white_piece_list=None, white_location_list=None,
                   black_piece_list=None, black_location_list=None):
    white_piece_list = white_pieces if white_piece_list is None else white_piece_list
    white_location_list = white_locations if white_location_list is None else white_location_list
    black_piece_list = black_pieces if black_piece_list is None else black_piece_list
    black_location_list = black_locations if black_location_list is None else black_location_list
    pieces, locations, _, _ = sideState(
        by_color, white_piece_list, white_location_list, black_piece_list, black_location_list)
    occupied = set(white_location_list + black_location_list)
    target_x, target_y = square

    for piece, (x, y) in zip(pieces, locations):
        dx, dy = target_x - x, target_y - y
        if piece == 'pawn':
            direction = 1 if by_color == 'white' else -1
            if abs(dx) == 1 and dy == direction:
                return True
        elif piece == 'knight':
            if (abs(dx), abs(dy)) in ((1, 2), (2, 1)):
                return True
        elif piece == 'king':
            if max(abs(dx), abs(dy)) == 1:
                return True
        else:
            diagonal = abs(dx) == abs(dy) and dx != 0
            straight = (dx == 0) != (dy == 0)
            if piece == 'rook' and not straight:
                continue
            if piece == 'bishop' and not diagonal:
                continue
            if piece == 'queen' and not (straight or diagonal):
                continue
            if piece not in ('rook', 'bishop', 'queen'):
                continue

            step_x = (dx > 0) - (dx < 0)
            step_y = (dy > 0) - (dy < 0)
            check_x, check_y = x + step_x, y + step_y
            blocked = False
            while (check_x, check_y) != square:
                if (check_x, check_y) in occupied:
                    blocked = True
                    break
                check_x += step_x
                check_y += step_y
            if not blocked:
                return True
    return False

def kingInCheck(color, white_piece_list=None, white_location_list=None,
                black_piece_list=None, black_location_list=None):
    white_piece_list = white_pieces if white_piece_list is None else white_piece_list
    white_location_list = white_locations if white_location_list is None else white_location_list
    black_piece_list = black_pieces if black_piece_list is None else black_piece_list
    black_location_list = black_locations if black_location_list is None else black_location_list
    pieces, locations, _, _ = sideState(
        color, white_piece_list, white_location_list, black_piece_list, black_location_list)
        
    if 'king' not in pieces:
        return True
        
    king_square = locations[pieces.index('king')]
    enemy_color = 'black' if color == 'white' else 'white'
    return squareAttacked(king_square, enemy_color, white_piece_list, white_location_list,
                          black_piece_list, black_location_list)

def isKingCapture(target, color):
    enemy_pieces = black_pieces if color == 'white' else white_pieces
    enemy_locations = black_locations if color == 'white' else white_locations
    return any(piece == 'king' and location == target
               for piece, location in zip(enemy_pieces, enemy_locations))

def moveLeavesKingSafe(piece_index, source, target, color):
    white_piece_list, white_location_list = white_pieces.copy(), white_locations.copy()
    black_piece_list, black_location_list = black_pieces.copy(), black_locations.copy()
    own_pieces, own_locations, enemy_pieces, enemy_locations = sideState(
        color, white_piece_list, white_location_list, black_piece_list, black_location_list)
    moving_piece = own_pieces[piece_index]
    own_locations[piece_index] = target

    if target in enemy_locations:
        captured_index = enemy_locations.index(target)
        enemy_locations.pop(captured_index)
        enemy_pieces.pop(captured_index)

    if moving_piece == 'king' and abs(target[0] - source[0]) == 2:
        row = source[1]
        if target[0] == 6:
            rook_source, rook_target = (7, row), (5, row)
        else:
            rook_source, rook_target = (0, row), (3, row)
            
        if rook_source not in own_locations:
            return False
        own_locations[own_locations.index(rook_source)] = rook_target

    return not kingInCheck(color, white_piece_list, white_location_list,
                           black_piece_list, black_location_list)

def kingSafeAt(color, target):
    white_piece_list, white_location_list = white_pieces.copy(), white_locations.copy()
    black_piece_list, black_location_list = black_pieces.copy(), black_locations.copy()
    own_pieces, own_locations, enemy_pieces, enemy_locations = sideState(
        color, white_piece_list, white_location_list, black_piece_list, black_location_list)
    king_index = own_pieces.index('king')
    
    if target in enemy_locations:
        captured_index = enemy_locations.index(target)
        enemy_locations.pop(captured_index)
        enemy_pieces.pop(captured_index)
    own_locations[king_index] = target
    
    return not kingInCheck(color, white_piece_list, white_location_list,
                           black_piece_list, black_location_list)

def castlingMoves(color, king_position):
    row = 0 if color == 'white' else 7
    if king_position != (4, row) or kingInCheck(color):
        return []

    pieces = white_pieces if color == 'white' else black_pieces
    locations = white_locations if color == 'white' else black_locations
    rights = castling_rights[color]
    moves = []

    for side, rook_start, clear_squares, transit_squares, king_target in (
            ('king_side', (7, row), ((5, row), (6, row)), ((5, row), (6, row)), (6, row)),
            ('queen_side', (0, row), ((1, row), (2, row), (3, row)), ((3, row), (2, row)), (2, row))):
        if not rights[side] or rook_start not in locations:
            continue
        rook_index = locations.index(rook_start)
        if pieces[rook_index] != 'rook':
            continue
        if any(square in white_locations or square in black_locations for square in clear_squares):
            continue
        if all(kingSafeAt(color, square) for square in transit_squares):
            moves.append(king_target)
    return moves

def updateCastlingRights(color, piece, source, target, captured_piece=None):
    if piece == 'king':
        castling_rights[color]['king_side'] = False
        castling_rights[color]['queen_side'] = False
    elif piece == 'rook':
        row = 0 if color == 'white' else 7
        if source == (0, row):
            castling_rights[color]['queen_side'] = False
        elif source == (7, row):
            castling_rights[color]['king_side'] = False

    enemy_color = 'black' if color == 'white' else 'white'
    enemy_row = 0 if enemy_color == 'white' else 7
    if captured_piece == 'rook':
        if target == (0, enemy_row):
            castling_rights[enemy_color]['queen_side'] = False
        elif target == (7, enemy_row):
            castling_rights[enemy_color]['king_side'] = False

def hasLegalMove(color, options):
    pieces = white_pieces if color == 'white' else black_pieces
    return any(moves for piece, moves in zip(pieces, options))

def makeMove(color, piece_index, target):
    global turn_step, selection, valid_moves, black_options, white_options
    global winner, game_over

    own_pieces = white_pieces if color == 'white' else black_pieces
    own_locations = white_locations if color == 'white' else black_locations
    enemy_pieces = black_pieces if color == 'white' else white_pieces
    enemy_locations = black_locations if color == 'white' else white_locations
    source = own_locations[piece_index]
    moving_piece = own_pieces[piece_index]
    captured_piece = None

    if target in enemy_locations:
        captured_index = enemy_locations.index(target)
        captured_piece = enemy_pieces[captured_index]
    updateCastlingRights(color, moving_piece, source, target, captured_piece)

    if captured_piece is not None:
        captured_index = enemy_locations.index(target)
        enemy_pieces.pop(captured_index)
        enemy_locations.pop(captured_index)
        if color == 'white':
            captured_white_pieces.append(captured_piece)
        else:
            captured_black_pieces.append(captured_piece)

    own_locations[piece_index] = target
    if moving_piece == 'king' and abs(target[0] - source[0]) == 2:
        row = source[1]
        rook_source, rook_target = ((7, row), (5, row)) if target[0] == 6 else ((0, row), (3, row))
        rook_index = own_locations.index(rook_source)
        own_locations[rook_index] = rook_target

    black_options = checkOptions(black_pieces, black_locations, 'black')
    white_options = checkOptions(white_pieces, white_locations, 'white')
    turn_step = 2 if color == 'white' else 0
    selection = 100
    valid_moves = []

    next_color = 'black' if color == 'white' else 'white'
    next_options = black_options if next_color == 'black' else white_options
    if not hasLegalMove(next_color, next_options):
        if kingInCheck(next_color):
            winner = 'White' if color == 'white' else 'Black'
        else:
            winner = 'draw'
        game_over = True

def checkValidMoves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options
    
def drawValid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
        
    for i in range(len(moves)):
        pygame.draw.circle(
            screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
            
def drawCaptured():
    for i in range(len(captured_white_pieces)):
        captured_piece = captured_white_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
        
    for i in range(len(captured_black_pieces)):
        captured_piece = captured_black_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))

# draw a flashing square around king if in check
def drawCheck():
    if turn_step < 2:
        if 'king' in white_pieces and kingInCheck('white'):
            king_index = white_pieces.index('king')
            if counter < 15:
                pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                      white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces and kingInCheck('black'):
            king_index = black_pieces.index('king')
            if counter < 15:
                pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                       black_locations[king_index][1] * 100 + 1, 100, 100], 5)
def drawGameOver():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    message = 'Stalemate: draw.' if winner == 'draw' else f'{winner} wins!'
    screen.blit(font.render(message, True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to restart.', True, 'white'), (210, 240))

# Main game loop
black_options = checkOptions(black_pieces, black_locations, 'black')
white_options = checkOptions(white_pieces, white_locations, 'white')
run = True

while run:
    timer.tick(fps)
    
    if counter < 30: counter += 1
    else: counter = 0
    
    screen.fill('dark gray')
    drawBoard()
    drawPieces()
    drawCaptured()
    drawCheck()
    
    if selection != 100:
        valid_moves = checkValidMoves()
        drawValid(valid_moves)

# Event handling must run every frame so the window stays responsive.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Handling left mouse button clicks when the game is not over
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)

            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'Black'
                elif click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    turn_step = 1
                    valid_moves = white_options[selection]
                elif selection != 100 and click_coords in valid_moves:
                    makeMove('white', selection, click_coords)

            else:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'White'
                elif click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    turn_step = 3
                    valid_moves = black_options[selection]
                elif selection != 100 and click_coords in valid_moves:
                    makeMove('black', selection, click_coords)

        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_RETURN:
            game_over = False
            winner = ''
            white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                            'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
            white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                               (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
            black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                            'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
            black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                               (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
            captured_white_pieces = []
            captured_black_pieces = []
            castling_rights = {
                'white': {'king_side': True, 'queen_side': True},
                'black': {'king_side': True, 'queen_side': True},
            }
            turn_step = 0
            selection = 100
            valid_moves = []
            black_options = checkOptions(black_pieces, black_locations, 'black')
            white_options = checkOptions(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        drawGameOver()

    # Present the frame; without this, Pygame keeps showing a blank window.
    pygame.display.flip()

pygame.quit()
