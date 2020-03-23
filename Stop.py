
import numpy as np
import pandas as pd

### Scraping FOMC Transcripts and Generating Path
from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os

link_to_file_on_website = False
path_to_local_pdf = False
path_to_local_txt = True

if link_to_file_on_website:
    base_url = "https://www.federalreserve.gov/monetarypolicy/"
if path_to_local_pdf or path_to_local_txt:
    base_directory = "./feddata/"

transcript_links = {}
for year in range(2019, 2020):  # from 1982 - 2020

    if link_to_file_on_website:
        path = "fomchistorical" + str(year) + ".htm"
        html_doc = requests.get(base_url + path)
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        links = soup.find_all("a", string=re.compile('Transcript .*'))
        link_base_url = "https://www.federalreserve.gov"
        transcript_links[str(year)] = [link_base_url + link["href"] for link in links]

    elif path_to_local_pdf or path_to_local_txt:
        files = []
        path_to_folder = base_directory + str(year)
        new_files = os.walk(path_to_folder)
        for file in new_files:
            for f in file[2]:
                if path_to_local_pdf:
                    if f[-3:] == "minutes.pdf":
                        files.append(str(file[0]) + "/" + f)
                elif path_to_local_txt:
                    if f[-11:] == "minutes.txt":
                        files.append(str(file[0]) + "/" + f)
                if path_to_local_pdf:
                    if f[-3:] == "statement.pdf":
                        files.append(str(file[0]) + "/" + f)
                elif path_to_local_txt:
                    if f[-13:] == "statement.txt":
                        files.append(str(file[0]) + "/" + f)
        transcript_links[str(year)] = files
    print("Year Complete: ", year)

##Create a sorted list of transcripts
###The ordering in this will be important, as we will generate a corresponding list with weigthed word counts
sorted_transcripts = []
for linkset in transcript_links.values():
    sorted_transcripts += linkset
sorted_transcripts = sorted(sorted_transcripts)
print("Number of Documents", len(sorted_transcripts))

# remove stop words from txt files
from nltk.corpus import stopwords
i = 0
for f in sorted_transcripts:
     infile = open(f, 'r')
     text = infile.readlines()
     newfile = open(f[:-4] + 'Stopp.txt','w')
     new_text = []
     for line in text:
         mod_line = line[:-1].split(" ")
         new_line = [word for word in mod_line if word.lower() not in stopwords.words('english')]
         new_string = ""
         for word in new_line:
             new_string += " " + word
         new_string += "\n"
         new_text += new_string
     newfile.writelines(new_text)
     newfile.close()
     infile.close()
     i += 1
     print("File " + str(i) + " of " + str(len(sorted_transcripts)) + " Completed")

#We will now re-adjust our sorted_transcripts list
# run all the adjusting of variable sorted_transcripts in order
mod_transcripts = []
for link in sorted_transcripts:
    mod_transcripts.append(str(link)[:-4] + "Stop.txt")
sorted_transcripts = mod_transcripts
print("Number of Documents", len(sorted_transcripts))
