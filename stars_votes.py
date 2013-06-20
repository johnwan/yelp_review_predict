from __future__ import division
import sys
import json

fileHandle = open( 'test.txt', 'w' ) 
keywords_dic = {}
bsn_dic = {}
user_dic = {}
checkin_dic = {}

def remove_sym(line):
    line.lstrip(",.;:~!@#$%^&*()?")
    line.lstrip("\n")
    line.replace("/",' ')
    return line

def review(input_file):    
    global stars_dic,bsn_dic
    context = input_file.readlines()
    for response in context:
        try:
             # This will store each tweet's json object in response_result in type(<'dict'>)
            response_result = json.loads(response)
            bsn_id = response_result["business_id"].encode('utf-8')
            review = response_result["text"].encode('utf-8')            # get the state of the review
            votes = int(response_result["votes"]["useful"])
            # put the useful votes count to bsn_dic 
##            if bsn_dic.has_key(bsn_id):
##                bsn_dic[bsn_id][1] += votes
            # caculate the average useful votes of a review ralated to stars
            lines = review.split("\n")
            for l in lines:
                li = remove_sym(l)
                words = li.split(" ")
                for w in words:
                    if keywords_dic.has_key(w):
                        keywords_dic[w][0] += 1
                        keywords_dic[w][1] += votes/len(words)
                    else:
                        keywords_dic[w] = [1,votes/len(words)]
        except Exception,e:
             pass

def bsn_average(input_file):    
    global bsn_dic
    context = input_file.readlines()
    for response in context:
        try:
            response_result = json.loads(response)
            bsn_id = response_result["business_id"].encode('utf-8')            # get the state of the review
            count = int(response_result["review_count"])
            # caculate the average useful votes of a review ralated to stars
            bsn_dic[bsn_id] = [count,0]
        except Exception,e:
             pass

def user_average(input_file):
    global user_dic
    context = input_file.readlines()
    for response in context:
        try:
            response_result = json.loads(response)
            user_id = response_result["user_id"].encode('utf-8')            # get the state of the review
            votes = int(response_result["votes"]["useful"])
            count = int(response_result["review_count"])
            # caculate the average useful votes of a review ralated to stars
            user_dic[user_id] = [count,votes]
            #print str(user_dic[user_id])
        except Exception,e:
             pass

def checein_count(response_result):
    global check_dic
    bsn_id = response_result["business_id"].encode('utf-8')
    if bsn_dic.has_key(bsn_id):
        check_dic[bsn_id] += 1   

def cal_dic(dic):
    global fileHandle
    for e in dic:
        #print str(e) + 'count=' + str(dic[e][0]) +  ' sum=' + str(dic[e][1])
        dic[e][1] = dic[e][1]/dic[e][0]
        #print str(e) + ' ' + str(dic[e][1])
        fileHandle.write(str(e) + ' ' + str(dic[e][1]) + "\n")

def main():
    review_file = open('../csv/yelp_training_set/yelp_training_set_review.json')
    bsn_file = open('../csv/yelp_training_set/yelp_training_set_business.json')
    user_file = open('../csv/yelp_training_set/yelp_training_set_user.json')
    check_file = open('../csv/yelp_training_set/yelp_training_set_checkin.json')
    #test_file =
    review(review_file)
    print len(keywords_dic)
    cal_dic(keywords_dic)
    fileHandle.close()
    

if __name__ == '__main__':
    main()
