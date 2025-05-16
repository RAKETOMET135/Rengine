class Camera:
    def __init__(self, scene = None, background_color: tuple[int] = (0, 0, 0), background_image: str = None):
        """
        Creates a camera instance that has size of the window. Camera instance has to be assigned to a scene.

        Args:
            scene (Scene): Optional scene. Can be added later using created scene's set_camera method.
            background_color (tuple[int]): Optional color for the camera's background.
            background_image (str): Optional image for camera's background. Enter image path string.
        """

        if scene:
            self.scene = scene
            scene.camera = self

        self.x = 0
        self.y = 0
        self.pivot_game_object = None
        self.background_color = background_color
        self.background_image = None

        if background_image:
            self.background_image = self.__create_background(background_image)
    
    def __create_background(self, background_image: str):
        """
        Creates Image class instance for given image path and return it.

        Args:
            background_image (str): Path to background image.
        
        Returns:
            Image: Image class instance with background Image.
        """

        from .image import Image

        background: Image = Image(background_image)

        return background
    
    def _resize_background_image(self, window_size: tuple[int]) -> None:
        """
        Resizes the background image to window size.

        Args:
            window_size (tuple[int]): Size of Pygame window.
        """

        self.background_image.resize_image(window_size[0], window_size[1])

    def set_pivot(self, pivot_game_object = None) -> None:
        """
        Makes the camera center on GameObject and follow it during game loop. Set GameObject to None or not set it to remove camera pivot.

        Args:
            pivot_game_object (GameObject): GameObject to follow by camera.
        """

        self.pivot_game_object = pivot_game_object
    
    def get_game_object_position(self, game_object) -> tuple[int]:
        """
        Returns tuple containing x and y position of gameObject based on camera position. Example: (0, 5)

        Args:
            game_object (GameObject): GameObject to calculate position for.

        Returns:
            tuple[int]: X and Y position of GameObject.
        """

        game_object_offset: tuple[int] = (game_object.x - self.x, game_object.y - self.y)

        return game_object_offset
    
    def is_position_in_camera_view(self, position: tuple[int], window_size: tuple[int]) -> bool:
        """
        Returns True if position is inside camera view.

        Args:
            position (tuple[int]): Position to check for.
            window_size (tuple[int]): Size of Pygame window.

        Returns:
            bool: Is position inside camera view.
        """

        is_inside: bool = False

        is_x: bool = False
        is_y: bool = False

        if position[0] >= self.x and position[0] <= self.x + window_size[0]:
            is_x = True
        
        if position[1] >= self.y and position[1] <= self.y + window_size[1]:
            is_y = True

        is_inside = is_x and is_y

        return is_inside

    def is_game_object_in_bounds(self, game_object, window_size: tuple[int]) -> bool:
        """
        Returns True if GameObject can be visible inside camera view.

        Args:
            game_object (GameObject): GameObject to check bounds for.
            window_size (tuple[int]): Size of Pygame window.
        
        Returns:
            bool: Is GameObject inside camera bounds.
        """

        is_in_bounds: bool = False

        game_object_points: tuple[int] = (
            (game_object.x, game_object.y),
            (game_object.x + game_object.width, game_object.y),
            (game_object.x, game_object.y + game_object.height),
            (game_object.x + game_object.width, game_object.y + game_object.height)
        )

        for game_object_point in game_object_points:
            if not self.is_position_in_camera_view(game_object_point, window_size):
                continue

            is_in_bounds = True

            break

        return is_in_bounds
    
    def _update_position_pivot(self, window_size: tuple[int]) -> None:
        """
        Called by Scene instance to make camera follow pivot GameObject.

        Args:
            window_size (tuple[int]): Size of Pygame window.
        """

        if not self.pivot_game_object:
            return
        
        game_object_center_position: tuple[int] = (self.pivot_game_object.x + int(self.pivot_game_object.width / 2), self.pivot_game_object.y + int(self.pivot_game_object.height / 2))
        camera_center_position: tuple[int] = (game_object_center_position[0] - int(window_size[0] / 2), game_object_center_position[1] - int(window_size[1] / 2))

        self.x = camera_center_position[0]
        self.y = camera_center_position[1]