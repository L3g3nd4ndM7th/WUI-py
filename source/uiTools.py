import tkinter as tk
from tkinter import ttk
import drawTools
import gameMapTools
from config import game
import tkcolorpicker

"""


Handlers



"""

def handle_canvas_click(event):
    tool = game['ui']['selectedTool'].get()
    print(f"Canvas clicked with tool: {tool}")
    click_tool_actions = {
        "Select": select_cell,
        "Paint": paint_cell,
        "Place Node": place_node,
        "Place Text": place_text,
        "Delete": delete_cell
        # Exclude Clear Path from the click actions
    }
    if tool in click_tool_actions:
        click_tool_actions[tool](event)
    if hasattr(handle_canvas_drag, 'last_dragged_cell'):
        del handle_canvas_drag.last_dragged_cell

# Update handle_canvas_drag to include "Clear Path"
def handle_canvas_drag(event):
    tool = game['ui']['selectedTool'].get()
    print(f"Canvas dragged with tool: {tool}")
    drag_tool_actions = {
        "Paint": paint_cell,
        "Place Path": place_path,
        "Delete": delete_cell,
        "Place Node": place_node,
        "Place Text": place_text,
        "Clear Path": clear_path  # Add Clear Path to the tool actions
    }
    if tool in drag_tool_actions:
        drag_tool_actions[tool](event)

"""


Tools



"""

def place_path(event):
    current_cell = get_cell_at_event(event)
    
    if not hasattr(place_path, 'last_cell'):
        place_path.last_cell = current_cell
        return
    
    if current_cell and current_cell != place_path.last_cell:
        direction = determine_direction(place_path.last_cell.x, place_path.last_cell.y, current_cell.x, current_cell.y)
        if direction:
            color = game['ui']['selected_path_color']
            place_path.last_cell.pathColor = color
            current_cell.pathColor = color
            setattr(place_path.last_cell, direction.lower(), current_cell.id)
            setattr(current_cell, get_opposite_direction(direction).lower(), place_path.last_cell.id)
            display_cell_properties(place_path.last_cell)
            display_cell_properties(current_cell)
            drawTools.drawMap(game['currentMap'])
        place_path.last_cell = current_cell

def clear_path(event):
    current_cell = get_cell_at_event(event)
    
    if not hasattr(clear_path, 'last_cell'):
        clear_path.last_cell = current_cell
        return
    
    if current_cell and current_cell != clear_path.last_cell:
        direction = determine_direction(clear_path.last_cell.x, clear_path.last_cell.y, current_cell.x, current_cell.y)
        if direction:
            setattr(clear_path.last_cell, direction.lower(), "")
            setattr(current_cell, get_opposite_direction(direction).lower(), "")
            display_cell_properties(clear_path.last_cell)
            display_cell_properties(current_cell)
            drawTools.drawMap(game['currentMap'])
        clear_path.last_cell = current_cell

def place_node(event):
    current_cell = get_cell_at_event(event)
    if current_cell:
        shape = game['ui']['selected_shape'].get()
        color = game['ui']['selected_node_color']
        current_cell.nodeShape = shape
        current_cell.nodeColor = color
        display_cell_properties(current_cell)
        drawTools.drawMap(game['currentMap'])

def place_text(event):
    current_cell = get_cell_at_event(event)
    if current_cell:
        text = game['ui']['text_entry'].get()
        color = game['ui']['selected_text_color']
        current_cell.cellText = text
        current_cell.textColor = color
        display_cell_properties(current_cell)
        drawTools.drawMap(game['currentMap'])

def delete_cell(event):
    current_cell = get_cell_at_event(event)
    if current_cell:
        reset_cell(current_cell)
        display_cell_properties(current_cell)
        drawTools.drawMap(game['currentMap'])

def select_cell(event):
    cell = get_cell_at_event(event)
    if cell:
        game['ui']['canvas']['selected_cell'] = cell
        display_cell_properties(cell)

