import numpy as np
import nltk
from nltk.stem import PorterStemmer
import re
import operator

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


def parseFeatureWords(filename):
    featureWords = []

    with open(filename) as file:
        for i in range(numberAspects):
            line = file.readline()
            words = line.split()
            #get rid of aspect name
            words.pop(0)
            #lowercase, stemming, remove stop words
            
            ps = PorterStemmer()
            wordArray = []

            for word in words:
                word = ps.stem(word)
                word = word.lower()
                wordArray.append(word)
            

            featureWords.append(wordArray)
            '''
            featureWords.append(words)
            '''

    return featureWords
        

#preprocess data set
#remove reviews with missing aspect rating or doc length less than 50 words
#convert all words to lowercase
#remove punctuations and stop words, and terms occurring in less than 10 reviews
#use stemming
def parseReviews(filename, stopWords):
    reviews = []                     #list of parsed reviews, each review is a list of sentences
    ratings = []
    vocab = []

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

            contentWords = contentLine.split('>')[1]
           
            if len(contentWords) < 50:
                continue

            #skip if a rating is missing
            skip = False
            ratingsList = ratingLine.split('>')[1].split()
            ratingsInts = []
            for rating in ratingsList:
                if rating == '-1':
                    print("found -1")
                    skip = True
                    break
                else:
                    ratingsInts.append(int(rating))

            if skip:
                continue

            ratings.append(ratingsInts)
            
            
            #split by sentence
            sentences = re.split(r'[!.?]+', contentWords)
            finalContentWords = []

            for sentence in sentences:
                if len(sentence) == 0:
                    continue

                #remove punctuation
            
                punctuations = '''!()-[]{};:'"\,./?@#$%^&*_~'''
            
                for char in sentence:
                    if char in punctuations:
                        sentence = sentence.replace(char, "")

                words = sentence.split()
                if len(words) == 0:
                    continue

                #lowercase, stemming, remove stop words
                ps = PorterStemmer()
                wordArray = []

                for word in words:
                    word = ps.stem(word)
                    word = word.lower()
                    if word not in stopWords:
                        wordArray.append(word)
                        if word not in vocab:
                            vocab.append(word)

                if len(wordArray) > 0:
                    finalContentWords.append(wordArray)

            reviews.append(finalContentWords)
            

    return reviews, ratings, vocab


#go sentence by sentence
#classify a sentence as describing the topic whose feature words it has the most of
def assignTopics(reviews, featureWords):
    topicAssignments = []       #2D array, a review has a topic assignment per sentence

    for review in reviews:
        assignments = []            #get a topic number per sentence

        for sentence in review:     
            counter = {}        #counter dictionary, topic to feature word count
            for i in range(len(featureWords)):
                counter[i] = 0

            for word in sentence:
                for topic in range(len(featureWords)):
                    topicFeatureWords = featureWords[topic]

                    if word in topicFeatureWords:
                        counter[topic] += 1
                        
            #assign topic number to the sentence
            print(counter)
            topicNum = max(counter.items(), key=operator.itemgetter(1))[0]
            assignments.append(topicNum)

        topicAssignments.append(assignments)

    
    return topicAssignments

#returns ratings of each topic for each review by sentiment analysis
def assignTopicRatings(reviews, topicAssignments):
    topicRatings = []




    return topicRatings


def main():
    aspects = ["Value", "Rooms", "Location", "Cleanliness", "Check in/front desk", "Service", "Business service"]
    #aspect_weights = np.zeros((d, len(aspects))), d reviews
    #aspect_ratings = np.zeros((d, len(aspects))), d reviews

    stopWords = getStopWords("Data/StopWords.txt")

    featureWords = parseFeatureWords("Data/FeatureWords.txt")
    
    #reviews is a 3D array
    #sentence is array of words
    #a review is array of sentences
    #ratings is 2D array
    reviews, ratings, vocab = parseReviews("Data/temp.txt", stopWords)

    topicAssignments = assignTopics(reviews, featureWords)
    print(topicAssignments)

    #get topic ratings
    topicRatings = assignTopicRatings(reviews, topicAssignments)
    

if __name__ == '__main__':

    main()