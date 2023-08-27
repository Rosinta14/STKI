!pip install requests
import requests
import pandas as pd
import json
import os
from bs4 import BeautifulSoup
import csv
from itertools import chain
def get_href(url, selector):
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.select(selector)
    href = [item.get('href') for item in element]
    return href
  else:
    print(response.status_code)

abjad = get_href('http://repository.lppm.unila.ac.id/view/creators/', '#content > div > div > div > a')
abjad.append('index.=3F-3.html')
abjad

author = []
base_url = 'http://repository.lppm.unila.ac.id/view/creators/'
for i in abjad:
  author.append(get_href(base_url + i, '#content > div > table > tr > td > ul > li > a'))
author

fields = ['divisions', 'title', 'abstract', 'subjects', 'publication', 'publisher', 'date', 'keywords']
with open('data_publikasi.csv', 'a') as f:
  writer = csv.DictWriter(f, fieldnames=fields)
  writer.writeheader()

  for item in list(chain.from_iterable(author)):
    url = "http://repository.lppm.unila.ac.id/cgi/exportview/creators/" + item[:-5] + "/JSON/" + item[:-5] + ".js"

    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      for value in data:
        writer.writerow({field: value.get(field) for field in fields})
    else:
      print(response.status_code)
