## Version  1.0.10



from bs4 import BeautifulSoup
import time
import requests
import re
from selenium import webdriver

driver = webdriver.Chrome()
def run(url):
    dictio=set()
    pagenumber = 1

    fw = open('testdata.txt', 'w')


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
            fw.write(test+'\t')

            time.sleep(2)

    fw.close()
    return dictio

def ite(dictio):
    url = "http://www.careerbuilder.com/jobs-data-analyst?page_number="
    for value in dictio:
        #print(value)
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(url + value)
                html=response.content # get the html
                print(html)
                driver.get(url + value)
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                #time.sleep(2) # wait 2 secs



if __name__ == "__main__":
    url = "http://www.careerbuilder.com/jobs-data-analyst?page_number="
    ite(run(url))
