# Guitar chord analyzer and finder

# To-do:
# Fix slash chords for the same root note, e.g.:
    # print(eadgbe(0,4,2,0,2,0))

# Intervals relevant to chord analysis
interval_dict = {
    0: 'root',
    1: 'minor 2nd',
    2: 'major 2nd',
    3: 'minor 3rd',
    4: 'major 3rd',
    5: 'perfect 4th',
    6: 'tritone',
    7: 'perfect 5th',
    8: 'minor 6th',
    9: 'major 6th',
    10: 'minor 7th',
    11: 'major 7th',
    13: 'minor 9th',
    14: 'major 9th',
    17: 'perfect 11th',
    20: 'minor 13th',
    21: 'major 13th'
}

# List of chord types roughly in order of likelihood so as to penalize slash interpretations
chord_dict = {
    "Major": ['root', 'major 3rd', 'perfect 5th'],
    "Minor": ['root', 'minor 3rd', 'perfect 5th'],
    "Major 7": ['root', 'major 3rd', 'perfect 5th', 'major 7th'],
    "Minor 7": ['root', 'minor 3rd', 'perfect 5th', 'minor 7th'],
    "7": ['root', 'major 3rd', 'perfect 5th', 'minor 7th'],
    "add 9": ['root', 'major 3rd', 'perfect 5th', 'major 9th'],
    "Major 9": ['root', 'major 3rd', 'perfect 5th', 'major 7th', 'major 9th'],
    "9": ['root', 'major 3rd', 'perfect 5th', 'minor 7th', 'major 9th'],
    "flat 9": ['root', 'major 3rd', 'perfect 5th', 'minor 7th', 'minor 9th'],
    "Minor add 9": ['root', 'minor 3rd', 'perfect 5th', 'major 9th'],
    "Minor 9": ['root', 'minor 3rd', 'perfect 5th', 'minor 7th', 'major 9th'],
    "Minor Major 9": ['root', 'minor 3rd', 'perfect 5th', 'major 7th', 'major 9th'],
    "add 11": ['root', 'major 3rd', 'perfect 5th', 'perfect 11th'],
    "add sharp 11": ['root', 'major 3rd', 'perfect 5th', 'tritone'],    
    "Major 11": ['root', 'major 3rd', 'perfect 5th', 'major 7th', 'perfect 11th'],
    "Major sharp 11th": ['root', 'major 3rd', 'perfect 5th', 'major 7th', 'tritone'],
    "11": ['root', 'major 3rd', 'perfect 5th', 'minor 7th', 'major 9th', 'perfect 11th'],
    "Minor 11": ['root', 'minor 3rd', 'perfect 5th', 'minor 7th', 'perfect 11th'],
    "Sus 4": ['root', 'perfect 4th', 'perfect 5th'],
    "Sus 2": ['root', 'major 2nd', 'perfect 5th'],
    "Major add 4": ['root', 'major 3rd','perfect 4th', 'perfect 5th'],
    "Major add 2": ['root', 'major 2nd', 'major 3rd','perfect 5th'],
    "Minor add 4": ['root', 'minor 3rd','perfect 4th', 'perfect 5th'],
    "Minor add 2": ['root', 'major 2nd', 'minor 3rd','perfect 5th'],
    "6": ['root', 'major 3rd', 'perfect 5th', 'major 6th', 'major 13th'],
    "6/9": ['root', 'major 3rd', 'perfect 5th', 'major 6th', 'major 9th'],
    "Minor 6": ['root', 'minor 3rd', 'perfect 5th', 'major 6th'],
    "Diminished 7": ['root', 'minor 3rd', 'tritone', 'major 6th'],
    "Half Diminished 7": ['root', 'minor 3rd', 'tritone', 'minor 7th'],
    "Minor Major 7": ['root', 'minor 3rd', 'perfect 5th', 'major 7th'],
    "Diminished": ['root', 'minor 3rd', 'tritone'],
    "Augmented": ['root', 'major 3rd', 'minor 6th'],
    "Augmented 7": ['root', 'major 3rd', 'minor 6th', 'minor 7th'],
    "13": ['root', 'major 3rd', 'perfect 5th', 'minor 7th', 'major 9th', 'perfect 11th', 'major 13th'],
    "Minor 13": ['root', 'minor 3rd', 'perfect 5th', 'minor 7th', 'major 9th', 'major 13th', 'major 6th'],
    "Major 13": ['root', 'major 3rd', 'perfect 5th', 'major 7th', 'major 9th', 'perfect 11th', 'major 13th', 'major 6th'],
    # Add more chords as needed
}

