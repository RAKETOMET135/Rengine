import pygame

class ImageAnimationTrack:
    def __init__(self, image_paths: list[str], length: float, looped: bool = False, animation_name: str = None):
        """
        Creates ImageAnimationTrack instance with frames count equal to image_paths length with total length of animation.

        Args:
            image_paths (list[str]): List of all image paths. Each image is a frame. Animation order is list order.
            length (flaot): Animation length. Total time in seconds.
            looped (bool): Make the track play again after it finishes.
            animation_name (str): Optional animation name. Can be used for ImageAnimator track play.
        """

        self.image_paths = image_paths
        self.length = length
        self.images = self.__get_images_from_image_paths(image_paths)
        self.sprite_sheet = None
        self.sprite_sheet_path = None
        self.looped = looped
        self.animation_name = animation_name

        self.__sprite_sheet_mode = False
        
    def __get_images_from_image_paths(self, image_paths: list[str]) -> list[pygame.Surface]:
        """
        Returns list of loaded Pygame images from image_paths.

        Args:
            image_paths (list[str]): List of image paths to load.
        """

        images: list[pygame.Surface] = []

        for image_path in image_paths:
            image: pygame.Surface = pygame.image.load(image_path)

            images.append(image)
        
        return images
    
    def add_images_sprite_sheet(self, width: int, height: int, sprite_positions: list[tuple[int]], color_key: tuple[int] = (0, 0, 0)) -> None:
        """
        Creates images from sprite sheet and adds them to the end of the track.

        Args:
            width (int): Cut width.
            height (int): Cut height.
            sprite_positions (list[tuple[int]]): List of image positions to add from sprite sheet. Row and column.
            color_key (tuple[int]): Color that becomes transparent. Set to None to disable.
        """

        if not self.__sprite_sheet_mode:
            print(f'Sprite sheet was not assigned. ImageAnimationTrack.add_images_sprite_sheet')

            return

        for sprite_position in sprite_positions:
            image: pygame.Surface = pygame.Surface((width, height))
            image.blit(self.sprite_sheet, (0, 0), ((sprite_position[0] * width), (sprite_position[1] * height), width, height))

            if color_key:
                image.set_colorkey(color_key)
            
            self.images.append(image)
            self.image_paths.append("sprite_sheet_image")

    def use_with_sprite_sheet(self, sprite_sheet_path: str) -> None:
        """
        Makes the track use sprite sheet. Other images will be removed and can not be added.

        Use add_images_sprite_sheet method to add images from the sprite sheet.

        Args:
            sprite_sheet_path (str): Sprite sheet to load.
        """

        self.__sprite_sheet_mode = True
        self.sprite_sheet_path = sprite_sheet_path
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.image_paths = []
        self.images = []
    
    def replace_image_paths(self, image_paths: list[str]) -> None:
        """
        Removes all previous animation images and adds the new ones.

        Removes sprite sheet if it was used.

        Args:
            image_paths (list[str]): List of new images to add.
        """

        if self.__sprite_sheet_mode:
            self.__sprite_sheet_mode = False
            self.sprite_sheet = None
            self.sprite_sheet_path = None

        self.image_paths = image_paths
        self.images = self.__get_images_from_image_paths(image_paths)

    def remove_image(self, animation_track_position: int = None) -> None:
        """
        Removes image from animation track at specific position. Set animation_track_position to None to remove last image.

        Args:
            animation_track_position (int): Position in track where image will be removed. Set to None to remove last image.
        """

        if not animation_track_position:
            del self.image_paths[len(self.image_paths) - 1]
            del self.images[len(self.images) - 1]
        else:
            if animation_track_position >= len(self.image_paths):
                print(f'Image could not be removed due to: animation_track_position is out of range. ImageAnimationTrack.remove_image')

                return
            
            del self.image_paths[animation_track_position]
            del self.images[animation_track_position]
        
    def add_image(self, image_path: str, animation_track_position: int = None) -> None:
        """
        Adds image to animation track to specific position. Set animation_track_position to None to add to end.

        Args:
            image_path (str): Path to image that is added to track.
            animation_track_position (int): Position in track where image will be added. Set to None to add to end.
        """

        if self.__sprite_sheet_mode:
            print(f'Image with path: {image_path} could not be added due to: sprite sheet is used. ImageAnimationTrack.add_image')

            return

        if not animation_track_position:
            image: pygame.Surface = pygame.image.load(image_path)

            self.image_paths.append(image_path)
            self.images.append(image)
        else:
            if animation_track_position >= len(self.image_paths):
                print(f'Image with path: {image_path} could not be added due to: animation_track_position is out of range. ImageAnimationTrack.add_image')

                return
            else:
                image: pygame.Surface = pygame.image.load(image_path)
                new_image_paths: list[str] = []

                for i, _image_path in enumerate(self.image_paths):
                    if i == animation_track_position:
                        new_image_paths.append(image_path)

                    new_image_paths.append(_image_path)
                
                self.image_paths = new_image_paths
                self.images = self.__get_images_from_image_paths(self.image_paths)

