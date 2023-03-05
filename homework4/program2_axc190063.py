import pickle

# Load the pickled dictionaries
with open('en_unigrams.pickle', 'rb') as f:
    english_unigrams = pickle.load(f)
with open('en_bigrams.pickle', 'rb') as f:
    english_bigrams = pickle.load(f)

with open('fr_unigrams.pickle', 'rb') as f:
    french_unigrams = pickle.load(f)
with open('fr_bigrams.pickle', 'rb') as f:
    french_bigrams = pickle.load(f)

with open('it_unigrams.pickle', 'rb') as f:
    italian_unigrams = pickle.load(f)
with open('it_bigrams.pickle', 'rb') as f:
    italian_bigrams = pickle.load(f)

# Load the test file and correct classifications
with open('data/LangId.test', 'r') as f:
    test_lines = f.readlines()

with open('data/wordLangId.out', 'r') as f:
    output_lines = f.readlines()


# Define a function to calculate probability for a line in the test file
def calculate_probability(line, unigram_dict, bigram_dict):
    tokens = line.strip().split()
    unigram_prob = 1
    bigram_prob = 1
    for token in tokens:
        unigram_count = unigram_dict.get((token,), 0)
        unigram_prob *= unigram_count / sum(unigram_dict.values())
        if tokens.index(token) > 0:
            bigram_count = bigram_dict.get((tokens[tokens.index(token) - 1], token), 0)
            bigram_prob *= bigram_count / unigram_count
    return unigram_prob * bigram_prob


# Classify each line in the test file and write the predicted language to a file
with open('LangId.out', 'w') as f:
    for line in test_lines:
        english_prob = calculate_probability(line, english_unigrams, english_bigrams)
        french_prob = calculate_probability(line, french_unigrams, french_bigrams)
        italian_prob = calculate_probability(line, italian_unigrams, italian_bigrams)
        probs = {'ENGLISH': english_prob, 'FRENCH': french_prob, 'ITALIAN': italian_prob}
        predicted_lang = max(probs, key=probs.get)
        f.write(predicted_lang + '\n')

# Calculate accuracy and output incorrectly classified lines
num_correct = 0
incorrect_lines = []
for i in range(len(output_lines)):
    if output_lines[i].strip() == open('LangId.out', 'r').readlines()[i].strip():
        num_correct += 1
    else:
        incorrect_lines.append(i + 1)
accuracy = num_correct / len(output_lines)

print(f'Accuracy: {accuracy:.2%}')
print(f'Incorrectly classified lines: {incorrect_lines}')
