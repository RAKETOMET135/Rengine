import pygame
from .camera import Camera

class Scene:
    current_id = 0
    scenes = []

    def __init__(self, scene_name: str):
        """
        Creates an instance of a scene class.

        Args:
            scene_name (str): Name of this scene.
        """

        self.id = Scene.current_id
        Scene.current_id += 1
        self.scene_name = scene_name
        Scene.scenes.append(self)
        self.camera = None
        self.gui = None

        self.__game_objects = []
        self.__player_controls = []
    
    def add_game_object(self, game_object) -> None:
        """
        Adds GameObject to scene.

        Args:
            game_object (GameObject): GameObject instance or inherited instance from GameObject.
        """

        self.__game_objects.append(game_object)
    
    def remove_game_object(self, game_object) -> None:
        """
        Removes GameObject from scene.

        Args:
            game_object (GameObject): GameObject to remove.
        """

        if game_object in self.__game_objects:
            self.__game_objects.remove(game_object)
    
    def get_all_game_objects(self) -> list:
        """
        Returns a list containing all GameObjects in scene.

        Returns:
            list: List of scene GameObjects.
        """
        
        return self.__game_objects
    
    def set_camera(self, camera: Camera) -> None:
        """
        Sets the camera that is used to render scene.
        """

        camera.scene = self
        self.camera = camera
    
    def add_player_controls(self, player_controls) -> None:
        """
        Adds player controls to Scene and updates them.

        Args:
            player_controls (PlayerControls): PlayerControls to add.
        """

        self.__player_controls.append(player_controls)

    def render(self, screen: pygame.display, window_size: tuple[int], delta_time: float, pressed_keys: pygame.key.ScancodeWrapper) -> None:
        """
        Renders the scene. Called by Rengine.

        Args:
            screen (display): Pygame screen.
            window_size (tuple[int]): Size of Pygame window.
            delta_time (float): The time from last frame.
            pressed_keys (ScancodeWrapper): Currently pressed keys.
        """

        to_remove_game_objects: list = []

        for player_controls in self.__player_controls:
            player_controls.update(pressed_keys, delta_time)

        for game_object in self.__game_objects:
            if hasattr(game_object, "_animator"):
                if game_object._animator and game_object._animator.current_track:
                    animator = game_object._animator
                    animator._track_time += delta_time

                    is_stopped: bool = False

                    if animator._track_time >= animator.current_track.length:
                        if not animator.current_track.looped:
                            animator.stop(animator.current_track)
                            is_stopped = True
                        else:
                            animator._track_time = delta_time
                    
                    if not is_stopped:
                        length_per_frame: float = animator.current_track.length / len(animator.current_track.images)
                        current_animation_frame: int = int(animator._track_time / length_per_frame)

                        game_object.image = animator._track_images[current_animation_frame]

            if not game_object._remove:
                continue

            to_remove_game_objects.append(game_object)

        for to_remove_game_object in to_remove_game_objects:
            self.__game_objects.remove(to_remove_game_object)

        if not self.camera:
            screen.fill((0, 0, 0))

            for game_object in self.__game_objects:
                if hasattr(game_object, "render") and callable(getattr(game_object, "render")) and not game_object.hidden:
                    game_object.render(screen, (game_object.x, game_object.y))
        else:
            self.camera._update_position_pivot(window_size)

            if not self.camera.background_image:
                screen.fill(self.camera.background_color)
            else:
                if self.camera.background_image.width == 0:
                    self.camera._resize_background_image(window_size)
                
                self.camera.background_image.render(screen, (0, 0))

            for game_object in self.__game_objects:
                if hasattr(game_object, "render") and callable(getattr(game_object, "render")) and not game_object.hidden:
                    in_bounds: bool = self.camera.is_game_object_in_bounds(game_object, window_size)

                    if not in_bounds:
                        continue

                    game_object.render(screen, self.camera.get_game_object_position(game_object))

        if self.gui:
            self.gui.render(screen, delta_time, window_size, pressed_keys)