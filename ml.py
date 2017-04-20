##@author: Mohammed Yusuf Khan
## Version: 1.0.0

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import csv

## We have the read the traindata and the testdata
train_data=[]
train_applicants=[]
test_data=[]
test_applicants=[]
with open('traintest.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
       train_data.append(row['Job_Name'] + row['Date'] + row['Description'])
       train_applicants.append(row['Applicants'])

with open('traintest.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
       test_data.append(row['Job_Name'] + row['Date'] + row['Description'])
       test_applicants.append(row['Applicants'])

y_train, y_test = train_applicants, test_applicants
vectorizer=CountVectorizer()

X_train = vectorizer.fit_transform(train_data)
X_test = vectorizer.transform(test_data)
#Naive bayes classifier
clf=MultinomialNB(alpha=0.1)
clf.fit(X_train, y_train)

#Predicting accuracy
pred = clf.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("Accuracy:   %0.3f" % score)
