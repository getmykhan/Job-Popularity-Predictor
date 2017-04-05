## Version  1.7.10


from bs4 import BeautifulSoup
import time
import requests
import re
from selenium import webdriver

def run(url):
    dictio=set()
    pagenumber = 2


    for page in range(1,pagenumber + 1): # for each page
        print ('page',page)

        html=None
        pageLink=url + str(page)


        for i in range(5): # try 5 times
            try:
                    #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs

        if not html:continue

        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')

        datum = soup.findAll('div', attrs = {'class': 'job-row'})

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

    fw = open('testdata.txt', 'a+')
    url = "http://www.careerbuilder.com"
    print(dictio)
    
"""
    for value in dictio:
        #print(value)
        try:
            #use the browser to access the url
            response=requests.get(url + value)
            html=response.content # get the html
            #print(html)
            soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml')
            #print(soup)
            #driver.get(url + value)
            time.sleep(5)
            applicant = 'NA'
            applicantChunk=soup.find('div',{'class': 'application-count'})
            #print(applicantChunk)
            if applicantChunk:
                applicant=applicantChunk.text
                print(applicant)
            fw.write(applicant+'\t')
            break # we got the file, break the loop
        except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
            print ('failed attempt',Exception)
                #time.sleep(2) # wait 2 secs
        fw.close()

"""

if __name__ == "__main__":
    url = "http://www.careerbuilder.com/jobs-data-analyst?page_number="
    run(url)
