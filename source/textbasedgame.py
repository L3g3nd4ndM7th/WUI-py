import tkinter as tk
import json

# Load JSON Data
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Define empty classes
class Game:
    pass

class UI:
    pass

class Player:
    pass

# Initialize instances
game = Game()
game.ui = UI()
game.player = Player()

# Assign properties to the game object
game.mode = 'normal'
game.creatures = load_json_data('creatures.json')
game.gameMaps = load_json_data('maps.json')
game.dialogues = load_json_data('dialogues.json')
game.npcs = load_json_data('npcs.json')
game.cursorSelected = None

# Assign properties to the player object
game.player.currentRoom = 'arthelmTown'
game.player.hp = 100
game.player.attack = 10

# Functions
def send_message(*texts):
    game.ui.textScroller.config(state=tk.NORMAL)
    for text in texts:
        game.ui.textScroller.insert(tk.END, text + "\n")
    game.ui.textScroller.insert(tk.END, "-"*75 + "\n")
    game.ui.textScroller.config(state=tk.DISABLED)
    game.ui.textScroller.see(tk.END)

def move(direction):
    currentRoom = game.player.currentRoom
    if game.gameMaps['arthelm']['rooms'][currentRoom][direction]:
        game.player.currentRoom = game.gameMaps['arthelm']['rooms'][currentRoom][direction]['room']
    else:
        send_message(f"There is no path to the {direction}.")
        return
    
    newRoom = game.player.currentRoom
    game.ui.nodeNameLabel.config(text=game.gameMaps['arthelm']['rooms'][newRoom]['name'])
    
    # First message: Room name and description
    send_message(
        f"You have moved to {game.gameMaps['arthelm']['rooms'][newRoom]['name']}",
        game.gameMaps['arthelm']['rooms'][newRoom]['description']
    )
    
    # Second message: Directions
    currentRoom = game.player.currentRoom
    directions = {
        'n': 'north', 'ne': 'northeast', 'e': 'east', 'se': 'southeast', 
        's': 'south', 'sw': 'southwest', 'w': 'west', 'nw': 'northwest'
    }
    messages = []
    for dirKey, dirName in directions.items():
        if game.gameMaps['arthelm']['rooms'][currentRoom][dirKey]:
            place = game.gameMaps['arthelm']['rooms'][currentRoom][dirKey]['room']
            messages.append(f"{dirName}: {game.gameMaps['arthelm']['rooms'][place]['name']}")
    
    send_message(*messages)
    
    draw_minimap()
    update_npc_list()

def calculate_room_positions():
    startPos = (0, 0)
    roomPositions = {game.player.currentRoom: startPos}
    queue = [(game.player.currentRoom, startPos)]
    directions = {
        'n': 'north', 'ne': 'northeast', 'e': 'east', 'se': 'southeast', 
        's': 'south', 'sw': 'southwest', 'w': 'west', 'nw': 'northwest'
    }

    while queue:
        currentRoom, pos = queue.pop(0)
        for dirKey in directions.keys():
            if game.gameMaps['arthelm']['rooms'][currentRoom][dirKey]:
                nextRoom = game.gameMaps['arthelm']['rooms'][currentRoom][dirKey]['room']
                nextPos = get_room_position(pos, dirKey, game.gameMaps['arthelm']['rooms'][currentRoom][dirKey]['distance'])
                if nextRoom not in roomPositions:
                    roomPositions[nextRoom] = nextPos
                    queue.append((nextRoom, nextPos))

    return roomPositions

def get_room_position(startPos, direction, distance):
    x, y = startPos
    unit = 40  # Increased distance unit in pixels
    if direction == 'n':
        y -= distance * unit
    elif direction == 'ne':
        x += distance * unit
        y -= distance * unit
    elif direction == 'e':
        x += distance * unit
    elif direction == 'se':
        x += distance * unit
        y += distance * unit
    elif direction == 's':
        y += distance * unit
    elif direction == 'sw':
        x -= distance * unit
        y += distance * unit
    elif direction == 'w':
        x -= distance * unit
    elif direction == 'nw':
        x -= distance * unit
        y -= distance * unit
    return (x, y)

