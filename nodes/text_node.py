import dearpygui.dearpygui as dpg
from utils import get_unique_tag
import node_manager # To access trigger_next_node, register_node_input_executor, NODE_EDITOR_TAG

def _on_text_execute(node_tag): # Removed sender, app_data as they are not used from lambda
    """Execute when Text node is triggered"""
    print(f"Executing Text Node: {node_tag}")
    text_value = dpg.get_value(f"{node_tag}_text")
    print(f"Text value: {text_value}")
    
    if text_value and text_value.strip():
        output_attr_tag = f"{node_tag}_out_success"
        print("Text node: Success path")
    else:
        output_attr_tag = f"{node_tag}_out_failure"
        print("Text node: Failure path")
    
    node_manager.trigger_next_node(output_attr_tag)

def add_text_node():
    """Add a Text node to the editor"""
    node_tag = get_unique_tag()
    input_attr_tag = f"{node_tag}_in_1"

    with dpg.node(label="Text Node", tag=node_tag, parent=node_manager.get_node_editor_tag()):
        with dpg.node_attribute(label="Text Input", attribute_type=dpg.mvNode_Attr_Input, tag=input_attr_tag):
            dpg.add_input_text(label="Text", width=150, tag=f"{node_tag}_text")
        with dpg.node_attribute(label="Success", attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}_out_success"):
            dpg.add_text("Success Path")
        with dpg.node_attribute(label="Failure", attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}_out_failure"):
            dpg.add_text("Failure Path")
    
    node_manager.register_node_input_executor(input_attr_tag, lambda: _on_text_execute(node_tag))
    return node_tag