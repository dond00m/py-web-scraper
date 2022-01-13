'''
Example of web scraping using Python and BeautifulSoup. 

Sraping ESPN College Football data 
http://www.espn.com/college-sports/football/recruiting/databaseresults/_/sportid/24/class/2006/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited

The script will loop through a defined number of pages to extract footballer data. 
'''

from asyncio.log import logger
from bs4 import BeautifulSoup
import requests
import os 
import os.path
import csv 
import time 
import logging


def writeCSV(rows, filename):
    with open(filename, 'a', encoding='utf-8') as toWrite:
        writer = csv.writer(toWrite)
        writer.writerows(rows)
 

def getHTMLDocument(url):
    logging.info(f"Get HTML Doc from {url}")
    '''
    Get Beautiful Soup object for provided URL
    '''

    # prepare headers
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

    # fetching the url, raising error if operation fails
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.error(e)
        exit()

    htmlDocument = BeautifulSoup(response.text, "html.parser")

    return htmlDocument

def getWinnerYears(htmlDocument):
    '''
    Parse elements from HTML document and return list of years
    '''
    
    logging.info("Parse HTML Doc")

    # Initialize array to save all extract fields
    winners = []

    # Get iterable of all <h2> headers
    results = htmlDocument.find_all("h2")
    for section in results:
        year = section.text
        logger.debug(f"Found {year}")
        winners.append([year])

    return winners


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    '''
    Set CSV file name. 
    Remove if file alreay exists to ensure a fresh start
    '''
    filename = "nobel_prize_winners.csv"

    # Reset file
    if os.path.exists(filename):
        os.remove(filename)
    
    '''
    Url to fetch
    '''
    baseurl = "https://www.nobelprize.org/prizes/lists/all-nobel-prizes/" 
    page = 1

    # scrape page
    htmlDocument = getHTMLDocument(baseurl)
    # parse page
    winners = getWinnerYears(htmlDocument)
    # write to CSV        
    writeCSV(winners, filename)