def draw_minimap():
    canvasWidth = int(game.ui.minimap.cget('width'))
    canvasHeight = int(game.ui.minimap.cget('height'))
    centerX = canvasWidth // 2
    centerY = canvasHeight // 2
    
    game.ui.minimap.delete("all")
    game.ui.minimap.configure(bg=game.gameMaps['arthelm']['backgroundColor'])
    roomPositions = calculate_room_positions()

    # Adjust positions to center the player at the center of the canvas
    playerPos = roomPositions[game.player.currentRoom]
    offsetX = centerX - playerPos[0]
    offsetY = centerY - playerPos[1]
    for room in roomPositions:
        x, y = roomPositions[room]
        roomPositions[room] = (x + offsetX, y + offsetY)

    # Draw path lines
    for room, pos in roomPositions.items():
        x, y = pos
        for direction, info in game.gameMaps['arthelm']['rooms'][room].items():
            if info and 'room' in info:
                targetRoom = info['room']
                if targetRoom in roomPositions:
                    targetPos = roomPositions[targetRoom]
                    game.ui.minimap.create_line(x, y, targetPos[0], targetPos[1], fill='white', width=2)

    # Draw rooms (nodes)
    for room, pos in roomPositions.items():
        x, y = pos
        nodeColor = game.gameMaps['arthelm']['rooms'][room].get('nodeColor', 'gray')  # Default color is gray if nodeColor is not specified
        if room == game.player.currentRoom:
            color = 'blue'
        else:
            color = nodeColor
        game.ui.minimap.create_oval(x-10, y-10, x+10, y+10, fill=color)  # Increased node size

    # Draw text (room names) only for the current room
    currentRoomPos = roomPositions[game.player.currentRoom]
    game.ui.minimap.create_text(currentRoomPos[0], currentRoomPos[1]-20, text=game.gameMaps['arthelm']['rooms'][game.player.currentRoom]['name'], fill='white', font=('Helvetica', 12))  # Increased text size

def draw_ui():
    for frame in [game.ui.normalUI, game.ui.combatUI, game.ui.dialogueUI]:
        frame.pack_forget()
    
    if game.mode == 'normal':
        game.ui.normalUI.pack(fill=tk.BOTH, expand=True)
    elif game.mode == 'combat':
        game.ui.combatUI.pack(fill=tk.BOTH, expand=True)
    elif game.mode == 'dialogue':
        game.ui.dialogueUI.pack(fill=tk.BOTH, expand=True)

def update_npc_list():
    currentRoom = game.player.currentRoom
    npc_list = [npc['name'] for npc in game.npcs.values() if npc['currentRoom'] == currentRoom]
    game.ui.npcListbox.delete(0, tk.END)
    for npc in npc_list:
        game.ui.npcListbox.insert(tk.END, npc)

