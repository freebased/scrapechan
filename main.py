#!/usr/bin/env python3

import os
import argparse
import webbrowser
import requests
from urllib.request import urlopen
import shutil
from bs4 import BeautifulSoup

img = "./img"

#Creating images directory
try:
    os.mkdir(img)
except OSError:
    print("%s directory already exists!" % img)
else:
    print("Successfully created the %s directory!" % img)

parser = argparse.ArgumentParser(description='board and thread')
parser.add_argument("board", help = "Board shortcut")
parser.add_argument("thread", help="Thread number")
args = parser.parse_args()

board = str(args.board)
thread = str(args.thread)

boards_list = ["a", "c", "g", "k", "m", "o", "p", "v", "vg", "vr", "w", "vip", "qa", "cm", "lgbt",
                "3", "adv", "an", "asp", "biz", "cgl", "ck", "co", "diy", "fa", "fit", "gd", "his",
                "int", "jp", "lit", "mlp", "mu", "n", "news", "out", "po", "qst", "sci", "sp", "tg",
                "toy", "trv", "tv", "vp", "wsg", "wsr", "x"]

#Checking for board and thread values
while True:
    try:
        if board not in boards_list or len(thread) < 1:
            print("There was some problem with inputs ;(")
            board = input("Enter a \u001b[31mboard\u001b[0m you'd like to use scrapper on: (b, g, etc.)\n")
            thread = input("Enter a \u001b[31mthread\u001b[0m you'd like to get scrapped: (e.g 14881783)\n")
    except ValueError:
        print("You didn't enter a value.")
        continue
    else:
        break

path = "./img/" + str(thread)

#Creating thread images directory
try:
    os.mkdir(path)
except OSError:
    print("Directory %s already exists!" % path)
else:
    print("Succcessfully created the directory %s" % path)


#Making url request
url = "boards.4channel.org/" + board + "/thread/" + thread
response = requests.get("https://" + url)

#Finding all links with "fileThumb" class
soup = BeautifulSoup(response.text, "html.parser")
tag = soup.find_all("a", class_="fileThumb")

image_info = []

#Appending image info to the list
for a in tag:
    image_tag = a.findChildren("img")
    image_info.append((image_tag[0]["src"], image_tag[0]["alt"]))

#Downloading image function
def download_image(image):
    response = requests.get("https:" + image[0], stream=True)
    realname = ''.join(e for e in image[1] if e.isalnum())

    file = open(path + "/{}.jpg".format(realname), 'wb')

    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    del response

#Downloading image
for i in range(0, len(image_info)):
    print("Working on \u001b[31m" + str(image_info[i]) + "\u001b[0m")
    download_image(image_info[i])

print("Process finished!")

