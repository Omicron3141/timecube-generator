import numpy as np

import random as rand

vocab = np.zeros((1))
transitions = np.zeros((1,1))

minlength = 10

def load(filename):
    global vocab
    global transitions

    npzfile = np.load(filename)
    vocab = npzfile['vocab']
    transitions = npzfile['transitions']

def create_sentence():
	return postprocess(generate())

def generate():
	currenttoken = np.where(vocab == "<s>")[0][0]
	endtoken = np.where(vocab == "</s>")[0][0]
	vocab_size = vocab.shape[0]
	sentence = []
	while currenttoken != endtoken:
		index = np.random.choice(np.arange(vocab_size), p=transitions[currenttoken])
		sentence += [vocab[index]]
		currenttoken = index
	if len(sentence) < minlength:
		return generate()
	else:
		return sentence[:-1]

def postprocess(tokens):
	capitalize = ["i", "gene", "god", "jesus", "dr", "washington", "earth", "ray", "bible", "wikipedia", "jesus", "santa"]
	no_prev_space = ["n't", "'s", ",", ".", "?", "!", "10,000.00"]
	sentence = ""
	for i in range(len(tokens)-1):
		this = tokens[i]
		if this in capitalize or i == 0:
			this = this.capitalize()
		nxt = tokens[i+1]
		if nxt in no_prev_space:
			sentence += this
		else:
			sentence += this+" "
	sentence += tokens[-1]

	return sentence

if __name__ == '__main__':
    load("model.npz")
    for i in range(10):
    	print postprocess(generate())