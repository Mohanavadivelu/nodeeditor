import dearpygui.dearpygui as dpg
from utils import get_unique_tag
import node_manager # To access register_node_input_executor, NODE_EDITOR_TAG

def _on_end_execute(node_tag): # Removed sender, app_data
    """Execute when End node is reached"""
    print(f"Executing End Node: {node_tag}")
    status_text_tag = f"{node_tag}_status"
    dpg.set_value(status_text_tag, "Green (Success)")

def add_end_node():
    """Add an End node to the editor"""
    node_tag = get_unique_tag()
    input_attr_tag = f"{node_tag}_in_1"

    with dpg.node(label="End Node", tag=node_tag, parent=node_manager.get_node_editor_tag()):
        with dpg.node_attribute(label="End Input", attribute_type=dpg.mvNode_Attr_Input, tag=input_attr_tag):
            status_text_tag = f"{node_tag}_status"
            dpg.add_text("Waiting...", tag=status_text_tag)
    
    node_manager.register_node_input_executor(input_attr_tag, lambda: _on_end_execute(node_tag))
    return node_tag