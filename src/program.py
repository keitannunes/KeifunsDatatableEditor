"""
DANGER: No one should ever attempt to maintain this codebase
"""

import tkinter as tk
import os
import sys
from src import datatable as dt
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from typing import List
from src import config, parse_tja, fumen, common
from src import updater as ud
import traceback
import shutil
import webbrowser



GENRE_MAPPING = {
    "0. POP": 0,
    "1. Anime": 1,
    "2. Kids": 2,
    "3. VOCALOID™ Music": 3,
    "4. Game Music": 4,
    "5. NAMCO Original": 5,
    "6. Variety": 6,
    "7. Classic": 7,
}

class Program:
    window: tk.Tk
    frame: tk.Frame

    menu_bar: tk.Menu
    file_menu: tk.Menu
    help_menu: tk.Menu

    #Frames
    song_details_frame: tk.LabelFrame
    language_frame: tk.Frame
    difficulty_info_label_frame: tk.LabelFrame
    difficulty_info_frame: tk.Frame
    difficulty_info_sub_frames: List[tk.LabelFrame]

    #Labels
    songid_label: tk.Label
    song_name_label: tk.Label
    song_sub_label: tk.Label
    song_detail_label: tk.Label
    unique_id_label: tk.Label
    genre_label: tk.Label
    song_filename_label: tk.Label
    spike_on_labels: List[tk.Label]
    star_labels: List[tk.Label]
    shinuchi_labels: List[tk.Label]
    shinuchi_score_labels: List[tk.Label]
    onpu_num_labels: List[tk.Label]
    renda_time_labels: List[tk.Label]
    fuusen_total_labels: List[tk.Label]
    ai_sections_labels: List[tk.Label]


    #Entries
    songid_entry: tk.Entry
    song_name_entry: tk.Entry
    song_sub_entry: tk.Entry
    song_detail_entry: tk.Entry
    song_filename_entry: tk.Entry
    renda_time_entries: List[tk.Entry]
    renda_time_values: List[tk.StringVar]
    song_name_var: tk.StringVar
    song_sub_var: tk.StringVar
    song_detail_var: tk.StringVar
    song_filename_var: tk.StringVar
    new_var: tk.BooleanVar
    papamama_var: tk.BooleanVar
    unique_id_var: tk.IntVar
    genre_var: tk.StringVar
    dancer_var: tk.StringVar

    #Combobox
    genre_combobox: ttk.Combobox
    #ai_sections_comboboxes: List[ttk.Combobox]

    #Spinbox
    unique_id_spinbox: tk.Spinbox
    star_spinboxes: List[tk.Spinbox]
    star_values: List[tk.IntVar]
    shinuchi_spinboxes: List[tk.Spinbox]
    shinuchi_values: List[tk.IntVar]
    shinuchi_score_spinboxes: List[tk.Spinbox]
    shinuchi_score_values: List[tk.IntVar]
    onpu_num_spinboxes: List[tk.Spinbox]
    onpu_num_values: List[tk.IntVar]
    fuusen_total_spinboxes: List[tk.Spinbox]
    fuusen_total_values: List[tk.IntVar]

    #Checkbutton
    decouple_duet_checkbutton: tk.Checkbutton
    decouple_duet_var: tk.BooleanVar
    new_checkbutton: tk.Checkbutton
    papamama_checkbutton: tk.Checkbutton
    branch_spike_frames: List[tk.Frame]
    branch_checkbuttons: List[tk.Checkbutton]
    branch_values: List[tk.BooleanVar]
    spike_on_spinboxes: List[tk.Spinbox]
    spike_on_values: List[tk.IntVar]
    ai_hard_checkbuttons: List[tk.Checkbutton]
    ai_hard_values: List[tk.BooleanVar] 

    #Button
    music_order_button: tk.Button

    #Radio Buttons
    language_value: tk.IntVar
    language_radiobuttons: List[tk.Radiobutton]
    ai_sections_frames: List[tk.Frame]
    ai_sections_radiobuttons: List[List[tk.Radiobutton]]
    ai_sections_values: List[tk.IntVar]

    ### Music Order

    music_order_window: tk.Toplevel
    music_order_genre_order_labels: List[tk.Label]
    music_order_genre_frame: List[tk.Frame]
    music_order_genre_display_checkbuttons: List[tk.Checkbutton]
    music_order_genre_display_var:  List[tk.BooleanVar]
    music_order_genre_order_spinboxes: List[tk.Spinbox]
    music_order_genre_order_var: List[tk.IntVar]
    music_order_submit_button: tk.Button

    ### New Song

    new_song_window: tk.Toplevel
    new_song_id_label: tk.Label
    new_song_id_entry: tk.Entry
    new_song_confirm: tk.Button

    #Other Variables
    current_songid: str
    previous_language: int
    datatable: dt.Datatable
    song_info: dt.Song
    initial: bool #I'm genuinely convinced this variable is never used, scared and lazy to check
    duet_change_ignore_flag: bool #I absolutely fucking hate this variable; Theres definitely a better solution that my retarded ass cannot think of

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Keifun's Datatable Editor")
        self.window.resizable(False, False)
        #self.window.geometry("1280x720")  # Set window size to 720p

        img = Image.open(common.resource_path("src/assets/icon.png"))  # Replace with the path to your .png file
        icon = ImageTk.PhotoImage(img)

        # Set the window icon
        self.window.wm_iconphoto(True, icon) # type: ignore

        self.menu_bar = tk.Menu(self.window, tearoff=0)

        #File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Datatable", accelerator="Ctrl+O", command=self.open_datatable)
        self.file_menu.add_command(label="Save Datatable", accelerator="Ctrl+S", command=self.save_datatable)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="New Song", accelerator="Ctrl+N", command=self.on_new_song) 
        self.file_menu.add_command(label="New Song From TJA", accelerator="Ctrl+Shift+N", command=self.on_new_song_tja) 
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Configure Keys", accelerator="Ctrl+,", command=self.create_config_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.window.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        #Utilities Menu

        self.util_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.util_menu.add_command(label="Add Ura to Chart", accelerator="Ctrl+U", command=self.on_add_ura)
        self.menu_bar.add_cascade(label="Utilities", menu=self.util_menu)

        #Help Menu
        
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.window.config(menu=self.menu_bar)

        #Bind keys

        self.window.bind("<Control-n>", self.on_new_song) #type: ignore
        self.window.bind("<Control-N>", self.on_new_song_tja) #type: ignore
        self.window.bind("<Control-o>", self.open_datatable) #type: ignore
        self.window.bind("<Control-s>", self.save_datatable) #type: ignore
        self.window.bind("<Control-,>", self.create_config_window) #type: ignore
        self.window.bind("<Control-u>", self.on_add_ura)  # type: ignore


        self.songid_label = tk.Label(self.window, text="Song Id:")
        self.songid_label.grid(row=0, column=0)

        self.songid_frame = tk.Frame(self.window)
        self.songid_frame.grid(row=1, column=0)

        self.songid_entry = tk.Entry(self.songid_frame)
        self.songid_entry.grid(row=0, column=0)

        self.songid_entry.bind("<Return>", self.on_songid)

        self.song_delete_button = tk.Button(self.songid_frame, text="Delete", command=self.delete_song)
        self.song_delete_button.grid(row=0, column=1)


        
        ### Song Details ###
        self.language_frame = tk.Frame(self.window, pady=5)

        self.language_radiobuttons = list()
        self.language_value = tk.IntVar()
        self.language_value.set(0)
        self.language_value.trace_add("write", self.on_language_change)

        for i, lang in enumerate(['JPN', 'ENG', 'zh-TW', 'KOR']):
            self.language_radiobuttons.append(tk.Radiobutton(self.language_frame, text=lang, variable=self.language_value, value=i))
            self.language_radiobuttons[i].grid(row=0, column=i)

        self.language_frame.grid(row=2, column=0)
        
        self.song_details_frame = tk.LabelFrame(self.window, text="Song Details", padx=20, pady=20)
        self.song_details_frame.grid(row=3, column=0)

        self.song_details_subframes = list()

        for i in range(4):
            self.song_details_subframes.append(tk.Frame(self.song_details_frame, padx=8))
            self.song_details_subframes[i].grid(row=0, column=i, sticky="nsew")

        # Make sure columns resize evenly by configuring column weights
        self.song_details_frame.grid_columnconfigure(0, weight=1)
        self.song_details_frame.grid_columnconfigure(1, weight=1)
        self.song_details_frame.grid_columnconfigure(2, weight=1)
        self.song_details_frame.grid_columnconfigure(3, weight=1)

        # Create variables for each widget
        self.song_name_var = tk.StringVar()
        self.song_name_font_var = tk.IntVar()
        self.song_sub_var = tk.StringVar()
        self.song_sub_font_var = tk.IntVar()
        self.song_detail_var = tk.StringVar()
        self.song_detail_font_var = tk.IntVar()
        self.song_filename_var = tk.StringVar()
        self.new_var = tk.BooleanVar()
        self.papamama_var = tk.BooleanVar()
        self.unique_id_var = tk.IntVar()
        self.double_play_var = tk.BooleanVar()
        self.genre_var = tk.StringVar()
        self.dancer_var = tk.StringVar()

        ## COL 1 - Anchored Left and Expanded
        self.font_label = tk.Label(self.song_details_subframes[0], text="Font")
        self.font_label.grid(row=0, column=1, sticky="w")
        # SONG NAME
        self.song_name_label = tk.Label(self.song_details_subframes[0], text="Song Name:", anchor="w", width=20)
        self.song_name_label.grid(row=0, column=0, sticky="w")

        self.song_name_entry = tk.Entry(self.song_details_subframes[0], textvariable=self.song_name_var)
        self.song_name_entry.grid(row=1, column=0, sticky="ew")
        self.song_name_font_spinbox = tk.Spinbox(self.song_details_subframes[0], from_=0, to=3, width=2, textvariable=self.song_name_font_var)
        self.song_name_font_spinbox.grid(row=1, column=1, sticky="w")

        # SONG SUB
        self.song_sub_label = tk.Label(self.song_details_subframes[0], text="Song Sub:", anchor="w", width=20)
        self.song_sub_label.grid(row=2, column=0, sticky="w")

        self.song_sub_entry = tk.Entry(self.song_details_subframes[0], textvariable=self.song_sub_var)
        self.song_sub_entry.grid(row=3, column=0, sticky="ew")
        self.song_sub_font_spinbox = tk.Spinbox(self.song_details_subframes[0], from_=0, to=3, width=2, textvariable=self.song_sub_font_var)
        self.song_sub_font_spinbox.grid(row=3, column=1, sticky="w")

        # SONG DETAIL
        self.song_detail_label = tk.Label(self.song_details_subframes[0], text="Song Detail:", anchor="w", width=20)
        self.song_detail_label.grid(row=4, column=0, sticky="w")

        self.song_detail_entry = tk.Entry(self.song_details_subframes[0], textvariable=self.song_detail_var)
        self.song_detail_entry.grid(row=5, column=0, sticky="ew")
        self.song_detail_font_spinbox = tk.Spinbox(self.song_details_subframes[0], from_=0, to=3, width=2, textvariable=self.song_detail_font_var)
        self.song_detail_font_spinbox.grid(row=5, column=1, sticky="w")

        ## COL 2 - Anchored Left and Expanded
        # Unique ID
        self.unique_id_label = tk.Label(self.song_details_subframes[1], text="Unique Id:", anchor="w", width=20)
        self.unique_id_label.grid(row=0, column=0, sticky="w")

        self.unique_id_spinbox = tk.Spinbox(self.song_details_subframes[1], from_=0, to=9999, textvariable=self.unique_id_var)
        self.unique_id_spinbox.grid(row=1, column=0, sticky="ew")

        # Main Genre
        self.genre_label = tk.Label(self.song_details_subframes[1], text="Main Genre:", anchor="w", width=20)
        self.genre_label.grid(row=2, column=0, sticky="w")

        self.genre_combobox = ttk.Combobox(self.song_details_subframes[1], values=list(GENRE_MAPPING.keys()), textvariable=self.genre_var)
        self.genre_combobox.grid(row=3, column=0, sticky="ew")

        # Song Filename
        self.song_filename_label = tk.Label(self.song_details_subframes[1], text="Song Filename:", anchor="w", width=20)
        self.song_filename_label.grid(row=4, column=0, sticky="w")

        self.song_filename_entry = tk.Entry(self.song_details_subframes[1], textvariable=self.song_filename_var)
        self.song_filename_entry.grid(row=5, column=0, sticky="ew")

        ## COL 3 - Anchored Left
        
        #Dancer
        self.dancer_label = tk.Label(self.song_details_subframes[2], text="Dancer:", anchor="w", width=20)
        self.dancer_label.grid(row=0, column=0, sticky="w")

        self.dancer_combobox = ttk.Combobox(self.song_details_subframes[2], values=["000_default"] + list(config.config.dancers.keys()), textvariable=self.dancer_var)
        self.dancer_combobox.grid(row=1, column=0, sticky="ew")

        #Placeholder label

        self.song_filename_label = tk.Label(self.song_details_subframes[2], text="", anchor="w", width=20)
        self.song_filename_label.grid(row=2, column=0, sticky="w")

        self.music_order_button = tk.Button(self.song_details_subframes[2], text="Set Music Order", command=self.open_musicorder_window)
        self.music_order_button.grid(row=3, column=0, sticky="ew")
        
        ## COL 4

        self.new_checkbutton = tk.Checkbutton(self.song_details_subframes[3], text="New", variable=self.new_var)
        self.new_checkbutton.grid(row=0, column=0, sticky="w")

        self.papamama_checkbutton = tk.Checkbutton(self.song_details_subframes[3], text="Papamama", variable=self.papamama_var)
        self.papamama_checkbutton.grid(row=1, column=0, sticky="w")

        self.double_play_checkbutton = tk.Checkbutton(self.song_details_subframes[3], text="Double Play", variable=self.double_play_var)
        self.double_play_checkbutton.grid(row=2, column=0, sticky="ew")

        # Make sure the subframes resize properly
        self.song_details_subframes[0].grid_columnconfigure(0, weight=1)
        self.song_details_subframes[1].grid_columnconfigure(0, weight=1)
        self.song_details_subframes[2].grid_columnconfigure(0, weight=1)
        self.song_details_subframes[3].grid_columnconfigure(0, weight=1)

                
        ### Difficulty Info ###
        self.difficulty_info_label_frame = tk.LabelFrame(self.window, text="Difficulty Info", padx=20, pady=10)
        self.difficulty_info_label_frame.grid(row=4, column=0)
        self.show_duet_var = tk.BooleanVar(value=False)
        self.show_duet_var.trace_add("write", self.on_duet_change)
        self.decouple_duet_var = tk.BooleanVar(value=False)
        self.decouple_duet_var.trace_add("write", self.on_decouple_duet_change)
        self.duet_frame = tk.Frame(self.difficulty_info_label_frame)
        self.duet_frame.grid(row=0, column=0)    

        self.decouple_duet_checkbutton = tk.Checkbutton(self.duet_frame, text="Decouple Duet Values", variable=self.decouple_duet_var)
        self.decouple_duet_checkbutton.grid(row=0, column=0)
        self.show_duet_checkbutton = tk.Checkbutton(self.duet_frame, text="Show Duet Values", variable=self.show_duet_var, anchor="w", width=112)
        self.show_duet_checkbutton.grid(row=0, column=1)
        self.difficulty_info_frame = tk.Frame(self.difficulty_info_label_frame)
        self.difficulty_info_frame.grid(row=1, column=0)

        self.difficulty_info_sub_frames = [
            tk.LabelFrame(self.difficulty_info_frame, text="Easy", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Normal", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Hard", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Oni", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Ura", padx=10, pady=10),
        ]

        self.spike_on_labels = list()
        self.star_labels = list()
        self.shinuchi_labels = list()
        self.shinuchi_score_labels = list()
        self.onpu_num_labels = list()
        self.renda_time_labels = list()
        self.fuusen_total_labels = list()
        self.ai_sections_labels = list()

        self.branch_spike_frames = list()

        self.branch_checkbuttons = list()
        self.branch_values =  [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
        self.spike_on_spinboxes = list()
        self.spike_on_values =  [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.star_spinboxes = list()
        self.star_values =  [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.shinuchi_spinboxes = list()
        self.shinuchi_values =  [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.shinuchi_score_spinboxes = list()
        self.shinuchi_score_values =  [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.onpu_num_spinboxes = list()
        self.onpu_num_values =  [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.renda_time_entries = list()
        self.renda_time_values =  [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.fuusen_total_spinboxes = list()
        self.fuusen_total_values =  [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.ai_sections_comboboxes = list()
        self.ai_sections_frames = list()
        self.ai_sections_radiobuttons = list()
        self.ai_sections_values = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        for e in self.ai_sections_values:
            e.set(5)
        self.ai_hard_checkbuttons = list()
        self.ai_hard_values = [tk.BooleanVar(), tk.BooleanVar()]

        for i in range(5):
            self.difficulty_info_sub_frames[i].grid(row=1, column=i)
            
            self.star_labels.append(tk.Label(self.difficulty_info_sub_frames[i], text="Star Difficulty:", anchor="w", width=20))
            self.shinuchi_labels.append(tk.Label(self.difficulty_info_sub_frames[i], text="Shinuchi:", anchor="w", width=20))
            self.shinuchi_score_labels.append(tk.Label(self.difficulty_info_sub_frames[i], text="Shinuchi Score:", anchor="w", width=20))
            self.onpu_num_labels.append(tk.Label(self.difficulty_info_sub_frames[i], text="Onpu Number:", anchor="w", width=20))
            self.renda_time_labels.append(tk.Label(self.difficulty_info_sub_frames[i], text="Renda Time:", anchor="w", width=20))            
            self.fuusen_total_labels.append(tk.Label(self.difficulty_info_sub_frames[i], text="Fuusen Total:", anchor="w", width=20))
            self.ai_sections_labels.append(tk.Label(self.difficulty_info_sub_frames[i], text="AI sections:", anchor="w", width=20))
            
            self.star_labels[i].grid(row=1, column=0)
            self.shinuchi_labels[i].grid(row=3, column=0)
            self.shinuchi_score_labels[i].grid(row=5, column=0)
            self.onpu_num_labels[i].grid(row=7, column=0)
            self.renda_time_labels[i].grid(row=9, column=0)
            self.fuusen_total_labels[i].grid(row=11, column=0)
            self.ai_sections_labels[i].grid(row=13, column=0)

            self.branch_spike_frames.append(tk.Frame(self.difficulty_info_sub_frames[i]))
            self.branch_checkbuttons.append(tk.Checkbutton(self.branch_spike_frames[i], text="Branch", variable=self.branch_values[i], width=7, anchor='w')) 
            self.spike_on_spinboxes.append(tk.Spinbox(self.branch_spike_frames[i], textvariable=self.spike_on_values[i], width=2, from_=0, to=99)) 

            self.spike_on_labels.append(tk.Label(self.branch_spike_frames[i], text="Spike On"))

            self.star_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=0, to=10, textvariable=self.star_values[i]))
            self.shinuchi_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=1, to=99999999, textvariable=self.shinuchi_values[i]))
            self.shinuchi_score_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=1, to=99999999, textvariable=self.shinuchi_score_values[i]))
            self.onpu_num_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=0, to=99999999, textvariable=self.onpu_num_values[i]))
            self.renda_time_entries.append(tk.Entry(self.difficulty_info_sub_frames[i], textvariable=self.renda_time_values[i], width=22))
            self.fuusen_total_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], textvariable=self.fuusen_total_values[i], from_=0, to=99999999))
            #self.ai_sections_comboboxes.append(ttk.Combobox(self.difficulty_info_sub_frames[i], values=['3','5']))
            self.ai_sections_frames.append(tk.Frame(self.difficulty_info_sub_frames[i]))
            self.ai_sections_radiobuttons.append(
                [
                    tk.Radiobutton(self.ai_sections_frames[i], text="3", variable=self.ai_sections_values[i], value=3),
                    tk.Radiobutton(self.ai_sections_frames[i], text="5", variable=self.ai_sections_values[i], value=5)
                ]
            )

            if i >= 3:
                self.ai_hard_checkbuttons.append(tk.Checkbutton(self.ai_sections_frames[i], text="Hard", variable=self.ai_hard_values[i-3]))
                self.ai_hard_checkbuttons[i-3].grid(row=0, column=3)
            
            self.branch_spike_frames[i].grid(row=0, column=0)
            self.branch_checkbuttons[i].grid(row=0, column=0)
            self.spike_on_spinboxes[i].grid(row=0, column=1)
            self.spike_on_labels[i].grid(row=0, column=2)
            self.star_spinboxes[i].grid(row=2, column=0)
            self.shinuchi_spinboxes[i].grid(row=4, column=0)
            self.shinuchi_score_spinboxes[i].grid(row=6, column=0)
            self.onpu_num_spinboxes[i].grid(row=8, column=0)
            self.renda_time_entries[i].grid(row=10, column=0)
            self.fuusen_total_spinboxes[i].grid(row=12, column=0)
            #self.ai_sections_comboboxes[i].grid(row=14, column=0)
            self.ai_sections_frames[i].grid(row=14, column=0)
            self.ai_sections_radiobuttons[i][0].grid(row=0, column=0)
            self.ai_sections_radiobuttons[i][1].grid(row=0, column=1)

            for widget in self.difficulty_info_sub_frames[i].winfo_children():
                widget.grid_configure(padx=5, pady=1)

        self.current_songid = ''
        self.duet_change_ignore_flag = False
        self.previous_language = 0
        self.initial = True
        self.disable_all_widgets(self.window)
        self.song_info = dt.Song()

        updater = ud.Updater(self.window)
        updater.check_for_updates()

    def open_musicorder_window(self):
        self.music_order_window = tk.Toplevel(self.window)
        self.music_order_window.attributes('-toolwindow', True)
        self.music_order_window.grab_set()
        self.music_order_window.title(f'Music Order - {self.current_songid}')

        self.music_order_genre_order_labels = []
        self.music_order_genre_frame = []
        self.music_order_genre_display_checkbuttons = []
        self.music_order_genre_display_var = []
        self.music_order_genre_order_spinboxes = []
        self.music_order_genre_order_var = []
        self.music_order_genre_close_disp_type_spinbox = []
        self.music_order_genre_close_disp_type_var = []

        # Create a frame for the entire layout to maintain alignment
        main_frame = tk.Frame(self.music_order_window)
        main_frame.grid(row=0, column=0, padx=5, pady=5)

        # Add headers for "Order" and "CloseDispType"
        tk.Label(main_frame, text="Order", anchor="w", width=6).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(main_frame, text="Disp Type", anchor="w", width=10).grid(row=0, column=3, padx=5, pady=5)

        for i, genre in enumerate(GENRE_MAPPING.keys()):
            # Row for genre name and checkbox
            self.music_order_genre_display_var.append(tk.BooleanVar())
            self.music_order_genre_display_var[i].set(self.song_info.musicOrder[i][0] != -1)


            # Frame to contain each genre's components
            self.music_order_genre_frame.append(tk.Frame(main_frame))
            self.music_order_genre_frame[i].grid(row=i+1, column=0, sticky="w", pady=5)

            # Genre name label
            self.music_order_genre_order_labels.append(tk.Label(self.music_order_genre_frame[i], text=f"{genre}:", pady=5, anchor="w", width=20))
            self.music_order_genre_order_labels[i].grid(row=0, column=0, padx=3, sticky="w")

            # Checkbox for display (placed between the genre label and the spinbox)
            self.music_order_genre_display_checkbuttons.append(tk.Checkbutton(self.music_order_genre_frame[i], variable=self.music_order_genre_display_var[i]))
            self.music_order_genre_display_checkbuttons[i].grid(row=0, column=1, padx=5)

            # Order Spinbox
            self.music_order_genre_order_var.append(tk.IntVar())
            self.music_order_genre_order_var[i].set(self.song_info.musicOrder[i][0])
            self.music_order_genre_order_spinboxes.append(tk.Spinbox(main_frame, textvariable=self.music_order_genre_order_var[i], from_=-1, to=9999, width=6))
            self.music_order_genre_order_spinboxes[i].grid(row=i+1, column=2, padx=5, sticky="w")

            # Close Disp Type Spinbox
            self.music_order_genre_close_disp_type_var.append(tk.IntVar(value=self.song_info.musicOrder[i][1]))
            self.music_order_genre_close_disp_type_spinbox.append(tk.Spinbox(main_frame, from_=0, to=99, width=6, textvariable=self.music_order_genre_close_disp_type_var[i]))
            self.music_order_genre_close_disp_type_spinbox[i].grid(row=i+1, column=3, padx=5, sticky="w")

        # Add the submit button at the bottom and center it
        self.music_order_button_frame = tk.Frame(self.music_order_window, pady=5)
        self.music_order_button_frame.grid(row=len(GENRE_MAPPING)+2, column=0, pady=5)

        self.music_order_submit_button = tk.Button(self.music_order_button_frame, text="Update", command=self.on_music_order_submit)
        self.music_order_submit_button.grid(row=0, column=0)

        # Adjust the column stretching to resize properly
        self.music_order_window.grid_columnconfigure(0, weight=1)

    def disable_all_widgets(self, parent):
        self.song_delete_button.config(state="disabled")
        for child in parent.winfo_children():
            if child == self.songid_entry:
                continue 
            if isinstance(child, (tk.Entry, tk.Radiobutton, tk.Checkbutton, tk.Spinbox, tk.Button)):
                child.config(state="disabled")
            elif isinstance(child, (tk.Frame, tk.LabelFrame)):
                self.disable_all_widgets(child)  # Recurse into frames

    def enable_all_widgets(self, parent):
        self.song_delete_button.config(state="normal")
        for child in parent.winfo_children():
            if child == self.songid_entry:
                continue 
            elif child in [self.genre_combobox, self.dancer_combobox, self.song_name_font_spinbox, self.song_sub_font_spinbox, self.song_detail_font_spinbox]:
                child.config(state="readonly")
            elif isinstance(child, (tk.Entry, tk.Radiobutton, tk.Checkbutton, tk.Spinbox, tk.Button)):
                child.config(state="normal")
            elif isinstance(child, (tk.Frame, tk.LabelFrame)):
                self.enable_all_widgets(child)  # Recurse into frames

    def delete_song(self, *args):
        if messagebox.askyesno('Delete Song', f'Are you sure you want to delete song {self.current_songid}?'):
            try:
                self.datatable.delete_song(self.current_songid)
                self.song_info = dt.Song()
                self.current_songid = ""
                self.populate_ui(True)
                self.songid_entry.delete(0, tk.END)
                self.disable_all_widgets(self.window)
                self.initial = True
                messagebox.showinfo('Delete Song', 'Song deleted successfully')
            except Exception as e:
                messagebox.showerror('Delete Song', f'Delete Song Error: {e}')
                return


    def on_new_song(self, *args):
        if not hasattr(self, 'datatable'):
            messagebox.showerror('New Song', f'Open datatable first')
            return
        if self.current_songid:
            try:
                self.save_song()
            except Exception as e:
                messagebox.showerror('Save Song', f'Song Save Error: {e}')
                traceback.print_exc()
                return

        self.new_song_window = tk.Toplevel(self.window, pady=10, padx=10)
        self.new_song_window.attributes('-toolwindow', True)

        self.new_song_window.grab_set()
        self.new_song_window.title(f'New Song')

        self.new_song_id_label = tk.Label(self.new_song_window, text="Song Id:", anchor="w", width=20)
        self.new_song_id_label.grid(row=0, column=0)
        # self.new_song_id_frame = tk.Frame(self.new_song_window)
        # self.new_song_id_frame.grid(row=1, column=0)
        self.new_song_id_entry = tk.Entry(self.new_song_window)
        self.new_song_id_entry.grid(row=1, column=0, padx=5)
        self.new_song_id_entry.focus()

        new_id = ''
        def on_create(*args):
            nonlocal new_id
            new_id_candidate = self.new_song_id_entry.get()
            if not new_id_candidate:
                messagebox.showerror('New Song', 'Enter a Song Id')
                return  
            if 3 > len(new_id_candidate) or len(new_id_candidate) > 8:
                messagebox.showerror('New Song', 'Song Id must be between 3 and 8 characters long')
                return 
            if self.datatable.is_song_id_taken(new_id_candidate):
                messagebox.showerror('New Song', 'Song Id already taken')
                return
            new_id = new_id_candidate
            self.new_song_window.destroy()
            
        self.new_song_id_entry.bind('<Return>', on_create)
        self.new_song_confirm = tk.Button(self.new_song_window, text="Create", command=on_create) #type: ignore
        self.new_song_confirm.grid(row=1, column=1)

        self.new_song_window.wait_window()

        if not new_id: return
        self.song_info = dt.Song(id=new_id)
        self.songid_entry.delete(0, tk.END)
        self.songid_entry.insert(0, new_id)
        self.current_songid = new_id
        self.populate_ui(no_query=True)
        self.song_info.uniqueId = -1
        if self.initial:
            self.initial = False
            # self.enable_all_widgets(self.window)

    def on_new_song_tja(self, *args): #I know a lot of the code here is mostly a copy of above but who gives
        if not hasattr(self, 'datatable'):
            use_without_datatable = messagebox.askokcancel('New Song from TJA','No datatable is loaded. Do you want to create fumen/sound files anyway?')
            if not use_without_datatable:
                return
        else:
            use_without_datatable = False
        if self.current_songid:
            try:
                self.save_song()
            except Exception as e:
                messagebox.showerror('Save Song', f'Song Save Error: {e}')
                traceback.print_exc()
                return
        
        self.new_song_window = tk.Toplevel(self.window, pady=10, padx=10)
        self.new_song_window.attributes('-toolwindow', True)

        self.new_song_window.grab_set()
        self.new_song_window.title(f'New Song')

        self.new_song_id_label = tk.Label(self.new_song_window, text="Song Id:", anchor="w", width=20)
        self.new_song_id_label.grid(row=0, column=0)
        # self.new_song_id_frame = tk.Frame(self.new_song_window)
        # self.new_song_id_frame.grid(row=1, column=0)
        self.new_song_id_entry = tk.Entry(self.new_song_window)
        self.new_song_id_entry.grid(row=1, column=0, padx=5)
        self.new_song_id_entry.focus()

        new_id = ''
        def on_create(*args):
            nonlocal new_id, use_without_datatable
            new_id_candidate = self.new_song_id_entry.get()
            if not new_id_candidate:
                messagebox.showerror('New Song', 'Enter a Song Id')
                return  
            if 3 > len(new_id_candidate) or len(new_id_candidate) > 8:
                messagebox.showerror('New Song', 'Song Id must be between 3 and 8 characters long')
                return 
            if not use_without_datatable and self.datatable.is_song_id_taken(new_id_candidate):
                messagebox.showerror('New Song', 'Song Id already taken')
                return
            new_id = new_id_candidate
            self.new_song_window.destroy()
            
        self.new_song_id_entry.bind('<Return>', on_create)
        self.new_song_confirm = tk.Button(self.new_song_window, text="Create", command=on_create) #type: ignore
        self.new_song_confirm.grid(row=1, column=1)

        self.new_song_window.wait_window()

        if not new_id: return

        tja_path = filedialog.askopenfilename(title="Select a TJA file", filetypes=[("TJA File", ".tja")])
        if not tja_path:
            return
        
        try:
            data = parse_tja.parse_and_get_data(tja_path)
        except Exception as e:
            messagebox.showerror('TJA Import', f'TJA Import Error: {e}')
            traceback.print_exc()
            return
        
        if use_without_datatable: 
            generate_files = True
        else:
            generate_files = messagebox.askyesno("TJA Import", "Do you want to generate fumen and sound files?")
        export_complete = False
        if (generate_files):
            if not config.config.fumenKey:
                messagebox.showerror('Fumen Generate', 'Fumen Generation Error: Empty Fumen Key')
                return
            
            #check if ffmpeg components are in path
            ffmpeg_present = shutil.which('ffmpeg') is not None
            ffprobe_present = shutil.which('ffprobe') is not None

            if not ffmpeg_present or not ffprobe_present:
                missing_components = []
                if not ffmpeg_present:
                    missing_components.append("ffmpeg")
                if not ffprobe_present:
                    missing_components.append("ffprobe")
                
                missing_str = " and ".join(missing_components)
                
                error_title = "Missing Components"
                error_message = f"{missing_str} {'is' if len(missing_components) == 1 else 'are'} not found in the system PATH.\n"
                error_message += "Please install the missing component(s) and add them to your system PATH."
            
                messagebox.showerror(error_title, error_message)
                return
            
            
            def set_sound():
                sound_filepath.set(filedialog.askopenfilename(title="Select a Sound file", filetypes=[("Audio Files", ".wav .ogg")]))

            def set_out_dir():
                path = filedialog.askdirectory(title='Export Directory')
                config.config.update_game_files_out_dir(path)
                out_dir_path.set(path)

            def submit_config():
                nonlocal export_complete
                try:
                    # Retrieve the current values of the offsets
                    preview_offset = preview_offset_var.get()
                    chart_start_offset = chart_start_offset_var.get()
                    
                    # Convert to milliseconds if the user has selected seconds ('s')
                    if time_unit_var.get() == "s":
                        preview_offset *= 1000  # Convert seconds to milliseconds
                        chart_start_offset *= 1000  # Convert seconds to milliseconds

                    # If the time unit is 'ms', leave the values as they are (already in ms)
                    
                    # Pass the offsets (in ms) to the fumen conversion function
                    fumen.convert_tja_to_fumen_files(
                        new_id, 
                        tja_path, 
                        sound_filepath.get(), 
                        preview_offset, 
                        chart_start_offset, 
                        out_dir_path.get()
                    )

                    export_complete = True
                    config_window.destroy()
                    messagebox.showinfo('Fumen Generate', 'Successfully generated files')
                except Exception as e:
                    messagebox.showerror('Fumen Generate', f'Fumen Generation Error: {e}')
                    traceback.print_exc()


            # Create a new Toplevel window
            config_window = tk.Toplevel()
            config_window.grab_set()
            config_window.attributes('-toolwindow', True)
            config_window.title("Generate Fumen Files")

            sound_filepath = tk.StringVar()
            out_dir_path = tk.StringVar(value=config.config.gameFilesOutDir)
            preview_offset_var = tk.DoubleVar(value=data.demo_start)
            chart_start_offset_var = tk.DoubleVar(value=0.0)
            time_unit_var = tk.StringVar(value="s")  # Default to seconds

            tk.Label(config_window, text="TJA File:").grid(row=0, column=0, padx=10, pady=2)
            tja_entry = tk.Entry(config_window, width=70, state="readonly", textvariable=tk.StringVar(value=tja_path))
            tja_entry.grid(row=1, column=0, padx=10, pady=2)

            tk.Label(config_window, text="Sound File:").grid(row=2, column=0, padx=10, pady=2)
            sound_entry = tk.Entry(config_window, width=70, state="readonly", textvariable=sound_filepath)
            sound_entry.grid(row=3, column=0, padx=10, pady=2)
            sound_button = tk.Button(config_window, text="Set", command=set_sound, padx=5)
            sound_button.grid(row=3, column=1)

            tk.Label(config_window, text="Export Directory:").grid(row=4, column=0, padx=10, pady=2)
            out_entry = tk.Entry(config_window, width=70, state="readonly", textvariable=out_dir_path)
            out_entry.grid(row=5, column=0, padx=10, pady=2)
            out_button = tk.Button(config_window, text="Set", command=set_out_dir, padx=5)
            out_button.grid(row=5, column=1, padx=5)

            # Create a Frame for Time-related settings (Preview Offset, Chart Start Offset, Time Unit)
            time_frame = tk.Frame(config_window)
            time_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

            # Label and Spinbox for Preview Offset inside the time_frame
            tk.Label(time_frame, text="Preview Offset:").grid(row=0, column=0, padx=10, pady=2)
            preview_offset_spinbox = tk.Entry(
                time_frame, width=15,
                textvariable=preview_offset_var
            )
            preview_offset_spinbox.grid(row=0, column=1, padx=10, pady=2)

            # Label and Spinbox for Chart Start Offset inside the time_frame
            tk.Label(time_frame, text="Add blank audio before song start:").grid(row=1, column=0, padx=10, pady=2)
            chart_start_offset_spinbox = tk.Spinbox(
                time_frame, from_=-10.0, to=10.0, increment=0.1, format="%.1f", width=8,
                textvariable=chart_start_offset_var
            )
            chart_start_offset_spinbox.grid(row=1, column=1, padx=10, pady=2)

            # Radio buttons for selecting time unit (ms or s) inside the time_frame
            tk.Label(time_frame, text="Time Unit:").grid(row=2, column=0, padx=10, pady=2)
            time_unit_frame = tk.Frame(time_frame)
            time_unit_frame.grid(row=2, column=1, padx=10, pady=2)

            ms_radio = tk.Radiobutton(time_unit_frame, text="ms", variable=time_unit_var, value="ms")
            ms_radio.pack(side="left")
            s_radio = tk.Radiobutton(time_unit_frame, text="s", variable=time_unit_var, value="s")
            s_radio.pack(side="left")

            # Create Submit Button
            generate_button = tk.Button(config_window, text="Generate", command=submit_config)
            generate_button.grid(row=7, column=0, pady=5)

            config_window.wait_window()
            
        if use_without_datatable or generate_files and not export_complete: return
        
        self.song_info = dt.Song(id=new_id, 
                                 star=data.star,
                                 shinuti=data.shinuti,
                                 shinuti_duet=data.shinuti,
                                 shinuti_score=data.shinuti_score,
                                 shinuti_score_duet=data.shinuti_score,
                                 onpu_num=data.onpu_num,
                                 fuusen_total=data.fuusen_total,
                                 renda_time=data.renda_time,
                                 music_ai_section=[5 if l > 100 else 3 for l in data.length],
                                 songFileName=f'sound/song_{new_id}'
                                 )
        
        for i in range(4):
            self.song_info.songNameList[i] = (data.title, i)
            self.song_info.songSubList[i] = (data.sub, i)
        self.songid_entry.delete(0, tk.END)
        self.songid_entry.insert(0, new_id)
        self.current_songid = new_id
        self.populate_ui(no_query=True)
        self.song_info.uniqueId = -1 #Do this so when saving song it always checks for existing unique id
        if self.initial:
            self.initial = False
            # self.enable_all_widgets(self.window)

    def on_add_ura(self, *args):
        if not hasattr(self, 'datatable'):
            messagebox.showerror('Add Ura to Chart', 'No datatable loaded')
            return

        if self.current_songid:
            try:
                self.save_song()
            except Exception as e:
                messagebox.showerror('Save Song', f'Song Save Error: {e}')
                traceback.print_exc()
                return

        self.new_song_window = tk.Toplevel(self.window, pady=10, padx=10)
        self.new_song_window.attributes('-toolwindow', True)

        self.new_song_window.grab_set()
        self.new_song_window.title(f'Add Ura to Chart')

        self.new_song_id_label = tk.Label(self.new_song_window, text="Song Id:", anchor="w", width=20)
        self.new_song_id_label.grid(row=0, column=0)
        # self.new_song_id_frame = tk.Frame(self.new_song_window)
        # self.new_song_id_frame.grid(row=1, column=0)
        self.new_song_id_entry = tk.Entry(self.new_song_window)
        self.new_song_id_entry.grid(row=1, column=0, padx=5)
        self.new_song_id_entry.focus()

        song_id = ''

        def on_create(*args):
            nonlocal song_id
            new_id_candidate = self.new_song_id_entry.get()
            if not new_id_candidate:
                messagebox.showerror('Add Ura to Chart', 'Enter a Song Id')
                return
            if not self.datatable.is_song_id_taken(new_id_candidate):
                messagebox.showerror('Add Ura to Chart', 'Song Id not found')
                return
            song_id = new_id_candidate
            self.new_song_window.destroy()


        self.new_song_id_entry.bind('<Return>', on_create)
        self.new_song_confirm = tk.Button(self.new_song_window, text="Create", command=on_create)  # type: ignore
        self.new_song_confirm.grid(row=1, column=1)

        self.new_song_window.wait_window()

        if not song_id: return

        tja_path = filedialog.askopenfilename(title="Select a TJA file", filetypes=[("TJA File", ".tja")])
        if not tja_path:
            return

        try:
            data = parse_tja.parse_and_get_data(tja_path)
        except Exception as e:
            messagebox.showerror('TJA Import', f'TJA Import Error: {e}')
            traceback.print_exc()
            return

        if data.star[4] == 0:
            messagebox.showerror('Add Ura to Chart', f'TJA File has no Ura chart')
            return

        path_to_x64 = filedialog.askdirectory(initialdir=config.config.gameFilesOutDir, title="Import/Export Directory (x64 directory)")

        try:
            fumen.add_ura_to_song(song_id, tja_path, path_to_x64)
        except Exception as e:
            messagebox.showerror('Add Ura to Chart', f'Add Ura to Chart Error: {e}')
            return

        self.song_info = self.datatable.get_song_info(song_id)
        self.song_info.star[4] = data.star[4]
        self.song_info.shinuti[4] = data.shinuti[4]
        self.song_info.shinuti_score[4] = data.shinuti_score[4]
        self.song_info.onpu_num[4] = data.onpu_num[4]
        self.song_info.fuusen_total[4] = data.fuusen_total[4]
        self.song_info.renda_time[4] = data.renda_time[4]
        self.song_info.music_ai_section[4] = self.song_info.music_ai_section[3]
        self.songid_entry.delete(0, tk.END)
        self.songid_entry.insert(0, song_id)
        self.current_songid = song_id
        self.populate_ui(no_query=True)
        if self.initial:
            self.initial = False


    def check_and_confirm_uid(self, uniqueId: int) -> bool:
        """
        Returns if uid can be used / uid initially in use is changed
        """
        if not self.datatable.is_uid_taken(uniqueId): return True
        
        response = messagebox.askyesno("Duplicate UniqueId", f"UniqueId {uniqueId} already exists, use anyway?")
        if not response: return False

        ret = False

        def submit(*args):
            nonlocal ret
            uniqueId_input = new_uid_var.get()
            if not uniqueId_input:
                messagebox.showerror(f'Update uniqueId {uniqueId}', 'Enter a uniqueId')
                return
            if self.datatable.is_uid_taken(uniqueId_input):
                messagebox.showerror(f'Update uniqueId {uniqueId}', f'UniqueId already {uniqueId_input} taken')
                return
            self.datatable.update_uid(uniqueId, uniqueId_input)
            ret = True
            new_uid_window.destroy()

        new_uid_window = tk.Toplevel(pady=10, padx=10)
        new_uid_window.attributes('-toolwindow', True)

        new_uid_window.grab_set()
        new_uid_window.title('Update uniqueId {uniqueId}')
        prompt = tk.Label(new_uid_window, text = 'Enter a new UniqueId for the song to overwrite the existing one')
        prompt.grid(row=0, column=0)
        new_uid_var = tk.IntVar()
        new_uid_entry = tk.Spinbox(new_uid_window, textvariable=new_uid_var)
        new_uid_entry.grid(row=1, column=0)
        new_uid_entry.bind('<Return>', submit)
        new_uid_entry.focus()
        confirm_button = tk.Button(new_uid_window, text='Update', command=submit)
        confirm_button.grid(row=2, column=0)

        new_uid_window.wait_window()
        return ret
    
    def run(self):
        self.window.mainloop()

    def save_datatable(self, *args):
        if not hasattr(self, 'datatable'):
            messagebox.showerror('Save Datatable', 'Save Datatable Error: Open datatable first')
            return
        if self.current_songid:
            try:
                self.save_song()
            except Exception as e:
                messagebox.showerror('Save Song', f'Song Save Error: {e}')
                traceback.print_exc()
                return
        selected_directory = filedialog.askdirectory(title="Select an export directory")
        if not selected_directory:
            messagebox.showerror('Export Error', f'Select a folderpath')
            return
        try:
            self.datatable.export_datatable(selected_directory)
            messagebox.showinfo('Export Datable', 'Export success')
        except Exception as e:
            messagebox.showerror('Export Error', f'Export Error: {e}')
            return

    def open_datatable(self, *args):
        if hasattr(self, 'datatable') and self.current_songid:
            try:
                self.save_song()
            except Exception as e:
                messagebox.showerror('Save Song', f'Song Save Error: {e}')
                traceback.print_exc()
                return
        selected_directory = filedialog.askdirectory(title="Select an import directory")
        if not selected_directory:
            return
        try:
            self.datatable = dt.Datatable(selected_directory)
            self.song_info = dt.Song()
            self.current_songid = ""
            self.populate_ui(True)
            self.songid_entry.delete(0,tk.END)
            self.disable_all_widgets(self.window)
            self.initial = True
            messagebox.showinfo('Import Datable', 'Import success')
        except Exception as e:
            messagebox.showerror('Import Error', f'Import Error: {e}')

    def show_about(self):
        webbrowser.open('https://github.com/keitannunes/KeifunsDatatableEditor')

    def create_config_window(self, *args):
        def submit_config():
            datatable_key = entry_datatable_key.get()
            fumen_key = entry_fumen_key.get()

            config.config.update_keys(datatable_key, fumen_key)
            config_window.destroy()

        # Create a new Toplevel window
        config_window = tk.Toplevel()
        config_window.grab_set()
        config_window.title("Enter Configuration")
        config_window.attributes('-toolwindow', True)


        # Create Label and Entry for Datatable Key
        tk.Label(config_window, text="Datatable Key:").grid(row=0, column=0, padx=10, pady=10)
        entry_datatable_key = tk.Entry(config_window, width=70)
        entry_datatable_key.focus()
        entry_datatable_key.grid(row=0, column=1, padx=10, pady=10)

        # Create Label and Entry for Fumen Key
        tk.Label(config_window, text="Fumen Key:").grid(row=1, column=0, padx=10, pady=10)
        entry_fumen_key = tk.Entry(config_window, width=70)
        entry_fumen_key.grid(row=1, column=1, padx=10, pady=5)

        entry_datatable_key.insert(0, config.config.datatableKey)
        entry_fumen_key.insert(0, config.config.fumenKey)

        # Create Submit Button
        submit_button = tk.Button(config_window, text="Submit", command=submit_config)
        submit_button.grid(row=2, column=0, columnspan=2, pady=5)

    def save_song(self):
        #Music order will always be up-to-date so we don't have to save that here
        #Same goes for wordlist vars asides current language

        if self.song_info.uniqueId != self.unique_id_var.get():
            if self.check_and_confirm_uid(self.unique_id_var.get()):
                self.song_info.uniqueId = self.unique_id_var.get()
            else:
                raise Exception("UniqueId already exists")


        self.song_info.songNameList[self.language_value.get()] = self.song_name_var.get(), self.song_name_font_var.get()
        self.song_info.songSubList[self.language_value.get()] = self.song_sub_var.get(), self.song_sub_font_var.get()
        self.song_info.songDetailList[self.language_value.get()] = self.song_detail_var.get(), self.song_detail_font_var.get()

        genre = self.genre_var.get()
        if genre in GENRE_MAPPING: 
            self.song_info.genreNo = GENRE_MAPPING[genre]
        else:
            raise Exception("Invalid Genre")
        
        if self.song_info.musicOrder[GENRE_MAPPING[genre]] == -1 and not all(x == -1 for x in self.song_info.musicOrder):
            raise Exception("Music Order cannot be -1 for main genre")


        self.song_info.songFileName = self.song_filename_var.get()
        self.song_info.new = self.new_var.get()
        self.song_info.papamama = self.papamama_var.get()
        self.song_info.doublePlay = self.double_play_var.get()
        self.song_info.dancer = self.dancer_var.get()

        for i in range(5):
            self.song_info.branch[i] = self.branch_values[i].get()
            self.song_info.spike_on[i] = int(self.spike_on_values[i].get())
            self.song_info.star[i] = self.star_values[i].get()
            if self.decouple_duet_var.get():
                if self.show_duet_var.get():
                    self.song_info.shinuti_duet[i] = self.shinuchi_values[i].get()
                    self.song_info.shinuti_score_duet[i] = self.shinuchi_score_values[i].get()
                else:
                    self.song_info.shinuti[i] = self.shinuchi_values[i].get()
                    self.song_info.shinuti_score[i] = self.shinuchi_score_values[i].get()
            else:
                self.song_info.shinuti[i] = self.shinuchi_values[i].get()
                self.song_info.shinuti_score[i] = self.shinuchi_score_values[i].get()
                self.song_info.shinuti_duet[i] = self.shinuchi_values[i].get()
                self.song_info.shinuti_score_duet[i] = self.shinuchi_score_values[i].get()
            self.song_info.onpu_num[i] = self.onpu_num_values[i].get()
            self.song_info.renda_time[i] = float(self.renda_time_values[i].get())
            self.song_info.fuusen_total[i] = self.fuusen_total_values[i].get()
            self.song_info.music_ai_section[i] = self.ai_sections_values[i].get()
        self.song_info.aiOniLevel11 = "o" if self.ai_hard_values[0].get() else ""
        self.song_info.aiUraLevel11 = "o" if self.ai_hard_values[1].get() else "" #what the fuck namco
        self.datatable.set_song_info(self.song_info)

    def on_songid(self, event: tk.Event):
        if event.widget.get() == self.current_songid: return
        if not hasattr(self, 'datatable'):
            messagebox.showerror('Song Load Error', f'Song Load Error: Open datatable first')
            return
        old_songid = self.current_songid
        self.current_songid = event.widget.get()
        if old_songid != '':
            try:
                self.save_song()
            except Exception as e:
                messagebox.showerror('Song Save Error', f'Song Save Error: {e}')
                traceback.print_exc()
                self.current_songid = old_songid
                self.songid_entry.delete(0, tk.END)
                self.songid_entry.insert(0, old_songid)
                return
        try:
            self.populate_ui()
            if self.initial:
                self.initial = False
                #self.enable_all_widgets(self.window)
        except Exception as e:
            messagebox.showerror('Song Load Error', f'Song Load Error: {e}')
            traceback.print_exc()
            self.current_songid = old_songid
            self.songid_entry.delete(0, tk.END)
            self.songid_entry.insert(0, old_songid)
    
    def on_language_change(self, *args):
        self.song_info.songNameList[self.previous_language] = self.song_name_var.get(), self.song_name_font_var.get()
        self.song_info.songSubList[self.previous_language] = self.song_sub_var.get(), self.song_sub_font_var.get()
        self.song_info.songDetailList[self.previous_language] = self.song_detail_var.get(), self.song_detail_font_var.get()
        self.previous_language = self.language_value.get()
        self.poplate_wordlist_vars()

    def on_decouple_duet_change(self, *args): 
        if self.decouple_duet_var.get():
            self.show_duet_checkbutton.config(state="active")
        else:
            self.show_duet_checkbutton.config(state="disabled")
            if self.show_duet_var.get(): self.show_duet_var.set(False)

    def change_duet_label(self, duet):
        for i in range(5):
            self.shinuchi_labels[i].config(text = "Shinuchi Duet:" if duet else "Shinuchi:")
            self.shinuchi_score_labels[i].config(text = "Shinuchi Score Duet:" if duet else "Shinuchi Score:")
    def on_duet_change(self, *args):
        if self.duet_change_ignore_flag: return #Ignore when data_load sets duet to false
        duet = self.show_duet_var.get()
        for i in range(5):
            self.change_duet_label(duet)
            if duet:
                #Normal -> Duet
                self.song_info.shinuti[i] = self.shinuchi_values[i].get()
                self.shinuchi_values[i].set(self.song_info.shinuti_duet[i])
                self.song_info.shinuti_score[i] = self.shinuchi_score_values[i].get()
                self.shinuchi_score_values[i].set(self.song_info.shinuti_score_duet[i])
            else:
                #Duet -> Normal
                self.song_info.shinuti_duet[i] = self.shinuchi_values[i].get()
                self.shinuchi_values[i].set(self.song_info.shinuti[i])
                self.song_info.shinuti_score_duet[i] = self.shinuchi_score_values[i].get()
                self.shinuchi_score_values[i].set(self.song_info.shinuti_score[i])
                
    def on_music_order_submit(self):
        for i, display in enumerate(self.music_order_genre_display_var):
            if display.get():
                self.song_info.musicOrder[i] = self.music_order_genre_order_var[i].get(), self.music_order_genre_close_disp_type_var[i].get()
            else:
                self.song_info.musicOrder[i] = -1, 0
        self.music_order_window.destroy()

    def populate_ui(self, no_query=False):
        if not no_query:
            self.song_info = self.datatable.get_song_info(self.current_songid)

        self.enable_all_widgets(self.window)
        self.duet_change_ignore_flag = True #Brain cancer 2000
        self.show_duet_var.set(False)
        self.change_duet_label(False)
        self.duet_change_ignore_flag = False
        self.decouple_duet_var.set(any(self.song_info.shinuti[i] != self.song_info.shinuti_duet[i] for i in range(5)) or any(self.song_info.shinuti_score[i] != self.song_info.shinuti_score_duet[i] for i in range(5)))
        self.poplate_wordlist_vars()
        self.unique_id_var.set(self.song_info.uniqueId)
        self.genre_var.set(next((k for k, v in GENRE_MAPPING.items() if v == self.song_info.genreNo), '')) #Do not question this line of code (getting key given value)
        self.song_filename_var.set(self.song_info.songFileName)
        self.new_var.set(self.song_info.new)
        self.papamama_var.set(self.song_info.papamama)
        self.double_play_var.set(self.song_info.doublePlay)
        self.dancer_var.set(self.song_info.dancer)

        for i in range(5):
            self.spike_on_values[i].set(bool(self.song_info.spike_on[i]))
            self.branch_values[i].set(self.song_info.branch[i])
            self.star_values[i].set(self.song_info.star[i])
            self.shinuchi_values[i].set(self.song_info.shinuti[i])
            self.shinuchi_score_values[i].set(self.song_info.shinuti_score[i])
            self.onpu_num_values[i].set(self.song_info.onpu_num[i])
            self.renda_time_values[i].set(str(self.song_info.renda_time[i]))
            self.fuusen_total_values[i].set(self.song_info.fuusen_total[i])
            self.ai_sections_values[i].set(self.song_info.music_ai_section[i])

        self.ai_hard_values[0].set(self.song_info.aiOniLevel11 == "o")
        self.ai_hard_values[1].set(self.song_info.aiUraLevel11 == "o")     

    def poplate_wordlist_vars(self):
        self.song_name_var.set(self.song_info.songNameList[self.language_value.get()][0])
        self.song_name_font_var.set(self.song_info.songNameList[self.language_value.get()][1])
        self.song_sub_var.set(self.song_info.songSubList[self.language_value.get()][0])
        self.song_sub_font_var.set(self.song_info.songSubList[self.language_value.get()][1])
        self.song_detail_var.set(self.song_info.songDetailList[self.language_value.get()][0])
        self.song_detail_font_var.set(self.song_info.songDetailList[self.language_value.get()][1])