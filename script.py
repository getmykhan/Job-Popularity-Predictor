## Version  1.9.12
## Author : Mohammed Yusuf

from bs4 import BeautifulSoup
import time
import requests
import re
from selenium import webdriver

def run(url):
    dictio=set() #hold all the links scraped.
    pagenumber = 50 #number of pages to scrape


    for page in range(1,pagenumber + 1):
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
                print(test)
                #print(dictio)
            #fw.write(test+'\t')

            time.sleep(2)

    fw = open('testdata.txt', 'a+') #testdata file in read/write mode
    url = "http://www.careerbuilder.com"
    print(dictio)

    print("Scraping...")
    for value in sorted(dictio):
        response = requests.get(url + value)
        html = response.content
        #print(html)
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
        #print(soup)
        #driver.get(url + value)
        applicant, date = 'NA', 'NA'
        # applicant number
        applicantChunk=soup.find('div',{'class': 'application-count'})
        #print(applicantChunk)
        if applicantChunk:applicant=applicantChunk.text

        #Date when the job was posted
        dateChunk = soup.find('h3', {'id': 'job-begin-date'})
        if dateChunk:date = dateChunk.text
        fw.write(applicant + '\t' + date + '\n')
        time.sleep(5)
    time.sleep(2)
    fw.close()



if __name__ == "__main__":
    url = "http://www.careerbuilder.com/jobs-data-analyst?page_number="
    run(url)


#Note: Because I have put the links in a set, it will be randomly selected
