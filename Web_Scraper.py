# Import required libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Get website URL from user
url_name = input("Enter the address of the desired site : ")
# Get target HTML class name from user
cl_name = input("Enter the desired class : ")
try:
    # Send a GET request to the provided URL
    requ = requests.get(url_name)
    # Check if the request was successful (status code should be 200)
    requ.raise_for_status()
except Exception as e:
    # If an error occurs (e.g., network issue or wrong URL), print it
    print(f"Error {e}")
    # Terminate the program
    exit()
# Convert HTML text into a BeautifulSoup object for easy searching
supe = BeautifulSoup(requ.text , 'html.parser')
# Find the <title> tag which contains the page title
title_name = supe.select("title")
# Print the page title
print(title_name)
# For cleaner output
print("-" * 50)

# Find all HTML tags that have the specified class name
cl_all = supe.find_all(class_ = cl_name)
# If no elements with that class are found, show error and exit
if not cl_all:
    print(f"{cl_name} not found!!")
    # Terminate the program
    exit()
    
# List to store extracted titles/texts
cl_title = []
# List to store extracted image links
img_link = []

# idd: Counter for item number (starts from 1)
# item: Each HTML element found with the target class
for idd,item in enumerate(cl_all, 1):
    # Search for h1, h2, h3, h4, a, or span tags inside the
    text_title = item.find(['h1','h2','h3','h4','a','span'])
    # If found, extract the text and strip extra whitespace
    if text_title:
        text = text_title.get_text(strip=True)
    # If no tag found, use a default value
    else:
        text = "not found"
    # Add the extracted text to the titles list
    cl_title.append(text)
    # Look for an <img> tag inside the current element
    img_title = item.find('img')
    # Variable to store the image URL (initially None)
    img_url = None
    
    # Check multiple attributes that might contain the image URL
    # Some websites use custom attributes like data-src
    if img_title:
        for tat in ['data-src','data-lazy-src','src','data-original']:
            if img_title.get(tat):
                # Get the image URL
                img_url = img_title.get(tat)
                # Stop loop once found
                break
        if img_url:
            # If URL starts with // (protocol-relative URL), add https:
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            # If URL starts with / (relative path from site root)
            elif img_url.startswith('/'):
                # Convert it to a full absolute URL
                img_url = urljoin(url_name,img_url)
    # If a valid image URL was found, add it to the images list
    if img_url:
        img_link.append(img_url)
# Print a separator line
print("=" * 50)
# Print the extracted titles
print("List of all titles : ")

# Loop through titles and print each one that isn't "not found"
for ta in cl_title:
    if ta != "not found":
        print(". " + ta)
# Print the extracted image links
print("List of all photos : ")
# Loop through image links and print each one
for link in img_link:
    print(". " + link)
