import numpy as np
import nltk
nltk.download('vader_lexicon')
from nltk.stem import PorterStemmer
import re
import operator
import random
import scipy.stats
import numpy as np
from scipy.stats import multivariate_normal
from nltk.sentiment.vader import SentimentIntensityAnalyzer

numberAspects = 7

oratings = []

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
            # get rid of aspect name
            words.pop(0)
            # lowercase, stemming, remove stop words

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


# preprocess data set
# remove reviews with missing aspect rating or doc length less than 50 words
# convert all words to lowercase
# remove punctuations and stop words, and terms occurring in less than 10 reviews
# use stemming
def parseReviews(filename, stopWords):
    reviews = []  # list of parsed reviews, each review is a list of sentences
    ratings = []
    vocab = []

    with open(filename) as file:
        while (True):
            authorLine = file.readline()
            if len(authorLine) == 0:
                # reached end of file
                break

            contentLine = file.readline()
            dateLine = file.readline()
            ratingLine = file.readline()
            blankLine = file.readline()

            contentWords = contentLine.split('>')[1]

            if len(contentWords) < 50:
                continue

            # skip if a rating is missing
            skip = False
            ratingsList = ratingLine.split('>')[1].split()
            ratingsInts = []
            isOverallRating = 1
            for rating in ratingsList:
                if isOverallRating == 1:
                    isOverallRating = 0
                    oratings.append(int(rating))
                if rating == '-1':
                    print("found -1")
                    skip = True
                    break
                else:
                    ratingsInts.append(int(rating))

            if skip:
                continue

            ratings.append(ratingsInts)

            # split by sentence
            sentences = re.split(r'[!.?]+', contentWords)
            finalContentWords = []

            for sentence in sentences:
                if len(sentence) == 0:
                    continue

                # remove punctuation

                punctuations = '''!()-[]{};:'"\,./?@#$%^&*_~'''

                for char in sentence:
                    if char in punctuations:
                        sentence = sentence.replace(char, "")

                words = sentence.split()
                if len(words) == 0:
                    continue

                # lowercase, stemming, remove stop words
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


# go sentence by sentence
# classify a sentence as describing the topic whose feature words it has the most of
def assignTopics(reviews, featureWords):
    topicAssignments = []  # 2D array, a review has a topic assignment per sentence

    for review in reviews:
        assignments = []  # get a topic number per sentence

        for sentence in review:
            counter = {}  # counter dictionary, topic to feature word count
            for i in range(len(featureWords)):
                counter[i] = 0

            for word in sentence:
                for topic in range(len(featureWords)):
                    topicFeatureWords = featureWords[topic]

                    if word in topicFeatureWords:
                        counter[topic] += 1

            # assign topic number to the sentence
            topicNum = max(counter.items(), key=operator.itemgetter(1))[0]
            assignments.append(topicNum)

        topicAssignments.append(assignments)

    return topicAssignments


# returns ratings of each topic for each review by sentiment analysis
def assignTopicRatings(reviews, topicAssignments, aspects):
    topicRatings = []

    sentimentAnalyzer = SentimentIntensityAnalyzer()

    for i in range(len(reviews)):
        review = reviews[i]

        ratings = []  # topic ratings for this review

        for j in range(len(aspects)):
            ratings.append(0)

        for j in range(len(review)):
            sentence = review[j]
            topic = topicAssignments[i][j]
            rating = 0

            for word in sentence:
                sentiment = sentimentAnalyzer.polarity_scores(word)['compound']
                rating += sentiment

            # find average of sentiments in the sentence, between [-1, 1]
            rating /= len(sentence)
            ratings[topic] += rating

        for k in range(len(aspects)):
            rating = ratings[k]
            rating *= 2  # range = [-2, 2]
            rating += 3  # range = [1, 5]
            ratings[k] = rating

        topicRatings.append(ratings)

    return topicRatings

def assignAspectWeight(topicRatings) :
    topic_weights = []
    for review in topicRatings:
        tmp_weight = [0] * 7
        iters = 0
        curr_prob = 0
        aspect_weight = []

        while iters < 100:
            # get random weight values
            for i in range(len(aspect_weight)): 
                tmp_weight[i] = round(random.uniform(0,1),3)

            # normalize vector 
            total_val = sum(aspect_weight)
            for i in range(len(aspect_weight)):
                tmp_weight[i] = round(tmp_weight[i]/total_val, 4)

            # mean is equal to the actual overall rating 
            mean = oratings[0]

            #std dev is the 
            variance = sum((x - mean)**2 for x in oratings)/ len(oratings)
            stdev = variance ** 0.5

            # find overall rating from rating and weight 
            pred_orating = sum([a*b for a,b in zip(topicRatings[0], tmp_weight)])

            #calculate prob of getting that rating from norm dist 
            test_prob = scipy.stats.multivariate_normal(mean, stdev, 0.6).pdf(pred_orating)

            # see if prob is higher than existing prob and if it is change aspect_weight to the new weight
            if(test_prob > curr_prob):
                curr_prob = test_prob
                aspect_weight = tmp_weight
            iters += 1

        topic_weights.append(aspect_weight)

    # find predicted overall rating for the reviews
    pred_oratings = []
    for i in range(len(topicRatings)):
        pred_oratings.append(sum([a*b for a,b in zip(topicRatings[i], topic_weights[i])]))
    
    return topic_weights, pred_oratings


def main():
    aspects = ["Value", "Rooms", "Location", "Cleanliness",
               "Check in/front desk", "Service", "Business service"]

    stopWords = getStopWords("Data/StopWords.txt")

    featureWords = parseFeatureWords("Data/FeatureWords.txt")

    # reviews is a 3D array
    # sentence is array of words
    # a review is array of sentences
    # ratings is 2D array
    reviews, ratings, vocab = parseReviews("Data/temp.txt", stopWords)

    topicAssignments = assignTopics(reviews, featureWords)
    print(topicAssignments)

    # get topic ratings
    topicRatings = assignTopicRatings(reviews, topicAssignments, aspects)
    print(topicRatings)

    topicWeights, pred_oratings = assignAspectWeight(topicRatings)
    print(topicWeights)
    print(pred_oratings)


if __name__ == '__main__':
    main()
