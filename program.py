import AO3 
import bs4
from AO3 import works, utils, search, GuestSession, Session, common

results = AO3.search.search(relationships="Dande | Leon/Sonia", sort_column="kudos_count", word_count=AO3.utils.Constraint(0, 50000), completion_status="complete")

def searchFics():
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
                    workname = a.string
                    workid = utils.workid_from_url(a['href'])
                    idList.append(workid)
        except AttributeError:
            pass

    maindiv = results.find("div", {"class": "works-search region", "id": "main"})
    total_results = int(maindiv.find("h3", {"class": "heading"}).getText().replace(',','').replace('.','').strip().split(" ")[0])
       

    print(f"Results found: {total_results}\nResults shown: {len(idList)}")

    forceExit = False

    for id in idList:
        work = AO3.Work(id)
        print(f"Do you want to download {work.title} by {work.authors}?\nIt was updated on {work.date_updated}, has {work.kudos} kudos and {work.words} words.\n")
        print(f"Relationships: {work.relationships}\nCharacters: {work.characters}\nTags: {work.tags}\n")
        
        response = input("Yes: y\nNo: n\nQuit:q\n").lower()
        if response == 'y':
            with open(f"fics/{work.title}.mobi", "wb") as file:
                file.write(work.download("MOBI"))
        elif response == 'q':
            print("Exiting program.")
            forceExit = True
            break
        else:
            print("Work skipped.\n")

    if forceExit == False:
        print("End of results on selected page.")

        


def main():
    searchFics()


main()