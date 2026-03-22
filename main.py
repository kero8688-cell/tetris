import sys
import pygame
from tetris.game import Game, SCREEN_WIDTH, SCREEN_HEIGHT


def build_fonts():
    return {
        'large':  pygame.font.SysFont('Arial', 28, bold=True),
        'medium': pygame.font.SysFont('Arial', 20, bold=True),
        'small':  pygame.font.SysFont('Arial', 14),
        'tiny':   pygame.font.SysFont('Arial', 12),
    }


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock  = pygame.time.Clock()
    fonts  = build_fonts()

    game = Game()

    # 키 반복 설정: 200ms 딜레이, 80ms 간격
    pygame.key.set_repeat(200, 80)

    while True:
        dt = clock.tick(60)  # ms

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        game.restart()
                    continue

                if event.key == pygame.K_p:
                    game.toggle_pause()
                    continue

                if game.paused:
                    continue

                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.soft_drop()
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()

        game.update(dt)
        game.draw(screen, fonts)
        pygame.display.flip()


if __name__ == '__main__':
    main()
