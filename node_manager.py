import dearpygui.dearpygui as dpg

# Global variables to store node connections and execution state
active_links = {}  # Maps output attribute tags to (input attribute tag, link item tag)
node_input_to_function_map = {}  # Maps input attribute tags to their execution functions
NODE_EDITOR_TAG = "node_editor"  # Store the node editor tag for reference

def get_node_editor_tag():
    return NODE_EDITOR_TAG

def register_node_input_executor(input_attr_tag, execution_function):
    """Registers an execution function for a specific node input attribute."""
    node_input_to_function_map[input_attr_tag] = execution_function
    print(f"Registered executor for {input_attr_tag}")

def trigger_next_node(current_output_attr_tag):
    """Trigger the next node in the execution chain"""
    print(f"Triggering next node from output: {current_output_attr_tag}")
    print(f"Active links: {active_links}")
    
    if current_output_attr_tag in active_links:
        next_input_attr_tag, link_id = active_links[current_output_attr_tag]
        print(f"Found next input: {next_input_attr_tag}")
        
        if next_input_attr_tag in node_input_to_function_map:
            print(f"Executing function for input: {next_input_attr_tag}")
            node_input_to_function_map[next_input_attr_tag]()
        else:
            print(f"No function mapped for input: {next_input_attr_tag}")
    else:
        print(f"No active link found for output: {current_output_attr_tag}")

def link_callback(sender, app_data):
    """Handle node connections"""
    print(f"Creating link: {app_data}")
    # Get the actual attribute tags from the link
    output_attr = dpg.get_item_alias(app_data[0])
    input_attr = dpg.get_item_alias(app_data[1])
    print(f"Output attribute: {output_attr}")
    print(f"Input attribute: {input_attr}")
    
    # app_data[0] and app_data[1] are the attribute item tags, not aliases
    dpg.add_node_link(app_data[0], app_data[1], parent=sender) # sender is the node editor
    active_links[output_attr] = (input_attr, app_data[0]) # Storing the link item tag is tricky, let's use output_attr for now
    # A better way to get the link ID itself after creation would be ideal, but DPG doesn't directly return it.
    # For now, we will identify links by the output_attr they originate from, assuming one link per output.
    # Or, we can use the output_attr and input_attr pair as a key for the link item if we need to delete by item.
    # Let's refine how we store link_id for deletion.
    # The `delink_callback` gives us the link_id (app_data) directly.
    # So we need to map output_attr to (input_attr, link_item_tag).
    # The add_node_link doesn't return the link_id.
    # We'll have to search for it or assume a pattern if DPG generates predictable IDs.
    # For simplicity, let's assume the link item tag is not easily retrievable on add_node_link directly for active_links.
    # We'll reconstruct the link removal logic in delink_callback.
    # The link_id given to delink_callback *is* the item tag of the link.
    # So, when adding, we store the pair:
    active_links[output_attr] = (input_attr, None) # We don't have the link_id yet
    # The 'link_id' (the visual link item) is created by dpg.add_node_link.
    # We need to find it to delete it later.
    # The `delink_callback` receives the link's item tag as `app_data`.
    # Let's adjust active_links to store the link item tag *when* `add_node_link` is called.
    # Actually, `dpg.add_node_link` *does* return the tag of the created link item!
    link_item_tag = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
    active_links[output_attr] = (input_attr, link_item_tag)

    print(f"Updated active links: {active_links}")


def delink_callback(sender, app_data):
    """Handle node disconnections"""
    # app_data is the tag of the link to be deleted
    link_to_delete = app_data
    print(f"Deleting link: {link_to_delete}")
    
    # Find and remove the link from active_links
    output_attr_to_remove = None
    for out_attr, (in_attr, link_tag_stored) in active_links.items():
        if link_tag_stored == link_to_delete:
            output_attr_to_remove = out_attr
            break
    
    if output_attr_to_remove:
        del active_links[output_attr_to_remove]
        print(f"Removed link from active_links originating from: {output_attr_to_remove}")
    else:
        print(f"Warning: Could not find link {link_to_delete} in active_links for removal.")
        # This might happen if the link was created outside this callback system
        # or if active_links got out of sync.

    dpg.delete_item(link_to_delete) # This actually deletes the visual link
    print(f"Updated active links: {active_links}")