import tkinter as tk
from tkinter import ttk
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

class Ui:
    window: tk.Tk
    frame: tk.Frame

    #Grids
    song_details_frame: tk.LabelFrame
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

    #Combobox
    genre_combobox: ttk.Combobox
    #ai_sections_comboboxes: List[ttk.Combobox]

    #Spinbox
    unique_id_spinbox: tk.Spinbox
    star_spinboxes: List[tk.Spinbox]
    shinuchi_spinboxes: List[tk.Spinbox]
    shinuchi_score_spinboxes: List[tk.Spinbox]
    onpu_num_spinboxes: List[tk.Spinbox]
    fuusen_total_spinboxes: List[tk.Spinbox]

    #Checkbutton
    new_checkbutton: tk.Checkbutton
    can_play_ura_checkbutton: tk.Checkbutton
    branch_checkbuttons: List[tk.Checkbutton]
    ai_hard_checkbuttons: List[tk.Checkbutton] 

    #Button
    music_order_button: tk.Button

    #Radio Buttons
    ai_sections_frames: List[tk.Frame]
    ai_sections_radiobuttons: List[List[tk.Radiobutton]]
    ai_sections_values: List[tk.IntVar]

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Keifun's Datatable Editor")
        #self.window.geometry("1280x720")  # Set window size to 720p

        self.songid_label = tk.Label(self.window, text="Song Id:")
        self.songid_entry = tk.Entry(self.window)

        self.songid_label.grid(row=0, column=0)
        self.songid_entry.grid(row=1, column=0)
        
        ### Song Details ###
        self.song_details_frame = tk.LabelFrame(self.window, text="Song Details", padx=20, pady=20)
        self.song_details_frame.grid(row=2, column=0)

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

        #Set Entries
        self.song_name_entry = tk.Entry(self.song_details_frame)
        self.song_name_entry.grid(row=1, column=0)
        self.song_sub_entry = tk.Entry(self.song_details_frame)
        self.song_sub_entry.grid(row=3, column=0)
        self.song_detail_entry = tk.Entry(self.song_details_frame)
        self.song_detail_entry.grid(row=5, column=0)
        self.song_filename_entry = tk.Entry(self.song_details_frame)
        self.song_filename_entry.grid(row=1, column=1)
        self.new_checkbutton = tk.Checkbutton(self.song_details_frame, text="New")
        self.new_checkbutton.grid(row=2, column=1)
        self.can_play_ura_checkbutton = tk.Checkbutton(self.song_details_frame, text="Ura Playable")
        self.can_play_ura_checkbutton.grid(row=3, column=1)
        self.music_order_button = tk.Button(self.song_details_frame, text="Set Music Order")
        self.music_order_button.grid(row=4, column=1)

        #Set Spinbox
        self.unique_id_spinbox = tk.Spinbox(self.song_details_frame, from_=0, to=9999)
        self.unique_id_spinbox.grid(row=7, column = 0)
        
        #Set Combobox
        self.genre_combobox = ttk.Combobox(self.song_details_frame, values=list(GENRE_MAPPING.keys()))
        self.genre_combobox.grid(row=9, column=0)
        

        #Set Padding for each element in song_details_frame

        for widget in self.song_details_frame.winfo_children():
            widget.grid_configure(padx=5, pady=1)


        ### Difficulty Info ###
        self.difficulty_info_frame = tk.LabelFrame(self.window, text="Difficulty Info", padx=20, pady=20)
        self.difficulty_info_frame.grid(row=3, column=0)
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
        self.star_spinboxes = list()
        self.shinuchi_spinboxes = list()
        self.shinuchi_score_spinboxes = list()
        self.onpu_num_spinboxes = list()
        self.renda_time_entries = list()
        self.fuusen_total_spinboxes = list()
        self.ai_sections_comboboxes = list()
        self.ai_sections_frames = list()
        self.ai_sections_radiobuttons = list()
        self.ai_sections_values = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        for e in self.ai_sections_values:
            e.set(3)
        self.ai_hard_checkbuttons = list()

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

            self.branch_checkbuttons.append(tk.Checkbutton(self.difficulty_info_sub_frames[i], text="Branch", width=20, anchor='w')) 
            self.star_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=0, to=10))
            self.shinuchi_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=1, to=99999999))
            self.shinuchi_score_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=1, to=99999999))
            self.onpu_num_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=0, to=99999999))
            self.renda_time_entries.append(tk.Entry(self.difficulty_info_sub_frames[i]))
            self.fuusen_total_spinboxes.append(tk.Spinbox(self.difficulty_info_sub_frames[i], from_=0, to=99999999))
            #self.ai_sections_comboboxes.append(ttk.Combobox(self.difficulty_info_sub_frames[i], values=['3','5']))
            self.ai_sections_frames.append(tk.Frame(self.difficulty_info_sub_frames[i]))
            self.ai_sections_radiobuttons.append(
                [
                    tk.Radiobutton(self.ai_sections_frames[i], text="3", variable=self.ai_sections_values[i], value=3),
                    tk.Radiobutton(self.ai_sections_frames[i], text="5", variable=self.ai_sections_values[i], value=5)
                ]
            )

            if i >= 3:
                self.ai_hard_checkbuttons.append(tk.Checkbutton(self.ai_sections_frames[i], text="Hard"))
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
            

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    ui = Ui()
    ui.run()