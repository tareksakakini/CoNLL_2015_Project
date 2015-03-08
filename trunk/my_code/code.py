import os
import gensim

model = gensim.models.word2vec.Word2Vec.load_word2vec_format(os.path.join(os.path.dirname('/home/tarek/Downloads/GoogleNews-vectors-negative300.bin'), 'GoogleNews-vectors-negative300.bin'), binary=True)

model.most_similar('dog')
