#!/usr/bin/env python3

import os
import argparse
import webbrowser
import requests
from urllib.request import urlopen
import shutil
from bs4 import BeautifulSoup

img = "./img/"

# Creating images directory
try:
    os.mkdir(img)
except OSError:
    print("Main directory already exists!")
else:
    print("Successfully created the %s directory!" % img)

parser = argparse.ArgumentParser(description='board and thread')
parser.add_argument("board", help="Board shortcut")
parser.add_argument("thread", help="Thread number")
args = parser.parse_args()

board = str(args.board)
thread = str(args.thread)
subfolder = board + "/" + thread

try:
    os.chdir(img)
    os.mkdir(board)
except OSError:
    print("Sub-directory already exists!")
else:
    print("Successfully created the %s directory!" % board)

boards_list =  ["a", "c", "w", "m", "cgl", "cm", "f", "n", "jp"
                "v", "vg", "vm", "vmg", "vp", "vr", "vrpg", "vst",
                "co", "g", "tv", "k", "o", "an", "tg", "sp", "asp",
                "sci", "his", "int", "out", "toy",
                "i", "po", "p", "ck", "ic", "wg", "lit", "mu", "fa",
                "3", "gd", "diy", "wsg", "qst",
                "biz", "trv", "fit", "x", "adv", "lgbt", "mlp", "news", "wsr", "vip",
                "b", "r9k", "pol", "bant", "soc", "s4s",
                "s", "hc", "hm", "h", "e", "u", "d", "y", "t", "hr", "gif", "aco", "r"]

# Checking for board and thread values
while True:
    try:
        if board not in boards_list or len(thread) < 1:
            print("There was some problem with inputs ;(")
            board = input("Enter a \u001b[31mboard\u001b[0m: (b, g, etc.)\n")
            thread = input("Enter a \u001b[31mthread\u001b[0m: (e.g 148817)\n")
    except ValueError:
        print("You didn't enter a value.")
        continue
    else:
        break

path = board + "/" + thread

# Creating thread images directory
try:
    os.mkdir(path)
except OSError:
    print("This thread directory already exists!")
else:
    print("Succcessfully created the %s directory!" % thread)


# Making url request
url = "boards.4channel.org/" + board + "/thread/" + thread
response = requests.get("https://" + url)

# Finding all links with "fileThumb" class
soup = BeautifulSoup(response.text, "html.parser")
tag = soup.find_all("a", class_="fileThumb")

image_info = []
valid_image = []
valid_image_name = []

# Appending image info to the list
for a in tag:
    image_tag = a.findChildren("img")
    image_info.append((image_tag[0]["src"], image_tag[0]["alt"]))

# Changing URL from shortcut to full-size img
for i in image_info:
    valid_url = "//is2.4chan."
    valid_format = ".jpg"
    i = valid_url + ((i[0][9:-5])) + valid_format
    valid_image.append(i)

# Changing filename
for i in image_info:
    if len(board) > 1:
        valid_name = (i[0][16:-5])
    else:
        valid_name = (i[0][15:-5])
    
    i = valid_name + ((i[1][:0]))
    valid_image_name.append(i)


# Downloading image function
def download_image(image):
    response = requests.get("https:" + valid_image[i], stream=True)
    realname = ''.join(e for e in valid_image_name[i] if e.isalnum())

    file = open(path + "/{}.jpg".format(realname), 'wb')

    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    del response

# Downloading image
for i in range(0, len(image_info)):
    print("Working on \u001b[31m" + str(valid_image_name[i]) + "\u001b[0m" + "!")
    download_image(image_info[i])

print("Process finished!")