def paint_cell(event):
    cell = get_cell_at_event(event)
    if cell:
        color = game['ui']['selected_paint_color']
        paint_choice = game['ui']['paint_tool']['paint_choice'].get()
        
        if paint_choice == "Cell":
            cell.cellColor = color
        elif paint_choice == "Node":
            cell.nodeColor = color
        elif paint_choice == "Path":
            cell.pathColor = color
        elif paint_choice == "Text":
            cell.textColor = color

        display_cell_properties(cell)
        drawTools.drawMap(game['currentMap'])

"""


Helpers



"""

def update_tool_selection(new_value):
    print(f"Updating tool selection to: {new_value}")
    game['ui']['selectedTool'].set(new_value)
    update_tool_space(new_value)

def update_button_selection(selected_tool):
    print(f"Button selected: {selected_tool}")
    game['ui']['selectedTool'].set(selected_tool)
    for button in game['ui']['radio_buttons']:
        if button['text'] == selected_tool:
            button.state(['selected'])
        else:
            button.state(['!selected'])
    update_tool_space(selected_tool)

def update_tool_space(tool):
    tool_spaces = {
        "Select": game['ui']['select_tool_space'],
        "Paint": game['ui']['paint_tool_space'],
        "Place Node": game['ui']['place_node_tool_space'],
        "Place Text": game['ui']['place_text_tool_space'],
        "Place Path": game['ui']['place_path_tool_space'],
        "Delete": game['ui']['delete_tool_space']
    }
    print(f"Updating tool space for: {tool}")
    for key, widget in tool_spaces.items():
        if key == tool:
            widget.pack(fill='both', expand=True)
        else:
            widget.pack_forget()

def choose_color(tool):
    color_code = tkcolorpicker.askcolor(title="Choose color")[1]
    if color_code:
        if tool == 'paint':
            game['ui']['selected_paint_color'] = color_code
        elif tool == 'node':
            game['ui']['selected_node_color'] = color_code
        elif tool == 'text':
            game['ui']['selected_text_color'] = color_code

def zoom(direction):
    if direction == "in":
        game['ui']['canvas']['cell_size'] *= 1.5
    elif direction == "out":
        game['ui']['canvas']['cell_size'] /= 1.5
    drawTools.drawMap(game['currentMap'])

def goto_origin():
    game['ui']['canvas']['widget'].xview_moveto(0)
    game['ui']['canvas']['widget'].yview_moveto(0)

def reset_drag_state():
    if hasattr(place_path, 'last_cell'):
        del place_path.last_cell

