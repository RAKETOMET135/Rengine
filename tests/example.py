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
image: rengine.Image = rengine.Image("assets/spritesheet.png", 250, 50, 100, 100)
image.sprite_sheet_cut(16, 16, 0, 0)
image.add_to_scene(main_scene)

# Creation of an animation and animator
image_animation: rengine.ImageAnimationTrack = rengine.ImageAnimationTrack([], 0.5, True)
image_animation.use_with_sprite_sheet("assets/character_spritesheet.png")
image_animation.add_images_sprite_sheet(15, 16, [(0, 0), (1, 0), (2, 0)])

image_animator: rengine.ImageAnimator = rengine.ImageAnimator(image, [image_animation])
image_animator.play(image_animation)

# Update method that runs every render, needs to be given to game instance (update_function=update)
def update(delta_time: float) -> None:
    global image

    if image:
        if rengine.Collision.is_collision(rectangle, image):
            image.destroy()
            image = None
    
    if rengine.Input.is_left_mouse_button_click():
        if image:
            image.change_image("assets/paint-brush.png")

# Creation of game instance
engine: rengine.Rengine = rengine.Rengine(update_function=update, frames_per_second=120)
# Adds scene to game instance
engine.add_scene(main_scene)
# Adds player controls to game instance
engine.add_player_controls(player_controls)
# Runs game instance
engine.run()