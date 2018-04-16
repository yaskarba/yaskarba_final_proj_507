import requests
import json
import sqlite3
from bs4 import BeautifulSoup
import re
from statistics import mean
import plotly.plotly as py

CACHE_FNAME="final_proj_cache_yk.json"
DBNAME = 'dogs.db'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
  unique_ident = get_unique_key(url)

  if unique_ident in CACHE_DICTION:
      # print("Getting cached data...")
      return CACHE_DICTION[unique_ident]

  else:
      print("Making a request for new data...")
      # Make the request and cache the new data
      resp = requests.get(url)
      CACHE_DICTION[unique_ident] = resp.text
      dumped_json_cache = json.dumps(CACHE_DICTION)
      fw = open(CACHE_FNAME,"w")
      fw.write(dumped_json_cache)
      fw.close() # Close the open file
      return CACHE_DICTION[unique_ident]

def get_dogs():
  dog_sites=[]
  full_dog_list=[]
  for i in range(16):

    url="http://www.akc.org/dog-breeds/page/"+str(i+1)+"/?group%5B0%5D=sporting&group%5B1%5D=hound&group%5B2%5D=working&group%5B3%5D=terrier&group%5B4%5D=toy&group%5B5%5D=non-sporting&group%5B6%5D=herding"
    resp = make_request_using_cache(url)
    soup=BeautifulSoup(resp, "html.parser")
    search_soup=soup.find(class_="breed-card-type-grid")
    sites=search_soup.find_all(class_="grid-col")
    for site in sites:
      dog_sites.append(site.find("a")["href"])
    # Find the basic data
  for item in dog_sites:
    dog_list=[]
    doggo=make_request_using_cache(item)
    beautiful_doggo=BeautifulSoup(doggo, "html.parser")

    # Dog breed name
    search_doggo=beautiful_doggo.find("h1")
    search_doggo_name=search_doggo.text.strip()
    dog_list.append(search_doggo_name)

    # Dog rank
    search_doggo2=beautiful_doggo.find_all(class_="attribute-list__description attribute-list__text ")
    if len(search_doggo2) !=5:
      pass
    else:
      # Rank
      rank_1=search_doggo2[0].text.strip()
      rank_2=re.findall(r'\d+', rank_1)
      rank_3=int(rank_2[0])
      dog_list.append(rank_3)
      # Height
      height_1=search_doggo2[1].text.strip()
      height_2=re.findall(r'\d+', height_1)
      height_3=[]
      for item in height_2:
        height_3.append(int(item))
      height_4=mean(height_3)
      height_5=int(height_4)
      dog_list.append(height_5)
      # Weight
      weight_1=search_doggo2[2].text.strip()
      weight_2=re.findall(r'\d+', weight_1)
      weight_3=[]
      for item in weight_2:
        weight_3.append(int(item))
      try:
        weight_4=mean(weight_3)
        weight_5=int(weight_4)
        # print(weight_5)
      except:
        weight_5=99
      dog_list.append(weight_5)

      #Life expectancy
      life=search_doggo2[3].text.strip()
      life_2=re.findall(r'\d+', life)
      life_3=[]
      for item in life_2:
        life_3.append(int(item))
      try:
        life_4=mean(life_3)
        life_5=int(life_4)
      except:
        life_5=16
      dog_list.append(life_5)

      # Group
      group=search_doggo2[4].text.strip()
      dog_list.append(group)

      full_dog_list.append(dog_list)
  return full_dog_list
def create_db():
    try:
        conn = sqlite3.connect('dogs.db')
        cur = conn.cursor()
    except Exception as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'Dogs';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Groups';
    '''
    cur.execute(statement)

    conn.commit()

    # Your code goes here
    statement = '''
        CREATE TABLE 'Dogs' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' TEXT,
        'Rank' INTEGER,
        'Height' INTEGER,
        'Weight' INTEGER,
        'LifeExpectancy' INTEGER,
        'Groups' INTEGER,
        FOREIGN KEY (Groups) REFERENCES Groups(Id)
        );
    '''
    cur.execute(statement)
    statement = '''
        CREATE TABLE 'Groups' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'GroupName' TEXT
        );
    '''
    cur.execute(statement)
    conn.commit()

create_db()

x=get_dogs()

def populate_database(x):
  conn=sqlite3.connect(DBNAME)
  cur=conn.cursor()
  for item in x:
    insert_var=(item[0], item[1], item[2], item[3], item[4], item[5])
    statement="INSERT INTO Dogs "
    statement+="VALUES(NULL, ?, ?, ?, ?, ?, ?)"
    cur.execute(statement, insert_var)
  conn.commit()

group_list=["Sporting Group", "Working Group", "Toy Group", "Non-Sporting Group", "Herding Group", "Terrier Group", "Hound Group"]
def pop_groups(group_list):
  conn=sqlite3.connect(DBNAME)
  cur=conn.cursor()
  for group in group_list:
    insert_var=(group,)
    statement="INSERT INTO Groups "
    statement+="VALUES(NULL, ?)"
    # print(statement, insert_var)
    cur.execute(statement, insert_var)
  conn.commit()

populate_database(x)
pop_groups(group_list)
