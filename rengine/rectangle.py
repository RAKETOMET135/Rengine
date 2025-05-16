import pygame
from .game_object import GameObject
from .scene import Scene

class Rectangle(GameObject):
    def __init__(self, x: int = 0, y: int = 0, width: int = 100, height: int = 100, color: tuple[int] = (255, 255, 255)):
        """
        Creates a rectangle that can be rendered on screen.

        Args:
            x (int): Setup x-axis position.
            y (int): Setup y-axis position.
            width (int): Rectangle's width.
            height (int): Rectangle's height.
            color (tuple[int]): Rectangle's color.
        """

        self.color = color

        super().__init__(x, y, width, height)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen: pygame.display, camera_object_position: tuple[int]) -> None:
        """
        Renders the GameObject on screen. Called automatically by Rengine.

        Args:
            screen (display): Current game instance's screen.
            camera_object_position (tuple[int]): Position in scene based on camera position.
        """

        self.rect.topleft = camera_object_position

        pygame.draw.rect(screen, self.color, self.rect)
    
    def add_to_scene(self, scene: Scene):
        """
        Adds this GameObject to scene.

        Args:
            scene (Scene): Scene where will the GameObject be added.
        """

        return super().add_to_scene(scene)