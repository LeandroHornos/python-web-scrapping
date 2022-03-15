# Scraping scientic update's website

## Goal
The idea behind this project is to practice web scraping with BeautifulSoup4.

## Website
The chosen website is Scientific Uptate, a company that sells training courses for profesionals in chemistry-related fields. The idea is to explore all available courses and extract the most relevant information about each of them.

## Structure
Inside dev/ you will find a notebook where the html of the website is studied and functions powered by bs4 are developed in order to extract all relevan information. <br>
In src/ you will find a library called bs4functions.py with all the functions needed to scrap Scientific Update's website. A jupyter notebook is also provided where the sited is crawled and information is dumped to a json file as  an example.

## How to use
Import the function crawlScientificUpdate from bs4functions. In scientific update's site find the url of the courses list and pass it to crawlScientificUpdate as an argument. The function returns an object with a list name "courses" containing the scraped data, and a list of errors obtained.

### example: 
<code>
start_url = "https://www.scientificupdate.com/training/courses/"
data = crawlScientificUpdate(start_url)
</code>