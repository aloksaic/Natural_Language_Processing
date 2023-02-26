import sys  # To get the system parameter

import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

if __name__ == '__main__':
    # Checks for the correct file path
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    # Open the file input for reading
    with open(str(sys.argv[1])) as f:
        contents = f.read()

    tokens = contents.strip()
    tokens = contents.split()
    tokens = word_tokenize(contents)
    tokens = [t.lower() for t in tokens]
    tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english')]
    set1 = set(tokens)

    # lexical diversity
    print("\nLexical diversity: %.2f" % (len(set1) / len(tokens)))

    # get the lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    # make unique
    lemmas_unique = list(set(lemmas))
    # make a dictionary of counts
    counts = {t: lemmas.count(t) for t in lemmas_unique}

    tags = nltk.pos_tag(lemmas_unique)
    print("\n20 tagged words:")
    for i in range(20):
        print(tags[i])

    for i in lemmas_unique:
        if i[0] == 'NN':
            nouns = nouns.append(i)

    # print most common words
    # dicts are unordered, so we sort it and put it in a list of tuples
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    print("\n50 most common words:")
    for i in range(50):
        print(sorted_counts[i])

    print("\nNumber of tokens:", len(tokens))
    print("\nNumber of nouns:", len(nouns))
