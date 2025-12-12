# Chess Game với UI/UX hiện đại
# Sử dụng Pygame để tạo giao diện đồ họa

import pygame as p
import ChessEngine, ChessAI
import sys
from multiprocessing import Process, Queue

# ===== CẤU HÌNH GIAO DIỆN =====
BOARD_WIDTH = BOARD_HEIGHT = 640  # Tăng kích thước (cũ: 512)
MOVE_LOG_PANEL_WIDTH = 280  # Tăng theo tỷ lệ
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 60  # Tăng FPS cho mượt hơn
IMAGES = {}

# ===== BẢNG MÀU - MULTIPLE THEMES =====
THEMES = {
    'chess.com': {
        'name': 'Chess.com',
        'light_square': p.Color(238, 238, 210),      # Kem
        'dark_square': p.Color(118, 150, 86),        # Xanh lá
        'selected': p.Color(246, 246, 105),
        'last_move_light': p.Color(247, 247, 105),
        'last_move_dark': p.Color(187, 203, 43),
        'panel_bg': p.Color(49, 46, 43),
        'panel_header': p.Color(39, 37, 34),
    },
    'lichess': {
        'name': 'Cờ Vua VN',
        'light_square': p.Color(240, 218, 200),      # Hồng kem nhạt
        'dark_square': p.Color(180, 135, 100),       # Nâu xám
        'selected': p.Color(205, 210, 90),           # Vàng xanh (highlight)
        'last_move_light': p.Color(205, 210, 90),
        'last_move_dark': p.Color(170, 165, 70),
        'panel_bg': p.Color(60, 45, 35),
        'panel_header': p.Color(50, 35, 25),
    },
    'wood': {
        'name': 'Classic Wood',
        'light_square': p.Color(255, 206, 158),      # Gỗ sáng
        'dark_square': p.Color(209, 139, 71),        # Gỗ tối
        'selected': p.Color(255, 255, 100),
        'last_move_light': p.Color(255, 223, 150),
        'last_move_dark': p.Color(225, 170, 90),
        'panel_bg': p.Color(60, 40, 20),
        'panel_header': p.Color(45, 30, 15),
    },
    'ocean': {
        'name': 'Ocean Blue',
        'light_square': p.Color(222, 235, 247),      # Xanh nhạt
        'dark_square': p.Color(86, 150, 185),        # Xanh biển
        'selected': p.Color(135, 206, 250),
        'last_move_light': p.Color(180, 220, 255),
        'last_move_dark': p.Color(100, 170, 210),
        'panel_bg': p.Color(30, 50, 70),
        'panel_header': p.Color(20, 40, 60),
    },
    'purple': {
        'name': 'Royal Purple',
        'light_square': p.Color(230, 220, 240),      # Tím nhạt
        'dark_square': p.Color(136, 97, 168),        # Tím đậm
        'selected': p.Color(200, 180, 255),
        'last_move_light': p.Color(220, 200, 255),
        'last_move_dark': p.Color(160, 120, 200),
        'panel_bg': p.Color(45, 35, 55),
        'panel_header': p.Color(35, 25, 45),
    },
}

THEME_NAMES = list(THEMES.keys())
current_theme_index = 0

def get_colors():
    """Lấy bảng màu hiện tại"""
    theme = THEMES[THEME_NAMES[current_theme_index]]
    return {
        'light_square': theme['light_square'],
        'dark_square': theme['dark_square'],
        'selected': theme['selected'],
        'last_move_light': theme['last_move_light'],
        'last_move_dark': theme['last_move_dark'],
        'valid_move_dot': p.Color(0, 0, 0, 50),
        'capture_hint': p.Color(235, 97, 80),
        'panel_bg': theme['panel_bg'],
        'panel_header': theme['panel_header'],
        'text_white': p.Color(255, 255, 255),
        'text_gray': p.Color(180, 180, 180),
        'overlay': p.Color(0, 0, 0, 180),
        'check_highlight': p.Color(235, 97, 80, 200),
        'theme_name': theme['name'],
    }


def loadImages():
    """Tải hình ảnh các quân cờ từ thư mục images"""
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), 
            (SQUARE_SIZE, SQUARE_SIZE)
        )


# ===== ÂM THANH =====
SOUNDS = {}

