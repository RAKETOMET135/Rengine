import pygame
from enum import Enum

class MovementType(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
    COMBINED = 3

class MovementControls(Enum):
    KEYS = 1
    ARROWS = 2

class MovementDirection(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,
    STATIC = 5

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
        self.left_image_animation_track = None
        self.right_image_animation_track = None
        self.up_image_animation_track = None
        self.down_image_animation_track = None

        self.__moving = False
        self.__moving_right = False
        self.__moving_left = False
        self.__moving_down = False
        self.__moving_up = False
        self.__use_directional_movement_animations = False
        self.__animator = None
    
    def enable_directional_movement_animations(
            self, image_animator, left_image_animation_track = None, right_image_animation_track = None, up_image_animation_track = None, down_image_animation_track = None
            ) -> None:
        """
        Enables the directional movement animations for controlled GameObject if it is Image.

        Args:
            image_animator (ImageAnimator): ImageAnimator that will be used.
            left_image_animation_track (ImageAnimationTrack): ImageAnimationTrack for movement left.
            right_image_animation_track (ImageAnimationTrack): ImageAnimationTrack for movement right.
            up_image_animation_track (ImageAnimationTrack): ImageAnimationTrack for movement up.
            down_image_animation_track (ImageAnimationTrack): ImageAnimationTrack for movement down.
        """

        self.__animator = image_animator
        self.__use_directional_movement_animations = True
        self.left_image_animation_track = left_image_animation_track
        self.right_image_animation_track = right_image_animation_track
        self.up_image_animation_track = up_image_animation_track
        self.down_image_animation_track = down_image_animation_track
    
    def get_move_direction(self) -> MovementDirection:
        """
        Returns MovemenDirection Enum. If the GameObject is moving horizontally and vertically, the horizontal Enum will be given.

        Returns STATIC Enum if GameObject is not moving.
        """

        if not self.__moving:
            return MovementDirection.STATIC
        
        if self.__moving_left:
            return MovementDirection.LEFT
        
        if self.__moving_right:
            return MovementDirection.RIGHT
        
        if self.__moving_up:
            return MovementDirection.UP
        
        if self.__moving_down:
            return MovementDirection.DOWN
    
    def is_moving(self) -> bool:
        """
        Returns True if player controlled GameObject is moving.

        Returns:
            bool: True if player controlled GameObject is moving.
        """

        return self.__moving

    def __handle_directional_movement_animations(self) -> None:
        movement_direction: MovementDirection = self.get_move_direction()

        match movement_direction:
            case MovementDirection.LEFT:
                if self.left_image_animation_track and not self.__animator.is_playing(self.left_image_animation_track):
                    self.__animator.play(self.left_image_animation_track)
            case MovementDirection.RIGHT:
                if self.right_image_animation_track and not self.__animator.is_playing(self.right_image_animation_track):
                    self.__animator.play(self.right_image_animation_track)
            case MovementDirection.UP:
                if self.up_image_animation_track and not self.__animator.is_playing(self.up_image_animation_track):
                    self.__animator.play(self.up_image_animation_track)
            case MovementDirection.DOWN:
                if self.down_image_animation_track and not self.__animator.is_playing(self.down_image_animation_track):
                    self.__animator.play(self.down_image_animation_track)
            case _:
                self.__animator.stop_current_animation()
        

    def update(self, keys: pygame.key.ScancodeWrapper, delta_time: float) -> None:
        """
        Updates the controlled object based on movement type and user input. Called automatically by Rengine.

        Args:
            keys (ScancodeWrapper): Keys pressed during the current game loop cycle.
            delta_time (float): Time from the previous frame in seconds.
        """

        player_move: int = int(self.speed * delta_time)
    
        is_move: bool = False
        is_move_right: bool = False
        is_move_left: bool = False
        is_move_down: bool = False
        is_move_up: bool = False

        match self.movement_type:
            case MovementType.VERTICAL:
                if keys[pygame.K_UP] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_w] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y -= player_move
                    is_move = True
                    is_move_up = True
                if keys[pygame.K_DOWN] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_s] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y += player_move
                    is_move = True
                    is_move_down = True
            case MovementType.HORIZONTAL:
                if keys[pygame.K_LEFT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_a] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x -= player_move
                    is_move = True
                    is_move_left = True
                if keys[pygame.K_RIGHT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_d] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x += player_move
                    is_move = True
                    is_move_right = True
            case MovementType.COMBINED:
                if keys[pygame.K_UP] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_w] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y -= player_move
                    is_move = True
                    is_move_up = True
                if keys[pygame.K_DOWN] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_s] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.y += player_move
                    is_move = True
                    is_move_down = True
                if keys[pygame.K_LEFT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_a] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x -= player_move
                    is_move = True
                    is_move_left = True
                if keys[pygame.K_RIGHT] and self.movement_controls == MovementControls.ARROWS or keys[pygame.K_d] and self.movement_controls == MovementControls.KEYS:
                    self.game_object.x += player_move
                    is_move = True
                    is_move_right = True
            case _:
                pass   
        
        self.__moving = is_move
        self.__moving_right = is_move_right
        self.__moving_left = is_move_left
        self.__moving_down = is_move_down
        self.__moving_up = is_move_up

        if self.__use_directional_movement_animations:
            self.__handle_directional_movement_animations()