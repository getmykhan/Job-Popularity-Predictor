import csv
import re
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from nltk.corpus import stopwords
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression,MultiTaskElasticNet,BayesianRidge
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, AdaBoostClassifier

stopLex=set(stopwords.words('english'))

train_data=[]
train_applicants=[]
test_data=[]
test_applicants=[]
#train_Data
with open('train.csv','r') as csvfile:
   fw = open("popular.txt","w")
   reader = csv.DictReader(csvfile)
   for row in reader:
       b=''
       a= (row['Description']+row['Job_Name'])

       sentences=a.split('.') # split the text into sentences
       for sentence in sentences: # for each sentence
           sentence=sentence.lower().strip() # loewr case and strip
           sentence=re.sub('[^a-z]',' ',sentence) # replace all non-letter characters  with a space
           words=sentence.split(' ')
           for word in words: # for each word in the sentence
               if word=='' or word in stopLex:
                   continue # ignore empty words and stopwords
               else:
                   b=(b+' '+word)

       train_data.append(b)
       applicants = int(row['Applicants'])
       #Classifying jobs
       #0- Less Popular
       if 30<= applicants:
           fw.write(row['Job_Name']+'\n')

       if 0<= applicants <= 5:
           train_applicants.append(1)
       elif 6<=applicants<= 10:
           train_applicants.append(2)
       elif 11<= applicants <= 20:
           train_applicants.append(3)
       #1 - Popular
       elif 21<= applicants <= 30:
           train_applicants.append(4)
       #2- Very Popular
       else:
           train_applicants.append(5)

#test Data
with open('test.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
       b=''
       a= (row['Description']+row['Job_Name'])

       sentences=a.split('.') # split the text into sentences
       for sentence in sentences: # for each sentence
           sentence=sentence.lower().strip() # loewr case and strip
           sentence=re.sub('[^a-z]',' ',sentence) # replace all non-letter characters  with a space
           words=sentence.split(' ')
           for word in words: # for each word in the sentence
               if word=='' or word in stopLex:
                   continue # ignore empty words and stopwords
               else:
                   b=(b+' '+word)

       test_data.append(b)
       applicants = int(row['Applicants'])
       if 0<= applicants <= 5:
           test_applicants.append(1)
       elif 6<=applicants<= 10:
           test_applicants.append(2)
       elif 11<= applicants <= 20:
           test_applicants.append(3)
       #1 - Popular
       elif 21<= applicants <= 30:
           test_applicants.append(4)
       #2- Very Popular
       else:
           test_applicants.append(5)
       #test_applicants.append(int(row['Applicants']))
y_train, y_test = train_applicants, test_applicants
vectorizer=CountVectorizer()

X_train = vectorizer.fit_transform(train_data)
X_test = vectorizer.transform(test_data)

#Naive bayes classifier
clf=MultinomialNB(alpha=0.1)
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
multinomialscore = metrics.accuracy_score(y_test, pred)
print("MultinomialNB accuracy:   %0.3f" % multinomialscore)

#Random Forest classifier
clf =  RandomForestClassifier(n_estimators=2500, n_jobs=15,criterion="entropy",max_features='log2',random_state=150,max_depth=600,min_samples_split=163)
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
randomforestscore = metrics.accuracy_score(y_test, pred)
print("RandomForest accuracy:   %0.3f" % randomforestscore)

#SGDClassifier
clf =  SGDClassifier()
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
SGDscore = metrics.accuracy_score(y_test, pred)
print("SGD accuracy:   %0.3f" % SGDscore)

#AdaBoostClassifier
clf =  AdaBoostClassifier()
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
Adascore = metrics.accuracy_score(y_test, pred)
print("AdaBoost accuracy:   %0.3f" % Adascore)


#logistics
clf =  LogisticRegression()
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
Logisticscore = metrics.accuracy_score(y_test, pred)
print("Logistic accuracy:   %0.3f" % Logisticscore)

#BernoulliNB
clf =  BernoulliNB()
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
Bernoulliscore = metrics.accuracy_score(y_test, pred)
print("BernoulliNB accuracy:   %0.3f" % Bernoulliscore)

#KNeighbors
clf =  KNeighborsClassifier()
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
Kscore = metrics.accuracy_score(y_test, pred)
print("KNeighbors accuracy:   %0.3f" % Kscore)

clf =  SVC()
clf.fit(X_train, y_train)
#predicting accuracy
pred = clf.predict(X_test)
SVCscore = metrics.accuracy_score(y_test, pred)
print("SVC accuracy:   %0.3f" % SVCscore)
#Plotting Accuracy
l=[multinomialscore,SVCscore,randomforestscore,SGDscore,Adascore,Logisticscore,Bernoulliscore,Kscore]
m=[0,1,2,3,4,5,6,7]
n=['Mnomial','SVC','RForest','SGD','ADA','Logistic','Bernoulli','KNeigh']
plt.ylabel('Accuracy')
plt.xlabel('Algorithms')
plt.ylim(0,1)
plt.xticks(m,n)
plt.bar(m,l)
plt.show()


#plotting Popularity

train_data=[]
train_applicants=[]
test_data=[]
test_applicants=[]

with open('train.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
       a= int(row['Date'])
       train_data.append(a)
       b= int(row['Applicants'])
       train_applicants.append(b)
#print(max(train_applicants))
plt.ylabel('Popularity(No.of.Applicants)')
plt.xlabel('Number of days')
plt.ylim(0,90)
plt.xlim(9,31)
plt.scatter(train_data,train_applicants)
plt.figure(num=None, figsize=(20, 14), dpi=80, facecolor='w', edgecolor='k')
plt.show()
