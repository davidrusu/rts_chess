BLACK = 0
WHITE = 1

PAWN = 0
BISHOP = 1
KNIGHT = 2
ROOK = 3
QUEEN = 4
KING = 5

class Piece:
    def __init__(self, x, y, type, player):
        self.x = x
        self.y = y
        self.type = type
        self.player = player

pieces = [
    Piece(0, 0, ROOK, WHITE),
    Piece(1, 0, KNIGHT, WHITE),
    Piece(2, 0, BISHOP, WHITE),
    Piece(3, 0, QUEEN, WHITE),
    Piece(4, 0, KING, WHITE),
    Piece(5, 0, BISHOP, WHITE),
    Piece(6, 0, KNIGHT, WHITE),
    Piece(7, 0, ROOK, WHITE)
] + [Piece(x, 1, PAWN, WHITE) for x in range(0, 8)]
pieces += [
    Piece(0, 7, ROOK, BLACK),
    Piece(1, 7, KNIGHT, BLACK),
    Piece(2, 7, BISHOP, BLACK),
    Piece(3, 7, QUEEN, BLACK),
    Piece(4, 7, KING, BLACK),
    Piece(5, 7, BISHOP, BLACK),
    Piece(6, 7, KNIGHT, BLACK),
    Piece(7, 7, ROOK, BLACK)
] + [Piece(x, 6, PAWN, BLACK) for x in range(0, 8)]

selected_piece = None
mouse_is_pressed = False
panning = False

cell_s = 50
offset = PVector(0, 0)
drag_start = None

def setup():
    size(500, 500)

