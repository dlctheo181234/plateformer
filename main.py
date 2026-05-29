import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60


def on_ground(rect, platforms):
    rect.y += 1
    grounded = False
    for plat in platforms:
        if rect.colliderect(plat):
            grounded = True
            break
    rect.y -= 1
    return grounded


def move_player(rect, platforms, dx, dy):
    rect.x += dx
    for plat in platforms:
        if rect.colliderect(plat):
            if dx > 0:
                rect.right = plat.left
            elif dx < 0:
                rect.left = plat.right

    rect.y += dy
    for plat in platforms:
        if rect.colliderect(plat):
            if dy > 0:
                rect.bottom = plat.top
                return 0
            elif dy < 0:
                rect.top = plat.bottom
                return 0

    return dy


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Platformer")
    clock = pygame.time.Clock()

    player = pygame.Rect(50, HEIGHT - 150, 40, 60)
    vel_x = 0
    vel_y = 0
    speed = 5
    jump_strength = 16
    gravity = 0.9

    platforms = [
        pygame.Rect(0, HEIGHT - 20, WIDTH, 20),
        pygame.Rect(150, HEIGHT - 150, 200, 20),
        pygame.Rect(450, HEIGHT - 250, 200, 20),
        pygame.Rect(300, HEIGHT - 350, 150, 20),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x = -speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x = speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground(player, platforms):
            vel_y = -jump_strength

        vel_y += gravity
        vel_y = move_player(player, platforms, vel_x, vel_y)

        screen.fill((135, 206, 235))
        for plat in platforms:
            pygame.draw.rect(screen, (110, 62, 10), plat)
        pygame.draw.rect(screen, (255, 0, 0), player)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
