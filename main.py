from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from selenium import webdriver

def currentpageurl(url, currentpage):
    nextPageIndex = currentpage*10
    url = 'https://se.indeed.com/jobb?q=Internship&start=' + str(nextPageIndex)
    return url

def returnHTMLpage(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    return page_soup


def returnJobPortalApplications(parsed_html):
    links = []
    for link in parsed_html.findAll('a', attrs={'href': re.compile("^/rc/clk")}):
        links.append('https://se.indeed.com' + link.get('href'))
    return links


def iteratePortalLinks(links):
    for link in links:
        parsed_HTML = returnHTMLpage(link)
        returnApplicationLink(parsed_HTML)


def returnApplicationLink(links):
    app_list = []
    for link in links:
        parsed_html = returnHTMLpage(link)
        link_found = parsed_html.find("a", attrs={'href': re.compile("^https://se.indeed.com/rc/clk")})
        app_list.append(link_found.get("href"))
    return app_list

#def retrieveBtnLink(parsed_html,pagenumber):
   # pageValue = 10*pagenumber
   # href_str = "/jobs?q=Internship&amp;start=" + "" + str(pageValue)
#    link_found = parsed_html.find("a", attrs={'href': re.compile("^" + "" + href_str)})

def filtrateJobs_KeyWords(listOfJobs, keywords):
    job_list_temp = []
    for url in listOfJobs:
        parsed_html = returnHTMLpage(url)
        jobDescription = parsed_html.find('div', {"id":"jobDescriptionText"})
        if(goodMatch(jobDescription, keywords)):
            job_list_temp.append(url)



###Slutade här när jag inte kunde hitta ord i html parsingen
def goodMatch(jobDescription, keywords):
    counter = 0
    print(jobDescription)
    print(type(jobDescription))
    for word in keywords:
        #print("hej")
        print("word:" + word)
        if(jobDescription.findAll(text=re.compile(word))):
            counter += 1
    if(counter> 0):
        print(counter)
        return True
    print(counter)






###################################################

#my_url = 'https://se.indeed.com/Internship-jobb'
my_url = 'https://se.indeed.com/jobb?q=Internship&start=0'
currentpage = 0
required_key_words = ['bachelors']
#prefered_key_words = ['cations']
job_list = []
while True:
    if(currentpage == 1):
        print(currentpage)
        break
    else:
                 #starting at 0
        my_url = currentpageurl(my_url,currentpage)
        currentpage+=1
        #print(currentpage)
        #print(my_url)
        parsed_HTML = returnHTMLpage(my_url)
        jobPortalPage = returnJobPortalApplications(parsed_HTML)
        job_list = job_list + jobPortalPage


filtrateJobs_KeyWords(job_list,key_words)
print()
###################################################

#print(retrieveBtnLink(parsed_HTML,1))

#filtratedList = filtrateJobs_KeyWords(jobPortalPage, ["We are responsible", "Thank you", "1", "Visa", "1-2","Nordea"])


#my_url2 = 'https://se.indeed.com/viewjob?jk=bef25f175416ca9d&tk=1emib66i8st9i800&from=serp&vjs=3'
#page = returnHTMLpage(my_url2)
#jobDescription = page.find('div', {"id":"jobDescriptionText"})
#print(jobDescription)