from bs4 import BeautifulSoup

# getAccordionInfo(accordion, split_tag="str")

# This function gets the beautifulsoup object containing the accordion code. 
# # The accordion is a component present in the course overview wich is used 
# # to display basic information about the course, splited in cards containing 
# a title and the info. At the end of the accordion there is info that is not 
# relevant and therefore that part of the code has to be removed. 
# The function receives a substring that indicates where to cut the code

def getAccordionInfo(accordion, split_tag="<h3>Testimonials</h3>"):
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


def getDescriptionInfo(description):
    #config
    tag_changes = [{"old":"<br/>", "new":"" },
         {"old": "|","new": ""},
         {"old": "<p><strong>", "new": "<p>"},
         {"old": "<strong>", "new": "</p><p>"},
         {"old": "</strong>", "new": ""},]
     
    mode = description.find_all("p")[1].find("strong").text.lower()
    dates = []
    raw_dates = description.find_all("p")[2]
    dates_str = str(raw_dates)
    for change in tag_changes:
        dates_str = dates_str.replace(change["old"],change["new"])
    date_ps = BeautifulSoup(dates_str, "html.parser")

    for p in date_ps:
        if p.text.strip() != "":
            dates.append(date.strip().replace(u'\xa0', "").replace("th","th;"))
    return({"dates":dates, "mode":mode})

    