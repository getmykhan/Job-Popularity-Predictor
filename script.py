## Version  3.1.9
## @author: Mohammed Yusuf Khan

from bs4 import BeautifulSoup
import time
import requests
import re
from selenium import webdriver
import csv
import timeit


def run(url):
    starttime = time.time()
    dictio=set() #hold all the links scraped.
    listo = []
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
                time.sleep(2)

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

            time.sleep(2)

    #fw = open('traindata.txt', 'a+') #testdata file in read/write mode
    url = "http://www.careerbuilder.com"
    listtoholdjob = []
    listtoholdcount = []
    listtoholddescription = []
    listtoholddate = []
    print(listo)

    print("Scraping...")
    for value in listo:
        response = requests.get(url + value)
        html = response.content
        #print(html)
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        #print(soup)
        #driver.get(url + value)
        jobname, applicant, date, description = 'NA', 'NA', 'NA', 'NA'
        # Job Title (Complete Title)
        jobnameChunk = soup.find('div', {'class': 'small-12 item'})
        if jobnameChunk:
            jobname = jobnameChunk.text
            listtoholdjob.append(jobname)

        # applicant number
        applicantChunk=soup.find('div',{'class': 'application-count'})
        #print(applicantChunk)
        if applicantChunk:
            applicant=applicantChunk.text
            listtoholdcount.append(applicant)

        descriptionChunk = soup.find('div', {'class': 'small-12 columns item'})
        if descriptionChunk:
            description = descriptionChunk.text
            #print(description)
        #print(listtoholddescription)
            fw = open('descriptiondata.txt', 'a+')
            for line in description:
                newline = line.rstrip('\r\n')
                fw.write(newline)
            #listtoholddescription.add(newline)
            fw.write("\n")
            fw.write("\n")
            #fw.write(jobname + '\t' + description)
            fw.close()


        #Date when the job was posted

        dateChunk = soup.find('h3', {'id': 'job-begin-date'})
        if dateChunk:
            date = dateChunk.text
            listtoholddate.append(date)

        time.sleep(5)
        final_listtoholdjob = []
        final_listtoholddescription = []
        final_listtoholddate = []

        for j in listtoholdjob:
            final_listtoholdjob.append(j.strip())

        while "\n" in listtoholddescription:
            listtoholddescription.remove("\n")

        for k in listtoholddescription:
            final_listtoholddescription.append(k.strip())

        for v in listtoholddate:
            final_listtoholddate.append(v.strip())

        rows = zip(final_listtoholdjob,listtoholdcount, final_listtoholddate)

        with open('train.csv', 'a+') as outcsv:
            #configure writer to write standard csv file
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            #writer.writerow(['Job Title ','Total Applicant', 'Job Description', 'Date'])
            for row in rows:
                writer.writerow(row)

        outcsv.close()

        #fw.write(jobname + applicant + date + description +'\n')
    time.sleep(2)
    #fw.close()
    endtime = time.time()
    total_time = (endtime - starttime)
    total_time = (total_time / 3600)
    print("Total time to execute the script in hours is:", total_time)

if __name__ == "__main__":
    url = "http://www.careerbuilder.com/jobs-data-analyst?page_number="
    run(url)


#Note: Because I have put the links in a set, it will be randomly selected
