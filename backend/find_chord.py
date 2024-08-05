from music21 import chord, pitch, key, interval, roman

def get_chord_name(note_set, key_name=None):
    notes = []
    for n in note_set:
        try:
            if isinstance(n, str) and n:
                notes.append(pitch.Pitch(n))
            elif isinstance(n, pitch.Pitch):
                notes.append(n)
            else:
                raise ValueError(f"Invalid note format: {n}")
        except Exception:
            return "Invalid note format", None

    if not notes:
        return "No valid notes provided", None

    c = chord.Chord(notes)
    chord_name = c.pitchedCommonName
    
    # if key, call function to calculate chord relationship
    if key_name:
        chord_relation = get_chord_relationship(c, key_name)
        return chord_name, chord_relation
    else:
        return chord_name, None

def get_chord_relationship(chord_obj, key_name):
    try:
        key_obj = key.Key(key_name)
    except Exception as e:
        return f"Invalid key: {e}"
    
    # find root
    root = chord_obj.root()
    
    if not root:
        return "Cannot determine root for the chord."
    
    # compute interval between root and the tonic of key
    try:
        tonic = key_obj.tonic
        intvl = interval.Interval(noteStart=tonic, noteEnd=root)
        
        # make sure to use major key's roman numeral due to bug calculating a major or minor key's iii and III chord
        major_key_obj = key.Key(tonic.name)
    
        # get the degree of the chord relative to the key
        roman_numeral = roman.romanNumeralFromChord(chord_obj, major_key_obj)
        
        key_type = "minor" if key_obj.mode == "minor" else "major"
        
        return f"The key is {key_name} {key_type}\nThis chord is a(n) {intvl.niceName} from the tonic ({tonic.name})\nThis chord is the {roman_numeral.figure} chord in the key of {key_name}"
    except Exception as e:
        return f"Error calculating chord relationship: {e}"