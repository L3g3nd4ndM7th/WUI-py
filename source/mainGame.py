import drawTools
from ui import initialize_ui
from config import game
from randomMap import generate_random_map

initialize_ui()
game['currentMap'] = generate_random_map()
drawTools.drawMap(game['currentMap'])
game['ui']['root'].mainloop()
