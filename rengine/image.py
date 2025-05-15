import pygame
from .game_object import GameObject
from .scene import Scene

class Image(GameObject):
    def __init__(self, image_path: str, x: int = 0, y: int = 0, width: int = None, height: int = None):
        """
        Creates an image that can be rendered on screen.

        Args:
            image_path (str): Path to image location.
            x (int): Setup x-axis position.
            y (int): Setup y-axis position.
            width (int): Optional image fixed width.
            height (int): Optional image fixed height.
        """

        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()

        super().__init__(x, y, self.rect.width, self.rect.height)

        if self.width and not self.height:
            self.image = pygame.transform.scale(self.image, (width, self.rect.height))
        elif self.height and not self.width:
            self.image = pygame.transform.scale(self.image, (self.rect.width, height))
        elif self.width and self.height:
            self.image = pygame.transform.scale(self.image, (width, height))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def render(self, screen: pygame.display) -> None:
        """
        Renders the GameObject on screen. Called automatically by Rengine.

        Args:
            screen (display): Current game instance's screen.
        """

        self.rect.topleft = (self.x, self.y)

        screen.blit(self.image, self.rect)
    
    def add_to_scene(self, scene: Scene):
        """
        Adds this GameObject to scene.

        Args:
            scene (Scene): Scene where will the GameObject be added.
        """

        return super().add_to_scene(scene)