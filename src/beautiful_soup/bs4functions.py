from bs4 import BeautifulSoup
import re


def getHeader(soup):
    try:
        main_item = soup.find("div", class_="main-item")
        for match in main_item.find_all("span", class_="title"):
            match.replaceWith("")
        title = main_item.h1.text.capitalize().strip()
        date = main_item.find("p", "date").text.strip()
        location = main_item.find("p", "location").text.strip()
        return {"title": title, "date": date, "location": location}
    except Exception as e:
        print("Header information could not be scrapped:\n", e)
        return {"title": None, "date": None, "location": None}


# getAccordionInfo(soup: bs4_obj, split_tag: string)
# --------------------------------------------


# This function gets the beautifulsoup object containing the accordion code.
# The accordion is a component present in the course overview wich is used
# to display basic information about the course, splited in cards containing
# a title and the info. At the end of the accordion there is info that is not
# relevant and therefore that part of the code has to be removed.
# The function receives a substring that indicates where to cut the code


def getAccordionInfo(soup, split_tag="<h3>Testimonials</h3>"):
    try:
        accordion = soup.find(id="accordion")
        # config
        changes = [
            {"old": "<li>", "new": ""},
            {"old": "</li>", "new": ". "},
            {"old": "<ul>", "new": "<p>"},
            {"old": "</ul>", "new": "</p>"},
            {"old": "<strong>", "new": ""},
            {"old": "</strong>", "new": " "},
        ]

        # Accordion is splitted and only the beggining is kept
        splitted = str(accordion).split(split_tag)[0]
        accordion = BeautifulSoup(splitted, "lxml").find(id="accordion")

        children = []
        texts = []
        children = accordion.findChildren(recursive=False)
        for child in children:
            if child.name in ["h1", "h2", "h3"]:
                texts.append(child.text.strip().upper() + ":")
            else:
                texts.append(child.text.strip())
        text = " ".join(texts)
        # Remove any double spaces
        text = re.sub(r"([a-z])([A-Z])", r"\1. \2", text)
        return {"information": text}
    except Exception as e:
        print("Accordion information could not be scrapped:\n", e)
        return {"information": None}


# getDescriptionInfo(soup:bs4_obj)
# ---------------------------------------

# This function extracts the info from the description box of the website
# it gets the dates and times of the classes, the mode (online or irl)
# and a short pictch describing what the course is about.


def getDescriptionInfo(soup):
    description = soup.find(class_="description")
    # config
    tag_changes = [
        {"old": "<br/>", "new": ""},
        {"old": "|", "new": ""},
        {"old": "<p><strong>", "new": "<p>"},
        {"old": "<strong>", "new": "</p><p>"},
        {"old": "</strong>", "new": ""},
    ]

    # Get the raw data from the description html

    raw_pitch = description.find_all("p")

    # Unify the pitch in one single text
    pitch = ""
    for p in raw_pitch:
        pitch = pitch + " " + p.text
    pitch = pitch.strip()

    return {"pitch": pitch}


# getFeeInfo(soup:bs4_obj):
# --------------------------------

# This function takes a code soup and identifies the
# div that contains the fee info, and then extracts it


def getFeeInfo(soup):
    no_result = {"price": None, "currency": None}
    boxes = soup.find_all("div", class_="box")
    box = None
    for div in boxes:
        if div.h3:
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
    return {"price": value[1:], "currency": value[0]}


# scrapCourse(soup:bs4_obj):
# --------------------------------

# This function calls all the other functions
# in order to completely scrap all the info
# in a course overview page, feeded as a bs4 object


def scrapCourse(soup):
    # Scrap all data
    header = getHeader(soup)
    information = getAccordionInfo(soup)
    description = getDescriptionInfo(soup)
    fee = getFeeInfo(soup)
    # Merge all in a single dictionary
    data = header | information | description | fee
    return data
