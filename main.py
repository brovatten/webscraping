from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
from selenium import webdriver

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
    print(links)
    for link in links:
        parsed_html = returnHTMLpage(link)
        link_found = parsed_html.find("a", attrs={'href': re.compile("^https://se.indeed.com/rc/clk")})
        app_list.append(link_found.get("href"))
    return app_list
    # print(applicationLink)


###Här slutade jag senast. Hittade inte referensen till nästa knapp.
def retrieveBtnLink(parsed_html,pagenumber):
    print(parsed_html)
    pageValue = 10*pagenumber
    href_str = "/jobs?q=Internship&amp;start=" + "" + str(pageValue)
    print(href_str)
    link_found = parsed_html.find("a", attrs={'href': re.compile("^" + "" + href_str)})
    print(link_found)

def filtrateJobs_KeyWords(listOfJobs, keywords):
    for url in listOfJobs:
        parsed_html = returnHTMLpage(url)
        jobDescription = parsed_html.find('div', {"id":"jobDescriptionText"})
        keyWordAlgorithm(jobDescription, keywords)


###Slutade här när jag inte kunde hitta ord i html parsingen
def keyWordAlgorithm(jobDescription, keywords):
    counter = 0
    print(jobDescription)
    for word in keywords:
        #print("hej")
        if(jobDescription.find(text=word)):
            counter += 1
    print(counter)










###################################################

my_url = 'https://se.indeed.com/Internship-jobb'

parsed_HTML = returnHTMLpage(my_url)
jobPortalPage = returnJobPortalApplications(parsed_HTML)
#jobLink = returnApplicationLink(jobPortalPage)
#print(jobLink)
###################################################

#retrieveBtnLink(parsed_HTML,1)

filtratedList = filtrateJobs_KeyWords(jobPortalPage, ["We are responsible", "Thank you", "1", "Visa", "1-2","Nordea"])


#my_url2 = 'https://se.indeed.com/viewjob?jk=bef25f175416ca9d&tk=1emib66i8st9i800&from=serp&vjs=3'
#page = returnHTMLpage(my_url2)
#jobDescription = page.find('div', {"id":"jobDescriptionText"})
#print(jobDescription)