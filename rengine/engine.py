from typing import Callable, Optional
from .scene import Scene
from .player_controls import PlayerControls
from .input import Input
import pygame

class Rengine:
    def __init__(self, width: int = 800, height: int = 600, title: str = "Game window", update_function: Callable = None, frames_per_second: int = 60):
        """
        Creates a game instance with game loop.

        Args:
            width (int): Window width.
            height (int): Window height.
            title (str): Window title.
            update_function (Callable): Function called every render.
            frames_per_second (int): How many game loop cycles runs every second.
        """

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = False
        self.update_function = update_function
        self.scenes = []
        self.current_scene = ""
        self.frames_per_second = frames_per_second
        self.player_controls = []
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

    def get_window_size(self) -> tuple[int]:
        """
        Returns the size of the Pygame window.

        Returns:
            tuple[int]: Pygame window size.
        """

        return (self.screen_width, self.screen_height)
    
    def add_scene(self, scene: Scene) -> None:
        """
        Adds scene into game. Makes the scene active if it is the first one.

        Args:
            scene (Scene): Scene to add.
        """

        self.scenes.append(scene)

        if len(self.scenes) == 1:
            self.current_scene = scene

    def get_scene_by_name(self, scene_name: str) -> Optional[Scene]:
        """
        Returns a scene with given name if exists.

        Returns:
            Optional[Scene]: Scene with given name.
        """

        for scene in self.scenes:
            if not scene.scene_name == scene_name:
                continue

            return scene
        
        return None
    
    def get_active_scene(self) -> Scene:
        """
        Returns currently active scene that renders every frame.

        Returns:
            Scene: Currently active scene.
        """

        return self.current_scene
    
    def change_active_scene(self, scene: Scene) -> None:
        """
        Sets a scene as active and stops rendering previously active scene. Does not need to be added to game scenes.

        Args:
            scene (Scene): Scene to make active.
        """

        self.current_scene = scene
    
    def add_player_controls(self, player_controls: PlayerControls) -> None:
        """
        Adds player controls to Rengine and updates them.

        Args:
            player_controls (PlayerControls): PlayerControls to add.
        """

        self.player_controls.append(player_controls)

    def __get_pressed_keys_list(self, pressed_keys: pygame.key.ScancodeWrapper) -> list[str]:
        pressed_keys_list: list[str] = []

        for key_code in range(len(pressed_keys)):
            if pressed_keys[key_code]:
                key_name = pygame.key.name(key_code)

                if key_name:
                    pressed_keys_list.append(key_name)
            
        if pressed_keys[pygame.K_LEFT]:
            pressed_keys_list.append("left")
        if pressed_keys[pygame.K_RIGHT]:
            pressed_keys_list.append("right")
        if pressed_keys[pygame.K_UP]:
            pressed_keys_list.append("up")
        if pressed_keys[pygame.K_DOWN]:
            pressed_keys_list.append("down")

        return pressed_keys_list

    def run(self) -> None:
        """
        Runs the game instance.
        """

        self.running = True
        while self.running:
            delta_time: float = self.clock.tick(self.frames_per_second) / 1000
            pressed_keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

            events: list[pygame.event.Event] = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            Input._update_input(events, pressed_keys)

            if self.update_function:
                self.update_function(delta_time)
            
            for player_controls in self.player_controls:
                player_controls.update(pressed_keys, delta_time)

            if self.current_scene:
                self.current_scene.render(self.screen, (self.screen_width, self.screen_height), delta_time)

            pygame.display.update()
        
        pygame.quit()
    
    