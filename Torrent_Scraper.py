import pyperclip as pyperclip
from bs4 import BeautifulSoup
import PySimpleGUI as sg
import cfscrape #for Scraping Cloudflare website to bypass
runner = cfscrape.create_scraper()
title=[]
all_title=[]
magnet_links = []


def search_torrent(query):
    url = 'https://zooqle.unblockit.win/search?q=' + query
    source = runner.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    magnet_results = soup.find_all('a', title='Magnet link', href=True)
    i = 1
    for a in soup.find_all('a', class_='small', href=True):
        all_title.append(a['href'][1:-11])
        i += 1

    for level in range(70,len(all_title)):
        title.append(all_title[level])

    if len(title) == 0:
        sg.Popup("No results Found")
        title.clear()
        all_title.clear()

        return []
    else:
        for links in magnet_results:
            magnet_links.append(links['href'])
        return title


sg.theme("DarkBlue")

layout = [[sg.Text("Torrent Scraper",font=("",23))],
          [sg.Text("Developed by Henry Richard J",font=("",7))],
          [sg.Text("Search: ",font=("",30)),sg.Input(key="query",size=(50,40),font=("",15))],
          [sg.Button("Search",key="Perform_Search")],
          [sg.Text("Results Here:",font=("",20))],
          [sg.Listbox(values=[],key="Results_List",size=(100,20),font=("",15),enable_events=True)]

          ]

window = sg.Window('Torrent Searcher', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
     break


    if event == 'Perform_Search':
        if len(title) !=0:
         title.clear()
         all_title.clear()
         magnet_links.clear()
        window.Element("Results_List").update(values=search_torrent(values['query']))
    if event == 'Results_List':
       selected_List = values["Results_List"][0]
       pyperclip.copy(magnet_links[title.index(selected_List)])
       sg.Popup("Magnet Links","Magnet Links Copied To Clipboard")
