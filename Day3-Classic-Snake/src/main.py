import Core

root = Core.Core()
current_scene = "Menu"
while True:
    # if current_scene == "Menu":  
    #     current_scene = root.main_menu()
    # elif current_scene == "Game":
    #     current_scene = root.game_loop()
    # elif current_scene == "Options":
    #     current_scene = root.options_menu()

    root.game_loop()

    root.update()


