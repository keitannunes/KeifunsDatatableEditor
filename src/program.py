import tkinter as tk
import datatable as dt
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from typing import List

GENRE_MAPPING = {
    "J-POP": 0,
    "アニメ": 1,
    "キッズ": 2,
    "VOCALOID": 3,
    "ゲームミュージック": 4,
    "ナムコオリジナル": 5,
    "バラエティー": 6,
    "クラシック": 7,
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
    difficulty_info_frame: tk.LabelFrame
    difficulty_info_sub_frames: List[tk.LabelFrame]

    #Labels
    songid_label: tk.Label
    song_name_label: tk.Label
    song_sub_label: tk.Label
    song_detail_label: tk.Label
    unique_id_label: tk.Label
    genre_label: tk.Label
    song_filename_label: tk.Label
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
    can_play_ura_var: tk.BooleanVar
    unique_id_var: tk.IntVar
    genre_var: tk.StringVar

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
    new_checkbutton: tk.Checkbutton
    can_play_ura_checkbutton: tk.Checkbutton
    branch_checkbuttons: List[tk.Checkbutton]
    branch_values: List[tk.BooleanVar]
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

    #Other Variables
    current_songid: str
    datatable: dt.Datatable
    song_info: dt.Song

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Keifun's Datatable Editor")
        #self.window.geometry("1280x720")  # Set window size to 720p

        img = Image.open("src/assets/icon.png")  # Replace with the path to your .png file
        icon = ImageTk.PhotoImage(img)

        # Set the window icon
        self.window.wm_iconphoto(False, icon) # type: ignore

        self.menu_bar = tk.Menu(self.window, tearoff=0)

        #File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Datatable", command=self.open_datatable)
        self.file_menu.add_command(label="Save Datatable", command=self.save_datatable)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="New Song", command=self.new_song)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.window.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        #Help Menu
        
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.window.config(menu=self.menu_bar)

        self.songid_label = tk.Label(self.window, text="Song Id:")
        self.songid_entry = tk.Entry(self.window)

        self.songid_label.grid(row=0, column=0)
        self.songid_entry.grid(row=1, column=0)

        self.songid_entry.bind("<Return>", self.on_songid)
        self.songid_entry.bind("<FocusOut>", self.on_songid)

        
        ### Song Details ###
        self.language_frame = tk.Frame(self.window, pady=5)

        self.language_radiobuttons = list()
        self.language_value = tk.IntVar()
        self.language_value.set(0)
        self.language_value.trace_add("write", self.on_language_change)

        for i, lang in enumerate(['ja', 'en', 'zh-TW', 'zh-CN', 'ko']):
            self.language_radiobuttons.append(tk.Radiobutton(self.language_frame, text=lang, variable=self.language_value, value=i))
            self.language_radiobuttons[i].grid(row=0, column=i)

        self.language_frame.grid(row=2, column=0)
        
        self.song_details_frame = tk.LabelFrame(self.window, text="Song Details", padx=20, pady=20)
        self.song_details_frame.grid(row=3, column=0)

        #Set Labels
        self.song_name_label = tk.Label(self.song_details_frame, text="Song Name:", anchor="w", width=20)
        self.song_name_label.grid(row=0, column=0)
        self.song_sub_label = tk.Label(self.song_details_frame, text="Song Sub:", anchor="w", width=20)
        self.song_sub_label.grid(row=2, column=0)
        self.song_detail_label = tk.Label(self.song_details_frame, text="Song Detail:", anchor="w", width=20)
        self.song_detail_label.grid(row=4, column=0)
        self.unique_id_label = tk.Label(self.song_details_frame, text="Unique Id:", anchor="w", width=20)
        self.unique_id_label.grid(row=6, column=0)
        self.genre_label = tk.Label(self.song_details_frame, text="Main Genre:", anchor="w", width=20)
        self.genre_label.grid(row=8, column=0)
        self.song_filename_label = tk.Label(self.song_details_frame, text="Song Filename:", anchor="w", width=20)
        self.song_filename_label.grid(row=0, column=1)

        # Create variables for each widget
        self.song_name_var = tk.StringVar()
        self.song_sub_var = tk.StringVar()
        self.song_detail_var = tk.StringVar()
        self.song_filename_var = tk.StringVar()
        self.new_var = tk.BooleanVar()
        self.can_play_ura_var = tk.BooleanVar()
        self.unique_id_var = tk.IntVar()
        self.genre_var = tk.StringVar()

        # Entry widgets bound to StringVar
        self.song_name_entry = tk.Entry(self.song_details_frame, textvariable=self.song_name_var)
        self.song_name_entry.grid(row=1, column=0)

        self.song_sub_entry = tk.Entry(self.song_details_frame, textvariable=self.song_sub_var)
        self.song_sub_entry.grid(row=3, column=0)

        self.song_detail_entry = tk.Entry(self.song_details_frame, textvariable=self.song_detail_var)
        self.song_detail_entry.grid(row=5, column=0)

        self.song_filename_entry = tk.Entry(self.song_details_frame, textvariable=self.song_filename_var)
        self.song_filename_entry.grid(row=1, column=1)

        # Checkbutton widgets bound to BooleanVar
        self.new_checkbutton = tk.Checkbutton(self.song_details_frame, text="New", variable=self.new_var)
        self.new_checkbutton.grid(row=2, column=1)

        self.can_play_ura_checkbutton = tk.Checkbutton(self.song_details_frame, text="Ura Playable", variable=self.can_play_ura_var)
        self.can_play_ura_checkbutton.grid(row=3, column=1)

        # Button (no variable needed, as it’s an action trigger)
        self.music_order_button = tk.Button(self.song_details_frame, text="Set Music Order")
        self.music_order_button.grid(row=4, column=1)

        # Spinbox widget bound to IntVar
        self.unique_id_spinbox = tk.Spinbox(self.song_details_frame, from_=0, to=9999, textvariable=self.unique_id_var)
        self.unique_id_spinbox.grid(row=7, column=0)

        # Combobox widget bound to StringVar
        self.genre_combobox = ttk.Combobox(self.song_details_frame, values=list(GENRE_MAPPING.keys()), textvariable=self.genre_var)
        self.genre_combobox.grid(row=9, column=0)
        

        #Set Padding for each element in song_details_frame

        for widget in self.song_details_frame.winfo_children():
            widget.grid_configure(padx=5, pady=1)


        ### Difficulty Info ###
        self.difficulty_info_frame = tk.LabelFrame(self.window, text="Difficulty Info", padx=20, pady=20)
        self.difficulty_info_frame.grid(row=4, column=0)
        self.difficulty_info_sub_frames = [
            tk.LabelFrame(self.difficulty_info_frame, text="Easy", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Normal", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Hard", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Oni", padx=10, pady=10),
            tk.LabelFrame(self.difficulty_info_frame, text="Ura", padx=10, pady=10),
        ]

        self.star_labels = list()
        self.shinuchi_labels = list()
        self.shinuchi_score_labels = list()
        self.onpu_num_labels = list()
        self.renda_time_labels = list()
        self.fuusen_total_labels = list()
        self.ai_sections_labels = list()

        self.branch_checkbuttons = list()
        self.branch_values =  [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
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
            e.set(3)
        self.ai_hard_checkbuttons = list()
        self.ai_hard_values = [tk.BooleanVar(), tk.BooleanVar()]

        for i in range(5):
            self.difficulty_info_sub_frames[i].grid(row=0, column=i)
            
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

            self.branch_checkbuttons.append(tk.Checkbutton(self.difficulty_info_sub_frames[i], text="Branch", variable=self.branch_values[i], width=20, anchor='w')) 
            self.star_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=0, to=10, textvariable=self.star_values[i]))
            self.shinuchi_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=1, to=99999999, textvariable=self.shinuchi_values[i]))
            self.shinuchi_score_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=1, to=99999999, textvariable=self.shinuchi_score_values[i]))
            self.onpu_num_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=0, to=99999999, textvariable=self.onpu_num_values[i]))
            self.renda_time_entries.append(tk.Entry(self.difficulty_info_sub_frames[i], textvariable=self.renda_time_values[i]))
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

            self.branch_checkbuttons[i].grid(row=0, column=0)
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
        self.datatable = dt.Datatable('C:\\Users\\knunes\\Downloads\\out\\KeifunsDatatableEditor\\datatable') #TODO: Variable dt

            

    def run(self):
        self.window.mainloop()

    def save_datatable(self):
        pass

    def open_datatable(self):
        pass

    def new_song(self):
        pass

    def show_about(self):
        pass

    def on_songid(self, event: tk.Event):
        if event.widget.get() == self.current_songid: return
        old_songid = self.current_songid
        self.current_songid = event.widget.get()
        try:
            self.populate_ui()
        except Exception:
            messagebox.showerror('Song Load Error', f"Songid {self.current_songid} not found")
            self.current_songid = old_songid
            self.songid_entry.delete(0, tk.END)
            self.songid_entry.insert(0, old_songid)
    
    def on_language_change(self, *args):
        self.poplate_wordlist_vars()

    def populate_ui(self):
        self.song_info = self.datatable.get_song_info(self.current_songid)

        self.poplate_wordlist_vars()
        self.unique_id_var.set(self.song_info.uniqueId)
        self.genre_var.set(next((k for k, v in GENRE_MAPPING.items() if v == self.song_info.genreNo), '')) #Do not question this line of code (getting key given value)
        self.song_filename_var.set(self.song_info.songFileName)
        self.new_var.set(self.song_info.new)
        self.can_play_ura_var.set(self.song_info.ura)

        self.branch_values[0].set(self.song_info.branchEasy)
        self.branch_values[1].set(self.song_info.branchNormal)
        self.branch_values[2].set(self.song_info.branchHard)
        self.branch_values[3].set(self.song_info.branchMania)
        self.branch_values[4].set(self.song_info.branchUra)

        self.star_values[0].set(self.song_info.starEasy)
        self.star_values[1].set(self.song_info.starNormal)
        self.star_values[2].set(self.song_info.starHard)
        self.star_values[3].set(self.song_info.starMania)
        self.star_values[4].set(self.song_info.starUra)

        self.shinuchi_values[0].set(self.song_info.shinutiEasy)
        self.shinuchi_values[1].set(self.song_info.shinutiNormal)
        self.shinuchi_values[2].set(self.song_info.shinutiHard)
        self.shinuchi_values[3].set(self.song_info.shinutiMania)
        self.shinuchi_values[4].set(self.song_info.shinutiUra)

        self.shinuchi_score_values[0].set(self.song_info.shinutiScoreEasy)
        self.shinuchi_score_values[1].set(self.song_info.shinutiScoreNormal)
        self.shinuchi_score_values[2].set(self.song_info.shinutiScoreHard)
        self.shinuchi_score_values[3].set(self.song_info.shinutiScoreMania)
        self.shinuchi_score_values[4].set(self.song_info.shinutiScoreUra)

        self.onpu_num_values[0].set(self.song_info.easyOnpuNum)
        self.onpu_num_values[1].set(self.song_info.normalOnpuNum)
        self.onpu_num_values[2].set(self.song_info.hardOnpuNum)
        self.onpu_num_values[3].set(self.song_info.maniaOnpuNum)
        self.onpu_num_values[4].set(self.song_info.uraOnpuNum)

        self.renda_time_values[0].set(str(self.song_info.rendaTimeEasy))
        self.renda_time_values[1].set(str(self.song_info.rendaTimeNormal))
        self.renda_time_values[2].set(str(self.song_info.rendaTimeHard))
        self.renda_time_values[3].set(str(self.song_info.rendaTimeMania))
        self.renda_time_values[4].set(str(self.song_info.rendaTimeUra))

        self.fuusen_total_values[0].set(self.song_info.fuusenTotalEasy)
        self.fuusen_total_values[1].set(self.song_info.fuusenTotalNormal)
        self.fuusen_total_values[2].set(self.song_info.fuusenTotalHard)
        self.fuusen_total_values[3].set(self.song_info.fuusenTotalMania)
        self.fuusen_total_values[4].set(self.song_info.fuusenTotalUra)

        self.ai_sections_values[0].set(self.song_info.aiEasy)
        self.ai_sections_values[1].set(self.song_info.aiNormal)
        self.ai_sections_values[2].set(self.song_info.aiHard)
        self.ai_sections_values[3].set(self.song_info.aiOni)
        self.ai_sections_values[4].set(self.song_info.aiUra)

        self.ai_hard_values[0].set(self.song_info.aiOniLevel11 == "o")
        self.ai_hard_values[1].set(self.song_info.aiUraLevel11 == "o")
        
        
        
        
        
        

        

    def poplate_wordlist_vars(self):
        self.song_name_var.set(self.song_info.songNameList[self.language_value.get()])
        self.song_sub_var.set(self.song_info.songSubList[self.language_value.get()])
        self.song_detail_var.set(self.song_info.songDetailList[self.language_value.get()])


if __name__ == "__main__":
    ui = Program()
    ui.run()