import dearpygui.dearpygui as dpg
import gui # To setup the GUI components

def main():
    dpg.create_context()

    gui.setup_gui() # Defines the GUI structure

    # Viewport must be created BEFORE dpg.setup_dearpygui()
    dpg.create_viewport(title='Story Flow Node Editor', width=1280, height=720)
    
    # DPG finalizes setup, processes items, and will trigger the viewport_resize_callback
    dpg.setup_dearpygui() 

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()