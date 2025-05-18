from enum import Enum
from .scene import Scene

class RenderType(Enum):
    RECTANGLE: 1
    IMAGE: 2

class GameObject:
    def __init__(self, x: int = 0, y: int = 0, width: int = 100, height: int = 100):
        """
        Creates an instance of a gameObject.

        Args:
            x (int): Setup x-axis position.
            y (int): Setup y-axis position.
            width (int): GameObject's width.
            height (int): GameObject's height.
        """
    
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hidden = False

        self._remove = False
    
    def add_to_scene(self, scene: Scene) -> None:
        scene.add_game_object(self)
    
    def destroy(self) -> None:
        """
        Destroys the GameObject in next game loop cycle.
        
        To remove GameObject from memory make the reference None or use del.
        """

        self._remove = True