def loadSounds():
    """Tải file âm thanh - hỗ trợ MP3 và WAV"""
    p.mixer.init()
    sound_files = {
        'move': ['sounds/move.mp3', 'sounds/move.wav'],
        'capture': ['sounds/capture.mp3', 'sounds/capture.wav'],
        'check': ['sounds/check.mp3', 'sounds/check.wav'],
        'checkmate': ['sounds/checkmate.mp3', 'sounds/checkmate.wav']
    }
    
    import os
    for sound_name, file_paths in sound_files.items():
        for path in file_paths:
            if os.path.exists(path) and os.path.getsize(path) > 100:  # Check file tồn tại và > 100 bytes
                try:
                    SOUNDS[sound_name] = p.mixer.Sound(path)
                    SOUNDS[sound_name].set_volume(0.5)
                    break
                except:
                    continue
    
    if not SOUNDS:
        print("Warning: Could not load any sounds")

def playSound(sound_name):
    """Phát âm thanh"""
    if sound_name in SOUNDS:
        SOUNDS[sound_name].play()

def showDifficultyMenu(screen, clock):
    """Màn hình chọn độ khó với thiết kế hiện đại"""
    menu_running = True
    selected_index = 2  # Mặc định chọn Hard
    difficulties = list(ChessAI.DIFFICULTY_LEVELS.keys())
    
    # Fonts
    title_font = p.font.SysFont("Segoe UI", 42, True, False)
    subtitle_font = p.font.SysFont("Segoe UI", 16, False, False)
    button_font = p.font.SysFont("Segoe UI", 20, True, False)
    desc_font = p.font.SysFont("Segoe UI", 16, False, False)
    
    # Colors
    bg_color = p.Color(28, 28, 35)
    card_color = p.Color(45, 45, 55)
    card_hover = p.Color(60, 60, 75)
    card_selected = p.Color(75, 140, 100)
    text_white = p.Color(255, 255, 255)
    text_gray = p.Color(160, 160, 170)
    accent_green = p.Color(118, 200, 120)
    
    # Descriptions for each level
    descriptions = {
        'easy': "Dành cho người mới bắt đầu",
        'medium': "Thử thách vừa phải",
        'hard': "Dành cho người có kinh nghiệm",
        'very_hard': "Cực kỳ khó - AI suy nghĩ lâu"
    }
    
    # Card dimensions - Tăng kích thước để không vỡ chữ
    card_width = 200
    card_height = 140
    card_spacing = 15
    total_width = len(difficulties) * card_width + (len(difficulties) - 1) * card_spacing
    start_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - total_width) // 2
    card_y = 260
    
    hover_index = -1
    animation_offset = 0
    
    while menu_running:
        mouse_pos = p.mouse.get_pos()
        
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                return None
            
            if e.type == p.MOUSEBUTTONDOWN:
                # Check if clicked on a card
                for i in range(len(difficulties)):
                    card_x = start_x + i * (card_width + card_spacing)
                    card_rect = p.Rect(card_x, card_y, card_width, card_height)
                    if card_rect.collidepoint(mouse_pos):
                        selected_index = i
                        ChessAI.set_difficulty(difficulties[i])
                        menu_running = False
                        break
            
            if e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    selected_index = (selected_index - 1) % len(difficulties)
                elif e.key == p.K_RIGHT:
                    selected_index = (selected_index + 1) % len(difficulties)
                elif e.key == p.K_RETURN or e.key == p.K_SPACE:
                    ChessAI.set_difficulty(difficulties[selected_index])
                    menu_running = False
        
        # Animation
        animation_offset = (animation_offset + 1) % 360
        
        # Draw background with gradient effect
        screen.fill(bg_color)
        
        # Decorative circles (subtle)
        for i in range(3):
            alpha_surface = p.Surface((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT), p.SRCALPHA)
            radius = 150 + i * 100
            p.draw.circle(alpha_surface, (118, 150, 86, 15), 
                         (100 + i * 50, 100), radius)
            p.draw.circle(alpha_surface, (86, 150, 185, 15),
                         (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - 100 - i * 50, BOARD_HEIGHT - 100), radius)
            screen.blit(alpha_surface, (0, 0))
        
        # Title with shadow
        title_shadow = title_font.render("Chess AI", True, p.Color(0, 0, 0))
        title_text = title_font.render("Chess AI", True, text_white)
        title_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - title_text.get_width()) // 2
        screen.blit(title_shadow, (title_x + 2, 82))
        screen.blit(title_text, (title_x, 80))
        
        # Subtitle
        subtitle = subtitle_font.render("Chon do kho de bat dau", True, text_gray)
        subtitle_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - subtitle.get_width()) // 2
        screen.blit(subtitle, (subtitle_x, 140))
        
        # Draw difficulty cards
        for i, diff_key in enumerate(difficulties):
            diff_info = ChessAI.DIFFICULTY_LEVELS[diff_key]
            card_x = start_x + i * (card_width + card_spacing)
            card_rect = p.Rect(card_x, card_y, card_width, card_height)
            
            # Check hover
            is_hovered = card_rect.collidepoint(mouse_pos)
            is_selected = (i == selected_index)
            
            # Card background with rounded corners effect
            if is_selected:
                color = card_selected
                # Glow effect for selected
                glow_surface = p.Surface((card_width + 10, card_height + 10), p.SRCALPHA)
                p.draw.rect(glow_surface, (118, 200, 120, 50), 
                           p.Rect(0, 0, card_width + 10, card_height + 10), border_radius=15)
                screen.blit(glow_surface, (card_x - 5, card_y - 5))
            elif is_hovered:
                color = card_hover
            else:
                color = card_color
            
            # Draw card
            p.draw.rect(screen, color, card_rect, border_radius=12)
            
            # Border
            border_color = accent_green if is_selected else p.Color(80, 80, 90)
            p.draw.rect(screen, border_color, card_rect, 2, border_radius=12)
            
            # Emoji (larger)
            emoji_font = p.font.SysFont("Segoe UI Emoji", 32)
            emoji_text = emoji_font.render(diff_info['emoji'], True, text_white)
            emoji_x = card_x + (card_width - emoji_text.get_width()) // 2
            screen.blit(emoji_text, (emoji_x, card_y + 20))
            
            # Difficulty name
            name_text = button_font.render(diff_info['name'], True, text_white)
            name_x = card_x + (card_width - name_text.get_width()) // 2
            screen.blit(name_text, (name_x, card_y + 65))
            
            # Depth info
            depth_text = desc_font.render(f"Depth: {diff_info['depth']}", True, text_gray)
            depth_x = card_x + (card_width - depth_text.get_width()) // 2
            screen.blit(depth_text, (depth_x, card_y + 100))
        
        # Description for hovered/selected card
        current_key = difficulties[selected_index]
        desc_text = desc_font.render(descriptions[current_key], True, text_gray)
        desc_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - desc_text.get_width()) // 2
        screen.blit(desc_text, (desc_x, card_y + card_height + 30))
        
        # Instructions
        inst_text = desc_font.render("Click de chon | Enter de xac nhan | <- -> de di chuyen", True, text_gray)
        inst_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - inst_text.get_width()) // 2
        screen.blit(inst_text, (inst_x, BOARD_HEIGHT - 50))
        
        # Footer
        footer = desc_font.render("HAUI - Tri Tue Nhan Tao", True, p.Color(100, 100, 110))
        footer_x = (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - footer.get_width()) // 2
        screen.blit(footer, (footer_x, BOARD_HEIGHT - 25))
        
        p.display.flip()
        clock.tick(60)
    
    return difficulties[selected_index]


