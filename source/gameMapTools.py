import json
from tkinter import filedialog
from classGameMap import GameMap
from classCell import Cell
import drawTools
from config import game

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

            drawTools.drawMap(game['currentMap'])

def generate_map(game_map):
    cells = []
    cell_id_counter = 0
    for y in range(game_map.height):
        for x in range(game_map.width):
            cell_id = cell_id_counter
            cell = Cell(
                x=x,
                y=y,
                id=f"Cell{cell_id}",
                description=f"Description for Cell{cell_id}"
            )
            cells.append(cell)
            cell_id_counter += 1
    game_map.cells = cells
    game['currentMap'] = game_map
    drawTools.drawMap(game_map)