class ImageAnimator:
    def __init__(self, game_object, image_animation_tracks: list[ImageAnimationTrack] = None):
        """
        Creates ImageAnimator instance for an Image GameObject. Add ImageAnimationTracks to be able to play them for this Image GameObject.

        Image GameObject can only have one ImageAnimator. The newest created ImageAnimator will be used.

        Args:
            game_object (GameObject): Image GameObject used by the ImageAnimator.
            image_animation_tracks (list[ImageAnimationTrack]): Optional list of ImageAnimationTracks to add. ImageAnimationTracks can be added later.
        """

        self.game_object = game_object
        self.tracks = []
        self.current_track = None

        if image_animation_tracks:
            self.tracks = image_animation_tracks
        
        self.game_object._animator = self

        self._track_time = 0
        self._track_images = []
        self.__stopped_animation_time = 0
        self.__stopped_animation_images = []
        self.__stopped_animation = None
    
    def __adjust_track_to_game_object(self, image_animation_track: ImageAnimationTrack) -> list[pygame.Surface]:
        """
        Makes all images in ImageAnimatioTrack have the size of Image GameObject size.

        Args:
            image_animation_track (ImageAnimationTrack): ImageAnimationTrack to adjust.

        Returns:
            list[Surface]: Adjusted images.
        """

        adjusted_images: list[pygame.Surface] = []

        for image in image_animation_track.images:
            adjusted_image: pygame.Surface = pygame.transform.scale(image, (self.game_object.width, self.game_object.height))

            adjusted_images.append(adjusted_image)
        
        return adjusted_images
    
    def is_playing(self, image_animation_track: ImageAnimationTrack = None, image_animation_name: str = None) -> bool:
        """
        Returns True if ImageAnimationTrack is currently playing.

        You can use track or track name.

        Args:
            image_animation_track (ImageAnimationTrack): ImageAnimationTrack to check.
            image_animation_name (str): ImageAnimationTrack name to check.
        """

        if image_animation_track:
            if self.current_track == image_animation_track:
                return True
            else:
                return False
        
        if image_animation_name:
            for track in self.tracks:
                if not track.animation_name == image_animation_name:
                    continue

                if self.current_track == track:
                    return True
                else:
                    return False
        
        return False

    def add_image_animation_track(self, image_animation_track: ImageAnimationTrack) -> None:
        """
        Adds ImageAnimationTrack into ImageAnimator.

        Args:
            image_animation_track (ImageAnimationTrack): ImageAnimationTrack to add to ImageAnimator.
        """

        self.tracks.append(image_animation_track)
    
    def remove_image_animation_track(self, image_animation_track: ImageAnimationTrack) -> None:
        """
        Removex ImageAnimationTrack from ImageAnimator.

        Args:
            image_animation_track (ImageAnimationTrack): ImageAnimationTrack to remove from ImageAnimator.
        """

        if image_animation_track in self.tracks:
            if self.current_track == image_animation_track:
                self.current_track = None

            self.tracks.remove(image_animation_track)
    
    def play(self, image_animation_track: ImageAnimationTrack = None, image_animation_name: str = None) -> None:
        """
        Plays ImageAnimationTrack. Adds the ImageAnimationTrack into ImageAnimator if it does not exist (only for track).

        You can use track or track name.

        Args:
            image_animation_track (ImageAnimationTrack): ImageAnimationTrack to play.
            image_animation_name (str): ImageAnimationTrack name to play.
        """

        if image_animation_track:
            self.current_track = image_animation_track
            self._track_time = 0
            self._track_images = self.__adjust_track_to_game_object(self.current_track)

            if not image_animation_track in self.tracks:
                self.tracks.append(image_animation_track)

        if image_animation_name and not image_animation_track:
            for track in self.tracks:
                if not track.animation_name == image_animation_name:
                    continue

                self.current_track = track
                self._track_time = 0
                self._track_images = self.__adjust_track_to_game_object(self.current_track)

                break
        
        if not image_animation_name and not image_animation_track:
            print(f'ImageAnimationTrack could not be played due to: both arguments are None. ImageAnimator.play')

    def resume_last_animation(self) -> None:
        """
        Plays the last stopped animation track from stop point.
        """

        self.current_track = self.__stopped_animation
        self._track_images = self.__stopped_animation_images
        self._track_time = self.__stopped_animation_time

    def stop_current_animation(self) -> None:
        """
        Stops the currently playing ImageAnimationTrack.
        """

        self.__stopped_animation_time = self._track_time
        self.__stopped_animation_images = self._track_images
        self.__stopped_animation = self.current_track
        self.current_track = None

    def stop(self, image_animation_track: ImageAnimationTrack = None, image_animation_name: str = None, keep_last_frame: bool = False) -> None:
        """
        Stops ImageAnimationTrack if it is playing.

        You can use track or track name.

        Args:
            image_animation_track (ImageAnimationTrack): ImageAnimationTrack to stop.
            image_animation_name (str): ImageAnimationTrack name to stop.
            keep_last_frame (bool): Make the Image GameObject keep the current image from stopped track.
        """

        if image_animation_track:
            if image_animation_track == self.current_track:
                self.__stopped_animation_time = self._track_time
                self.__stopped_animation_images = self._track_images
                self.__stopped_animation = self.current_track
                self.current_track = None
        
        if image_animation_name and not image_animation_track:
            for track in self.tracks:
                if not track.animation_name == image_animation_name:
                    continue

                if track == self.current_track:
                    self.__stopped_animation_time = self._track_time
                    self.__stopped_animation_images = self._track_images
                    self.__stopped_animation = self.current_track
                    self.current_track = None
                
                break
        
        if image_animation_name or image_animation_track:
            if not keep_last_frame:
                self.game_object.image = self.game_object._default_image
        
        if not image_animation_name and not image_animation_track:
            print(f'ImageAnimationTrack could not be stopped due to: both arguments are None. ImageAnimator.stop')