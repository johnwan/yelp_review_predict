import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

csv_file_object = csv.reader(open('../csv/yelp_review_train.csv', 'rb')) #Load in the training csv file
header = csv_file_object.next() #Skip the fist line as it is a header
train_data=[] #Creat a variable called 'train_data'
for row in csv_file_object: #Skip through each row in the csv file
    train_data.append(row) #adding each row to the data variable
train_data = np.array(train_data) #Then convert from a list to an array

#All the bsn_score with no data make the median of the data
train_data[train_data[0::,2] == '',2] = np.median(train_data[train_data[0::,2]\
                                           != '',2].astype(np.float))
#All the user_score with no data make the median of the data
train_data[train_data[0::,3] == '',3] = np.median(train_data[train_data[0::,3]\
                                           != '',3].astype(np.float))

test_file_object = csv.reader(open('../csv/yelp_review_test.csv', 'rb')) #Load in the test csv file
header = test_file_object.next() #Skip the fist line as it is a header
test_data=[] #Creat a variable called 'test_data'
for row in test_file_object: #Skip through each row in the csv file
    test_data.append(row) #adding each row to the data variable
test_data = np.array(test_data) #Then convert from a list to an array

#All the bsn_score with no data make the median of the data
test_data[test_data[0::,1] == '',1] = np.median(test_data[test_data[0::,1]\
                                           != '',1].astype(np.float))
#All the user_score with no data make the median of the data
test_data[test_data[0::,2] == '',2] = np.median(test_data[test_data[0::,2]\
                                           != '',2].astype(np.float))

print 'Training '
forest = RandomForestClassifier(n_estimators=10)

forest = forest.fit(train_data[0::,3::],train_data[0::,0])

print 'Predicting'
output = forest.predict(test_data[0::,2::])

f = open("../csv/submission.csv", "wb")
#open_file_object = csv.writer(f, dialect='excel', delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL) #Load in the csv file
open_file_object = csv.writer(f)
test_file_object = csv.reader(open('../csv/yelp_review_RF.csv', 'rb')) #Load in the test csv file

first_row = ['id','votes']
open_file_object.writerow(first_row)

test_file_object.next()
i = 0
for row in test_file_object:
    #row.insert(1,output[i].astype(np.uint8))
    #result = [row[0]]+[round(float(row[3]))]
    result = [row[0]]+[output[i].astype(np.uint8)]
    open_file_object.writerow(result)
    i += 1


f.close()
