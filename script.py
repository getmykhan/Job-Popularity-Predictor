## Version 1.0



from bs4 import BeautifulSoup
import re
import requests
import time

def start(url):

    pagenumber = 6

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
            testChunk=data.find('div',{'class': 'columns large-2 medium-3 small-12'})
            if testChunk:
                test=testChunk.text
                print(test)
            fw.write(test+'\t')

            time.sleep(2)

    fw.close()

if __name__ == "__main__":
    url = "http://www.careerbuilder.com/jobs-data-analyst?page_number="
    start(url)
