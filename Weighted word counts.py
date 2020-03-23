import glob
sorted_list = glob.glob("/Users/lukaskoston/FOMCAnalysis/LemmatizedData/Output//*.txt")



from sklearn.feature_extraction.text import TfidfVectorizer

input_vectorizer = TfidfVectorizer(input="filename", stop_words=None)
m = input_vectorizer.fit_transform(sorted_list)

print("Number of Word Stem Vectors:", m.shape[1])
print("Shape of Vector Matrix:", m.shape)

from collections import Counter

def word_count(filename):
    with open(filename, 'r') as f:
        c = Counter()
        for line in f:
            c.update(line.strip().split(' '))
        return c

files = glob.glob("/Users/lukaskoston/FOMCAnalysis/LemmatizedData/Output//*.txt")
counters = [word_count(filename) for filename in files]

# counters content (example):
# [Counter({'world': 2, 'foo': 2, 'bar': 2, 'hello': 2, 'baz': 1}),
#  Counter({'foo': 5, 'world': 2, 'bar': 2, 'hello': 2, 'baz': 1})]

# Add all the word counts together:
total = sum(counters, Counter())  # sum needs an empty counter to start with

# total content (example):
# Counter({'foo': 7, 'world': 4, 'bar': 4, 'hello': 4, 'baz': 2})