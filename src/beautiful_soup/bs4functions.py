from bs4 import BeautifulSoup
import re

def getTitle(soup):
    title = None
    main_item = soup.find("div", class_="main-item")
    title = main_item.h1.text
    return({"title": title})

# getAccordionInfo(soup: bs4_obj, split_tag: string)
# --------------------------------------------


# This function gets the beautifulsoup object containing the accordion code. 
# The accordion is a component present in the course overview wich is used 
# to display basic information about the course, splited in cards containing 
# a title and the info. At the end of the accordion there is info that is not 
# relevant and therefore that part of the code has to be removed. 
# The function receives a substring that indicates where to cut the code

def getAccordionInfo(soup, split_tag="<h3>Testimonials</h3>"):
    accordion = soup.find(id="accordion")
    #config
    changes = [{"old":"<li>", "new":"" },
         {"old": "</li>","new": ". "},
         {"old": "<ul>", "new": "<p>"},
         {"old": "</ul>", "new": "</p>"},
         {"old": "<strong>", "new": ""},
         {"old": "</strong>", "new": " "}]
    
    # Accordion is splitted and only the beggining is kept
    splitted = str(accordion).split(split_tag)[0]
    accordion = BeautifulSoup(splitted, "lxml").find(id="accordion")
    
    # Get titles and divs
    titles = accordion.find_all("h3")
    divs = accordion.find_all("div")
    
    # Clean content
    new_divs= []

    for div in divs:
        string = str(div)
        for change in changes:
            string = string.replace(change["old"], change["new"])
        code = BeautifulSoup(string, "html.parser")
        new_divs.append(code)
        
    # Prepare data and return it
    data = []

    for i in range(len(titles)):
        data.append({"title":titles[i].text, "content":new_divs[i].text})
    
    return data

# getDescriptionInfo(soup:bs4_obj)
# ---------------------------------------

# This function extracts the info from the description box of the website
# it gets the dates and times of the classes, the mode (online or irl)
# and a short pictch describing what the course is about.

def getDescriptionInfo(soup):
    description = soup.find(class_="description")
    #config
    tag_changes = [{"old":"<br/>", "new":"" },
         {"old": "|","new": ""},
         {"old": "<p><strong>", "new": "<p>"},
         {"old": "<strong>", "new": "</p><p>"},
         {"old": "</strong>", "new": ""},]
     
    # Get the raw data from the description html
    mode = description.find_all("p")[1].find("strong").text.lower()
    raw_pitch = description.find_all("p")[3:]
    raw_dates = description.find_all("p")[2]
    
    # Unify the pitch in one single text
    pitch = ""
    for p in raw_pitch:
        pitch = pitch + " " + p.text
    pitch = pitch.strip()
    
    # Format the dates
    dates=[]
    dates_str = str(raw_dates)
    for change in tag_changes:
        dates_str = dates_str.replace(change["old"],change["new"])
    date_ps = BeautifulSoup(dates_str, "html.parser")

    for p in date_ps:
        if p.text.strip() != "":
            dates.append(p.text.strip().replace(u'\xa0', "").replace("th","th;"))
    return({"dates":dates, "mode":mode, "pitch": pitch})


# getFeeInfo(soup:bs4_obj):
# --------------------------------

# This function takes a code soup and identifies the
# div that contains the fee info, and then extracts it
# using the getPrice(price:bs4_obj) function

def getPrice(price):
    value = None
    match = re.match("^\£?\$?\d+\.\d+", price.text)
    if(match):
        value = match.group(0)
    return {"price": value[1:], "currency": value[0] }


def getFeeInfo(soup):
    no_result = {"price": None, "currency": None}
    boxes = soup.find_all("div", class_="box")
    box = None
    for div in boxes:
        if(div.h3):
            if div.h3.text.upper() == "FEE INFO":
                box = div
    if not box:
        return no_result
    price = box.find("span", class_="price")
    if not price:
         return no_result
    value = None
    match = re.match("^\£?\$?\d+\.\d+", price.text)
    if match:
        value = match.group(0)
    return {"price": value[1:], "currency": value[0] }