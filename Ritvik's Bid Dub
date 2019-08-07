from flask import Flask, render_template, request
import webbrowser, sys, requests, bs4, selenium
import cgi
import cgitb;
import pandas

name1 = "Huang"
name2 = "Manifredi"

f = open("BIDS.txt", "r") #open file

#keep iterating through lines until you get the right one
text= f.readline()
while text.find(name1)==-1 or text.find(name2)==-1:
    text=f.readline()
    
    
#make a string with a list of all their numbers 
new_text = f.readline()
while(new_text.find("&")==-1):
    text+= new_text
    new_text= f.readline()
    
    
    
# in a list like 0,1,0,2 we only care about 0 and 0. The fact that they are both 0 means there are two silver bids. 
#A non-zero value indicates a gold bid
even=True #this helps switch off every other number

silver_count=0;
gold_count=0;
for elem in text:
    if (elem>= "0" and elem<= "9"): #if the element we are looking at is a number
            if even: #if its one of the 0th, 2nd, 4th, etc element (the ones we care about)
                if elem=="0":
                    silver_count+=1  #if 0, silver
                else:
                    gold_count+=1 #if not, gold
                even=False
            else:
                even=True

print("Gold: " + str(gold_count) + " Silver: " + str(silver_count))
