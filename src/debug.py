import pygame

from settings import ENV


def display(text, x: int = 10, y: int = 10):
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(text), True, "White")
    debug_rect = debug_surf.get_rect(topleft=(x, y))

    pygame.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)


class FreeCamera(pygame.sprite.Sprite):
    def __init__(self, scale: float, groups) -> None:
        super().__init__(groups)
        self.pos = (0, 0)
        self.image = pygame.Surface((ENV.TILE_SIZE / 2 * scale, ENV.TILE_SIZE / 2 * scale))
        self.rect = self.image.get_rect(topleft=self.pos)
        self.direction: pygame.Vector2 = pygame.math.Vector2()
        self.speed = 10 * scale

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2()
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, speed) -> None:
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed

    def update(self) -> None:
        self.handle_input()
        self.move(self.speed)
