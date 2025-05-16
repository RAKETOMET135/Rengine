import rengine

# Creation of a scene
main_scene: rengine.Scene = rengine.Scene("main_scene")

# Creation of a scene camera
camera: rengine.Camera = rengine.Camera(main_scene)

# Creation of a rectangle
rectangle: rengine.Rectangle = rengine.Rectangle()
rectangle.add_to_scene(main_scene)
# Adds the ability to move the rectangle, needs to be added to game instance (add_player_controls)
player_controls: rengine.PlayerControls = rengine.PlayerControls(rectangle, rengine.MovementType.COMBINED)
# Make camera follow rectangle
camera.set_pivot(rectangle)

# Creation of an image
image: rengine.Image = rengine.Image("paint-brush.png", 250, 50, 50, 50)
image.add_to_scene(main_scene)

# Update method that runs every render, needs to be given to game instance (update_function=update)
def update(delta_time: float, pressed_keys: list[str]) -> None:
    pass

# Creation of game instance
engine: rengine.Rengine = rengine.Rengine(update_function=update, frames_per_second=120)
# Adds scene to game instance
engine.add_scene(main_scene)
# Adds player controls to game instance
engine.add_player_controls(player_controls)
# Runs game instance
engine.run()