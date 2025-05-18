import rengine

main_scene: rengine.Scene = rengine.Scene("main_scene")
main_scene_camera: rengine.Camera = rengine.Camera(main_scene)

player: rengine.Image = rengine.Image("assets/character_spritesheet.png", width=100, height=100)
player.sprite_sheet_cut(15, 16, 0, 0)
player.add_to_scene(main_scene)
player_controls: rengine.PlayerControls = rengine.PlayerControls(player, rengine.MovementType.COMBINED)
main_scene.add_player_controls(player_controls)

walk_animation_down: rengine.ImageAnimationTrack = rengine.ImageAnimationTrack([], 0.4, True)
walk_animation_down.use_with_sprite_sheet("assets/character_spritesheet.png")
walk_animation_down.add_images_sprite_sheet(15, 16, [(0, 0), (1, 0), (2, 0)])
walk_animation_up: rengine.ImageAnimationTrack = rengine.ImageAnimationTrack([], 0.4, True)
walk_animation_up.use_with_sprite_sheet("assets/character_spritesheet.png")
walk_animation_up.add_images_sprite_sheet(15, 16, [(0, 1), (1, 1), (2, 1)])
walk_animation_left: rengine.ImageAnimationTrack = rengine.ImageAnimationTrack([], 0.4, True)
walk_animation_left.use_with_sprite_sheet("assets/character_spritesheet.png")
walk_animation_left.add_images_sprite_sheet(15, 16, [(0, 2), (1, 2), (2, 2)])
walk_animation_right: rengine.ImageAnimationTrack = rengine.ImageAnimationTrack([], 0.4, True)
walk_animation_right.use_with_sprite_sheet("assets/character_spritesheet.png")
walk_animation_right.add_images_sprite_sheet(15, 16, [(0, 3), (1, 3), (2, 3)])

player_animator: rengine.ImageAnimator = rengine.ImageAnimator(player, [walk_animation_right, walk_animation_left, walk_animation_down, walk_animation_up])
player_controls.enable_directional_movement_animations(player_animator, walk_animation_left, walk_animation_right, walk_animation_up, walk_animation_down)

wheet_bag: rengine.Image = rengine.Image("assets/spritesheet.png", 150, 150, 75, 75)
wheet_bag.sprite_sheet_cut(16, 16, 0, 0)
wheet_bag.add_to_scene(main_scene)

main_scene_camera.set_pivot(player)

game: rengine.Rengine = rengine.Rengine(frames_per_second=120)
game.add_scene(main_scene)

game.run()