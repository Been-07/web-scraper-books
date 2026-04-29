import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


url_name = input("Enter the address of the desired site : ")
cl_name = input("Enter the desired class : ")

try:
    requ = requests.get(url_name)
    requ.raise_for_status()
except Exception as e:
    print(f"Error {e}")
    exit()

supe = BeautifulSoup(requ.text , 'html.parser')
title_name = supe.select("title")
print(title_name)
print("-" * 50)

cl_all = supe.find_all(class_ = cl_name)
if not cl_all:
    print(f"{cl_name} not found!!")

cl_title = []
img_link = []

for idd,item in enumerate(cl_all, 1):
    text_title = item.find(['h1','h2','h3','h4','a','span'])
    if text_title:
        text = text_title.get_text(strip=True)
    else:
        text = "not found"
    
    cl_title.append(text)
    img_title = item.find('img')
    img_url = None
    
    if img_title:
        for tat in ['data-src','data-lazy-src','src','data-original']:
            if img_title.get(tat):
                img_url = img_title.get(tat)
                break
        if img_url:
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif img_url.startswith('/'):
                img_url = urljoin(url_name,img_url)
    if img_url:
        img_link.append(img_url)

print("=" * 50)
print("List of all titles : ")

for ta in cl_title:
    if ta != "not found":
        print(". " + ta)

print("List of all photos : ")
for link in img_link:
    print(". " + link)