def on_npc_select(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        npc_name = event.widget.get(index)
        for npc in game.npcs.values():
            if npc['name'] == npc_name:
                game.cursorSelected = npc
                break

def talk_to_npc():
    if game.cursorSelected:
        npc = game.cursorSelected
        dialogue_id = npc['dialogue']
        start_dialogue(dialogue_id)

def start_dialogue(dialogue_id):
    game.mode = 'dialogue'
    draw_ui()

    game.ui.dialogueTextScroller.config(state=tk.NORMAL)
    game.ui.dialogueTextScroller.delete('1.0', tk.END)
    game.ui.dialogueTextScroller.insert(tk.END, game.dialogues[dialogue_id]['start']['text'] + "\n")
    game.ui.dialogueTextScroller.config(state=tk.DISABLED)
    
    # Clear previous response buttons
    for widget in game.ui.dialogueResponseFrame.winfo_children():
        widget.destroy()
    
    for response_text, next_dialogue in game.dialogues[dialogue_id]['start']['responses'].items():
        btn = tk.Button(game.ui.dialogueResponseFrame, text=response_text, command=lambda d=next_dialogue: continue_dialogue(dialogue_id, d))
        btn.pack(fill=tk.X)

    game.ui.dialogueResponseFrame.pack(fill=tk.BOTH, expand=True)

def continue_dialogue(dialogue_id, next_dialogue):
    if next_dialogue == 'end':
        game.mode = 'normal'
        draw_ui()  # Draw the UI for normal mode
    else:
        game.ui.dialogueTextScroller.config(state=tk.NORMAL)
        game.ui.dialogueTextScroller.delete('1.0', tk.END)
        game.ui.dialogueTextScroller.insert(tk.END, game.dialogues[dialogue_id][next_dialogue]['text'] + "\n")
        game.ui.dialogueTextScroller.config(state=tk.DISABLED)
        
        # Clear previous response buttons
        for widget in game.ui.dialogueResponseFrame.winfo_children():
            widget.destroy()
        
        for response_text, next_dialogue in game.dialogues[dialogue_id][next_dialogue]['responses'].items():
            btn = tk.Button(game.ui.dialogueResponseFrame, text=response_text, command=lambda d=next_dialogue: continue_dialogue(dialogue_id, d))
            btn.pack(fill=tk.X)

# UI Widgets Setup
# Initialize UI components
game.ui.root = tk.Tk()

# Configure the dark theme
game.ui.root.configure(bg='#333333')

# Create frames for different modes
game.ui.normalUI = tk.Frame(game.ui.root, bg='#333333')
game.ui.combatUI = tk.Frame(game.ui.root, bg='#333333')
game.ui.dialogueUI = tk.Frame(game.ui.root, bg='#333333')

# Normal UI setup
game.ui.mainFrame = tk.Frame(game.ui.normalUI, bg='#333333')
game.ui.mainFrame.pack(fill=tk.BOTH, expand=True)

# Create three column panels
game.ui.leftColumn = tk.Frame(game.ui.mainFrame, bg='#333333')
game.ui.leftColumn.pack(side=tk.LEFT)

game.ui.middleColumn = tk.Frame(game.ui.mainFrame, bg='#333333')
game.ui.middleColumn.pack(side=tk.LEFT)

game.ui.rightColumn = tk.Frame(game.ui.mainFrame, bg='#333333')
game.ui.rightColumn.pack(side=tk.LEFT)

# Create the minimap in the first panel
game.ui.minimapFrame = tk.Frame(game.ui.leftColumn, bg='#333333')
game.ui.minimapFrame.pack()
game.ui.minimap = tk.Canvas(game.ui.minimapFrame, bg='#222222', width=200, height=200, highlightbackground="light grey", highlightthickness=2)
game.ui.minimap.pack()

# Create a label for the room name and pack it at the top of the middle column
game.ui.nodeNameLabel = tk.Label(game.ui.middleColumn, text=game.gameMaps['arthelm']['rooms'][game.player.currentRoom]['name'], bg='#666666', fg='#FFFFFF', font=('Helvetica', 24))
game.ui.nodeNameLabel.pack(fill=tk.X, padx=5, pady=5)

# Create a text scroller in the middle column
game.ui.eventTextScrollerFrame = tk.Frame(game.ui.middleColumn, bg='#444444')
game.ui.eventTextScrollerFrame.pack()
game.ui.textScroller = tk.Text(game.ui.eventTextScrollerFrame, bg='#222222', fg='#FFFFFF', wrap=tk.WORD, state=tk.DISABLED, width=75, height=25)
game.ui.scrollbar = tk.Scrollbar(game.ui.eventTextScrollerFrame, command=game.ui.textScroller.yview, bg='#444444')
game.ui.textScroller.config(yscrollcommand=game.ui.scrollbar.set)

# Pack the text scroller and scrollbar
game.ui.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
game.ui.textScroller.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a frame for the directional buttons and use grid
game.ui.buttonFrame = tk.Frame(game.ui.middleColumn, bg='#333333')
game.ui.buttonFrame.pack(side=tk.LEFT)

# Create directional buttons with a dark theme
button_style = {
    'bg': '#666666', 'fg': '#FFFFFF',
    'activebackground': '#777777', 'activeforeground': '#FFFFFF',
    'relief': tk.FLAT, 'width': 4
}

game.ui.nwButton = tk.Button(game.ui.buttonFrame, text='nw', **button_style, command=lambda: move('nw'))
game.ui.nButton = tk.Button(game.ui.buttonFrame, text='n', **button_style, command=lambda: move('n'))
game.ui.neButton = tk.Button(game.ui.buttonFrame, text='ne', **button_style, command=lambda: move('ne'))
game.ui.wButton = tk.Button(game.ui.buttonFrame, text='w', **button_style, command=lambda: move('w'))
game.ui.eButton = tk.Button(game.ui.buttonFrame, text='e', **button_style, command=lambda: move('e'))
game.ui.swButton = tk.Button(game.ui.buttonFrame, text='sw', **button_style, command=lambda: move('sw'))
game.ui.sButton = tk.Button(game.ui.buttonFrame, text='s', **button_style, command=lambda: move('s'))
game.ui.seButton = tk.Button(game.ui.buttonFrame, text='se', **button_style, command=lambda: move('se'))

# Position the directional buttons in a grid within the button frame
game.ui.nwButton.grid(row=0, column=0)
game.ui.nButton.grid(row=0, column=1)
game.ui.neButton.grid(row=0, column=2)
game.ui.wButton.grid(row=1, column=0)
game.ui.eButton.grid(row=1, column=2)
game.ui.swButton.grid(row=2, column=0)
game.ui.sButton.grid(row=2, column=1)
game.ui.seButton.grid(row=2, column=2)

# Create a frame for the action buttons next to the directional buttons
game.ui.actionButtonFrame = tk.Frame(game.ui.middleColumn, bg='#333333')
game.ui.actionButtonFrame.pack(side=tk.LEFT, padx=10)

# Create action buttons with a dark theme
game.ui.lookButton = tk.Button(game.ui.actionButtonFrame, text='Look', **button_style)
game.ui.exploreButton = tk.Button(game.ui.actionButtonFrame, text='Explore', **button_style)
game.ui.useButton = tk.Button(game.ui.actionButtonFrame, text='Use', **button_style)
game.ui.talkButton = tk.Button(game.ui.actionButtonFrame, text='Talk', **button_style, command=talk_to_npc)
game.ui.itemButton = tk.Button(game.ui.actionButtonFrame, text='Item', **button_style)
game.ui.attackButton = tk.Button(game.ui.actionButtonFrame, text='Attack', **button_style)
game.ui.campButton = tk.Button(game.ui.actionButtonFrame, text='Camp', **button_style)

# Position the action buttons in a grid within the action button frame
game.ui.lookButton.grid(row=0, column=0)
game.ui.exploreButton.grid(row=0, column=1)
game.ui.useButton.grid(row=0, column=2)
game.ui.talkButton.grid(row=1, column=0)
game.ui.itemButton.grid(row=1, column=1)
game.ui.attackButton.grid(row=1, column=2)
game.ui.campButton.grid(row=2, column=1)

# Add NPC listbox to the third panel (rightColumn)
game.ui.npcListbox = tk.Listbox(game.ui.rightColumn, bg='#222222', fg='#FFFFFF', selectbackground='#666666')
game.ui.npcListbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
game.ui.npcListbox.bind('<<ListboxSelect>>', on_npc_select)

# Combat UI setup
game.ui.combatFrame = tk.Frame(game.ui.combatUI, bg='#333333')
game.ui.combatFrame.pack(fill=tk.BOTH, expand=True)

game.ui.combatTopRow = tk.Frame(game.ui.combatFrame, bg='#333333')
game.ui.combatTopRow.pack()

game.ui.combatLeftColumn = tk.Frame(game.ui.combatTopRow, bg='#333333')
game.ui.combatLeftColumn.pack(side=tk.LEFT)

game.ui.combatRightColumn = tk.Frame(game.ui.combatTopRow, bg='#333333')
game.ui.combatRightColumn.pack(side=tk.LEFT)

game.ui.combatButtonsGrid = tk.Frame(game.ui.combatFrame, bg='#333333')
game.ui.combatButtonsGrid.pack()

# Dialogue UI setup
game.ui.dialogueFrame = tk.Frame(game.ui.dialogueUI, bg='#333333')
game.ui.dialogueFrame.pack(fill=tk.BOTH, expand=True)

game.ui.dialogueTextScroller = tk.Text(game.ui.dialogueFrame, bg='#222222', fg='#FFFFFF', wrap=tk.WORD, state=tk.DISABLED, height=15)
game.ui.dialogueTextScroller.pack(fill=tk.BOTH, expand=True)

game.ui.dialogueResponseFrame = tk.Frame(game.ui.dialogueFrame, bg='#444444')
game.ui.dialogueResponseFrame.pack(fill=tk.BOTH, expand=True)

# Bind arrow keys to movement
game.ui.root.bind('<Left>', lambda event: move('w'))
game.ui.root.bind('<Right>', lambda event: move('e'))
game.ui.root.bind('<Up>', lambda event: move('n'))
game.ui.root.bind('<Down>', lambda event: move('s'))

# Start Game
# Example usage: Adding text to the event text scroller
send_message("Welcome to the game!")
send_message(
    game.gameMaps['arthelm']['rooms'][game.player.currentRoom]['name'],
    game.gameMaps['arthelm']['rooms'][game.player.currentRoom]['description']
)

currentRoom = game.player.currentRoom
directions = {
    'n': 'north', 'ne': 'northeast', 'e': 'east', 'se': 'southeast', 
    's': 'south', 'sw': 'southwest', 'w': 'west', 'nw': 'northwest'
}
messages = []
for dirKey, dirName in directions.items():
    if game.gameMaps['arthelm']['rooms'][currentRoom][dirKey]:
        place = game.gameMaps['arthelm']['rooms'][currentRoom][dirKey]['room']
        messages.append(f"{dirName}: {game.gameMaps['arthelm']['rooms'][place]['name']}")

send_message(*messages)
draw_minimap()
update_npc_list()

# Draw initial UI
draw_ui()

# Run the game UI
game.ui.root.mainloop()