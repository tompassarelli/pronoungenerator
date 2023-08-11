import random
import string
from itertools import product
import nltk
nltk.download('words')
from nltk.corpus import words

english_words = set(words.words())

# Define the phoneme features
phoneme_features = {
    'a': {'place': 'varies', 'manner': 'vowel', 'voicing': 'voiced'},
    'b': {'place': 'bilabial', 'manner': 'plosive', 'voicing': 'voiced'},
    'c': {'place': 'varies', 'manner': 'plosive/fricative', 'voicing': 'voiceless'},
    'd': {'place': 'alveolar', 'manner': 'plosive', 'voicing': 'voiced'},
    'e': {'place': 'varies', 'manner': 'vowel', 'voicing': 'voiced'},
    'f': {'place': 'labiodental', 'manner': 'fricative', 'voicing': 'voiceless'},
    'g': {'place': 'velar', 'manner': 'plosive', 'voicing': 'voiced'},
    'h': {'place': 'glottal', 'manner': 'fricative', 'voicing': 'voiceless'},
    'i': {'place': 'varies', 'manner': 'vowel', 'voicing': 'voiced'},
    'j': {'place': 'palatal', 'manner': 'glide', 'voicing': 'voiced'},
    'k': {'place': 'velar', 'manner': 'plosive', 'voicing': 'voiceless'},
    'l': {'place': 'alveolar', 'manner': 'lateral_liquid', 'voicing': 'voiced'},
    'm': {'place': 'bilabial', 'manner': 'nasal', 'voicing': 'voiced'},
    'n': {'place': 'alveolar', 'manner': 'nasal', 'voicing': 'voiced'},
    'o': {'place': 'varies', 'manner': 'vowel', 'voicing': 'voiced'},
    'p': {'place': 'bilabial', 'manner': 'plosive', 'voicing': 'voiceless'},
    'q': {'place': 'varies', 'manner': 'plosive', 'voicing': 'voiced/voiceless'},
    'r': {'place': 'alveolar', 'manner': 'retroflex_liquid', 'voicing': 'voiced'},
    's': {'place': 'alveolar', 'manner': 'fricative', 'voicing': 'voiceless'},
    't': {'place': 'alveolar', 'manner': 'plosive', 'voicing': 'voiceless'},
    'u': {'place': 'varies', 'manner': 'vowel', 'voicing': 'voiced'},
    'v': {'place': 'labiodental', 'manner': 'fricative', 'voicing': 'voiced'},
    'w': {'place': 'bilabial', 'manner': 'glide', 'voicing': 'voiced'},
    'x': {'place': 'varies', 'manner': 'fricative', 'voicing': 'voiceless'},
    'y': {'place': 'palatal', 'manner': 'glide/vowel', 'voicing': 'voiced'},
    'z': {'place': 'alveolar', 'manner': 'fricative', 'voicing': 'voiced'},
    'th': {'place': 'dental', 'manner': 'fricative', 'voicing': 'varies'},
    'ch': {'place': 'postalveolar', 'manner': 'affricate', 'voicing': 'voiceless'},
    'sh': {'place': 'postalveolar', 'manner': 'fricative', 'voicing': 'voiceless'},
    'ng': {'place': 'velar', 'manner': 'nasal', 'voicing': 'voiced'}
}
def phonotactic_check(word):
    if word.startswith('h'): 
        return False
    if word.startswith('s'): 
        return False
    if word.startswith('f'): 
        return False
    if word.startswith('t'): 
        return False
    if word.startswith('ng'):
        return False
    if word.endswith('f'):
        return False
    if word.endswith('u'):
        return False
    if word.endswith('u'):
        return False
    if word.endswith('i'):
        return False
    if word.endswith('pq'):
        return False
    if word.startswith('tf') or word.startswith('tv') or word.startswith('tz'):
        return False
    if 'dou' in word:
        return False
    if 'uo' in word:
        return False
    if 'zf' in word:
        return False
    if 'kv' in word:
        return False
    if 'zco' in word:
        return False
    if 'ao' in word:
        return False
    if 'kc' in word:
        return False
    # Add more constraints as needed
    return True

def phoneme_similarity(phoneme1, phoneme2):
    """
    Calculate similarity between two phonemes based on their features.
    Returns the count of matching features.
    """
    features1 = phoneme_features.get(phoneme1, {})
    features2 = phoneme_features.get(phoneme2, {})
    return sum(1 for key in features1 if features1[key] == features2[key])

def sequence_similarity(seq1, seq2):
    """
    Calculate similarity between two sequences based on their phonemes.
    """
    return sum(phoneme_similarity(p1, p2) for p1, p2 in zip(seq1, seq2))

