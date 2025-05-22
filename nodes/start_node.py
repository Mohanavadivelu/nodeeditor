import dearpygui.dearpygui as dpg
from utils import get_unique_tag
import node_manager # To access trigger_next_node and NODE_EDITOR_TAG

def _on_start_execute(sender, app_data, user_data):
    """Execute when Start node's play button is pressed"""
    print(f"Executing Start Node: {user_data}")
    node_tag = user_data
    output_attr_tag = f"{node_tag}_out_1"
    print(f"Start node output attribute: {output_attr_tag}")
    node_manager.trigger_next_node(output_attr_tag)

def add_start_node():
    """Add a Start node to the editor"""
    node_tag = get_unique_tag()
    with dpg.node(label="Start Node", tag=node_tag, parent=node_manager.get_node_editor_tag()):
        with dpg.node_attribute(label="Start Output", attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}_out_1"):
            dpg.add_button(label="Play (>)", callback=_on_start_execute, user_data=node_tag)
    return node_tag