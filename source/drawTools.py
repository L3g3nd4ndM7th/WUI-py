from config import game

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
    else:
        print(f"Unknown shape: {shape}")

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