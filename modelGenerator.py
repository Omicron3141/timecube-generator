from nltk.tokenize import sent_tokenize, word_tokenize

import argparse

import numpy as np

import math

k = 0

"""
Main

Paramaters
------------------
file   -- the file to read raw text from
"""

def main(readfile, savefile):
    print("---- Beginning Read from %s ----" % readfile)
    # Load raw text from file
    f = open(readfile, 'r')
    lines = f.readlines()
    raw_string = ""
    for line in lines:
        raw_string += line.lower()[:-1]+" "
    f.close()
    print("Read Complete")
    print("---- Beginning Tokenization ----")

    sentences = [word_tokenize(t) for t in sent_tokenize(raw_string)]
    print("Tokenization complete: %i sentences found" % len(sentences))
    print("---- Beginning Counting ----")

    count_model = {}
    totals = {}
    for sentence in sentences:
        s = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(s)):
            if not s[i-1] in count_model:
                count_model[s[i-1]] = {}
            if not s[i] in count_model[s[i-1]]:
                count_model[s[i-1]][s[i]] = 1
            else:
                count_model[s[i-1]][s[i]] += 1

            if not s[i-1] in totals:
                totals[s[i-1]] = 1
            else:
                totals[s[i-1]] += 1

    print("Completed counting. %i start tokens found." % len(totals.keys()))
    print("---- Beginning probabilizing ----")
    vocab = totals.keys() + ["</s>"]
    prob_model = np.zeros((len(vocab)-1, len(vocab)))
    rules = 0
    for sIndex in range(len(vocab)-1):
        for eIndex in range(len(vocab)):
            start = vocab[sIndex]
            end = vocab[eIndex]
            if end in count_model[start]:
                rules += 1
                prob_model[sIndex][eIndex] = (float(count_model[start][end])+k)/(totals[start]+(len(vocab)-1)*k)
            elif not end == "</s>":
                prob_model[sIndex][eIndex] = k/(totals[start]+(len(vocab)-1)*k)
    print("Completed probabilizing. %i rules generated (%.2f%% of possible)." % (rules, float(rules)/(len(vocab)**2)*100))
    np_vocab = np.array(vocab)
    np.savez(savefile, vocab=np_vocab, transitions=prob_model)



parser = argparse.ArgumentParser(description='Generates a markov model from raw text')
parser.add_argument('readfile', default='corpus.txt',
    help='The raw text file to read from')
parser.add_argument('savefile', default='model.npz',
    help='The npz file to write to')


if __name__ == '__main__':
    namespace = parser.parse_args()
    args = vars(namespace)
    main(**args)