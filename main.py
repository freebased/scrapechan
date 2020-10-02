import os
import webbrowser
import requests
from urllib.request import urlopen
import shutil
from bs4 import BeautifulSoup

img = "./img"

try:
    os.mkdir(img)
except OSError:
    print("There was a problem with creating the %s directory (Already exists!)" % img)
else:
    print("Successfully created the %s directory!" % img)

while True:
    try:
        board = input("Enter a \u001b[31mboard\u001b[0m you'd like to use scrapper on: (b, g, etc.)\n")
        number = input("Enter a \u001b[31mthread\u001b[0m you'd like to get scrapped: (e.g 14881783)\n")
    except ValueError:
        print("You didn't enter a value.")
        continue
    else:
        break

path = "./img/" + str(number)

try:
    os.mkdir(path)
except OSError:
    print("Directory %s already exists!" % path)
else:
    print("Succcessfully created the directory %s" % path)

url = "boards.4channel.org/" + board + "/thread/" + number

response = requests.get("https://" + url)

soup = BeautifulSoup(response.text, "html.parser")

tag = soup.find_all("a", class_="fileThumb")

image_info = []

for a in tag:
    image_tag = a.findChildren("img")
    image_info.append((image_tag[0]["src"], image_tag[0]["alt"]))

def download_image(image):
    response = requests.get("https:" + image[0], stream=True)
    realname = ''.join(e for e in image[1] if e.isalnum())

    file = open(path + "/{}.jpg".format(realname), 'wb')

    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    del response

for i in range(0, len(image_info)):
    print("Working on \u001b[31m" + str(image_info[i]) + "\u001b[0m")
    download_image(image_info[i])

