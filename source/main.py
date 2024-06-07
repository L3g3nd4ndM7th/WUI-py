import tkinter as tk
from tkinter import ttk, filedialog
import json
import random
import tkcolorpicker

"""
CLASSES
"""

class GameMap:
    def __init__(self, name="Default Map", height=10, width=10, start=[0, 0], cells=[]):
        self.name = name
        self.height = height
        self.width = width
        self.start = start
        self.cells = cells

class Cell:
    def __init__(self, x=0, y=0, id="", type="", name="", description="", cellText="", cellColor="darkgray", textColor="#000000",
                 nodeShape="", nodeColor="", pathColor="#000000", n="", e="", s="", w="", ne="", nw="", se="", sw=""):
        self.x = x
        self.y = y
        self.id = id
        self.type = type
        self.name = name
        self.description = description
        self.cellText = cellText
        self.cellColor = cellColor
        self.textColor = textColor
        self.nodeShape = nodeShape
        self.nodeColor = nodeColor
        self.pathColor = pathColor
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.ne = ne
        self.nw = nw
        self.se = se
        self.sw = sw

# Define cell types for different map themes
map_themes = {
    "Sewer": [
        {"name": "walkway", "color": "#A9A9A9", "description": "A damp walkway.", "weight": 40, "node_color": "#808080", "cell_text": "w"},
        {"name": "water", "color": "#000080", "description": "Stagnant water.", "weight": 30, "node_color": "#00008B", "cell_text": "W"},
        {"name": "pipe", "color": "#708090", "description": "A large pipe.", "weight": 15, "node_color": "#2F4F4F", "cell_text": "p"},
        {"name": "room", "color": "#2E8B57", "description": "A maintenance room.", "weight": 10, "node_color": "#006400", "cell_text": "r"},
        {"name": "drain", "color": "#696969", "description": "A drain cover.", "weight": 5, "node_color": "#A9A9A9", "cell_text": "d"}
    ],
    "Tavern": [
        {"name": "bar", "color": "#8B4513", "description": "The bar area.", "weight": 40, "node_color": "#A0522D", "cell_text": "b"},
        {"name": "table", "color": "#D2691E", "description": "A table.", "weight": 30, "node_color": "#CD853F", "cell_text": "t"},
        {"name": "stage", "color": "#A52A2A", "description": "A small stage.", "weight": 15, "node_color": "#B22222", "cell_text": "s"},
        {"name": "kitchen", "color": "#DEB887", "description": "The kitchen area.", "weight": 10, "node_color": "#D2B48C", "cell_text": "k"},
        {"name": "room", "color": "#F4A460", "description": "A private room.", "weight": 5, "node_color": "#DAA520", "cell_text": "r"}
    ],
    "Castle": [
        {"name": "hallway", "color": "#D3D3D3", "description": "A grand hallway.", "weight": 40, "node_color": "#A9A9A9", "cell_text": "h"},
        {"name": "courtyard", "color": "#90EE90", "description": "An open courtyard.", "weight": 25, "node_color": "#6B8E23", "cell_text": "c"},
        {"name": "dungeon", "color": "#696969", "description": "A dark dungeon.", "weight": 15, "node_color": "#808080", "cell_text": "d"},
        {"name": "tower", "color": "#FFD700", "description": "A tall tower.", "weight": 10, "node_color": "#DAA520", "cell_text": "t"},
        {"name": "throne", "color": "#B22222", "description": "The throne room.", "weight": 10, "node_color": "#8B0000", "cell_text": "T"}
    ],
    "Grassland": [
        {"name": "grass", "color": "#98FB98", "description": "A grassy field.", "weight": 40, "node_color": "#6B8E23", "cell_text": "g"},
        {"name": "forest", "color": "#556B2F", "description": "A dense forest.", "weight": 25, "node_color": "#2E8B57", "cell_text": "f"},
        {"name": "town", "color": "#D2B48C", "description": "A small town.", "weight": 10, "node_color": "#8B4513", "cell_text": "t"},
        {"name": "cave", "color": "#696969", "description": "A dark cave.", "weight": 10, "node_color": "#808080", "cell_text": "c"},
        {"name": "meadow", "color": "#ADFF2F", "description": "A beautiful meadow.", "weight": 5, "node_color": "#6495ED", "cell_text": "m"}
    ],
    "Forest": [
        {"name": "clearing", "color": "#90EE90", "description": "A forest clearing.", "weight": 30, "node_color": "#32CD32", "cell_text": "C"},
        {"name": "dense_trees", "color": "#006400", "description": "Dense trees.", "weight": 40, "node_color": "#228B22", "cell_text": "D"},
        {"name": "stream", "color": "#4682B4", "description": "A flowing stream.", "weight": 10, "node_color": "#1E90FF", "cell_text": "S"},
        {"name": "path", "color": "#A0522D", "description": "A forest path.", "weight": 10, "node_color": "#8B4513", "cell_text": "P"},
        {"name": "cabin", "color": "#8B4513", "description": "A wooden cabin.", "weight": 10, "node_color": "#A0522D", "cell_text": "H"}
    ],
    "Swamp": [
        {"name": "bog", "color": "#556B2F", "description": "A murky bog.", "weight": 40, "node_color": "#6B8E23", "cell_text": "B"},
        {"name": "marsh", "color": "#2E8B57", "description": "A wet marsh.", "weight": 30, "node_color": "#3CB371", "cell_text": "M"},
        {"name": "quagmire", "color": "#8B4513", "description": "A treacherous quagmire.", "weight": 10, "node_color": "#A0522D", "cell_text": "Q"},
        {"name": "water", "color": "#000080", "description": "Stagnant water.", "weight": 10, "node_color": "#00008B", "cell_text": "W"},
        {"name": "hut", "color": "#6B8E23", "description": "A swamp hut.", "weight": 10, "node_color": "#556B2F", "cell_text": "H"}
    ],
    "Mountain": [
        {"name": "peak", "color": "#808080", "description": "A mountain peak.", "weight": 40, "node_color": "#696969", "cell_text": "P"},
        {"name": "trail", "color": "#A0522D", "description": "A rocky trail.", "weight": 30, "node_color": "#8B4513", "cell_text": "T"},
        {"name": "cave", "color": "#696969", "description": "A dark cave.", "weight": 10, "node_color": "#808080", "cell_text": "C"},
        {"name": "cliff", "color": "#B22222", "description": "A steep cliff.", "weight": 10, "node_color": "#8B0000", "cell_text": "C"},
        {"name": "lodge", "color": "#8B4513", "description": "A mountain lodge.", "weight": 10, "node_color": "#A0522D", "cell_text": "L"}
    ],
    "Desert": [
        {"name": "dune", "color": "#EDC9AF", "description": "A sandy dune.", "weight": 40, "node_color": "#C2B280", "cell_text": "D"},
        {"name": "oasis", "color": "#228B22", "description": "A lush oasis.", "weight": 20, "node_color": "#32CD32", "cell_text": "O"},
        {"name": "ruin", "color": "#8B4513", "description": "Ancient ruins.", "weight": 15, "node_color": "#A0522D", "cell_text": "R"},
        {"name": "rock", "color": "#A0522D", "description": "A large rock.", "weight": 15, "node_color": "#8B4513", "cell_text": "R"},
        {"name": "caravan", "color": "#F4A460", "description": "A traveling caravan.", "weight": 10, "node_color": "#DEB887", "cell_text": "C"}
    ],
    "Arctic": [
        {"name": "snowfield", "color": "#F0FFFF", "description": "A vast snowfield.", "weight": 40, "node_color": "#E0FFFF", "cell_text": "S"},
        {"name": "glacier", "color": "#ADD8E6", "description": "A slow-moving glacier.", "weight": 30, "node_color": "#B0E0E6", "cell_text": "G"},
        {"name": "ice_cave", "color": "#AFEEEE", "description": "An icy cave.", "weight": 15, "node_color": "#00CED1", "cell_text": "C"},
        {"name": "tundra", "color": "#4682B4", "description": "A frozen tundra.", "weight": 10, "node_color": "#5F9EA0", "cell_text": "T"},
        {"name": "igloo", "color": "#B0E0E6", "description": "A small igloo.", "weight": 5, "node_color": "#AFEEEE", "cell_text": "I"}
    ],
    "Wasteland": [
        {"name": "ruin", "color": "#8B4513", "description": "Ruined structures.", "weight": 40, "node_color": "#A0522D", "cell_text": "R"},
        {"name": "barren", "color": "#A9A9A9", "description": "Barren land.", "weight": 30, "node_color": "#808080", "cell_text": "B"},
        {"name": "scrap", "color": "#696969", "description": "Scrap heaps.", "weight": 15, "node_color": "#808080", "cell_text": "S"},
        {"name": "crater", "color": "#B22222", "description": "A large crater.", "weight": 10, "node_color": "#8B0000", "cell_text": "C"},
        {"name": "outpost", "color": "#8B4513", "description": "A desolate outpost.", "weight": 5, "node_color": "#A0522D", "cell_text": "O"}
    ],
    "Badland": [
        {"name": "canyon", "color": "#CD853F", "description": "A deep canyon.", "weight": 40, "node_color": "#8B4513", "cell_text": "C"},
        {"name": "mesa", "color": "#DEB887", "description": "A high mesa.", "weight": 30, "node_color": "#F4A460", "cell_text": "M"},
        {"name": "spires", "color": "#A0522D", "description": "Rock spires.", "weight": 15, "node_color": "#8B4513", "cell_text": "S"},
        {"name": "cliff", "color": "#8B4513", "description": "A steep cliff.", "weight": 10, "node_color": "#A0522D", "cell_text": "C"},
        {"name": "ravine", "color": "#8B0000", "description": "A narrow ravine.", "weight": 5, "node_color": "#B22222", "cell_text": "R"}
    ]
}

