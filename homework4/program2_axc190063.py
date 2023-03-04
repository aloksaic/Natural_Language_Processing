import pickle
import sys

# Load pickled dictionaries
with open('en_unigrams.pickle', 'rb') as f:
    english_unigram = pickle.load(f)
with open('fr_unigrams.pickle', 'rb') as f:
    french_unigram = pickle.load(f)
with open('it_unigrams.pickle', 'rb') as f:
    italian_unigram = pickle.load(f)
with open('en_bigrams.pickle', 'rb') as f:
    english_bigram = pickle.load(f)
with open('fr_bigrams.pickle', 'rb') as f:
    french_bigram = pickle.load(f)
with open('it_bigrams.pickle', 'rb') as f:
    italian_bigram = pickle.load(f)

# Open the test file and the output file
test_file = open(sys.argv[1], 'r')
output_file = open(sys.argv[2], 'w')

# Create a list of the languages
languages = ['English', 'French', 'Italian']

# Set up a count of correct classifications and a list of incorrectly classified items
correct_count = 0
incorrect_items = []

# Loop through each line in the test file
for i, line in enumerate(test_file):
    # Remove the newline character
    line = line.strip()
    # Tokenize the line
    tokens = line.split()
    # Initialize the probabilities for each language
    english_prob = 0
    french_prob = 0
    italian_prob = 0
    # Loop through each bigram in the line
    for j in range(len(tokens)-1):
        # Get the bigram
        bigram = tokens[j] + ' ' + tokens[j+1]
        # Calculate the probabilities for each language
        if bigram in english_bigram:
            english_prob += english_bigram[bigram]
        else:
            english_prob += english_unigram[tokens[j]]
        if bigram in french_bigram:
            french_prob += french_bigram[bigram]
        else:
            french_prob += french_unigram[tokens[j]]
        if bigram in italian_bigram:
            italian_prob += italian_bigram[bigram]
        else:
            italian_prob += italian_unigram[tokens[j]]
    # Choose the language with the highest probability
    max_prob = max(english_prob, french_prob, italian_prob)
    if max_prob == english_prob:
        lang = 'English'
    elif max_prob == french_prob:
        lang = 'French'
    else:
        lang = 'Italian'
    # Write the language to the output file
    output_file.write(lang + '\n')
    # Check if the classification is correct and update the count
    if lang == languages[int(sys.argv[3].split('.')[0])-1]:
        correct_count += 1
    else:
        incorrect_items.append(i+1)

# Close the files
test_file.close()
output_file.close()

# Calculate and print the accuracy and the list of incorrect items
accuracy = correct_count / (i+1) * 100
print(f"Accuracy: {accuracy:.2f}%")
if len(incorrect_items) > 0:
    print("Incorrect items:", incorrect_items)
else:
    print("All items classified correctly.")
