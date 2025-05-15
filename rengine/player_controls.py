import pygame
from enum import Enum

class MovementType(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
    COMBINED = 3

class MovementControls(Enum):
    KEYS = 1
    ARROWS = 2

class PlayerControls:
    def __init__(self, controlled_object, movement_type: MovementType, movement_controls: MovementControls = MovementControls.KEYS, speed: int = 500):
        """
        Creates player controls for GameObject.

        Args:
            controlled_object (Any): Controlled object by player controls.
            movement_type (MovementType): The type of the player controls movement.
            movement_controls (MovementControls): Use keys or arrows to move.
            speed (int): Speed of the character's move (modified by delta time).
        """

        self.game_object = controlled_object
        self.movement_type = movement_type
        self.movement_controls = movement_controls
        self.speed = speed

    def update(self, keys: pygame.key.ScancodeWrapper, delta_time: float) -> None:
        """
        Updates the controlled object based on movement type and user input. Called automatically by Rengine.

        Args:
            keys (ScancodeWrapper): Keys pressed during the current game loop cycle.
            delta_time (float): Time from the previous frame in seconds.
        """

        player_move: int = int(self.speed * delta_time)
    
        match self.movement_type:
            case MovementType.VERTICAL:
                if keys[pygame.K_UP] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_w] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y -= player_move
                if keys[pygame.K_DOWN] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_s] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y += player_move
            case MovementType.HORIZONTAL:
                if keys[pygame.K_LEFT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_a] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x -= player_move
                if keys[pygame.K_RIGHT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_d] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x += player_move
            case MovementType.COMBINED:
                if keys[pygame.K_UP] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_w] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y -= player_move
                if keys[pygame.K_DOWN] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_s] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y += player_move
                if keys[pygame.K_LEFT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_a] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x -= player_move
                if keys[pygame.K_RIGHT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_d] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x += player_move
            case _:
                pass   