# To label outputs with note names instead of numbers
note_dict = {
    0: 'E',
    1: 'F',
    2: 'F#',
    3: 'G',
    4: 'Ab',
    5: 'A',
    6: 'Bb',
    7: 'B',
    8: 'C',
    9: 'C#',
    10: 'D',
    11: 'Eb'
}

# Primary analysis function
def eadgbe(e='x',a='x',d='x',g='x',b='x',e2='x'):
    # Convert numbers to notes
    inputs = [e, a, d, g, b, e2]
    string_tunings = [0, 5, 10, 15, 19, 24]
    notes = []
    for i, string in zip(inputs, string_tunings):
        if isinstance(i, int):
            i += string
            notes.append(i)
    notes.sort()
    # Variables to store the best match and its index
    best_match = None
    best_index = len(chord_dict)  # Set initial index as the length of chord_dict

    # Identify the lowest note (for potential slash chords)
    lowest_note = min(notes)

    # Make a copy of original notes to adjust
    adjusted_notes = notes.copy()
    
    for j in range(len(notes)):
        # If chord is a slash chord or not
        slash = False

         # If current note isn't lowest, add two octaves to lower notes
        if notes[j] != min(notes):
            adjusted_notes[j] -= 12
            slash = True

        # Calculate intervals from current root note
        intervals = [(note - adjusted_notes[j]) for note in adjusted_notes if note != lowest_note]

        # Look up each interval in the dictionary
        interval_labels = []
        for i in intervals:
            # Handle large intervals not in the dictionary explicitly and negatives
            if i not in interval_dict:
                i -= 12
                if i not in interval_dict:
                    i = i % 12
            interval_labels.append(interval_dict[i])
        root_name = note_dict[adjusted_notes[j] % 12]

        for chord, chord_intervals in chord_dict.items():
            if set(interval_labels).issubset(set(chord_intervals)):
                chord_index = list(chord_dict.keys()).index(chord)
                # Penalty for slash chords
                if slash == True:
                    chord_index += 6
                # If current chord comes before the best match, update best match
                if chord_index < best_index:
                    best_index = chord_index
                    best_match = root_name + ' ' + chord
                    if slash:
                        best_match += '/' + note_dict[min(notes) % 12]
        
        # Reset adjusted_notes to original notes
        adjusted_notes = notes.copy()

    return best_match if best_match else "No match found"

# Dictonary to help convert tuning systems
tuning_dict = {
    "E": [0],
    "F": [1],
    "F#": [2],
    "Gb": [2],
    "G": [3],
    "G#": [4],
    "Ab": [4],
    "A": [5],
    "A#": [6],
    "Bb": [6],
    "B": [7],
    "C": [8],
    "C#": [9],
    "Db": [9],
    "D": [10],
    "D#": [11],
    "Eb": [11]
}

# Secondary analysis function for alternate tunings
def alt_tuning(e,a,d,g,b,e2,tuning):    
    # Break the tuning input string up into six separate strings and calculate change from standard
    tuning = tuning.split()
    tuning = [tuning_dict[t] for t in tuning]
    standard = [tuning_dict[t] for t in ['E', 'A', 'D', 'G', 'B', 'E']]
    change = [tuning[i][0] - standard[i][0] for i in range(len(tuning))]

    # Assuming three semitones up is the max adjustment (otherwise it's down)
    for i in range(len(change)):
        if change[i] > 3:
            change[i] -= 12

    # Adjust inputs and plug into eadgbe function above
    inputs = [e, a, d, g, b, e2]
    for i in range(len(inputs)):
        if isinstance(inputs[i], int):
            inputs[i] += change[i]
    return eadgbe(*inputs)


# Tests
# print(eadgbe('x',0,2,4,1,0))
# print(eadgbe(7,9,'x',8,7,9))
# print(alt_tuning(2,2,2,0,0,0,'F A C F A F'))
# print(eadgbe(0,2,2,0,0,2))
print(alt_tuning(5,5,0,0,0,0, 'D A D F# A D'))
# print(eadgbe(0,4,2,0,2,0))
print(alt_tuning('x',3,3,3,0,0, 'D G D G Bb D'))



