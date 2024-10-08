import customtkinter as ctk
import pygame
import sys, os

class VirtualKeyboard(ctk.CTkFrame):
    def __init__(self, parent, update_chord_callback, sound, sustain, free_play, color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = ctk.CTkCanvas(self, bg='white', height=97, width=1297)
        self.canvas.pack(fill=ctk.BOTH, expand=True)
        self.convert_enharmonics = False
        self.note_to_key_mapping = self.create_note_to_key_mapping()
        self.key_click_state = {} 
        self.last_clicked_note = None
        self.update_chord_callback = update_chord_callback
        self.sound = sound
        self.sustain = sustain
        self.free_play = free_play
        self.color = color
        self.create_keys()
        pygame.mixer.init()
        self.current_sounds = []
        self.current_sound = None
        self.note_sounds = self.load_note_sounds()
    
    def load_note_sounds(self):
        note_sounds = {}

        if hasattr(sys, '_MEIPASS'):
            base_path = os.path.join(sys._MEIPASS, 'sounds')
        else:
            base_path = 'sounds'

        for note in self.note_to_key_mapping.keys():
            try:
                sound_file_path = os.path.join(base_path, f'{note}.wav')
                note_sounds[note] = pygame.mixer.Sound(sound_file_path)
            except pygame.error:
                print(f"Sound file for {note} not found: {sound_file_path}")
        return note_sounds

    def play_note_sound(self, note):
        sound = self.note_sounds.get(note)
        if not sound:
            return
        
        if self.sustain:
            # prevent sound layering with same notes
            for current_sound in self.current_sounds:
                if current_sound.get_raw() == sound.get_raw():
                    current_sound.stop()
                    self.current_sounds.remove(current_sound)
                    break

            if len(self.current_sounds) >= 8:  # pygame only has 8 sound channels
                old_sound = self.current_sounds.pop(0)
                old_sound.stop()

            self.current_sounds.append(sound)
            sound.play()
        
        else:
            if self.current_sound:
                self.current_sound.stop()

            sound = self.note_sounds.get(note)
            if sound:
                self.current_sound = sound
                sound.play()

    def create_keys(self):
        self.keys = {}
        white_key_width = 25
        white_key_height = 100
        black_key_width = 15
        black_key_height = 60
        black_keys_offset = 8
        border_width = 1
        
        # create white keys
        for i in range(52):
            x = i * white_key_width
            
            key_id = self.canvas.create_rectangle(
                x, 0, x + white_key_width, white_key_height, 
                fill='white', 
                outline = 'black',
                width = border_width)
            
            self.keys[f'Wh{i + 1}'] = key_id
            self.key_click_state[key_id] = 0
            self.canvas.tag_bind(key_id, "<Button-1>", self.key_click_handler)
        
        # create black keys
        for i in range(51):
            if i not in (1, 4, 8, 11, 15, 18, 22, 25, 29, 32, 36, 39, 43, 46, 50):  # skip certain black keys
                x = (i + 1) * white_key_width - black_keys_offset
                
                key_id = self.canvas.create_rectangle(
                    x, 0, x + black_key_width, 
                    black_key_height, fill='black', 
                    outline = 'black', 
                    tags='black',
                    width = border_width)
                
                self.keys[f'Bl{i + 1}'] = key_id
                self.key_click_state[key_id] = 0
                self.canvas.tag_bind(key_id, "<Button-1>", self.key_click_handler)
    
    def create_note_to_key_mapping(self):
        # Map music21 notes to keys
        # note that every c and b# note was swapped around from their respective octaves to make sure that
        # c is found first before b# when mapping backwards to note
        return {
            # Octave 0
            'A0': 'Wh1', 'B0': 'Wh2',
            'A#0': 'Bl1', 'C1': 'Wh3',
            'B-0': 'Bl1', 
            'Bb0': 'Bl1',
            
            # Octave 1
            'B#0': 'Wh3', 'D1': 'Wh4', 'E1': 'Wh5', 'F1': 'Wh6', 'G1': 'Wh7', 'A1': 'Wh8', 'B1': 'Wh9',
            'C#1': 'Bl3', 'D#1': 'Bl4', 'E#1': 'Wh6', 'F#1': 'Bl6', 'G#1': 'Bl7', 'A#1': 'Bl8', 'C2': 'Wh10',
            'D-1': 'Bl3', 'E-1': 'Bl4', 'F-1': 'Wh5', 'G-1': 'Bl6', 'A-1': 'Bl7', 'B-1': 'Bl8', 'C-1': 'Wh2',
            'Db1': 'Bl3', 'Eb1': 'Bl4', 'Fb1': 'Wh5', 'Gb1': 'Bl6', 'Ab1': 'Bl7', 'Bb1': 'Bl8', 'Cb1': 'Wh2',
            
            # Octave 2
            'B#1': 'Wh10', 'D2': 'Wh11', 'E2': 'Wh12', 'F2': 'Wh13', 'G2': 'Wh14', 'A2': 'Wh15', 'B2': 'Wh16',
            'C#2': 'Bl10', 'D#2': 'Bl11', 'E#2': 'Wh13', 'F#2': 'Bl13', 'G#2': 'Bl14', 'A#2': 'Bl15', 'C3': 'Wh17',
            'D-2': 'Bl10', 'E-2': 'Bl11', 'F-2': 'Wh12', 'G-2': 'Bl13', 'A-2': 'Bl14', 'B-2': 'Bl15', 'C-2': 'Wh9',
            'Db2': 'Bl10', 'Eb2': 'Bl11', 'Fb2': 'Wh12', 'Gb2': 'Bl13', 'Ab2': 'Bl14', 'Bb2': 'Bl15', 'Cb2': 'Wh9',
            
            # Octave 3
            'B#2': 'Wh17', 'D3': 'Wh18', 'E3': 'Wh19', 'F3': 'Wh20', 'G3': 'Wh21', 'A3': 'Wh22', 'B3': 'Wh23',
            'C#3': 'Bl17', 'D#3': 'Bl18', 'E#3': 'Wh20', 'F#3': 'Bl20', 'G#3': 'Bl21', 'A#3': 'Bl22', 'C4': 'Wh24',
            'D-3': 'Bl17', 'E-3': 'Bl18', 'F-3': 'Wh19', 'G-3': 'Bl20', 'A-3': 'Bl21', 'B-3': 'Bl22', 'C-3': 'Wh16',
            'Db3': 'Bl17', 'Eb3': 'Bl18', 'Fb3': 'Wh19', 'Gb3': 'Bl20', 'Ab3': 'Bl21', 'Bb3': 'Bl22', 'Cb3': 'Wh16',
            
            # Octave 4
            'B#3': 'Wh24', 'D4': 'Wh25', 'E4': 'Wh26', 'F4': 'Wh27', 'G4': 'Wh28', 'A4': 'Wh29', 'B4': 'Wh30',
            'C#4': 'Bl24', 'D#4': 'Bl25', 'E#4': 'Wh27', 'F#4': 'Bl27', 'G#4': 'Bl28', 'A#4': 'Bl29', 'C5': 'Wh31',
            'D-4': 'Bl24', 'E-4': 'Bl25', 'F-4': 'Wh26', 'G-4': 'Bl27', 'A-4': 'Bl28', 'B-4': 'Bl29', 'C-4': 'Wh23',
            'Db4': 'Bl24', 'Eb4': 'Bl25', 'Fb4': 'Wh26', 'Gb4': 'Bl27', 'Ab4': 'Bl28', 'Bb4': 'Bl29', 'Cb4': 'Wh23',
            
            # Octave 5
            'B#4': 'Wh31', 'D5': 'Wh32', 'E5': 'Wh33', 'F5': 'Wh34', 'G5': 'Wh35', 'A5': 'Wh36', 'B5': 'Wh37',
            'C#5': 'Bl31', 'D#5': 'Bl32', 'E#5': 'Wh34', 'F#5': 'Bl34', 'G#5': 'Bl35', 'A#5': 'Bl36', 'C6': 'Wh38',
            'D-5': 'Bl31', 'E-5': 'Bl32', 'F-5': 'Wh33', 'G-5': 'Bl34', 'A-5': 'Bl35', 'B-5': 'Bl36', 'C-5': 'Wh30',
            'Db5': 'Bl31', 'Eb5': 'Bl32', 'Gb5': 'Bl34', 'Ab5': 'Bl35', 'Bb5': 'Bl36', 'Cb5': 'Wh30', 'Fb5': 'Wh33',
            
            # Octave 6
            'B#5': 'Wh38', 'D6': 'Wh39', 'E6': 'Wh40', 'F6': 'Wh41', 'G6': 'Wh42', 'A6': 'Wh43', 'B6': 'Wh44',
            'C#6': 'Bl38', 'D#6': 'Bl39', 'E#6': 'Wh41', 'F#6': 'Bl41', 'G#6': 'Bl42', 'A#6': 'Bl43', 'C7': 'Wh45',
            'D-6': 'Bl38', 'E-6': 'Bl39', 'F-6': 'Wh40', 'G-6': 'Bl41', 'A-6': 'Bl42', 'B-6': 'Bl43', 'C-6': 'Wh37',
            'Db6': 'Bl38', 'Eb6': 'Bl39', 'Fb6': 'Wh40', 'Gb6': 'Bl41', 'Ab6': 'Bl42', 'Bb6': 'Bl43', 'Cb6': 'Wh37',
            
            # Octave 7
            'B#6': 'Wh45', 'D7': 'Wh46', 'E7': 'Wh47', 'F7': 'Wh48', 'G7': 'Wh49', 'A7': 'Wh50', 'B7': 'Wh51',
            'C#7': 'Bl45', 'D#7': 'Bl46', 'E#7': 'Wh48', 'F#7': 'Bl48', 'G#7': 'Bl49', 'A#7': 'Bl50', 'C8': 'Wh52',
            'D-7': 'Bl45', 'E-7': 'Bl46', 'F-7': 'Wh47', 'G-7': 'Bl48', 'A-7': 'Bl49', 'B-7': 'Bl50', 'C-7': 'Wh44',
            'Db7': 'Bl45', 'Eb7': 'Bl46', 'Fb7': 'Wh47', 'Gb7': 'Bl48', 'Ab7': 'Bl49', 'Bb7': 'Bl50', 'Cb7': 'Wh44', 
            
            # Octave 8
            'B#7': 'Wh52',
            'C-8': 'Wh51',
            'Cb8': 'Wh51',
        }
        
    def note_to_key(self, note):
        return self.note_to_key_mapping.get(note, None)
    
    def get_note_from_key(self, key, second_mapping=False):
        notes = [note for note, mapped_key in self.note_to_key_mapping.items() if mapped_key == key]
        
        if second_mapping and len(notes) > 1:
            return notes[1]  
        elif len(notes) > 0:
            return notes[0]
        return None
    
    def highlight_key(self, note, highlight=True): 
        key = self.note_to_key(note)
        
        if note is not None:
            key_id = self.keys.get(key)
            if key_id:
                if highlight:
                    color = self.color
                self.canvas.itemconfig(key_id, fill=color)
    
    
    def reset_all_keys(self):
        for key_id in self.keys.values():
            if self.canvas.itemcget(key_id, 'fill') == self.color:
                if 'black' in self.canvas.gettags(key_id):
                    self.canvas.itemconfig(key_id, fill='black')
                else:
                    self.canvas.itemconfig(key_id, fill='white')
    
    def key_click_handler(self, event):
        x, y = event.x, event.y
        clicked_item = self.canvas.find_closest(x, y)[0]
        for key, key_id in self.keys.items():
            if key_id == clicked_item:
                
                note = self.get_note_from_key(key)
                shift_held = event.state & 0x0001
                if shift_held:
                    note = self.get_note_from_key(key, second_mapping=True)
                
                self.last_clicked_note = note
                
                if self.free_play:
                    self.play_note_sound(note)
                else:
                    key_color = self.canvas.itemcget(key_id, 'fill')
                    if self.sound and key_color != self.color:
                        self.play_note_sound(note)
                    
                    self.update_chord_callback(keyboard_triggered=True)
    
    def toggle_sound(self, sound):
        self.sound = sound
        
    def toggle_sustain(self, sustain):
        self.sustain = sustain
        
        # simulate letting go of sustain pedal, most recent note still plays to be less jarring
        if (self.sustain == False):
            for s in self.current_sounds[:-1]:
                s.stop()
        
    def toggle_free_play(self, free_play):
        self.free_play = free_play
    
    def setColor(self, color):
        self.color = color

            