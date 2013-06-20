from __future__ import division
import sys
import json
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

train_data = []
test_data = []
bsn_avg_score = 0
user_avg_score = 0
keywords_dic = {}
bsn_dic = {}
user_dic = {}


def remove_sym(line):
    line.lstrip(",.;:~!@#$%^&*()?")
    line.lstrip("\n")
    line.replace("/",' ')
    return line

def review(input_file):    
    global train_data,bsn_dic,user_dic
    context = input_file.readlines()
    for response in context:
            # This will store each tweet's json object in response_result in type(<'dict'>)
            response_result = json.loads(response)
            bsn_id = response_result["business_id"].encode('utf-8')
            review = response_result["text"].encode('utf-8')            # get the state of the review
            votes = int(response_result["votes"]["useful"])
            user_id = response_result["user_id"].encode('utf-8')
            review = remove_sym(review)
            words = review.split(" ")
            rev_score = review_score(words)            
            if bsn_dic.has_key(bsn_id):
                bsn_score = bsn_dic[bsn_id]
            else:
                bsn_score = ''
            if user_dic.has_key(user_id):
                user_score = user_dic[user_id]
            else:
                user_score = ''
            train_data.append([votes,rev_score,bsn_score,user_score])
            #print [votes,rev_score,bsn_score,user_score]


def test_review(input_file):    
    global test_data
    context = input_file.readlines()
    for response in context:
             # This will store each tweet's json object in response_result in type(<'dict'>)
            response_result = json.loads(response)
            bsn_id = response_result["business_id"].encode('utf-8')
            review = response_result["text"].encode('utf-8')            # get the state of the review
            review_id = response_result["review_id"].encode('utf-8') 
            #votes = int(response_result["votes"]["useful"])
            user_id = response_result["user_id"].encode('utf-8')
            review = remove_sym(review)
            words = review.split(" ")
            rev_score = review_score(words)
            if bsn_dic.has_key(bsn_id):
                bsn_score = bsn_dic[bsn_id]
            else:
                bsn_score = ''
            if user_dic.has_key(user_id):                    
                user_score = user_dic[user_id]
            else:
                user_score = ''
            test_data.append([review_id,rev_score,bsn_score,user_score])    


def review_score(words):
    global keywords_dic
    score = 0
    for w in words:
        if keywords_dic.has_key(w):
            score += keywords_dic[w]
    return score

def get_dic(input_file):
    dic = {}
    context = input_file.readlines()
    for response in context:
        words = response.split(" ")
        dic[words[0]] = float(words[1])
    return dic

open_file_object = csv.writer(open("../csv/yelp_review_RF.csv", "wb"))
first_row = ['useful_count','keywords_score','bsn_avg','user_avg']
open_file_object.writerow(first_row)


review_file = open('../csv/yelp_training_set/yelp_training_set_review.json')
test_file = open('../csv/yelp_test_set/yelp_test_set_review.json')
bsn_file = open('bsn_dic.txt')
user_file = open('user_dic.txt')
keywords_file = open('keywords_dic.txt')
bsn_dic = get_dic(bsn_file)
user_dic = get_dic(user_file)
keywords_dic = get_dic(keywords_file)
review(review_file)
test_review(test_file)
print len(train_data)
print len(test_data)

#convert from a list to an array
train_data = np.array(train_data)
#All the bsn_score with no data make the average of the data
train_data[train_data[0::,2] == '',2] = np.average(train_data[train_data[0::,2]\
                                           != '',2].astype(np.float))
#All the user_score with no data make the average of the data
train_data[train_data[0::,3] == '',3] = np.average(train_data[train_data[0::,3]\
                                           != '',3].astype(np.float))

#convert from a list to an array
test_data = np.array(test_data)
#All the bsn_score with no data make the average of the data
test_data[test_data[0::,2] == '',2] = np.average(test_data[test_data[0::,2]\
                                           != '',2].astype(np.float))
#All the user_score with no data make the average of the data
test_data[test_data[0::,3] == '',3] = np.average(test_data[test_data[0::,3]\
                                           != '',3].astype(np.float))
for row in test_data:
    open_file_object.writerow(row)