def main():
    """Vòng lặp chính của game"""
    global current_theme_index  # Khai báo global ở đầu hàm
    p.init()
    p.display.set_caption("♟️ Chess AI VIP PRO")
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False
    animate = False
    loadImages()
    loadSounds()  # Tải âm thanh
    
    # === HIỂN THỊ MENU CHỌN ĐỘ KHÓ ===
    selected_difficulty = showDifficultyMenu(screen, clock)
    if selected_difficulty is None:
        return  # User đóng game từ menu
    
    running = True
    square_selected = ()
    player_clicks = []
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    hover_square = ()  # Ô đang hover
    
    # Fonts
    move_log_font = p.font.SysFont("Segoe UI", 13, False, False)
    header_font = p.font.SysFont("Segoe UI", 16, True, False)
    coord_font = p.font.SysFont("Segoe UI", 11, True, False)
    
    player_one = True   # Người chơi quân trắng
    player_two = False  # AI chơi quân đen

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        
        # Lấy vị trí chuột để hover effect
        mouse_pos = p.mouse.get_pos()
        if mouse_pos[0] < BOARD_WIDTH:
            hover_square = (mouse_pos[1] // SQUARE_SIZE, mouse_pos[0] // SQUARE_SIZE)
        else:
            hover_square = ()
        
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
                
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    
                    if square_selected == (row, col) or col >= 8:
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                        
                    if len(player_clicks) == 2 and human_turn:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                    
                if e.key == p.K_r:  # Reset
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                
                if e.key == p.K_t:  # Đổi Theme
                    current_theme_index = (current_theme_index + 1) % len(THEME_NAMES)
                
                if e.key == p.K_d:  # Đổi Difficulty
                    ChessAI.cycle_difficulty()
                
                # End game options
                if game_over:
                    if e.key == p.K_1:  # Chơi lại
                        game_state = ChessEngine.GameState()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    
                    if e.key == p.K_2:  # Về menu chọn độ khó
                        if ai_thinking:
                            move_finder_process.terminate()
                        # Reset và quay về menu
                        selected_difficulty = showDifficultyMenu(screen, clock)
                        if selected_difficulty is None:
                            running = False
                        else:
                            game_state = ChessEngine.GameState()
                            valid_moves = game_state.getValidMoves()
                            square_selected = ()
                            player_clicks = []
                            move_made = False
                            animate = False
                            game_over = False
                            ai_thinking = False
                            move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ChessAI.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
                # Phát âm thanh sau khi animation
                last_move = game_state.move_log[-1]
                if last_move.is_capture:
                    playSound('capture')
                else:
                    playSound('move')
            valid_moves = game_state.getValidMoves()
            
            # Kiểm tra chiếu/chiếu hết để phát âm thanh
            if game_state.checkmate:
                playSound('checkmate')
            elif game_state.in_check:
                playSound('check')
            
            move_made = False
            animate = False
            move_undone = False

        # Vẽ giao diện
        drawGameState(screen, game_state, valid_moves, square_selected, hover_square)
        drawCoordinates(screen, coord_font)
        drawMoveLog(screen, game_state, move_log_font, header_font, ai_thinking)

        # Kiểm tra kết thúc game
        if not game_over:
            if game_state.checkmate:
                game_over = True
            elif game_state.stalemate:
                game_over = True
        
        # Vẽ thông báo kết thúc game (chỉ khi game_over = True)
        if game_over:
            if game_state.checkmate:
                if game_state.white_to_move:
                    drawEndGameText(screen, "Chiếu hết! Đen thắng", "Nhấn R để chơi lại")
                else:
                    drawEndGameText(screen, "Chiếu hết! Trắng thắng", "Nhấn R để chơi lại")
            elif game_state.stalemate:
                drawEndGameText(screen, "Hòa cờ!", "Nhấn R để chơi lại")

        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, game_state, valid_moves, square_selected, hover_square):
    """Vẽ toàn bộ trạng thái game"""
    drawBoard(screen)
    highlightSquares(screen, game_state, valid_moves, square_selected, hover_square)
    drawPieces(screen, game_state.board)


