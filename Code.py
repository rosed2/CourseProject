import numpy as np
import nltk
from nltk.stem import PorterStemmer

numberAspects = 7

def getStopWords(filename):
    file = open(filename, "r")
    words = []
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        if line not in words:
            words.append(line)
    return words


def parseFeatureWords(filename, matrix):
    with open(filename) as file:
        for i in range(numberAspects):
            line = file.readline()
            words = line.split()
            #get rid of aspect name
            words.pop(0)
            matrix.append(words)
        

#preprocess data set
#remove reviews with missing aspect rating or doc length less than 50 words
#convert all words to lowercase
#remove punctuations and stop words, and terms occurring in less than 10 reviews
#use stemming
def parseReviews(filename, reviews, ratings, stopWords):
    with open(filename) as file:
        while (True):
            authorLine = file.readline()
            if len(authorLine) == 0:
                #reached end of file
                break
            
            contentLine = file.readline()
            dateLine = file.readline()
            ratingLine = file.readline()
            blankLine = file.readline()

            #remove punctuation
            punctuations = '''!()-[]{};:'"\,./?@#$%^&*_~'''
            for char in contentLine:
                if char in punctuations:
                    contentLine = contentLine.replace(char, "")

            contentWords = contentLine.split('>')[1].split()
            if len(contentWords) < 50:
                continue

            skip = False
            ratingsList = ratingLine.split('>')[1].split()
            for rating in ratingsList:
                if rating == -1:
                    skip = True
                    break

            if skip:
                continue

            #lowercase, stemming, remove stop words
            ps = PorterStemmer()
            finalContentWords = []
            for word in contentWords:
                word = ps.stem(word)
                word = word.lower()
                if word not in stopWords:
                    finalContentWords.append(word)





def main():
    aspects = ["Value", "Rooms", "Location", "Cleanliness", "Check in/front desk", "Service", "Business service"]
    #aspect_weights = np.zeros((d, len(aspects))), d reviews
    #aspect_ratings = np.zeros((d, len(aspects))), d reviews
    reviews = []
    vocab = []
    featureWords = []
    ratings = []
    stopWords = getStopWords("Data/StopWords.txt")

    parseFeatureWords("Data/FeatureWords.txt", featureWords)
    
    parseReviews("Data/temp.txt", reviews, ratings, stopWords)
    """
    with open("one.txt") as file:
        line = file.readline()
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for char in line:
            if char in punctuations:
                line = line.replace(char, "")
        print(line.split()) 
    """


    #go sentence by sentence
    #classify a sentence as describing the topic whose feature words it has the most of

    #create featureWords matrix [7][n]

if __name__ == '__main__':
    main()