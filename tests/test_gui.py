import rengine

rengine.Rengine.init()

main_scene: rengine.Scene = rengine.Scene("main_scene")
main_gui: rengine.Gui = rengine.Gui(main_scene)

example_text: rengine.TextLabel = rengine.TextLabel("example", 25)
example_text.add_to_gui(main_gui)

example2_text: rengine.TextLabel = rengine.TextLabel("example", 25, (255, 0, 0), x=50, y=5)
example2_text.add_to_gui(main_gui)
example2_text.adjust_draw_order(-1)

def example_on_left_click() -> None:
    print("button left clicked")

def example_on_hover_exit() -> None:
    print("button hover exit")

example_button: rengine.TextButton = rengine.TextButton("example", 50, x=100, y=100, hover_scale=1.2, border_radius=15, border_width=2, border_color=(255, 255, 255),
                                                        background_transparency=0.5, background_hover_transparency=0.5, on_left_click=example_on_left_click,
                                                        on_hover_exit=example_on_hover_exit)
example_button.add_to_gui(main_gui)

frame: rengine.Frame = rengine.Frame(400, 100, width=300, height=400, background_color=(50, 255, 50), background_transparency=0.5,
                                     border_width=4)
frame.add_to_gui(main_gui)

text: rengine.TextLabel = rengine.TextLabel("Header", 50)
frame.add_gui_element(text)

button: rengine.TextButton = rengine.TextButton("Click", 50, x=50, y=50, border_width=2, border_color=(255, 255, 255), hover_scale=1.2)
frame.add_gui_element(button)

inside_frame: rengine.Frame = rengine.Frame(150, 150, height=200, background_color=(0, 0, 255), border_color=(0, 0, 0), border_width=10)
frame.add_gui_element(inside_frame)

i_text: rengine.TextLabel = rengine.TextLabel("text", 25, (0, 0, 0))
inside_frame.add_gui_element(i_text)

i_button: rengine.TextButton = rengine.TextButton("click", 32, x=5, y=100, border_color=(0, 0, 0), border_width=4)
inside_frame.add_gui_element(i_button)

game: rengine.Rengine = rengine.Rengine()
game.add_scene(main_scene)
game.run()