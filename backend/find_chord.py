from music21 import chord, pitch, key, roman, analysis

def get_chord_name(note_set, key_name=None, simplify_chords=True):
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

    if simplify_chords:
        es = analysis.enharmonics.EnharmonicSimplifier(notes)
        notes= es.bestPitches()
    
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
    

    # key pitches as Pitch objects, normalize to be comparable
    diatonic_pitch_classes = {p.pitchClass for p in key_obj.getPitches()}
    chord_pitch_classes = {p.pitchClass for p in chord_obj.pitches}   
    isDiatonic = chord_pitch_classes.issubset(diatonic_pitch_classes)
    
    try:
        # make sure to use major key's roman numeral due to bug calculating a major or minor key's iii and III chord
        major_key_obj = key.Key(key_obj.tonic.name)
        
        roman_numeral = roman.romanNumeralFromChord(chord_obj, major_key_obj)
        key_type = "minor" if key_obj.mode == "minor" else "major"
        
        if isDiatonic:
            return f"This chord is the {roman_numeral.figure} chord in the key of {key_name} {key_type}.\nThis chord is diatonic to the key of {key_name} {key_type}"
        else:
            return f"This chord is the {roman_numeral.figure} chord in the key of {key_name} {key_type}.\nThis chord is not diatonic to the key of {key_name} {key_type}"
    except Exception as e:
        return f"Error calculating chord relationship: {e}"