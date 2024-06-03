import tkinter as tk
from tkinter import ttk
import uiTools
from config import game

def initialize_ui():
    game['ui'] = {}
    game['ui']['root'] = tk.Tk()

    def initialize_canvas_settings():
        game['ui']['canvas'] = {}
        game['ui']['canvas']['cell_size'] = 64
        game['ui']['canvas']['selected_cell'] = None
        game['ui']['selectedTool'] = tk.StringVar(value="Select")
        game['ui']['selected_paint_color'] = "#000000"
        game['ui']['selected_node_color'] = "#000000"
        game['ui']['selected_text_color'] = "#000000"
        game['ui']['selected_path_color'] = "#000000"
        game['ui']['selected_shape'] = tk.StringVar(value="Circle")

    def apply_styles():
        game['ui']['style'] = ttk.Style()
        game['ui']['style'].theme_use('clam')
        game['ui']['style'].configure('TButton', background='#4d4d4d', foreground='white', borderwidth=1)
        game['ui']['style'].map('TButton', background=[('active', '#666666')])
        game['ui']['root'].configure(bg='#1e1e1e')

        game['ui']['style'].configure('TRadioButton.TButton', background='#4d4d4d', foreground='white', borderwidth=1)
        game['ui']['style'].map('TRadioButton.TButton', background=[('selected', '#444444'), ('active', '#666666')])

    def create_tool_panel():
        game['ui']['tool_panel'] = tk.Frame(game['ui']['root'], bg='#2b2b2b', padx=10, pady=10)
        game['ui']['tool_panel'].grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)
        game['ui']['tool_panel'].grid_rowconfigure(0, weight=1)
        game['ui']['tool_panel'].grid_rowconfigure(1, weight=1)
        game['ui']['tool_panel'].grid_rowconfigure(2, weight=1)
        game['ui']['tool_panel'].grid_columnconfigure(0, weight=1)
        create_menu_section()
        create_radio_button_section()
        create_tool_space_section()

    def create_menu_section():
        game['ui']['menu_section'] = tk.Frame(game['ui']['tool_panel'], bg='#2b2b2b')
        game['ui']['menu_section'].grid(row=0, column=0, sticky='nsew')
        game['ui']['menu_button'] = ttk.Button(game['ui']['menu_section'], text="Menu", command=uiTools.open_menu)
        game['ui']['menu_button'].pack(pady=10, padx=10)

    def create_radio_button_section():
        game['ui']['radio_section'] = tk.Frame(game['ui']['tool_panel'], bg='#2b2b2b')
        game['ui']['radio_section'].grid(row=1, column=0, sticky='nsew')
        game['ui']['radio_buttons'] = [
            ttk.Button(game['ui']['radio_section'], text="Select", style='TRadioButton.TButton', command=lambda: uiTools.update_button_selection("Select")),
            ttk.Button(game['ui']['radio_section'], text="Paint", style='TRadioButton.TButton', command=lambda: uiTools.update_button_selection("Paint")),
            ttk.Button(game['ui']['radio_section'], text="Place Node", style='TRadioButton.TButton', command=lambda: uiTools.update_button_selection("Place Node")),
            ttk.Button(game['ui']['radio_section'], text="Place Text", style='TRadioButton.TButton', command=lambda: uiTools.update_button_selection("Place Text")),
            ttk.Button(game['ui']['radio_section'], text="Place Path", style='TRadioButton.TButton', command=lambda: uiTools.update_button_selection("Place Path")),
            ttk.Button(game['ui']['radio_section'], text="Clear Path", style='TRadioButton.TButton', command=lambda: uiTools.update_button_selection("Clear Path")),
            ttk.Button(game['ui']['radio_section'], text="Delete", style='TRadioButton.TButton', command=lambda: uiTools.update_button_selection("Delete"))
        ]
        for btn in game['ui']['radio_buttons']:
            btn.pack(anchor='w')

    def create_tool_space_section():
        game['ui']['tool_space'] = tk.Frame(game['ui']['tool_panel'], bg='#2b2b2b')
        game['ui']['tool_space'].grid(row=2, column=0, sticky='nsew')
        game['ui']['paint_tool'] = {}
        game['ui']['select_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
        tk.Label(game['ui']['select_tool_space'], text="Select a cell to see its properties", bg='#2b2b2b', fg='white').pack()
        game['ui']['select_tool_space'].pack_forget()

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

        game['ui']['paint_tool']['color_button'] = ttk.Button(game['ui']['paint_tool_space'], text="Choose Color", command=lambda: uiTools.choose_color('paint'))
        game['ui']['paint_tool']['color_button'].pack()
        game['ui']['paint_tool_space'].pack_forget()

        game['ui']['place_node_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
        tk.Label(game['ui']['place_node_tool_space'], text="Choose Node Shape", bg='#2b2b2b', fg='white').pack()

        game['ui']['shape_choice_button'] = tk.Button(game['ui']['place_node_tool_space'], textvariable=game['ui']['selected_shape'], width=20)
        game['ui']['shape_choice_button'].pack()

        game['ui']['shape_choice_menu'] = tk.Menu(game['ui']['shape_choice_button'], tearoff=0)
        shapes = ["Circle", "Square", "Triangle", "Hexagon", "Star"]
        for shape in shapes:
            game['ui']['shape_choice_menu'].add_command(label=shape, command=lambda shp=shape: game['ui']['selected_shape'].set(shp))
        game['ui']['shape_choice_button'].bind("<Button-1>", lambda event: game['ui']['shape_choice_menu'].post(event.x_root, event.y_root))

        game['ui']['node_color_button'] = ttk.Button(game['ui']['place_node_tool_space'], text="Choose Node Color", command=lambda: uiTools.choose_color('node'))
        game['ui']['node_color_button'].pack()
        game['ui']['place_node_tool_space'].pack_forget()

        game['ui']['place_text_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
        tk.Label(game['ui']['place_text_tool_space'], text="Enter Text", bg='#2b2b2b', fg='white').pack()
        game['ui']['text_entry'] = tk.Entry(game['ui']['place_text_tool_space'], bg='#1e1e1e', fg='white', insertbackground='white')
        game['ui']['text_entry'].pack()
        game['ui']['text_color_button'] = ttk.Button(game['ui']['place_text_tool_space'], text="Choose Text Color", command=lambda: uiTools.choose_color('text'))
        game['ui']['text_color_button'].pack()
        game['ui']['place_text_tool_space'].pack_forget()

        game['ui']['place_path_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
        tk.Label(game['ui']['place_path_tool_space'], text="Click and drag to connect cells", bg='#2b2b2b', fg='white').pack()
        game['ui']['place_path_tool_space'].pack_forget()

        game['ui']['clear_path_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
        tk.Label(game['ui']['clear_path_tool_space'], text="Drag to delete paths", bg='#2b2b2b', fg='white').pack()
        game['ui']['clear_path_tool_space'].pack_forget()

        game['ui']['delete_tool_space'] = tk.Frame(game['ui']['tool_space'], bg='#2b2b2b')
        tk.Label(game['ui']['delete_tool_space'], text="Click and drag to delete cells", bg='#2b2b2b', fg='white').pack()
        game['ui']['delete_tool_space'].pack_forget()
    

    def create_canvas_tool_container():
        game['ui']['canvas_tool_container'] = tk.Frame(game['ui']['root'], bg='#2b2b2b', padx=10, pady=10)
        game['ui']['canvas_tool_container'].grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        game['ui']['zoom_in_button'] = ttk.Button(game['ui']['canvas_tool_container'], text="+", width=2, command=lambda: uiTools.zoom("in"))
        game['ui']['zoom_in_button'].pack(side='left', padx=5, pady=5)
        game['ui']['zoom_out_button'] = ttk.Button(game['ui']['canvas_tool_container'], text="-", width=2, command=lambda: uiTools.zoom("out"))
        game['ui']['zoom_out_button'].pack(side='left', padx=5, pady=5)
        game['ui']['coord_label'] = tk.Label(game['ui']['canvas_tool_container'], text="X: 0, Y: 0", bg='#2b2b2b', fg='#ffffff', width=10)
        game['ui']['coord_label'].pack(side='left', padx=10)
        game['ui']['goto_button'] = ttk.Button(game['ui']['canvas_tool_container'], text="Go to 0,0", command=uiTools.goto_origin)
        game['ui']['goto_button'].pack(side='left', padx=5, pady=5)

    def create_canvas_panel():
        game['ui']['canvas_panel'] = tk.Frame(game['ui']['root'], bg='#2b2b2b', padx=10, pady=10)
        game['ui']['canvas_panel'].grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        game['ui']['canvas']['widget'] = tk.Canvas(game['ui']['canvas_panel'], width=400, height=400, bg="#2b2b2b")
        game['ui']['canvas']['widget'].pack(expand=True)

    def create_cell_panel():
        game['ui']['cell_panel'] = tk.Frame(game['ui']['root'], bg='#2b2b2b', padx=10, pady=10)
        game['ui']['cell_panel'].grid(row=0, column=2, rowspan=2, sticky='nsew', padx=5, pady=5)
        create_cell_properties(game['ui']['cell_panel'])

    def configure_grid():
        game['ui']['root'].grid_columnconfigure(0, weight=1)
        game['ui']['root'].grid_columnconfigure(1, weight=2)
        game['ui']['root'].grid_columnconfigure(2, weight=1)
        game['ui']['root'].grid_rowconfigure(0, weight=0)
        game['ui']['root'].grid_rowconfigure(1, weight=1)

    def create_cell_properties(parent):
        properties = [
            'x', 'y', 'id', 'type', 'name', 'description', 'cellText', 
            'cellColor', 'textColor', 'nodeShape', 'nodeColor', 
            'pathColor', 'n', 'e', 's', 'w', 
            'ne', 'nw', 'se', 'sw'
        ]
        game['ui']['property_entries'] = {}
        for i, prop in enumerate(properties):
            tk.Label(parent, text=prop, bg='#2b2b2b', fg='#ffffff').grid(row=i, column=0, sticky='w', padx=5, pady=5)
            game['ui']['property_entries'][prop] = tk.Entry(parent, bg='#1e1e1e', fg='#ffffff', insertbackground='#ffffff')
            game['ui']['property_entries'][prop].grid(row=i, column=1, sticky='ew', padx=5, pady=5)
        game['ui']['save_button'] = ttk.Button(parent, text="Save", command=uiTools.save_cell_properties)
        game['ui']['save_button'].grid(row=len(properties), column=0, columnspan=2, pady=10)

    initialize_canvas_settings()
    apply_styles()
    create_tool_panel()
    create_canvas_tool_container()
    create_canvas_panel()
    create_cell_panel()
    configure_grid()

    # Bind keys
    game['ui']['canvas']['widget'].bind('<Button-1>', uiTools.handle_canvas_click)
    game['ui']['canvas']['widget'].bind('<Motion>', uiTools.update_coordinates)
    game['ui']['canvas']['widget'].bind('<B1-Motion>', uiTools.handle_canvas_drag)
    game['ui']['canvas']['widget'].bind('<ButtonRelease-1>', lambda event: uiTools.reset_drag_state())
    game['ui']['canvas']['widget'].bind('<Up>', lambda event: uiTools.move_map('up'))
    game['ui']['canvas']['widget'].bind('<Down>', lambda event: uiTools.move_map('down'))
    game['ui']['canvas']['widget'].bind('<Left>', lambda event: uiTools.move_map('left'))
    game['ui']['canvas']['widget'].bind('<Right>', lambda event: uiTools.move_map('right'))

    game['ui']['root'].bind('<Up>', lambda event: uiTools.move_map('up'))
    game['ui']['root'].bind('<Down>', lambda event: uiTools.move_map('down'))
    game['ui']['root'].bind('<Left>', lambda event: uiTools.move_map('left'))
    game['ui']['root'].bind('<Right>', lambda event: uiTools.move_map('right'))