## Version  4.1.1
## @author: Mohammed Yusuf Khan

from bs4 import BeautifulSoup
import time
import requests
import re
import csv


def run(url):
    starttime = time.time()
    dictio=set() #hold all the links scraped.
    listo = [] #holds all the links scraped.
    pagenumber = 1 #number of pages to scrape


    for page in range(1 ,pagenumber + 1):
        print ('page',page)

        html=None
        pageLink=url + str(page)


        for i in range(5):
            try:
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content
                break
            except Exception as e:
                print ('failed attempt',i)


        if not html:continue

        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') #decode html

        datum = soup.findAll('div', attrs = {'class': 'job-row'}) #find all

        #print(datum)

        for data in datum:

            test = 'NA'
            testChunk=data.find('a',{'href': re.compile('/job/')})
            if testChunk:
                test=testChunk.text
                dictio.add(testChunk.get('href'))
                listo.append(testChunk.get('href'))
                print(test)
                #print(dictio)
            #fw.write(test+'\t')

            #time.sleep(2)

    #fw = open('traindata.txt', 'a+') #testdata file in read/write mode
    url = "http://www.careerbuilder.com"
    listtoholdjob = []
    listtoholdcount = []
    listtoholddescription = []
    listtoholddate = []
    print(listo)
    print("length is:", len(listo))

    print("Scraping...")
    for value in listo:
        response = requests.get(url + value)
        html = response.content
        #print(html)
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        #print(soup)
        #driver.get(url + value)
        jobname, applicant, date, description = 'NA', '0', 'NA', 'NA'
        # Job Title (Complete Title)
        jobnameChunk = soup.find('div', {'class': 'small-12 item'})

        # applicant number
        applicantChunk=soup.find('div',{'class': 'application-count'})
        #print(applicantChunk)
        if applicantChunk:
            applicant=applicantChunk.text
            applicant=applicant.strip()
            listtoholdcount.append(applicant)
        descriptionChunk = soup.find('div', {'class': 'description'})
        #Date when the job was posted

        dateChunk = soup.find('h3', {'id': 'job-begin-date'})
        if dateChunk:
            date = dateChunk.text
            date=date.strip()
            listtoholddate.append(date)
            d = {"Posted 10 days ago":10, "Posted 11 days ago":11,"Posted 12 days ago":12,"Posted 13 days ago":13,"Posted 14 days ago":14,"Posted 15 days ago":15,"Posted 16 days ago":16,"Posted 17 days ago":17,"Posted 18 days ago":18,"Posted 19 days ago":19,"Posted 20 days ago":20,"Posted 21 days ago":21,"Posted 22 days ago":22,"Posted 23 days ago":23,"Posted 24 days ago":24,"Posted 25 days ago":25,"Posted 26 days ago":26,"Posted 27 days ago":27,"Posted 28 days ago":28,"Posted 29 days ago":29,"Posted 30 days ago":30}
            if d.get(date):
                date=d.get(date)
                #print(applicant)
                print(date)
                if applicant == '75+':
                    continue
                print(applicant)
                applicant = (int(applicant) // int(date))
            else:
                continue

        if jobnameChunk:
            jobname = jobnameChunk.text
            jw = open('jobnamefortrain.txt', 'a+')
            jw.write(jobname)
            jw.close()
            listtoholdjob.append(jobname)

        if descriptionChunk:
            description = descriptionChunk.text
            fw = open('descriptiondatafortrain.txt', 'a+')
            for line in description:
                newline = line.rstrip('\r\n')
                fw.write(newline)
            #listtoholddescription.add(newline)
            fw.write("\n")
            fw.write("\n")
            #fw.write(jobname + '\t' + description)
            fw.close()


        final_listtoholdjob = []
        final_listtoholddescription = []
        final_listtoholddate = []

        # To remove "\n" from the list
        for j in listtoholdjob:
            final_listtoholdjob.append(j.strip())

        #This part has to be worked on
        while "\n" in listtoholddescription:
            listtoholddescription.remove("\n")
        #listtoholddescription=filter(lambda x: x != '\n', listtoholddescription)
        for k in listtoholddescription:
            final_listtoholddescription.append(k.strip())

        #To remove "\n" from the list
        for v in listtoholddate:
            final_listtoholddate.append(v.strip())

        #this part basically when iterated will go in form of column
        #rows = zip(jobname,applicant,date)
        #print(jobname,applicant,date,description)

        l = [applicant,date] # iterating through a list
        with open('traintest.csv', 'a+') as outcsv: # opening the csv file to push data
            #configure writer to write standard csv file
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            #writer.writerow(['Job Title ','Total Applicant', 'Job Description', 'Date'])
            #for row in rows:
                #writer.writerow(row)
            writer.writerow(l)
        outcsv.close() #close the csv file

        #fw.write(jobname + applicant + date + description +'\n')
    #fw.close()

    endtime = time.time()
    total_time = (endtime - starttime)
    total_time = (total_time / 3600)
    print("Total time to execute the script in hours is:", total_time) # Total time taken to run the entire script

if __name__ == "__main__":
    url = "http://www.careerbuilder.com/jobs-developer?page_number="
    run(url)