def generate_candidates(length, num_candidates):
    """
    Generate random sequences of the given length.
    """
    allowed_chars = string.ascii_lowercase.replace('x', '')
    return [''.join(random.choice(allowed_chars) for _ in range(length)) for _ in range(num_candidates)]

exclusive_characters = {
    "subjective": ["h", "s", "e"],      
    "objective": [ "i", "m", "r", "e"],
    "possessive": ["i", "m", "r", "e", "s"]  
}

def is_valid_candidate(candidate, category):
    """
    Check if the candidate contains any exclusive character of common pronouns for the given category,
    if it's not an English dictionary word, and if it does not have repeated characters.
    """
    if candidate in english_words:
        return False

    if not phonotactic_check(candidate):
        return False

    for char in exclusive_characters[category]:
        if char in candidate:
            return False

    # Check for repeated characters
    for i in range(len(candidate) - 1):
        if candidate[i] == candidate[i + 1]:
            return False

    return True

# main
lengths = [2, 3]
num_candidates = 5000
subjective = ["he", "she", "they"]
objective = ["him", "her", "them"]
possessive = ["his", "hers", "theirs"]
pronoun_sets = {'subjective': subjective, 'objective': objective, 'possessive': possessive}

candidates_sets = {
    (pronoun_type, length): [
        candidate for candidate in generate_candidates(length, num_candidates)
        if is_valid_candidate(candidate, pronoun_type)
    ]
    for pronoun_type in pronoun_sets
    for length in lengths
}

valid_candidates_sets = candidates_sets  

scores_sets = {
    (pronoun_type, length): {
        candidate: sum(sequence_similarity(candidate, pronoun) for pronoun in pronoun_sets[pronoun_type])
        for candidate in valid_candidates
    }
    for (pronoun_type, length), valid_candidates in valid_candidates_sets.items()
}

sorted_candidates_sets = {
    (pronoun_type, length): sorted(scores.keys(), key=scores.get, reverse=True)
    for (pronoun_type, length), scores in scores_sets.items()
}

for pronoun_type in pronoun_sets:
    for length in lengths:
        print(f"Top Potential {pronoun_type} Pronouns of Length {length}:")
        for candidate in sorted_candidates_sets[(pronoun_type, length)][:10]:
            print(f"{candidate} (Score: {scores_sets[(pronoun_type, length)][candidate]})")
        print("-" * 40)

set_scores = {}

subj_scores = scores_sets[('subjective', 3)]
obj_scores = scores_sets[('objective', 3)]
pos_scores = scores_sets[('possessive', 3)]

# only consider top N candidates for combinations to save computational effort, could be more with patience
N = 80
top_subj_candidates = sorted(valid_candidates_sets[('subjective', 3)], key=subj_scores.get, reverse=True)[:N]
top_obj_candidates = sorted(valid_candidates_sets[('objective', 3)], key=obj_scores.get, reverse=True)[:N]
top_pos_candidates = sorted(valid_candidates_sets[('possessive', 3)], key=pos_scores.get, reverse=True)[:N]

def meets_criteria(pronoun_set):
    ''' more constraints if desired '''
    subj, obj, pos = pronoun_set
    #return (subj[0] == obj[0] and subj[0] == pos[0]) or (subj[1] == obj[1] and subj[1] == pos[1])
    return (subj[0] == obj[0] and subj[0] == pos[0])

# filter sets using the new criteria
filtered_sets = [(subj, obj, pos) for subj, obj, pos in product(top_subj_candidates, top_obj_candidates, top_pos_candidates) if meets_criteria((subj, obj, pos))]

# calculate set scores only for the filtered sets
for subj, obj, pos in filtered_sets:
    set_scores[(subj, obj, pos)] = subj_scores.get(subj, 0) + obj_scores.get(obj, 0) + pos_scores.get(pos, 0)

# sort sets by score
sorted_sets = sorted(set_scores.keys(), key=set_scores.get, reverse=True)

# Calculate set scores
for subj, obj, pos in product(top_subj_candidates, top_obj_candidates, top_pos_candidates):
    set_scores[(subj, obj, pos)] = subj_scores.get(subj, 0) + obj_scores.get(obj, 0) + pos_scores.get(pos, 0)
    ## debug
    #if subj not in subj_scores:
    #    print(f"Missing subj: {subj}")
    #if obj not in obj_scores:
    #    print(f"Missing obj: {obj}")
    #if pos not in pos_scores:
    #    print(f"Missing pos: {pos}")

# Sort sets by score
sorted_sets = sorted(set_scores.keys(), key=set_scores.get, reverse=True)

# Display the top pronoun sets
print("Top Potential Pronoun Sets:")
for pronoun_set in sorted_sets[:10]:
    subj, obj, pos = pronoun_set
    print(f"Subjective: {subj}, Objective: {obj}, Possessive: {pos} (Score: {set_scores[pronoun_set]})")
    print("-" * 40)
