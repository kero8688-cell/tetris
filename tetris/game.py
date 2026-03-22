import random
import pygame
from .pieces import Piece, SHAPE_NAMES, BLACK

COLS = 10
ROWS = 20
CELL_SIZE = 30

SIDEBAR_WIDTH = 150
SCREEN_WIDTH  = COLS * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = ROWS * CELL_SIZE

FALL_INTERVAL_INIT = 500   # ms
FALL_INTERVAL_MIN  = 100
LEVEL_SPEED_UP     = 50    # ms per level


class Game:
    def __init__(self):
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False

        self.fall_interval = FALL_INTERVAL_INIT
        self.fall_timer = 0

        self.current_piece = self._new_piece()
        self.next_piece    = self._new_piece()

    # ── 피스 생성 ─────────────────────────────────────────
    def _new_piece(self):
        return Piece(random.choice(SHAPE_NAMES))

    def _spawn_piece(self):
        self.current_piece = self.next_piece
        self.next_piece    = self._new_piece()
        if not self._valid(self.current_piece):
            self.game_over = True

    # ── 충돌 검사 ─────────────────────────────────────────
    def _valid(self, piece, dx=0, dy=0):
        for bx, by in piece.get_absolute_blocks():
            nx, ny = bx + dx, by + dy
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return False
            if ny >= 0 and self.board[ny][nx] is not None:
                return False
        return True

    # ── 피스 잠금 & 라인 클리어 ─────────────────────────
    def _lock_piece(self):
        for bx, by in self.current_piece.get_absolute_blocks():
            if by >= 0:
                self.board[by][bx] = self.current_piece.color
        self._clear_lines()
        self._spawn_piece()

    def _clear_lines(self):
        full = [r for r in range(ROWS) if all(c is not None for c in self.board[r])]
        if not full:
            return
        for r in full:
            del self.board[r]
            self.board.insert(0, [None] * COLS)

        count = len(full)
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += points.get(count, 800) * self.level
        self.lines += count
        self.level = self.lines // 10 + 1
        self.fall_interval = max(
            FALL_INTERVAL_MIN,
            FALL_INTERVAL_INIT - (self.level - 1) * LEVEL_SPEED_UP
        )

    # ── 입력 처리 ─────────────────────────────────────────
    def move_left(self):
        if self._valid(self.current_piece, dx=-1):
            self.current_piece.x -= 1

    def move_right(self):
        if self._valid(self.current_piece, dx=1):
            self.current_piece.x += 1

    def soft_drop(self):
        if self._valid(self.current_piece, dy=1):
            self.current_piece.y += 1
            self.score += 1
        else:
            self._lock_piece()

    def hard_drop(self):
        drop = 0
        while self._valid(self.current_piece, dy=drop + 1):
            drop += 1
        self.current_piece.y += drop
        self.score += drop * 2
        self._lock_piece()

    def rotate(self):
        self.current_piece.rotate()
        # 벽 킥: 회전 후 유효하지 않으면 좌우로 조금씩 밀어서 시도
        if not self._valid(self.current_piece):
            for kick in [1, -1, 2, -2]:
                if self._valid(self.current_piece, dx=kick):
                    self.current_piece.x += kick
                    return
            self.current_piece.rotate_back()

    def toggle_pause(self):
        self.paused = not self.paused

    def restart(self):
        self.__init__()

    # ── 업데이트 (자동 낙하) ─────────────────────────────
    def update(self, dt):
        if self.game_over or self.paused:
            return
        self.fall_timer += dt
        if self.fall_timer >= self.fall_interval:
            self.fall_timer = 0
            if self._valid(self.current_piece, dy=1):
                self.current_piece.y += 1
            else:
                self._lock_piece()

    # ── 유령 피스 위치 계산 ───────────────────────────────
    def get_ghost_y(self):
        drop = 0
        while self._valid(self.current_piece, dy=drop + 1):
            drop += 1
        return self.current_piece.y + drop

    # ── 렌더링 ───────────────────────────────────────────
    def draw(self, screen, fonts):
        screen.fill(BLACK)
        self._draw_board(screen)
        self._draw_ghost(screen)
        self._draw_current(screen)
        self._draw_grid(screen)
        self._draw_sidebar(screen, fonts)
        if self.game_over:
            self._draw_overlay(screen, fonts['large'], "GAME OVER", "R: 재시작")
        elif self.paused:
            self._draw_overlay(screen, fonts['large'], "PAUSE", "P: 계속")

    def _draw_board(self, screen):
        for r in range(ROWS):
            for c in range(COLS):
                color = self.board[r][c]
                if color:
                    pygame.draw.rect(screen, color,
                                     (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))

    def _draw_ghost(self, screen):
        ghost_y = self.get_ghost_y()
        ghost_color = (80, 80, 80)
        for bx, by in self.current_piece.blocks:
            rx = (self.current_piece.x + bx) * CELL_SIZE
            ry = (ghost_y + by) * CELL_SIZE
            pygame.draw.rect(screen, ghost_color,
                             (rx, ry, CELL_SIZE - 1, CELL_SIZE - 1), 2)

    def _draw_current(self, screen):
        for bx, by in self.current_piece.blocks:
            rx = (self.current_piece.x + bx) * CELL_SIZE
            ry = (self.current_piece.y + by) * CELL_SIZE
            if ry >= 0:
                pygame.draw.rect(screen, self.current_piece.color,
                                 (rx, ry, CELL_SIZE - 1, CELL_SIZE - 1))

    def _draw_grid(self, screen):
        grid_color = (40, 40, 40)
        for c in range(COLS + 1):
            pygame.draw.line(screen, grid_color,
                             (c * CELL_SIZE, 0), (c * CELL_SIZE, SCREEN_HEIGHT))
        for r in range(ROWS + 1):
            pygame.draw.line(screen, grid_color,
                             (0, r * CELL_SIZE), (COLS * CELL_SIZE, r * CELL_SIZE))

    def _draw_sidebar(self, screen, fonts):
        ox = COLS * CELL_SIZE + 10
        WHITE = (255, 255, 255)
        GRAY  = (180, 180, 180)

        # NEXT
        screen.blit(fonts['medium'].render("NEXT", True, WHITE), (ox, 10))
        mini = 20
        for bx, by in self.next_piece.blocks:
            pygame.draw.rect(screen, self.next_piece.color,
                             (ox + bx * mini, 40 + by * mini, mini - 1, mini - 1))

        # 점수/레벨/라인
        for i, (label, val) in enumerate([
            ("SCORE", self.score),
            ("LEVEL", self.level),
            ("LINES", self.lines),
        ]):
            y = 140 + i * 60
            screen.blit(fonts['small'].render(label, True, GRAY), (ox, y))
            screen.blit(fonts['medium'].render(str(val), True, WHITE), (ox, y + 18))

        # 조작법
        controls = ["← → : 이동", "↑ : 회전", "↓ : 소프트", "SPC : 하드", "P : 일시정지"]
        for i, txt in enumerate(controls):
            screen.blit(fonts['tiny'].render(txt, True, GRAY), (ox, 340 + i * 18))

    def _draw_overlay(self, screen, font, title, subtitle):
        overlay = pygame.Surface((COLS * CELL_SIZE, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        WHITE = (255, 255, 255)
        t = font.render(title, True, WHITE)
        s = font.render(subtitle, True, (200, 200, 200))
        cx = (COLS * CELL_SIZE) // 2
        screen.blit(t, t.get_rect(center=(cx, SCREEN_HEIGHT // 2 - 30)))
        screen.blit(s, s.get_rect(center=(cx, SCREEN_HEIGHT // 2 + 10)))
