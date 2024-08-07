import tkinter as tk
import re
from tkinter import ttk, filedialog
from backend.chord_extractor import get_score, label_consecutive_parts, extract_chords
from backend.find_chord import get_chord_name
from frontend.assets.virtual_keyboard import VirtualKeyboard

class MusicAnalyzer(tk.Tk):
    def __init__(self, simplify_chords=True):
        super().__init__()
        self.title("Music Analyzer")
        self.geometry("1200x700")
        self.simplify_chords = simplify_chords
        self.chord_finder_window = None
        self.enharmonics_var = tk.BooleanVar(value=True)
        self.create_widgets()

    def create_widgets(self):
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(fill=tk.X, pady=10)

        self.load_button = ttk.Button(self.header_frame, text="Load MusicXML File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.find_chord_button = ttk.Button(self.header_frame, text="Find Chord", command=self.open_chord_finder)
        self.find_chord_button.pack(side=tk.RIGHT, padx=10)

        self.filters_frame = ttk.Frame(self)
        self.filters_frame.pack(pady=10)

        # part filter
        self.part_label = ttk.Label(self.filters_frame, text="Part:")
        self.part_label.grid(row=0, column=0, padx=5)
        self.part_entry = ttk.Entry(self.filters_frame)
        self.part_entry.grid(row=0, column=1, padx=5)
        self.part_entry.bind("<KeyRelease>", self.apply_filters)

        # measure filters
        self.measure_from_label = ttk.Label(self.filters_frame, text="From measure:")
        self.measure_from_label.grid(row=0, column=2, padx=5)
        self.measure_from_entry = ttk.Entry(self.filters_frame)
        self.measure_from_entry.grid(row=0, column=3, padx=5)
        self.measure_from_entry.bind("<KeyRelease>", self.apply_filters)

        self.measure_until_label = ttk.Label(self.filters_frame, text="Until measure:")
        self.measure_until_label.grid(row=0, column=4, padx=5)
        self.measure_until_entry = ttk.Entry(self.filters_frame)
        self.measure_until_entry.grid(row=0, column=5, padx=5)
        self.measure_until_entry.bind("<KeyRelease>", self.apply_filters)

        # beat filters
        self.beat_from_label = ttk.Label(self.filters_frame, text="From beat:")
        self.beat_from_label.grid(row=1, column=2, padx=5)
        self.beat_from_entry = ttk.Entry(self.filters_frame)
        self.beat_from_entry.grid(row=1, column=3, padx=5)
        self.beat_from_entry.bind("<KeyRelease>", self.apply_filters)

        self.beat_until_label = ttk.Label(self.filters_frame, text="Until beat:")
        self.beat_until_label.grid(row=1, column=4, padx=5)
        self.beat_until_entry = ttk.Entry(self.filters_frame)
        self.beat_until_entry.grid(row=1, column=5, padx=5)
        self.beat_until_entry.bind("<KeyRelease>", self.apply_filters)

        # chord name filter
        self.chord_label = ttk.Label(self.filters_frame, text="Chord Name:")
        self.chord_label.grid(row=1, column=0, padx=5)
        self.chord_entry = ttk.Entry(self.filters_frame)
        self.chord_entry.grid(row=1, column=1, padx=5)
        self.chord_entry.bind("<KeyRelease>", self.apply_filters)

        # table
        self.tree = ttk.Treeview(self, columns=("Part", "Measure", "Beat", "Chord Name", "Notes"), show="headings")
        self.tree.heading("Part", text="Part")
        self.tree.heading("Measure", text="Measure")
        self.tree.heading("Beat", text="Beat")
        self.tree.heading("Chord Name", text="Chord Name")
        self.tree.heading("Notes", text="Notes (low to high)")
        
        # column widths and stretch
        self.tree.column("Part", width=200, stretch=tk.NO)
        self.tree.column("Measure", width=80, stretch=tk.NO)
        self.tree.column("Beat", width=80, stretch=tk.NO)
        self.tree.column("Chord Name", width=400, stretch=tk.YES)
        self.tree.column("Notes", width=200, stretch=tk.YES)      
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.tag_configure("padding", font=("Arial", 16))
        
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        # enharmonics toggle
        self.toggle_frame = ttk.Frame(self)
        self.toggle_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.toggle_button = ttk.Checkbutton(
            self.toggle_frame,
            text="Use Enharmonics Simplifier During Extraction",
            command=self.toggle_enharmonics,
            variable=self.enharmonics_var
        )
        self.toggle_button.pack(side=tk.LEFT, padx=10, pady=10)


    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("MusicXML Files", "*.musicxml"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            parts = get_score(file_path)
            if parts:
                label_consecutive_parts(parts)
                self.chords = extract_chords(parts, self.simplify_chords)
                self.update_table(self.chords)
                
    def apply_filters(self, event=None):
        part_filter = self.part_entry.get().lower()
        measure_from_filter = self.measure_from_entry.get()
        measure_until_filter = self.measure_until_entry.get()
        beat_from_filter = self.beat_from_entry.get()
        beat_until_filter = self.beat_until_entry.get()
        chord_filter = self.chord_entry.get().lower()

        filtered_chords = [chord for chord in self.chords
                           if (part_filter in chord[0].partName.lower() if part_filter else True) and
                           (measure_from_filter.isdigit() and int(measure_from_filter) <= chord[1] or not measure_from_filter) and
                           (measure_until_filter.isdigit() and chord[1] <= int(measure_until_filter) or not measure_until_filter) and
                           (beat_from_filter.isdigit() and int(beat_from_filter) <= chord[2] or not beat_from_filter) and
                           (beat_until_filter.isdigit() and chord[2] <= int(beat_until_filter) or not beat_until_filter) and
                           (chord_filter in chord[3].lower() if chord_filter else True)]

        self.update_table(filtered_chords)

    def update_table(self, chords):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for part, measure_number, offset, chord_name, notes in chords:
            part_name = part.partName or "Unknown Part"
            self.tree.insert("", "end", values=(part_name, measure_number, offset, chord_name, notes), tags=("padding"))

    def on_tree_double_click(self, event):
        if self.chord_finder_window and self.chord_finder_window.winfo_exists():
            self.chord_finder_window.destroy()
        
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        notes = values[4]  # notes are in the 5th column
        self.open_chord_finder(notes)
        self.after(10, self.update_chord_name) # need to use after few milliseconds to refresh
    
    def open_chord_finder(self, notes=""):
        
        self.chord_finder_window = tk.Toplevel(self)
        self.chord_finder_window.title("Chord Finder")
        self.chord_finder_window.geometry("1350x600")

        # Notes input field
        self.notes_label = ttk.Label(self.chord_finder_window, text="Enter Notes (comma-separated):")
        self.notes_label.pack(pady=10)
        self.notes_entry = ttk.Entry(self.chord_finder_window)
        self.notes_entry.pack(pady=10, padx=20, fill=tk.X)
        
        if notes: # insert notes if exist
            self.notes_entry.insert(0, notes)
            self.update_idletasks()
            self.update_chord_name
            
        self.notes_entry.bind("<KeyRelease>", self.update_chord_name)

        # Key input field
        self.key_label = ttk.Label(self.chord_finder_window, text="Enter Key (e.g., C):")
        self.key_label.pack(pady=10)
        self.key_entry = ttk.Entry(self.chord_finder_window)
        self.key_entry.pack(pady=10, padx=20, fill=tk.X)
        self.key_entry.bind("<KeyRelease>", self.update_chord_name)

        # Display chord name
        self.chord_name_label = ttk.Label(self.chord_finder_window, text="Chord Name:", font=("Helvetica", 22))
        self.chord_name_label.pack(pady=10)
        self.chord_name_display = ttk.Label(self.chord_finder_window, text="", font=("Helvetica", 18))
        self.chord_name_display.pack(pady=10)

        # Display chord relationship
        self.chord_relation_label = ttk.Label(self.chord_finder_window, text="Chord Relationship:", font=("Helvetica", 22))
        self.chord_relation_label.pack(pady=10)
        self.chord_relation_display = ttk.Label(self.chord_finder_window, text="", font=("Helvetica", 18))
        self.chord_relation_display.pack(pady=10)

        # Virtual keyboard
        self.virtual_keyboard = VirtualKeyboard(self.chord_finder_window)
        self.virtual_keyboard.pack(pady=20)

        # Info button
        self.info_button = ttk.Button(self.chord_finder_window, text="Info", command=self.show_info)
        self.info_button.pack(pady=10)

        # Enharmonics toggle
        self.toggle_button = ttk.Checkbutton(
            self.chord_finder_window, 
            text="Enharmonics Simplifier", 
            command=self.toggle_enharmonics,
            variable=self.enharmonics_var
        )
        self.toggle_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.chord_finder_window.protocol("WM_DELETE_WINDOW", self.on_chord_finder_close)
    
    def on_chord_finder_close(self):
        if self.chord_finder_window and self.chord_finder_window.winfo_exists():
            self.chord_finder_window.destroy()
            self.chord_finder_window = None
    
    def toggle_enharmonics(self):
        self.simplify_chords = not self.simplify_chords
        if self.chord_finder_window and self.chord_finder_window.winfo_exists():
            self.after(10, self.update_chord_name)

    def show_info(self):
        info_window = tk.Toplevel(self)
        info_window.title("Information")
        info_window.geometry("500x400")

        # make window modal
        info_window.transient(self)
        info_window.grab_set() 

        content_frame = ttk.Frame(info_window)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        info_text = ("Notes about the Chord Finder\n\n"
                    "Notes should be entered as a comma-seperated list (like a1, c#2, e2)\n\n"
                    "Using '-' or 'b' denotes flat while '#' denotes sharp.\n" 
                    "Sharping/flating notes multiple times are supported, but it won't appear on the keyboard.\n\n"
                    "For more granularity, end the note with a number to denote the exact note (like A#4 instead of A#)\n" 
                    "If you do not do this, all notes are all assumed to be in the 4th octave\n\n"
                    "Scales can also be entered here too\n"
                    "Just note that the tool does not distinguish between major and mino scales too well")

        info_label = ttk.Label(content_frame, text=info_text, wraplength=400, justify=tk.LEFT)
        info_label.pack(fill=tk.BOTH, expand=True)

        ok_button = ttk.Button(info_window, text="OK", command=info_window.destroy)
        ok_button.pack(side=tk.BOTTOM, pady=10)

        info_window.wait_window()
        
    def update_chord_name(self, event=None):
        notes_input = self.notes_entry.get().strip()
        key_input = self.key_entry.get().strip()
        
        notes_list = [note.strip() for note in notes_input.split(',') if note.strip()]
        note_set = set(notes_list)
        
        chord_name, chord_relation = get_chord_name(note_set, key_input, self.simplify_chords)
        
        self.chord_name_display.config(text=chord_name)
        if chord_relation:
            relation_text = chord_relation
        else:
            relation_text = "No key and/or chord provided"
        self.chord_relation_display.config(text=relation_text)
        
        # reset key colors before highlighting new ones
        self.virtual_keyboard.reset_all_keys()       
        
        # highlight the new keys
        for note in note_set:
            upperCaseNote = note = re.sub(r'^([a-z])', lambda x: x.group(1).upper(), note) # music21 only recognizes uppercase notes
            if not re.search(r'\d$', upperCaseNote):
                upperCaseNote += '4'  # music21 defaults to 4th octave if no exact note specified
                
            self.virtual_keyboard.highlight_key(upperCaseNote)
            

