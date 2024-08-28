import AO3 
from AO3 import works, utils, search, GuestSession, Session, common
import math, time

# stores how many fics user has downloaded
counter = 0


def searchCrit(pagenum):
    #**************************************************#
    #* Change these parameters to alter the search!!! *#
    #*          DO NOT ALTER THE PAGE NUMBER          *#
    #**************************************************#
    results = AO3.search.search(relationships="Dande | Leon/Sonia", sort_column="kudos_count", word_count=AO3.utils.Constraint(0, 3000), completion_status="complete", page=pagenum)    
    
    return results

def getIds(results):
    idList = []
    for work in results.find_all("li", {"role": "article"}):
        if work.h4 is None:
            continue

        try:
            for a in work.h4.find_all("a"):
                if 'rel' in a.attrs.keys():
                    if "author" in a['rel']:
                        continue
                elif a.attrs["href"].startswith("/works"):
                    workid = utils.workid_from_url(a['href'])
                    idList.append(workid)

        except AttributeError:
            pass
    return idList


def downloadFics(pageNum):
    global counter
    results = searchCrit(pageNum)
    ids = getIds(results)
    for id in ids:
        work = AO3.Work(id)
        counter = counter + 1
        print(f"[{counter}] Downloading {work.title} by {work.authors}")
        with open(f"auto_fics/{work.title}.mobi", "wb") as file:
            file.write(work.download("MOBI"))
        time.sleep(1.5)



    



def auto():
    results = searchCrit(1)

    maindiv = results.find("div", {"class": "works-search region", "id": "main"})
    totalResults = int(maindiv.find("h3", {"class": "heading"}).getText().replace(',','').replace('.','').strip().split(" ")[0])

    numPages = math.ceil(totalResults / 20)

    print(f"Results found: {totalResults}\nPages: {numPages}")

    try:
        for page in range(numPages):
            page +=  1
            print(f"PAGE {page}")
            downloadFics(page)
        print("Complete! Enjoy :3")

    except Exception:
        print(Exception.message)
        


def main():
    auto()


main()