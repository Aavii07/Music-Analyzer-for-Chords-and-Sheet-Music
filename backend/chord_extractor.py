from music21 import converter, note, chord, pitch, analysis

def get_score(score_path):
    try:
        return converter.parse(score_path).parts
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_chords(parts, simplify_chords=True):
    chords = []

    for part in parts:
        for measure in part.getElementsByClass('Measure'):
            notes_and_chords = measure.flatten().notes
            
            for element in notes_and_chords:
                if isinstance(element, note.Rest):
                    continue
                
                if isinstance(element, chord.Chord):
                    measure_number = element.measureNumber
                    offset = element.offset
                    
                    if simplify_chords:
                        try:
                            # extract pitches and create chord
                            pitches = [p.nameWithOctave for p in element.pitches]
                            pitch_objects = [pitch.Pitch(p) for p in pitches]

                            # simplify the chord
                            es = analysis.enharmonics.EnharmonicSimplifier(pitch_objects)
                            pitch_objects = es.bestPitches()

                            # create chord object
                            c = chord.Chord(pitch_objects)
                            chord_name = c.pitchedCommonName
                        except Exception as e:
                            #print(f"Error simplifying chord: {e}")
                            chord_name = element.pitchedCommonName + " (*Simplifier Failed*)"
                    else:
                        chord_name = element.pitchedCommonName  # get chord name directly
                    
                    notes = ", ".join(p.nameWithOctave for p in element.pitches)
                    
                    chords.append((part, measure_number, offset, chord_name, notes))
                    
    return chords

# used for instruments with multiple clefs (piano, harp, etc.)
def label_consecutive_parts(parts):
    part_labels = {}
    
    for i in range(len(parts)):
        part = parts[i]
        
        if i > 0 and parts[i - 1].partName == part.partName:
            if len(part_labels) == 0 or 'Bass Clef' not in part_labels[parts[i - 1]]:
                part_labels[parts[i - 1]] = f'{parts[i - 1].partName} (Treble Clef)'
                part_labels[part] = f'{part.partName} (Bass Clef)'
            else:
                part_labels[part] = f'{part.partName} (Additional Clef)'
        else:
            part_labels[part] = part.partName or "Unknown Part"
    
    for part in parts:
        part.partName = part_labels.get(part, "Unknown Part")
    
def format_chord_sheet(chords):
    chord_sheet = ""
    for part, measure_number, beat, chord_name, notes in chords:
        part_name = part.partName or "Unknown Part"
        chord_sheet += f"Part: {part_name}, Measure {measure_number}, Beat {beat}: {chord_name}, Notes: {notes}\n"
    return chord_sheet
