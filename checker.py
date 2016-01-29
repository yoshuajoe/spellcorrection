######################################
# Recomposed by Yoshua				 #
# Originated by Peter Norvig		 #
# Spelling Auto-correction 2 stairs  #
# Created at 2016					 #
######################################

import re
import collections
import sys
def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

lang = ""
for sy in sys.argv:
	w = sy.split('=')
	if w[0] == '-lang':
		lang = w[1]

NWORDS = train(words(file(lang+'.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)
	
query = raw_input("What do you want to search?")
temp = []
for q in query.split(" "):
	temp.append(correct(q))

res = ' '.join([wi for wi in temp])
if res != temp:
	print("Did you mean '%s'?"%res)