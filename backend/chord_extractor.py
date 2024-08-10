from music21 import converter, note, chord

def get_score_parts(score_path):
    try:
        return converter.parse(score_path).parts
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_chords(parts):
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
                    chord_name = element.pitchedCommonName
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
    