def valid_moves(piece):
    x_off = floor(offset.x / cell_s)
    y_off = floor(offset.y / cell_s)
    min_x = -x_off - 2
    min_y = -y_off - 2
    max_x = -x_off + int(width / cell_s + 1)
    max_y = -y_off + int(height / cell_s + 1)
    occupied = [(p.x, p.y) for p in pieces if p != piece]
    moves = []
    if piece.type == PAWN or piece.type == KING:
        moves = [
            (piece.x - 1, piece.y),
            (piece.x, piece.y - 1),
            (piece.x + 1, piece.y),
            (piece.x, piece.y + 1)
        ]
        moves = [m for m in moves if m not in occupied]
    elif piece.type == ROOK:
        for x in range(piece.x + 1, max_x):
            if (x, piece.y) in occupied:
                break
            moves.append((x, piece.y))
        for x in range(piece.x - 1, min_x, -1):
            if (x, piece.y) in occupied:
                break
            moves.append((x, piece.y))
        for y in range(piece.y + 1, max_y):
            if (piece.x, y) in occupied:
                break
            moves.append((piece.x, y))
        for y in range(piece.y - 1, min_y, -1):
            if (piece.x, y) in occupied:
                break
            moves.append((piece.x, y))
    elif piece.type == KNIGHT:
        moves = [
            (piece.x - 2, piece.y - 1),
            (piece.x - 2, piece.y + 1),
            (piece.x + 2, piece.y - 1),
            (piece.x + 2, piece.y + 1),
            (piece.x - 1, piece.y - 2),
            (piece.x + 1, piece.y - 2),
            (piece.x - 1, piece.y + 2),
            (piece.x + 1, piece.y + 2)
        ]
        moves = [m for m in moves if m not in occupied]
    elif piece.type == BISHOP:
        for x, y in zip(range(piece.x + 1, max_x), range(piece.y + 1, max_y)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
        for x, y in zip(range(piece.x - 1, min_x, -1), range(piece.y + 1, max_y)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
        for x, y in zip(range(piece.x + 1, max_x), range(piece.y - 1, min_y, -1)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
        for x, y in zip(range(piece.x - 1, min_x, -1), range(piece.y - 1, min_y, -1)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
    elif piece.type == QUEEN:
        # diags
        for x, y in zip(range(piece.x + 1, max_x), range(piece.y + 1, max_y)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
        for x, y in zip(range(piece.x - 1, min_x, -1), range(piece.y + 1, max_y)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
        for x, y in zip(range(piece.x + 1, max_x), range(piece.y - 1, min_y, -1)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
        for x, y in zip(range(piece.x - 1, min_x, -1), range(piece.y - 1, min_y, -1)):
            if (x, y) in occupied:
                break
            moves.append((x, y))
        # straights
        for x in range(piece.x + 1, max_x):
            if (x, piece.y) in occupied:
                break
            moves.append((x, piece.y))
        for x in range(piece.x - 1, min_x, -1):
            if (x, piece.y) in occupied:
                break
            moves.append((x, piece.y))
        for y in range(piece.y + 1, max_y):
            if (piece.x, y) in occupied:
                break
            moves.append((piece.x, y))
        for y in range(piece.y - 1, min_y, -1):
            if (piece.x, y) in occupied:
                break
            moves.append((piece.x, y))
        
    return moves

def grid_mouse():
    grid_x = floor((mouseX - offset.x) / cell_s)
    grid_y = floor((mouseY - offset.y) / cell_s)
    return (grid_x, grid_y)

def find_mouse_piece():
    mouse_on_grid = grid_mouse()
    for piece in pieces:
        if (piece.x, piece.y) == mouse_on_grid:
            return piece
    return None

def update():
    global selected_piece, drag_start, panning, cell_s

    if keyPressed:
        if key == 'z':
            cell_s *= 1.1;
        elif key == 'x':
            cell_s *= 0.9;

    if mouse_is_pressed:
        if selected_piece is None and not panning:
            selected_piece = find_mouse_piece()
        
        if selected_piece is None:
            panning = True
    
    if not mouse_is_pressed:
        if selected_piece is not None:
            grid_x, grid_y = grid_mouse()
            if (grid_x, grid_y) in valid_moves(selected_piece):
                selected_piece.x = grid_x
                selected_piece.y = grid_y
        elif drag_start is not None:
            offset.add(PVector(mouseX - drag_start.x, mouseY - drag_start.y))
        
        selected_piece = None
        drag_start = None
        panning = False

def mousePressed():
    global mouse_is_pressed, drag_start
    mouse_is_pressed = True
    drag_start = PVector(mouseX, mouseY)

def mouseReleased():
    global mouse_is_pressed, drag_start
    mouse_is_pressed = False

def draw():
    global drag_start, offset, cell_s
    update()

    real_offset = PVector(offset.x, offset.y)
    if drag_start is not None and selected_piece is None:
        real_offset.add(PVector(mouseX, mouseY).sub(drag_start))

    x_shift = real_offset.x - int(real_offset.x / cell_s) * cell_s    
    y_shift = real_offset.y - int(real_offset.y / cell_s) * cell_s
    
    x_off = int(real_offset.x / cell_s)
    y_off = int(real_offset.y / cell_s)
    noStroke()
    move_suggestions = valid_moves(selected_piece) if selected_piece else []
    for x in range(-1, int(width / cell_s) + 2):
        for y in range(-1, int(height / cell_s) + 2):
            grid_x = x - x_off
            grid_y = y - y_off
            if (grid_x, grid_y) in move_suggestions:
                fill(250, 250, 0)
            elif (grid_x + grid_y) % 2 == 0:
                fill(100)
            else:
                fill(150)
            rect(
              x * cell_s + x_shift,
              y * cell_s + y_shift,
              cell_s, cell_s
            )

    translate(real_offset.x, real_offset.y)
    for piece in pieces:
        pixel_x = piece.x * cell_s + cell_s / 2
        pixel_y = piece.y * cell_s + cell_s / 2
        translate(pixel_x, pixel_y);
        if piece.player == WHITE:
            fill(255)
        else:
            fill(0)
        if piece.type == PAWN:
            ellipse(0, -cell_s * 0.25, cell_s * 0.4, cell_s * 0.4)
            ellipse(0, -cell_s * 0.05, cell_s * 0.4, cell_s * 0.2)
            arc(0, cell_s * 0.4, cell_s * 0.9, cell_s * 0.85, -PI, 0, CHORD)
        elif piece.type == ROOK:
            rect(-cell_s * 0.25, -cell_s * 0.2, cell_s * 0.5, cell_s * 0.5)
            rect(-cell_s * 0.35, -cell_s * 0.4, cell_s * 0.7, cell_s * 0.1)
            arc(0, cell_s * 0.4, cell_s * 0.9, cell_s * .5, -PI, 0, CHORD)
            arc(0, -cell_s * 0.4, cell_s * 0.7, cell_s * .6, 0, PI, CHORD)
        elif piece.type == KNIGHT:
            beginShape()
            vertex(-cell_s * 0.25, -cell_s * 0.1)
            vertex(-cell_s * 0.30, -cell_s * 0.25)
            vertex(cell_s * 0., -cell_s * 0.4)
            vertex(cell_s * 0.25, -cell_s * 0.4)
            vertex(cell_s * 0.4, cell_s * 0.1)
            vertex(cell_s * 0., cell_s * 0.4)
            vertex(-cell_s * 0.3, cell_s * 0.25)
            vertex(-cell_s * 0.35, cell_s * 0.1)
            #vertex(cell_s * 0., -cell_s * 0.1)
            vertex(-cell_s * 0., -cell_s * 0.1)
            endShape(CLOSE)
            arc(0, cell_s * 0.4, cell_s * 0.9, cell_s * .5, -PI, 0, CHORD)
        elif piece.type == BISHOP:
            ellipse(0, -cell_s * 0.4, cell_s * 0.1, cell_s * 0.1)
            arc(0, -cell_s * 0.1, cell_s * 0.5, cell_s * .6, -PI/2 - PI / 5, PI + PI / 4, PIE)

            # ellipse(0, -cell_s * 0., cell_s * 0.4, cell_s * 0.4)
            ellipse(0, cell_s * 0.15, cell_s * 0.5, cell_s * 0.2)
            arc(0, cell_s * 0.4, cell_s * 0.9, cell_s * .5, -PI, 0, CHORD)
        elif piece.type == QUEEN:
            beginShape()
            vertex(-cell_s * 0.4, -cell_s * 0.4)
            vertex(-cell_s * 0.225, -cell_s * 0.05)
            vertex(-cell_s * 0.2, -cell_s * 0.4)
            vertex(cell_s * 0, -cell_s * 0.1)
            vertex(cell_s * 0.2, -cell_s * 0.4)
            vertex(cell_s * 0.225, -cell_s * 0.05)
            vertex(cell_s * 0.4, -cell_s * 0.4)
            vertex(cell_s * 0.3, cell_s * 0.4)
            vertex(-cell_s * 0.3, cell_s * 0.4)
            endShape(CLOSE)
            arc(0, cell_s * 0.4, cell_s * 0.9, cell_s * .5, -PI, 0, CHORD)
        elif piece.type == KING:
            beginShape()
            vertex(-cell_s * 0.4, -cell_s * 0.3)
            vertex(-cell_s * 0.3, -cell_s * 0.15)
            vertex(-cell_s * 0.05, -cell_s * 0.15)
            vertex(cell_s * 0, -cell_s * 0.4)
            vertex(cell_s * 0.05, -cell_s * 0.15)
            vertex(cell_s * 0.3, -cell_s * 0.15)
            vertex(cell_s * 0.4, -cell_s * 0.3)
            vertex(cell_s * 0.3, cell_s * 0.4)
            vertex(-cell_s * 0.3, cell_s * 0.4)
            endShape(CLOSE)
            arc(0, cell_s * 0.4, cell_s * 0.9, cell_s * .5, -PI, 0, CHORD)
            arc(-cell_s * 0.15, -cell_s * 0.1, cell_s * 0.4, cell_s * .3, -PI, 0, CHORD)
            arc(cell_s * 0.15, -cell_s * 0.1, cell_s * 0.4, cell_s * .3, -PI, 0, CHORD)
        else:
            ellipse(0, 0, cell_s * 0.9, cell_s * 0.9)
        translate(-pixel_x, -pixel_y)
