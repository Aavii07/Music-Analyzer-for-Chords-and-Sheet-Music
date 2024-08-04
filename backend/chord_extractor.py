import music21

def get_score(score_path):
    try:
        return music21.converter.parse(score_path).parts
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_chords(parts):
    chords = []

    for part in parts:
        for measure in part.getElementsByClass('Measure'):
            notes_and_chords = measure.flatten().notes
            
            for element in notes_and_chords:
                if isinstance(element, music21.note.Rest):
                    continue
                
                if isinstance(element, music21.chord.Chord):
                    measure_number = element.measureNumber
                    offset = element.offset
                    chord_name = element.pitchedCommonName
                    notes = ", ".join(p.name for p in element.pitches)
                    
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
