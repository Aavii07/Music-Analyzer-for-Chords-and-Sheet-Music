from music21 import chord, pitch, key, roman, analysis
import re

def get_chord_name(note_set, key_name=None, simplify_numeral=True, simplify_chords=True):
    notes = []
    invalid_note_pattern = re.compile(r'\d.*\d')  
    
    for n in note_set:
        try:
            if isinstance(n, str) and n:
                if invalid_note_pattern.search(n):
                    raise ValueError(f"Invalid note format with multiple numbers: {n}")
                notes.append(pitch.Pitch(n))
            elif isinstance(n, pitch.Pitch):
                notes.append(n)
            else:
                raise ValueError(f"Invalid note format: {n}")
        except Exception as e:
            return f"{e}", None
    
    if not notes:
        return "No valid notes provided", None

    # prevent lag
    if len(notes) > 16:
        return "Chord cannot exceed 16 notes", None
              
    if simplify_chords:
        pitch_list = [] 
        for note in notes:
            p = pitch.Pitch(note)
            pitch_list.append(p) 

        # simplify the pitch list (for notes with 2+ accidentals)
        simplified_notes = [str(p.simplifyEnharmonic(mostCommon=True)) for p in pitch_list]
        es = analysis.enharmonics.EnharmonicSimplifier(simplified_notes)
        notes= es.bestPitches()

    c = chord.Chord(notes)
    chord_name = c.pitchedCommonName
    
    # music21 always gets scales wrong for some reason
    if re.search(r'\bscale\b', chord_name, re.IGNORECASE):
          return "Scales unsupported", None
    
    # if key, call function to calculate chord relationship
    if key_name:
        chord_relation = get_chord_relationship(c, key_name, simplify_numeral)
        return chord_name, chord_relation
    else:
        return chord_name, None

def get_chord_relationship(chord_obj, key_name, simplify_numeral):
    
    try:
        key_obj = key.Key(key_name)
    except Exception as e:
        return "Invalid key"
    
    # extract first letter from key_name and make it uppercase
    match = re.search(r'(\w)', key_name)
    if match:
        key_name_uppercase = match.group(1).upper()
    else:
        key_name_uppercase = None
    

    # key pitches as Pitch objects, normalize to be comparable
    diatonic_pitch_classes = {p.pitchClass for p in key_obj.getPitches()}
    chord_pitch_classes = {p.pitchClass for p in chord_obj.pitches}   
    isDiatonic = chord_pitch_classes.issubset(diatonic_pitch_classes)
    
    try:
        # make sure to use major key's roman numeral due to bug calculating a major or minor key's iii and III chord
        major_key_obj = key.Key(key_obj.tonic.name)
        
        roman_numeral = roman.romanNumeralFromChord(chord_obj, major_key_obj).figure
        if simplify_numeral:
            # extract the Roman numeral and sharps/flats at the beginning
            numeral_match = re.match(r'^[#b\-]*[ivIV]+', roman_numeral)
            if numeral_match:
                simplified_numeral = numeral_match.group()
                roman_numeral = simplified_numeral
        
        key_type = "minor" if key_obj.mode == "minor" else "major"
        
        if isDiatonic:
            return f"This chord is the {roman_numeral} chord in the key of {key_name_uppercase}\nThis chord is diatonic to the key of {key_name_uppercase} {key_type}"
        else:
            return f"This chord is the {roman_numeral} chord in the key of {key_name_uppercase}\nThis chord is not diatonic to the key of {key_name_uppercase} {key_type}"
    except Exception as e:
        return f"Error calculating chord relationship: {e}"