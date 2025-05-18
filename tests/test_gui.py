import rengine

rengine.Rengine.init()

main_scene: rengine.Scene = rengine.Scene("main_scene")
main_gui: rengine.Gui = rengine.Gui(main_scene)

example_text: rengine.TextLabel = rengine.TextLabel("example", 25)
example_text.add_to_gui(main_gui)

example2_text: rengine.TextLabel = rengine.TextLabel("example", 25, (255, 0, 0), x=50, y=5)
example2_text.add_to_gui(main_gui)
example2_text.adjust_draw_order(-1)

example_button: rengine.TextButton = rengine.TextButton("example", 50, x=100, y=100, hover_scale=1.2, border_radius=15, border_width=2, border_color=(255, 255, 255),
                                                        background_transparency=0.5, background_hover_transparency=0.5)
example_button.add_to_gui(main_gui)

game: rengine.Rengine = rengine.Rengine()
game.add_scene(main_scene)
game.run()