def drawBoard(screen):
    """Vẽ bàn cờ với màu hiện đại"""
    COLORS = get_colors()
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            is_light = (row + column) % 2 == 0
            color = COLORS['light_square'] if is_light else COLORS['dark_square']
            p.draw.rect(screen, color, 
                       p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected, hover_square):
    """Highlight các ô với hiệu ứng đẹp"""
    COLORS = get_colors()
    
    # 1. Highlight nước đi cuối cùng
    if len(game_state.move_log) > 0:
        last_move = game_state.move_log[-1]
        for sq in [(last_move.start_row, last_move.start_col), (last_move.end_row, last_move.end_col)]:
            is_light = (sq[0] + sq[1]) % 2 == 0
            color = COLORS['last_move_light'] if is_light else COLORS['last_move_dark']
            p.draw.rect(screen, color,
                       p.Rect(sq[1] * SQUARE_SIZE, sq[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    # 2. Highlight vua đang bị chiếu
    if game_state.in_check:
        if game_state.white_to_move:
            king_sq = game_state.white_king_location
        else:
            king_sq = game_state.black_king_location
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE), p.SRCALPHA)
        s.fill(COLORS['check_highlight'])
        screen.blit(s, (king_sq[1] * SQUARE_SIZE, king_sq[0] * SQUARE_SIZE))
    
    # 3. Highlight ô được chọn
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'):
            # Ô được chọn
            p.draw.rect(screen, COLORS['selected'],
                       p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Vẽ lại quân cờ lên ô được highlight
            piece = game_state.board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], 
                           p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Highlight nước đi hợp lệ với chấm tròn / viền tròn
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    center_x = move.end_col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = move.end_row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    if move.is_capture or game_state.board[move.end_row][move.end_col] != "--":
                        # Ô có quân địch - vẽ viền tròn
                        p.draw.circle(screen, COLORS['capture_hint'], 
                                     (center_x, center_y), SQUARE_SIZE // 2 - 2, 4)
                    else:
                        # Ô trống - vẽ chấm tròn nhỏ
                        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE), p.SRCALPHA)
                        p.draw.circle(s, (0, 0, 0, 40), 
                                     (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 6)
                        screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))
    
    # 4. Hover effect nhẹ
    if hover_square != () and hover_square != square_selected:
        row, col = hover_square
        if 0 <= row < 8 and 0 <= col < 8:
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE), p.SRCALPHA)
            s.fill((255, 255, 255, 30))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def drawPieces(screen, board):
    """Vẽ quân cờ lên bàn"""
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], 
                           p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawCoordinates(screen, font):
    """Vẽ tọa độ a-h, 1-8"""
    COLORS = get_colors()
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']
    
    for i in range(8):
        # Chữ cái ở dưới
        is_light = (7 + i) % 2 == 0
        color = COLORS['dark_square'] if is_light else COLORS['light_square']
        text = font.render(files[i], True, color)
        screen.blit(text, (i * SQUARE_SIZE + SQUARE_SIZE - 12, BOARD_HEIGHT - 14))
        
        # Số ở bên trái
        is_light = (i + 0) % 2 == 0
        color = COLORS['dark_square'] if is_light else COLORS['light_square']
        text = font.render(ranks[i], True, color)
        screen.blit(text, (3, i * SQUARE_SIZE + 2))


