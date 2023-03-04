import nltk
import pickle


def build_ngram_dicts(filename):
    # Step a: read in the text and remove newlines
    with open(filename, encoding="utf8") as f:
        text = f.read().replace("\n", " ")

    # Step b: tokenize the text
    tokens = nltk.word_tokenize(text)

    # Step d: use nltk to create a bigrams list
    bigrams = list(nltk.bigrams(tokens))

    # Step e: use nltk to create a unigrams list
    unigrams = tokens

    # Step f: use the bigram list to create a bigram dictionary of bigrams and counts
    bigram_dict = {}
    for bigram in bigrams:
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1

    # Step g: use the unigram list to create a unigram dictionary of unigrams and counts
    unigram_dict = {}
    for unigram in unigrams:
        if unigram in unigram_dict:
            unigram_dict[unigram] += 1
        else:
            unigram_dict[unigram] = 1

    # Step h: return the unigram dictionary and bigram dictionary from the function
    return unigram_dict, bigram_dict


if __name__ == '__main__':
    # Step i: in the main body of code, call the function 3 times for each training file,
    # pickle the 6 dictionaries, and save to files with appropriate names.

    # Call the function for each training file
    en_unigrams, en_bigrams = build_ngram_dicts("data/LangID.train.English")
    fr_unigrams, fr_bigrams = build_ngram_dicts("data/LangId.train.French")
    de_unigrams, de_bigrams = build_ngram_dicts("data/LangId.train.Italian")

    # Pickle the dictionaries
    with open("en_unigrams.pickle", "wb") as f:
        pickle.dump(en_unigrams, f)
    with open("en_bigrams.pickle", "wb") as f:
        pickle.dump(en_bigrams, f)

    with open("fr_unigrams.pickle", "wb") as f:
        pickle.dump(fr_unigrams, f)
    with open("fr_bigrams.pickle", "wb") as f:
        pickle.dump(fr_bigrams, f)

    with open("it_unigrams.pickle", "wb") as f:
        pickle.dump(de_unigrams, f)
    with open("it_bigrams.pickle", "wb") as f:
        pickle.dump(de_bigrams, f)
