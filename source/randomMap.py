import random
from classGameMap import GameMap
from classCell import Cell

class CellType:
    def __init__(self, name, color, description, weight, node_color, cell_text):
        self.name = name
        self.color = color
        self.description = description
        self.weight = weight
        self.node_color = node_color
        self.cell_text = cell_text

# Define different cell types with weights
cell_types = [
    CellType("grass", "#98FB98", "A grassy field.", 40, "#6B8E23", "g"),
    CellType("forest", "#556B2F", "A dense forest.", 25, "#2E8B57", "f"),
    CellType("town", "#D3D3D3", "A small town.", 10, "#A9A9A9", "t"),
    CellType("cave", "#696969", "A dark cave.", 10, "#808080", "c"),
    CellType("mountain", "#A0522D", "A rugged mountain.", 10, "#8B4513", "m"),
    CellType("water", "#4682B4", "A body of water.", 5, "#5F9EA0", "w"),
    CellType("desert", "#F0E68C", "A vast desert.", 5, "#C2B280", "d"),
    CellType("swamp", "#8FBC8F", "A murky swamp.", 5, "#6B8E23", "s"),
    CellType("volcano", "#FF7F50", "An active volcano.", 5, "#CD5C5C", "v"),
    CellType("meadow", "#F5DEB3", "A beautiful meadow.", 5, "#D2B48C", "m")
]

def choose_cell_type():
    total_weight = sum(cell_type.weight for cell_type in cell_types)
    rand_value = random.randint(1, total_weight)
    for cell_type in cell_types:
        if rand_value <= cell_type.weight:
            return cell_type
        rand_value -= cell_type.weight

def generate_random_map():
    demo_map = {
        "name": "DemoMap",
        "width": 10,
        "height": 10,
        "start": [0, 0],
        "cells": []
    }

    cell_id_counter = 1
    for y in range(10):
        for x in range(10):
            cell_type = choose_cell_type()
            cell = {
                "id": f"RoomID{cell_id_counter}",
                "x": x,
                "y": y,
                "type": cell_type.name,
                "name": cell_type.name.capitalize(),
                "description": cell_type.description,
                "cellText": cell_type.cell_text,
                "cellColor": cell_type.color,
                "textColor": "#ffffff",
                "nodeShape": "circle",
                "nodeColor": cell_type.node_color,
                "pathColor": "#000000",
                "n": "",
                "e": "",
                "s": "",
                "w": "",
                "ne": "",
                "nw": "",
                "se": "",
                "sw": ""
            }
            demo_map['cells'].append(cell)
            cell_id_counter += 1

    game_map = GameMap(
        name=demo_map['name'],
        height=demo_map['height'],
        width=demo_map['width'],
        start=demo_map['start'],
        cells=[Cell(**cell_data) for cell_data in demo_map['cells']]
    )

    return game_map