def drawMoveLog(screen, game_state, font, header_font, ai_thinking):
    """Vẽ panel lịch sử nước đi với thiết kế hiện đại"""
    COLORS = get_colors()
    # Background
    panel_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, COLORS['panel_bg'], panel_rect)
    
    # Header
    header_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, 40)
    p.draw.rect(screen, COLORS['panel_header'], header_rect)
    
    title = header_font.render("Lịch sử nước đi", True, COLORS['text_white'])
    screen.blit(title, (BOARD_WIDTH + 15, 10))
    
    # Đường kẻ phân cách
    p.draw.line(screen, COLORS['text_gray'], 
               (BOARD_WIDTH, 40), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, 40), 1)
    
    # AI thinking indicator
    if ai_thinking:
        thinking_text = font.render("🤔 AI đang suy nghĩ...", True, COLORS['selected'])
        screen.blit(thinking_text, (BOARD_WIDTH + 15, 50))
        start_y = 75
    else:
        start_y = 50
    
    # Move log content
    move_log = game_state.move_log
    if len(move_log) == 0:
        hint_text = font.render("Chưa có nước đi nào", True, COLORS['text_gray'])
        screen.blit(hint_text, (BOARD_WIDTH + 15, start_y))
    else:
        padding = 15
        line_height = 22
        text_y = start_y
        
        for i in range(0, len(move_log), 2):
            move_num = str(i // 2 + 1) + "."
            white_move = str(move_log[i])
            black_move = str(move_log[i + 1]) if i + 1 < len(move_log) else ""
            
            # Số thứ tự
            num_text = font.render(move_num, True, COLORS['text_gray'])
            screen.blit(num_text, (BOARD_WIDTH + padding, text_y))
            
            # Nước trắng
            white_text = font.render(white_move, True, COLORS['text_white'])
            screen.blit(white_text, (BOARD_WIDTH + padding + 30, text_y))
            
            # Nước đen
            if black_move:
                black_text = font.render(black_move, True, COLORS['text_white'])
                screen.blit(black_text, (BOARD_WIDTH + padding + 90, text_y))
            
            text_y += line_height
            
            # Giới hạn hiển thị
            if text_y > BOARD_HEIGHT - 50:
                more_text = font.render("...", True, COLORS['text_gray'])
                screen.blit(more_text, (BOARD_WIDTH + padding, text_y))
                break
    
    # Footer với hướng dẫn + Theme name
    footer_y = BOARD_HEIGHT - 50
    p.draw.line(screen, COLORS['text_gray'], 
               (BOARD_WIDTH, footer_y - 5), (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, footer_y - 5), 1)
    
    hint1 = font.render("Z: Undo | R: Reset | T: Theme | D: AI", True, COLORS['text_gray'])
    screen.blit(hint1, (BOARD_WIDTH + 15, footer_y))
    
    # Hiển thị theme hiện tại
    theme_text = font.render(f"🎨 {COLORS['theme_name']}", True, COLORS['text_white'])
    screen.blit(theme_text, (BOARD_WIDTH + 15, footer_y + 20))
    
    # Hiển thị AI difficulty
    diff_info = ChessAI.get_difficulty_info()
    diff_text = font.render(f"{diff_info['emoji']} AI: {diff_info['name']}", True, COLORS['text_white'])
    screen.blit(diff_text, (BOARD_WIDTH + 130, footer_y + 20))


def drawEndGameText(screen, main_text, sub_text):
    """Vẽ thông báo kết thúc game với overlay"""
    COLORS = get_colors()
    # Overlay mờ
    overlay = p.Surface((BOARD_WIDTH, BOARD_HEIGHT), p.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Text chính
    font_main = p.font.SysFont("Segoe UI", 36, True, False)
    font_sub = p.font.SysFont("Segoe UI", 16, False, False)
    font_options = p.font.SysFont("Segoe UI", 18, True, False)
    
    # Shadow effect
    shadow = font_main.render(main_text, True, p.Color(0, 0, 0))
    main = font_main.render(main_text, True, p.Color(255, 255, 255))
    
    main_rect = main.get_rect(center=(BOARD_WIDTH // 2, BOARD_HEIGHT // 2 - 50))
    screen.blit(shadow, main_rect.move(2, 2))
    screen.blit(main, main_rect)
    
    # Options box
    box_width = 280
    box_height = 80
    box_x = (BOARD_WIDTH - box_width) // 2
    box_y = BOARD_HEIGHT // 2
    
    # Draw options box
    box_surface = p.Surface((box_width, box_height), p.SRCALPHA)
    p.draw.rect(box_surface, (50, 50, 60, 220), p.Rect(0, 0, box_width, box_height), border_radius=10)
    p.draw.rect(box_surface, (100, 100, 110), p.Rect(0, 0, box_width, box_height), 2, border_radius=10)
    screen.blit(box_surface, (box_x, box_y))
    
    # Option 1
    opt1 = font_options.render("[1] Choi lai", True, p.Color(120, 220, 120))
    opt1_rect = opt1.get_rect(center=(BOARD_WIDTH // 2, box_y + 25))
    screen.blit(opt1, opt1_rect)
    
    # Option 2
    opt2 = font_options.render("[2] Ve menu chon do kho", True, p.Color(120, 180, 255))
    opt2_rect = opt2.get_rect(center=(BOARD_WIDTH // 2, box_y + 55))
    screen.blit(opt2, opt2_rect)


def animateMove(move, screen, board, clock):
    """Animation di chuyển quân mượt mà"""
    COLORS = get_colors()
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 8  # Nhanh hơn một chút
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    
    for frame in range(frame_count + 1):
        progress = frame / frame_count
        # Easing function (ease-out)
        progress = 1 - (1 - progress) ** 2
        
        row = move.start_row + d_row * progress
        col = move.start_col + d_col * progress
        
        drawBoard(screen)
        drawPieces(screen, board)
        
        # Xóa quân ở vị trí đích
        end_sq_light = (move.end_row + move.end_col) % 2 == 0
        color = COLORS['light_square'] if end_sq_light else COLORS['dark_square']
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        
        # Vẽ quân bị ăn
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        
        # Vẽ quân đang di chuyển
        screen.blit(IMAGES[move.piece_moved], 
                   p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