def get_cell_at_event(event):
    tool = game['ui']['selectedTool'].get()
    canvas_x = game['ui']['canvas']['widget'].canvasx(event.x)
    canvas_y = game['ui']['canvas']['widget'].canvasy(event.y)
    cell_size = game['ui']['canvas']['cell_size']

    if tool in ["Place Path", "Clear Path"]:
        detection_size = cell_size / 4
    else:
        detection_size = cell_size / 2

    x = int(canvas_x // cell_size)
    y = int(canvas_y // cell_size)

    for cell in game['currentMap'].cells:
        cell_center_x = cell.x * cell_size + cell_size / 2
        cell_center_y = cell.y * cell_size + cell_size / 2

        if (abs(canvas_x - cell_center_x) <= detection_size and 
            abs(canvas_y - cell_center_y) <= detection_size):
            return cell
    return None

def determine_direction(last_x, last_y, x, y):
    if x > last_x and y == last_y:
        return 'E'
    elif x < last_x and y == last_y:
        return 'W'
    elif y > last_y and x == last_x:
        return 'S'
    elif y < last_y and x == last_x:
        return 'N'
    elif x > last_x and y > last_y:
        return 'SE'
    elif x < last_x and y > last_y:
        return 'SW'
    elif x > last_x and y < last_y:
        return 'NE'
    elif x < last_x and y < last_y:
        return 'NW'
    else:
        return None

def get_opposite_direction(direction):
    opposites = {
        'N': 'S', 'NE': 'SW', 'E': 'W', 'SE': 'NW',
        'S': 'N', 'SW': 'NE', 'W': 'E', 'NW': 'SE'
    }
    return opposites.get(direction, '')

def display_cell_properties(cell):
    properties = [
        'x', 'y', 'id', 'type', 'name', 'description', 'cellText', 
        'cellColor', 'textColor', 'nodeShape', 'nodeColor', 
        'pathColor', 'n', 'e', 's', 'w', 
        'ne', 'nw', 'se', 'sw'
    ]
    print(f"Displaying properties for cell: {cell.id}")
    for prop in properties:
        game['ui']['property_entries'][prop].delete(0, tk.END)
        game['ui']['property_entries'][prop].insert(0, getattr(cell, prop, ''))

def reset_cell(cell):
    cell_attrs = ['name', 'type', 'description', 'cellColor', 'cellText', 'textColor',
                  'nodeShape', 'nodeColor', 'pathColor', 'n', 'ne', 'e', 'se', 's', 
                  'sw', 'w', 'nw']
    for attr in cell_attrs:
        setattr(cell, attr, "")
    clear_paths(cell)

def clear_paths(cell):
    directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    for direction in directions:
        target_id = getattr(cell, direction)
        if target_id:
            target_cell = next((c for c in game['currentMap'].cells if c.id == target_id), None)
            if target_cell:
                setattr(target_cell, get_opposite_direction(direction), "")
            setattr(cell, direction, "")
    display_cell_properties(cell)
    drawTools.drawMap(game['currentMap'])

def open_menu():
    game['ui']['menu_popup'] = tk.Toplevel(game['ui']['root'])
    game['ui']['menu_popup'].title("Menu")
    game['ui']['menu_popup'].configure(bg='#2b2b2b')
    ttk.Button(game['ui']['menu_popup'], text="New Map", command=gameMapTools.generate_map).pack(pady=5)
    ttk.Button(game['ui']['menu_popup'], text="Export Map (as JSON)", command=gameMapTools.export_map).pack(pady=5)
    ttk.Button(game['ui']['menu_popup'], text="Load Map (JSON file)", command=gameMapTools.load_map).pack(pady=5)

def get_direction_delta(direction):
    directions = {
        'N': (0, -1), 'NE': (1, -1), 'E': (1, 0), 'SE': (1, 1),
        'S': (0, 1), 'SW': (-1, 1), 'W': (-1, 0), 'NW': (-1, -1)
    }
    return directions.get(direction, (0, 0))

def save_cell_properties():
    selected_cell = game['ui']['canvas']['selected_cell']
    if not selected_cell:
        return
    properties = ['x', 'y', 'id', 'type', 'name', 'description', 'cellText', 
                  'cellColor', 'textColor', 'nodeShape', 'nodeColor', 
                  'pathColor', 'n', 'e', 's', 'w', 
                  'ne', 'nw', 'se', 'sw']
    for prop in properties:
        setattr(selected_cell, prop.lower(), game['ui']['property_entries'][prop].get())
    drawTools.drawMap(game['currentMap'])

def move_map(direction):
    if direction == 'up':
        game['ui']['canvas']['widget'].yview_scroll(-1, 'units')
    elif direction == 'down':
        game['ui']['canvas']['widget'].yview_scroll(1, 'units')
    elif direction == 'left':
        game['ui']['canvas']['widget'].xview_scroll(-1, 'units')
    elif direction == 'right':
        game['ui']['canvas']['widget'].xview_scroll(1, 'units')

def update_coordinates(event):
    canvas_x = game['ui']['canvas']['widget'].canvasx(event.x)
    canvas_y = game['ui']['canvas']['widget'].canvasy(event.y)
    x = int(canvas_x // game['ui']['canvas']['cell_size'])
    y = int(canvas_y // game['ui']['canvas']['cell_size'])
    game['ui']['coord_label'].config(text=f"X: {x}, Y: {y}")
