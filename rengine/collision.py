class Collision:
    @staticmethod
    def is_collision(game_object_0, game_object_1) -> bool:
        """
        Returns True if GameObjects collide with each other.

        Args:
            game_object_0 (GameObject): The first GameObject.
            game_object_1 (GameObject): The seconds GameObject.

        Returns:
            bool: True if both collide each other.
        """

        is_collision: bool = game_object_0.rect.colliderect(game_object_1.rect)

        return is_collision
    
    @staticmethod
    def is_collision_any(game_object, game_objects: list) -> bool:
        """
        Returns True if GameObject collides with atleast one of the GameObjects.

        Args:
            game_object (GameObject): GameObject to check collision for.
            game_objects (list[GameObject]): List of GameObjects to check collision for GameObject.

        Returns:
            bool: True if GameObject collides with atleast one of the GameObjects.
        """

        is_collision: bool = False

        for object in game_objects:
            if not game_object.rect.colliderect(object.rect):
                continue

            is_collision = True
        
        return is_collision