"""
Canvas Drawing
"""

def drawCells(game_map):
    cell_size = game['ui']['canvas']['cell_size']
    for cell in game_map.cells:
        color = cell.cellColor or "darkgray"
        game['ui']['canvas']['widget'].create_rectangle(
            cell.x * cell_size, cell.y * cell_size,
            (cell.x + 1) * cell_size, (cell.y + 1) * cell_size,
            fill=color, outline="black"
        )

def drawPaths(game_map):
    cell_size = game['ui']['canvas']['cell_size']
    for cell in game_map.cells:
        center_x = cell.x * cell_size + cell_size // 2
        center_y = cell.y * cell_size + cell_size // 2
        path_color = cell.pathColor

        directions = {
            'n': (center_x, center_y - cell_size // 2, center_x, center_y - cell_size),
            'e': (center_x + cell_size // 2, center_y, center_x + cell_size, center_y),
            's': (center_x, center_y + cell_size // 2, center_x, center_y + cell_size),
            'w': (center_x - cell_size // 2, center_y, center_x - cell_size, center_y),
            'ne': (center_x + cell_size // 2, center_y - cell_size // 2, center_x + cell_size, center_y - cell_size),
            'nw': (center_x - cell_size // 2, center_y - cell_size // 2, center_x - cell_size, center_y - cell_size),
            'se': (center_x + cell_size // 2, center_y + cell_size // 2, center_x + cell_size, center_y + cell_size),
            'sw': (center_x - cell_size // 2, center_y + cell_size // 2, center_x - cell_size, center_y + cell_size)
        }

        for direction, coords in directions.items():
            if getattr(cell, direction):
                game['ui']['canvas']['widget'].create_line(*coords, fill=path_color, width=3)

def drawNodes(game_map):
    for cell in game_map.cells:
        if cell.nodeShape:
            drawNode(cell.x, cell.y, cell.nodeShape, cell.nodeColor)

def drawNode(x, y, shape, color):
    cell_size = game['ui']['canvas']['cell_size']
    node_size = cell_size // 2
    center_x = x * cell_size + cell_size // 2
    center_y = y * cell_size + cell_size // 2

    if shape.lower() == 'circle':
        game['ui']['canvas']['widget'].create_oval(
            center_x - node_size // 2, center_y - node_size // 2,
            center_x + node_size // 2, center_y + node_size // 2,
            fill=color, outline=color
        )
    elif shape.lower() == 'square':
        game['ui']['canvas']['widget'].create_rectangle(
            center_x - node_size // 2, center_y - node_size // 2,
            center_x + node_size // 2, center_y + node_size // 2,
            fill=color, outline=color
        )
    elif shape.lower() == 'triangle':
        game['ui']['canvas']['widget'].create_polygon(
            center_x, center_y - node_size // 2,
            center_x - node_size // 2, center_y + node_size // 2,
            center_x + node_size // 2, center_y + node_size // 2,
            fill=color, outline=color
        )
    elif shape.lower() == 'hexagon':
        game['ui']['canvas']['widget'].create_polygon(
            center_x, center_y - node_size // 2,
            center_x + node_size * 0.5, center_y - node_size // 4,
            center_x + node_size * 0.5, center_y + node_size // 4,
            center_x, center_y + node_size // 2,
            center_x - node_size * 0.5, center_y + node_size // 4,
            center_x - node_size * 0.5, center_y - node_size // 4,
            fill=color, outline=color
        )
    elif shape.lower() == 'star':
        game['ui']['canvas']['widget'].create_polygon(
            center_x, center_y - node_size // 2,
            center_x + node_size * 0.15, center_y - node_size * 0.15,
            center_x + node_size // 2, center_y - node_size * 0.15,
            center_x + node_size * 0.25, center_y + node_size * 0.15,
            center_x + node_size * 0.35, center_y + node_size // 2,
            center_x, center_y + node_size * 0.25,
            center_x - node_size * 0.35, center_y + node_size // 2,
            center_x - node_size * 0.25, center_y + node_size * 0.15,
            center_x - node_size // 2, center_y - node_size * 0.15,
            center_x - node_size * 0.15, center_y - node_size * 0.15,
            fill=color, outline=color
        )

def drawTexts(game_map):
    cell_size = game['ui']['canvas']['cell_size']
    for cell in game_map.cells:
        if cell.cellText:
            text_color = cell.textColor or "white"
            game['ui']['canvas']['widget'].create_text(
                cell.x * cell_size + cell_size // 2,
                cell.y * cell_size + cell_size // 2,
                text=cell.cellText, fill=text_color
            )

def drawGrid(game_map):
    cell_size = game['ui']['canvas']['cell_size']
    for i in range(game_map.width):
        game['ui']['canvas']['widget'].create_line(i * cell_size, 0, i * cell_size, game_map.height * cell_size, fill="black")
    for i in range(game_map.height):
        game['ui']['canvas']['widget'].create_line(0, i * cell_size, game_map.width * cell_size, i * cell_size, fill="black")

def drawMap(game_map):
    game['ui']['canvas']['widget'].delete("all")
    drawCells(game_map)
    drawPaths(game_map)
    drawNodes(game_map)
    drawTexts(game_map)
    drawGrid(game_map)


"""
Canvas Event Handlers
"""

def handle_canvas_click(event):
    tool = game['ui']['selectedTool'].get()
    click_tool_actions = {
        "Select": select_cell,
        "Paint": paint_cell,
        "Place Node": place_node,
        "Place Text": place_text,
        "Delete": delete_cell
    }
    if tool in click_tool_actions:
        click_tool_actions[tool](event)
    if hasattr(handle_canvas_drag, 'last_dragged_cell'):
        del handle_canvas_drag.last_dragged_cell

def handle_canvas_drag(event):
    tool = game['ui']['selectedTool'].get()
    drag_tool_actions = {
        "Paint": paint_cell,
        "Place Path": place_path,
        "Delete": delete_cell,
        "Place Node": place_node,
        "Place Text": place_text,
        "Clear Path": clear_path
    }
    if tool in drag_tool_actions:
        drag_tool_actions[tool](event)

"""
Popup Management
"""

def create_popup(name, title, content_function):
    if name in game['ui']['popups']:
        print(f"Popup '{name}' already exists.")
        return

    overlay = create_overlay()
    popup_frame = create_popup_frame(overlay, title, content_function)
    close_button = create_close_button(popup_frame, name)

    game['ui']['popups'][name] = {
        "overlay": overlay,
        "popup_frame": popup_frame,
        "close_button": close_button
    }

def create_overlay():
    overlay = tk.Frame(game['ui']['root'], bg='gray')
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    return overlay

def create_popup_frame(overlay, title, content_function):
    popup_frame = tk.Frame(overlay, bd=2, relief=tk.RAISED, bg='white')
    popup_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    tk.Label(popup_frame, text=title, bg='white').pack(pady=10)
    content_function(popup_frame)
    return popup_frame

def create_close_button(popup_frame, name):
    close_button = tk.Button(popup_frame, text="Close", command=lambda: close_popup(name))
    close_button.pack(pady=10)
    return close_button

def close_popup(name):
    if name in game['ui']['popups']:
        game['ui']['popups'][name]["overlay"].destroy()
        del game['ui']['popups'][name]
    else:
        print(f"Popup '{name}' does not exist.")

"""
Specific Popup Functions
"""

def open_new_map_popup():
    # Ensure map themes are initialized
    if 'map_themes' not in game:
        game['map_themes'] = list(map_themes.keys())
    
    def new_map_content(frame):
        tk.Label(frame, text="Select a map type:").pack(pady=10)
        listbox = tk.Listbox(frame, selectmode=tk.SINGLE, bg='#1e1e1e', fg='white')
        for theme in game['map_themes']:  # Use dynamic map themes
            listbox.insert("end", theme)
        listbox.pack(pady=10)
        tk.Button(frame, text="Generate Map", command=lambda: on_map_selection(listbox)).pack(pady=10)
    
    create_popup("new_map_popup", "New Map", new_map_content)

def open_load_map_popup():
    def load_map_content(frame):
        tk.Button(frame, text="Load Map (JSON file)", command=load_map).pack(pady=10)
    
    create_popup("load_map_popup", "Load Map", load_map_content)

def open_export_map_popup():
    def export_map_content(frame):
        tk.Button(frame, text="Export Map (as JSON)", command=export_map).pack(pady=10)
    
    create_popup("export_map_popup", "Export Map", export_map_content)

def open_menu():
    def menu_content(frame):
        ttk.Button(frame, text="New Map", command=open_new_map_popup).pack(pady=5)
        ttk.Button(frame, text="Export Map (as JSON)", command=open_export_map_popup).pack(pady=5)
        ttk.Button(frame, text="Load Map (JSON file)", command=open_load_map_popup).pack(pady=5)
    
    create_popup("menu_popup", "Menu", menu_content)

def on_map_selection(listbox):
    selected_theme = listbox.get(listbox.curselection())
    new_map(selected_theme)
    drawMap(game['currentMap'])
    close_popup("new_map_popup")

"""
GameMap Actions
"""

def choose_cell_type(cell_types):
    total_weight = sum(cell_type["weight"] for cell_type in cell_types)
    rand_value = random.randint(1, total_weight)
    for cell_type in cell_types:
        if rand_value <= cell_type["weight"]:
            return cell_type
        rand_value -= cell_type["weight"]

def new_map(theme):
    if theme not in map_themes:
        raise ValueError(f"Theme '{theme}' is not defined.")
    
    cell_types = map_themes[theme]
    game_map = GameMap(
        name=f"{theme}Map",
        height=10,
        width=10,
        start=[0, 0],
        cells=[]
    )

    cell_id_counter = 1
    for y in range(10):
        for x in range(10):
            cell_type = choose_cell_type(cell_types)
            cell = Cell(
                x=x,
                y=y,
                id=f"{theme}ID{cell_id_counter}",
                type=cell_type["name"],  # Directly use properties from map_themes
                name=cell_type["name"].capitalize(),
                description=cell_type["description"],
                cellText=cell_type["cell_text"],
                cellColor=cell_type["color"],
                textColor="#ffffff",
                nodeShape="circle",
                nodeColor=cell_type["node_color"],
                pathColor="#000000"
            )
            game_map.cells.append(cell)
            cell_id_counter += 1

    game['currentMap'] = game_map
    drawMap(game['currentMap'])

def export_map():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        current_map = game['currentMap']
        export_data = {
            'name': current_map.name,
            'height': current_map.height,
            'width': current_map.width,
            'start': current_map.start,
            'cells': [cell.__dict__ for cell in current_map.cells]
        }
        with open(file_path, 'w') as file:
            json.dump(export_data, file, indent=4)

def load_map():
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            game['currentMap'] = GameMap(
                name=data['name'],
                height=data['height'],
                width=data['width'],
                start=data['start'],
                cells=[Cell(**cell_data) for cell_data in data['cells']]
            )

            drawMap(game['currentMap'])

"""
Tool Actions
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
            drawMap(game['currentMap'])
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
            drawMap(game['currentMap'])
        clear_path.last_cell = current_cell

def place_node(event):
    current_cell = get_cell_at_event(event)
    if current_cell:
        shape = game['ui']['selected_shape'].get()
        color = game['ui']['selected_node_color']
        current_cell.nodeShape = shape
        current_cell.nodeColor = color
        display_cell_properties(current_cell)
        drawMap(game['currentMap'])

def place_text(event):
    current_cell = get_cell_at_event(event)
    if current_cell:
        text = game['ui']['text_entry'].get()
        color = game['ui']['selected_text_color']
        current_cell.cellText = text
        current_cell.textColor = color
        display_cell_properties(current_cell)
        drawMap(game['currentMap'])

def delete_cell(event):
    current_cell = get_cell_at_event(event)
    if not current_cell:
        return
    
    directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    
    for direction in directions:
        target_id = getattr(current_cell, direction)
        if target_id:
            target_cell = next((c for c in game['currentMap'].cells if c.id == target_id), None)
            if target_cell:
                opposite_direction = get_opposite_direction(direction)
                setattr(target_cell, opposite_direction.lower(), "")
    
    for direction in directions:
        setattr(current_cell, direction, "")

    cell_attrs = ['type', 'name', 'description', 'cellText', 'cellColor', 
                  'textColor', 'nodeShape', 'nodeColor', 'pathColor']
    for attr in cell_attrs:
        setattr(current_cell, attr, "")

    drawMap(game['currentMap'])
    display_cell_properties(current_cell)

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
        drawMap(game['currentMap'])

"""
Helper Functions
"""

def update_tool_selection(new_value):
    game['ui']['selectedTool'].set(new_value)
    update_tool_space(new_value)

def update_button_selection(selected_tool):
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
        "Clear Path": game['ui']['clear_path_tool_space'],
        "Delete": game['ui']['delete_tool_space']
    }
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
    drawMap(game['currentMap'])

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
        return 'e'
    elif x < last_x and y == last_y:
        return 'w'
    elif y > last_y and x == last_x:
        return 's'
    elif y < last_y and x == last_x:
        return 'n'
    elif x > last_x and y > last_y:
        return 'se'
    elif x < last_x and y > last_y:
        return 'sw'
    elif x > last_x and y < last_y:
        return 'ne'
    elif x < last_x and y < last_y:
        return 'nw'
    else:
        return None

def get_opposite_direction(direction):
    opposites = {
        'n': 's', 'ne': 'sw', 'e': 'w', 'se': 'nw',
        's': 'n', 'sw': 'ne', 'w': 'e', 'nw': 'se'
    }
    return opposites.get(direction, '')

def display_cell_properties(cell):
    properties = [
        'x', 'y', 'id', 'type', 'name', 'description', 'cellText', 
        'cellColor', 'textColor', 'nodeShape', 'nodeColor', 
        'pathColor', 'n', 'e', 's', 'w', 
        'ne', 'nw', 'se', 'sw'
    ]
    for prop in properties:
        game['ui']['property_entries'][prop].delete(0, tk.END)
        game['ui']['property_entries'][prop].insert(0, getattr(cell, prop, ''))

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
    drawMap(game['currentMap'])

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

"""
GAME AND UI
"""

game = {}
game['ui'] = {}
game['ui']['root'] = tk.Tk()
game['ui']['root'].state('normal')  # Maximize the main window

# Set window size
game['ui']['root'].geometry('800x600')

# Add UI properties
game['ui']['popups'] = {}

# Canvas Settings
game['ui']['canvas'] = {}
game['ui']['canvas']['cell_size'] = 64
game['ui']['canvas']['selected_cell'] = None
game['ui']['selectedTool'] = tk.StringVar(value="Select")
game['ui']['selected_paint_color'] = "#000000"
game['ui']['selected_node_color'] = "#000000"
game['ui']['selected_text_color'] = "#000000"
game['ui']['selected_path_color'] = "#000000"
game['ui']['selected_shape'] = tk.StringVar(value="Circle")

# Style
game['ui']['style'] = ttk.Style()
game['ui']['style'].theme_use('clam')
game['ui']['style'].configure('TButton', background='#4d4d4d', foreground='white', borderwidth=1)
game['ui']['style'].map('TButton', background=[('active', '#666666')])
game['ui']['root'].configure(bg='#1e1e1e')
game['ui']['style'].configure('TRadioButton.TButton', background='#4d4d4d', foreground='white', borderwidth=1)
game['ui']['style'].map('TRadioButton.TButton', background=[('selected', '#444444'), ('active', '#666666')])

# Tool Panel
game['ui']['tool_panel'] = tk.Frame(game['ui']['root'], bg='#2b2b2b', padx=10, pady=10)
game['ui']['tool_panel'].pack(side='left', fill='y', padx=5, pady=5)

game['ui']['menu_section'] = tk.Frame(game['ui']['tool_panel'], bg='#2b2b2b')
game['ui']['menu_section'].pack(fill='x', pady=10)
game['ui']['menu_button'] = ttk.Button(game['ui']['menu_section'], text="Menu", command=open_menu)
game['ui']['menu_button'].pack(pady=10, padx=10)

game['ui']['radio_section'] = tk.Frame(game['ui']['tool_panel'], bg='#2b2b2b')
game['ui']['radio_section'].pack(fill='x', pady=10)
game['ui']['radio_buttons'] = [
    ttk.Button(game['ui']['radio_section'], text="Select", style='TRadioButton.TButton', command=lambda: update_button_selection("Select")),
    ttk.Button(game['ui']['radio_section'], text="Paint", style='TRadioButton.TButton', command=lambda: update_button_selection("Paint")),
    ttk.Button(game['ui']['radio_section'], text="Place Node", style='TRadioButton.TButton', command=lambda: update_button_selection("Place Node")),
    ttk.Button(game['ui']['radio_section'], text="Place Text", style='TRadioButton.TButton', command=lambda: update_button_selection("Place Text")),
    ttk.Button(game['ui']['radio_section'], text="Place Path", style='TRadioButton.TButton', command=lambda: update_button_selection("Place Path")),
    ttk.Button(game['ui']['radio_section'], text="Clear Path", style='TRadioButton.TButton', command=lambda: update_button_selection("Clear Path")),
    ttk.Button(game['ui']['radio_section'], text="Delete", style='TRadioButton.TButton', command=lambda: update_button_selection("Delete"))
]
for btn in game['ui']['radio_buttons']:
    btn.pack(anchor='w')

game['ui']['tool_space'] = tk.Frame(game['ui']['tool_panel'], bg='#2b2b2b')
game['ui']['tool_space'].pack(fill='both', expand=True)
game['ui']['paint_tool'] = {}

game['ui']['select_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
tk.Label(game['ui']['select_tool_space'], text="Select a cell to see its properties", bg='#2b2b2b', fg='white').pack()

game['ui']['paint_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
tk.Label(game['ui']['paint_tool_space'], text="Paint Tool", bg='#2b2b2b', fg='white').pack()
tk.Label(game['ui']['paint_tool_space'], text="Choose Cell Component", bg='#2b2b2b', fg='white').pack()
game['ui']['paint_tool']['paint_choice'] = tk.StringVar(value="Cell")
game['ui']['paint_tool']['paint_choice_button'] = tk.Button(game['ui']['paint_tool_space'], textvariable=game['ui']['paint_tool']['paint_choice'], width=20)
game['ui']['paint_tool']['paint_choice_button'].pack()
game['ui']['paint_tool']['paint_choice_menu'] = tk.Menu(game['ui']['paint_tool']['paint_choice_button'], tearoff=0)
paint_options = ["Cell", "Node", "Path", "Text"]
for option in paint_options:
    game['ui']['paint_tool']['paint_choice_menu'].add_command(label=option, command=lambda opt=option: game['ui']['paint_tool']['paint_choice'].set(opt))
game['ui']['paint_tool']['paint_choice_button'].bind("<Button-1>", lambda event: game['ui']['paint_tool']['paint_choice_menu'].post(event.x_root, event.y_root))
game['ui']['paint_tool']['color_button'] = ttk.Button(game['ui']['paint_tool_space'], text="Choose Color", command=lambda: choose_color('paint'))
game['ui']['paint_tool']['color_button'].pack()

game['ui']['place_node_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
tk.Label(game['ui']['place_node_tool_space'], text="Choose Node Shape", bg='#2b2b2b', fg='white').pack()
game['ui']['shape_choice_button'] = tk.Button(game['ui']['place_node_tool_space'], textvariable=game['ui']['selected_shape'], width=20)
game['ui']['shape_choice_button'].pack()
game['ui']['shape_choice_menu'] = tk.Menu(game['ui']['shape_choice_button'], tearoff=0)
shapes = ["Circle", "Square", "Triangle", "Hexagon", "Star"]
for shape in shapes:
    game['ui']['shape_choice_menu'].add_command(label=shape, command=lambda shp=shape: game['ui']['selected_shape'].set(shp))
game['ui']['shape_choice_button'].bind("<Button-1>", lambda event: game['ui']['shape_choice_menu'].post(event.x_root, event.y_root))
game['ui']['node_color_button'] = ttk.Button(game['ui']['place_node_tool_space'], text="Choose Node Color", command=lambda: choose_color('node'))
game['ui']['node_color_button'].pack()

game['ui']['place_text_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
tk.Label(game['ui']['place_text_tool_space'], text="Enter Text", bg='#2b2b2b', fg='white').pack()
game['ui']['text_entry'] = tk.Entry(game['ui']['place_text_tool_space'], bg='#1e1e1e', fg='white', insertbackground='white')
game['ui']['text_entry'].pack()
game['ui']['text_color_button'] = ttk.Button(game['ui']['place_text_tool_space'], text="Choose Text Color", command=lambda: choose_color('text'))
game['ui']['text_color_button'].pack()

game['ui']['place_path_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
tk.Label(game['ui']['place_path_tool_space'], text="Click and drag to connect cells", bg='#2b2b2b', fg='white').pack()

game['ui']['clear_path_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
tk.Label(game['ui']['clear_path_tool_space'], text="Drag to delete paths", bg='#2b2b2b', fg='white').pack()

game['ui']['delete_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
tk.Label(game['ui']['delete_tool_space'], text="Click and drag to delete cells", bg='#2b2b2b', fg='white').pack()

# Canvas Panel
game['ui']['canvas_panel'] = tk.Frame(game['ui']['root'], bg='#2b2b2b')
game['ui']['canvas_panel'].pack(side='left', fill='both', expand=True, padx=5, pady=5)

# Canvas Tool Container
game['ui']['canvas_tool_container'] = tk.Frame(game['ui']['canvas_panel'], bg='#2b2b2b')
game['ui']['canvas_tool_container'].pack(side='top', fill='x')

game['ui']['zoom_in_button'] = ttk.Button(game['ui']['canvas_tool_container'], text="+", width=2, command=lambda: zoom("in"))
game['ui']['zoom_in_button'].pack(side='left', padx=5, pady=5)
game['ui']['zoom_out_button'] = ttk.Button(game['ui']['canvas_tool_container'], text="-", width=2, command=lambda: zoom("out"))
game['ui']['zoom_out_button'].pack(side='left', padx=5, pady=5)
game['ui']['coord_label'] = tk.Label(game['ui']['canvas_tool_container'], text="X: 0, Y: 0", bg='#2b2b2b', fg='#ffffff', width=10)
game['ui']['coord_label'].pack(side='left', padx=10)
game['ui']['goto_button'] = ttk.Button(game['ui']['canvas_tool_container'], text="Go to 0,0", command=goto_origin)
game['ui']['goto_button'].pack(side='left', padx=5, pady=5)

# Canvas
game['ui']['canvas']['widget'] = tk.Canvas(game['ui']['canvas_panel'], bg="#2b2b2b")
game['ui']['canvas']['widget'].pack(fill='both', expand=True)

# Cell Panel
game['ui']['cell_panel'] = tk.Frame(game['ui']['root'], bg='#2b2b2b')
game['ui']['cell_panel'].pack(side='left', fill='y', padx=5, pady=5)

# Frame for organizing the cell details in a grid
game['ui']['cell_details'] = tk.Frame(game['ui']['cell_panel'], bg='#2b2b2b')
game['ui']['cell_details'].pack(fill='both', expand=True)

properties = [
    'x', 'y', 'id', 'type', 'name', 'description', 'cellText', 
    'cellColor', 'textColor', 'nodeShape', 'nodeColor', 
    'pathColor', 'n', 'e', 's', 'w', 
    'ne', 'nw', 'se', 'sw'
]
game['ui']['property_entries'] = {}

for i, prop in enumerate(properties):
    tk.Label(game['ui']['cell_details'], text=prop, bg='#2b2b2b', fg='#ffffff').grid(row=i, column=0, sticky='w', padx=5, pady=5)
    game['ui']['property_entries'][prop] = tk.Entry(game['ui']['cell_details'], bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff')
    game['ui']['property_entries'][prop].grid(row=i, column=1, sticky='ew', padx=5, pady=5)

game['ui']['save_button'] = ttk.Button(game['ui']['cell_panel'], text="Save", command=save_cell_properties)
game['ui']['save_button'].pack(pady=10)

# Configuration and bindings
game['ui']['menu_button'].config(command=open_menu)
for btn in game['ui']['radio_buttons']:
    btn.config(command=lambda btn=btn: update_button_selection(btn['text']))

game['ui']['canvas']['widget'].bind('<Button-1>', handle_canvas_click)
game['ui']['canvas']['widget'].bind('<Motion>', update_coordinates)
game['ui']['canvas']['widget'].bind('<B1-Motion>', handle_canvas_drag)
game['ui']['canvas']['widget'].bind('<ButtonRelease-1>', lambda event: reset_drag_state())
game['ui']['canvas']['widget'].bind('<Up>', lambda event: move_map('up'))
game['ui']['canvas']['widget'].bind('<Down>', lambda event: move_map('down'))
game['ui']['canvas']['widget'].bind('<Left>', lambda event: move_map('left'))
game['ui']['canvas']['widget'].bind('<Right>', lambda event: move_map('right'))
game['ui']['root'].bind('<Up>', lambda event: move_map('up'))
game['ui']['root'].bind('<Down>', lambda event: move_map('down'))
game['ui']['root'].bind('<Left>', lambda event: move_map('left'))
game['ui']['root'].bind('<Right>', lambda event: move_map('right'))

"""
START APP
"""

new_map('Sewer')
game['ui']['root'].mainloop()