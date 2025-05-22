import dearpygui.dearpygui as dpg
import random
from utils import get_unique_tag
import node_manager # To access trigger_next_node, register_node_input_executor, NODE_EDITOR_TAG

def _on_button_node_action_pressed(sender, app_data, user_data):
    """Execute when Button node's action button is pressed by user"""
    print(f"Button Node Action Pressed: {user_data}")
    node_tag = user_data
    # This is a user interaction, not part of the flow execution directly
    # We need to decide if this button press *itself* triggers the next node,
    # or if the node needs to be triggered by an input first, and then this button decides the path.
    # Original code implies this button itself triggers the next node.
    _execute_button_logic(node_tag)

def _execute_button_logic(node_tag):
    """Logic for button node execution, can be called by input trigger or button press"""
    print(f"Executing Button Node Logic for: {node_tag}")
    if random.choice([True, False]):
        output_attr_tag = f"{node_tag}_out_success"
        print("Button node: Success path")
    else:
        output_attr_tag = f"{node_tag}_out_failure"
        print("Button node: Failure path")
    node_manager.trigger_next_node(output_attr_tag)


def add_button_node():
    """Add a Button node to the editor"""
    node_tag = get_unique_tag()
    input_attr_tag = f"{node_tag}_in_1"

    with dpg.node(label="Button Node", tag=node_tag, parent=node_manager.get_node_editor_tag()):
        with dpg.node_attribute(label="Button Input", attribute_type=dpg.mvNode_Attr_Input, tag=input_attr_tag):
            # The button's callback directly triggers the logic.
            # If the node is triggered via input, the registered function below is called.
            dpg.add_button(label="Node Action", callback=_on_button_node_action_pressed, user_data=node_tag)
        with dpg.node_attribute(label="Success", attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}_out_success"):
            dpg.add_text("Success Path")
        with dpg.node_attribute(label="Failure", attribute_type=dpg.mvNode_Attr_Output, tag=f"{node_tag}_out_failure"):
            dpg.add_text("Failure Path")
    
    # This function is called when the node is triggered by an incoming link
    node_manager.register_node_input_executor(input_attr_tag, lambda: _execute_button_logic(node_tag))
    return node_tag