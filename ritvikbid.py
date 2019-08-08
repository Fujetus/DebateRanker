from flask import Flask, render_template, request
import webbrowser, sys, requests, bs4, selenium
import cgi
import cgitb;
import pandas

name1 = "Jain"
name2 = "Jain"

f = open("BIDS.txt", "r")  # open file

# keep iterating through lines until you get the right one
text= "nonsense"
while text!= "":
    text = f.readline()
    if(text.find(name1)!=-1 and text.find(name2)!=-1):
        if(name1==name2):
            index_of_ampersand= text.index("&")
            if(text[0:index_of_ampersand].find(name1)!= -1 and text[index_of_ampersand:text.__len__()].find(name1)!=-1):
                break
        else:
            break
# make a string with a list of all their numbers
if text.__len__()== 0:
    print("No Bids")
    exit()
else:
    new_text = f.readline()
    while (new_text.find("&") == -1):
        text += new_text
        new_text = f.readline()

    # in a list like 0,1,0,2 we only care about 0 and 0. The fact that they are both 0 means there are two silver bids.
    # A non-zero value indicates a gold bid
    even = True  # this helps switch off every other number

    silver_count = 0;
    gold_count = 0;
    for elem in text:
        if (elem >= "0" and elem <= "9"):  # if the element we are looking at is a number
            if even:  # if its one of the 0th, 2nd, 4th, etc element (the ones we care about)
                if elem == "0":
                    silver_count += 1  # if 0, silver
                else:
                    gold_count += 1  # if not, gold
                even = False
            else:
                even = True

    print("Gold: " + str(gold_count) + " Silver: " + str(silver_count))