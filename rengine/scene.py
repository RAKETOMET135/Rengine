import pygame

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

        self.__game_objects = []
    
    def add_game_object(self, game_object) -> None:
        """
        Adds game object to scene.

        Args:
            game_object (Any): GameObject instance or inherited instance from GameObject.
        """

        self.__game_objects.append(game_object)
    
    def get_all_game_objects(self) -> list:
        """
        Returns a list containing all GameObjects in scene.

        Returns:
            list: List of scene GameObjects.
        """
        
        return self.__game_objects

    def render(screen: pygame.display) -> None:
        pass