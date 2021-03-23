import requests
from bs4 import BeautifulSoup
import re
import time

def get_link(link):
    
    while True:
        try:
            headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
            page = requests.get(link, headers=headers)
            break
        except:
            print('Something Went Wrong! Retrying...')
            print(link)
            time.sleep(30)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    return soup

def find_page_links(soup):
    links = []
    uls = soup.find_all('ul', class_ = "Im_AnnouncesBlock")
    for ul in uls[0].find_all('li'):
        link = ul.find('a').attrs['href']
        full_link = f'https://www.imali.biz/{link}'
        links.append(full_link)
        
    return links

def find_all_links(page):
    num_page = page+1
    page = f'https://www.imali.biz/AnnounceBySection.html?pg={num_page}&section_id=24'
    soup = get_link(page)
    page_links = find_page_links(soup)
    
    return page_links

def get_houses_info(link):  
    house_info = get_link(link)
    try:
        date = house_info.find('span', class_ = 'Posted_date').text.replace('Posted on:','')
        price = house_info.find('span', class_ = 'Price').text
        location = house_info.find('div', class_ = "Im_Ann_Owner_Description").find('li').text.replace('City: ', '')
        details = house_info.find('div',  id = 'Im_Ann_Text').text
        details = re.sub(r'\n|\t|\r','',details)
    except:
        date = 'Failed'
        price = 'Failed'
        location = 'Failed'
        details = 'Failed'
    
    all_info = [date, link, price, location, details]
    
    return all_info

####################Multithreading#################################################################################
def get_houses_thread(links):
    all_info = []
    for link in links:
        house_info = get_link(link)
        date = house_info.find('span', class_ = 'Posted_date').text.replace('Posted on:','')
        price = house_info.find('span', class_ = 'Price').text
        location = house_info.find('div', class_ = "Im_Ann_Owner_Description").find('li').text.replace('City: ', '')
        details = house_info.find('div',  id = 'Im_Ann_Text').text
        details = re.sub(r'\n|\t|\r','',details)
        all_info.append([date, link, price, location, details])
    
    return all_info
