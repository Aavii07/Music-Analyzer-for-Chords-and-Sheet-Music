from music21 import chord, pitch, key, interval

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
        except Exception as e:
            return f"Error processing note '{n}': {e}", None

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
    
    # computer interval between root and the tonic of key
    try:
        tonic = key_obj.tonic
        intvl = interval.Interval(noteStart=tonic, noteEnd=root)
        return f"This chord is a {intvl.niceName} away from tonic ({tonic.name})"
    except Exception as e:
        return f"Error calculating chord relationship: {e}"
