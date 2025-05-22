import dearpygui.dearpygui as dpg
import node_manager # For callbacks and NODE_EDITOR_TAG
from nodes import add_start_node, add_text_node, add_button_node, add_end_node

PRIMARY_WINDOW_TAG = "primary_window"

# Renamed for clarity: this resizes the contents within the primary window
def _resize_primary_window_contents():
    if not dpg.is_viewport_ok(): # Safety check
        return

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    
    # The PRIMARY_WINDOW_TAG (our main window) is set as the primary window,
    # so DPG automatically resizes it to fill the viewport.
    # We need to resize its children, specifically the node editor.

    # Estimate menu bar height (Dear PyGui doesn't have a direct query for this)
    # Adjust this value if your menu bar appears taller or shorter.
    estimated_menu_bar_height = 25 

    node_editor_tag_val = node_manager.get_node_editor_tag()
    if dpg.does_item_exist(node_editor_tag_val):
        # The node editor should take up the remaining space in the primary window
        # after the menu bar.
        node_editor_width = viewport_width
        node_editor_height = viewport_height - estimated_menu_bar_height
        
        dpg.set_item_width(node_editor_tag_val, node_editor_width)
        dpg.set_item_height(node_editor_tag_val, node_editor_height)
        # print(f"Resized node editor ({node_editor_tag_val}) to {node_editor_width}x{node_editor_height}")


def setup_gui():
    """Create the main window with menu bar and node editor"""
    # The width/height here are initial suggestions; set_primary_window will manage actual size.
    with dpg.window(label="Node Editor", tag=PRIMARY_WINDOW_TAG, 
                    no_close=True, no_move=True, no_resize=True, no_title_bar=True):
        
        with dpg.menu_bar():
            with dpg.menu(label="Add Nodes"):
                dpg.add_menu_item(label="Add Start Node", callback=add_start_node)
                dpg.add_menu_item(label="Add Text Node", callback=add_text_node)
                dpg.add_menu_item(label="Add Button Node", callback=add_button_node)
                dpg.add_menu_item(label="Add End Node", callback=add_end_node)
        
        # Node editor is added as a child of the primary window.
        # It will be placed below the menu bar by DPG's default layout.
        # We don't set width/height here; _resize_primary_window_contents will handle it.
        with dpg.node_editor(callback=node_manager.link_callback, 
                             delink_callback=node_manager.delink_callback, 
                             tag=node_manager.get_node_editor_tag()):
            pass  # Nodes will be added dynamically

    # Set this window as the primary window. It will fill the viewport.
    dpg.set_primary_window(PRIMARY_WINDOW_TAG, True)
    
    # Register the resize callback. DPG will call this after setup and on viewport resize.
    dpg.set_viewport_resize_callback(_resize_primary_window_contents)
    
    # DO NOT call _resize_primary_window_contents() here.
    # DPG will trigger it automatically once the viewport is ready after dpg.setup_dearpygui().