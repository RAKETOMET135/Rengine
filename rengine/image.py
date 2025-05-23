from __future__ import annotations
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
        self.__root_width = width
        self.__root_height = height
        self._animator = None
        self._default_image = self.image

        super().__init__(x, y, self.rect.width, self.rect.height)

        if width and not height:
            self.image = pygame.transform.scale(self.image, (width, self.rect.height))
            self.width = width
        elif height and not width:
            self.image = pygame.transform.scale(self.image, (self.rect.width, height))
            self.height = height
        elif width and height:
            self.image = pygame.transform.scale(self.image, (width, height))
            self.width = width
            self.height = height
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def change_image(self, image_path: str) -> None:
        """
        Changes the image to new image on image_path.

        Args:
            image_path (str): Path to new image.
        """

        image: pygame.Surface = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (self.width, self.height))
        self.image = image
        self.image_path = image_path
        self._default_image = self.image

    def resize_image(self, width: int, height: int) -> None:
        """
        Resizes the image to new width and height.

        Args:
            width (int): New image width.
            height (int): New image height.
        """

        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.__root_width = width
        self.__root_height = height
        self._default_image = self.image
    
    def render(self, screen: pygame.display, camera_object_position: tuple[int]) -> None:
        """
        Renders the GameObject on screen. Called automatically by Rengine.

        Args:
            screen (display): Current game instance's screen.
            camera_object_position (tuple[int]): Position in scene based on camera position.
        """

        self.rect.topleft = camera_object_position

        screen.blit(self.image, self.rect)
    
    def add_to_scene(self, scene: Scene) -> None:
        """
        Adds this GameObject to scene.

        Args:
            scene (Scene): Scene where will the GameObject be added.
        """

        return super().add_to_scene(scene)
    
    def sprite_sheet_cut(self, cut_width: int, cut_height: int, x: int, y: int, color_key: tuple[int] = (0, 0, 0)) -> None:
        """
        Cuts the image into smaller part. Can be used for sprite sheets.

        Args:
            cut_width (int): Cut width.
            cut_height (int): Cut height.
            x (int): Row.
            y (int): Column.
            color_key (tuple[int]): Color that becomes transparent. Set to None to disable.
        """

        image: pygame.Surface = pygame.Surface((cut_width, cut_height))
        image.blit(pygame.image.load(self.image_path), (0, 0), ((x * cut_width), (y * cut_height), cut_width, cut_height))

        if color_key:
            image.set_colorkey(color_key)
        
        image = pygame.transform.scale(image, (self.__root_width, self.__root_height))

        self.image = image
        self._default_image = self.image