from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import popupJobs
from selenium import webdriver


def currentpageurl(url, currentpage):
    nextPageIndex = currentpage * 10
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


# def retrieveBtnLink(parsed_html,pagenumber):
# pageValue = 10*pagenumber
# href_str = "/jobs?q=Internship&amp;start=" + "" + str(pageValue)
#    link_found = parsed_html.find("a", attrs={'href': re.compile("^" + "" + href_str)})

def filtrateJobs_KeyWords(listOfJobs, preferredKeys, requiredKeys):
    job_dict = {}  # Storing {url:preferedkey_counter}
    for url in listOfJobs:
        parsed_html = returnHTMLpage(url)
        jobDescription = parsed_html.find('div', {"id": "jobDescriptionText"})
        numberOfpreferedkeys = keywordAlgo(jobDescription, preferredKeys, requiredKeys)
        if (numberOfpreferedkeys > -1):
            job_dict[url] = numberOfpreferedkeys
    job_dict = sortDictbyPreferedKeys(job_dict)
    return job_dict


def sortDictbyPreferedKeys(job_dict):
    return {k: v for k, v in sorted(job_dict.items(), key=lambda item: item[1])}


def containsRequiredKeys(jobDescription, requiredKeys):
    requiredWordCounter = 0
    for word in requiredKeys:
        if (jobDescription.findAll(text=re.compile(word))):
            requiredWordCounter += 1
    if (requiredWordCounter == len(requiredKeys)):
        return True
    else:
        return False


def preferedKeysCounter(jobDescription, preferredKeys):
    preferedWordCounter = 0
    for word in preferredKeys:
        if (jobDescription.findAll(text=re.compile(word))):
            preferedWordCounter += 1
    return preferedWordCounter


###Slutade här när jag inte kunde hitta ord i html parsingen
def keywordAlgo(jobDescription, preferredKeys, requiredKeys):
    if (containsRequiredKeys(jobDescription, requiredKeys)):
        return preferedKeysCounter(jobDescription, preferredKeys)
    return -1

def printFilteredJobs(job_dict):
    for key in job_dict:
        print(key + "  counter:" + str(job_dict[key]))

###################################################

my_url = 'https://se.indeed.com/jobb?q=Internship&start=0'
currentpage = 0
required_key_words = ['']
preferred_key_words = ['data science', 'machine learning', 'internship']
job_list = []

while True:
    if (currentpage == 1):
        print(currentpage)
        break
    else:
        # starting at 0
        my_url = currentpageurl(my_url, currentpage)
        currentpage += 1
        parsed_HTML = returnHTMLpage(my_url)
        jobPortalPage = returnJobPortalApplications(parsed_HTML)
        job_list = job_list + jobPortalPage

job_dict = filtrateJobs_KeyWords(job_list, preferred_key_words, required_key_words)
printFilteredJobs(job_dict)
popupJobs.startJobsSites(job_dict)
###################################################
