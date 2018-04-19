import requests
import time
start = time.time()
import json
import sqlite3
from bs4 import BeautifulSoup
import re
from statistics import mean
from prettytable import PrettyTable
import plotly.plotly as py
import plotly.graph_objs as go

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

# Comment this out if you're doing the demo
create_db()
x=get_dogs()
populate_database(x)
pop_groups(group_list)

# Time calculator
end = time.time()
final_time=float(end - start)
print("It took", round((final_time), 2), "seconds to scrape the websites & populate the databases.")



# Class:
class Dog_Info():
    def __init__(self, name):
      self.name=name
      conn=sqlite3.connect(DBNAME)
      cur=conn.cursor()
      statement='''SELECT * FROM Dogs
      WHERE Dogs.Name='''
      statement+="'"  + name + "'"
      # print(statement)
      cur.execute(statement)
      table_format=PrettyTable()
      table_format.field_names=["Id", "Name", "Rank", "Height", "Weight", "Life Expectancy", "Group"]
      for row in cur:
        table_format.add_row(row)
      print(table_format)
      return None

# Writing Queries for Averages:
def weights():
  conn=sqlite3.connect(DBNAME)
  cur=conn.cursor()
  return_list=[]
  for item in group_list:
    statement='''SELECT ROUND(AVG(Weight), 2)
    FROM Dogs
    WHERE Groups= '''
    statement= statement + '"' + item + '"'
    # print(statement)
    cur.execute(statement)
    table_format=PrettyTable()
    table_format.field_names=["Average Weight for " + item + " Dog"]
    for row in cur:
      table_format.add_row(row)
      return_list.append(row[0])
    print(table_format)
  # print(return_list)
  return return_list

def heights():
   conn=sqlite3.connect(DBNAME)
   cur=conn.cursor()
   return_list=[]
   for item in group_list:
     statement='''SELECT ROUND(AVG(Height), 2)
     FROM Dogs
     WHERE Groups= '''
     statement= statement + '"' + item + '"'
     # print(statement)
     cur.execute(statement)
     table_format=PrettyTable()
     table_format.field_names=["Average Height for " + item + " Dog"]
     for row in cur:
       table_format.add_row(row)
       return_list.append(row[0])
     print(table_format)
   # print(return_list)
   return return_list

def life_expectancy():
   conn=sqlite3.connect(DBNAME)
   cur=conn.cursor()
   return_list=[]
   for item in group_list:
     statement='''SELECT ROUND(AVG(LifeExpectancy), 2)
     FROM Dogs
     WHERE Groups= '''
     statement= statement + '"' + item + '"'
     # print(statement)
     cur.execute(statement)
     table_format=PrettyTable()
     table_format.field_names=["Average Life Expectancy for " + item + " Dog"]
     for row in cur:
       table_format.add_row(row)
       return_list.append(row[0])
     print(table_format)
   # print(return_list)
   return return_list


def plot_weights():
  return_weights=weights()
  data = [go.Bar(
              x=group_list,
              y=return_weights,
              marker=dict(color='rgb(158, 202, 225)')
      )]
  layout=go.Layout(
              title="Weight Comparison of AKC Dog Groups",
              xaxis=dict(
                title='Dog Groups',
                titlefont=dict(
                  family="Courier New, monospace",
                  size=18,
                  color='#7f7f7f'
                )
              ),
              yaxis=dict(
              title="Weight in lbs",
              titlefont=dict(
                family="Courier New, monospace",
                size=18,
                color='#7f7f7f'
              )
              )
  )
  fig=go.Figure(data=data, layout=layout)
  py.plot(fig, filename='Weights')

def plot_heights():
  return_heights=heights()
  data = [go.Bar(
              x=group_list,
              y=return_heights,
              marker=dict(color='rgb(158, 202, 225)')
      )]
  layout=go.Layout(
              title="Height Comparison of AKC Dog Groups",
              xaxis=dict(
                title='Dog Groups',
                titlefont=dict(
                  family="Courier New, monospace",
                  size=18,
                  color='#800000'
                )
              ),
              yaxis=dict(
              title="Height in Inches",
              titlefont=dict(
                family="Courier New, monospace",
                size=18,
                color='#800000'
              )
              )
  )
  fig=go.Figure(data=data, layout=layout)
  py.plot(fig, filename='Heights')

def plot_life_expectancy():
  return_life=life_expectancy()
  data = [go.Bar(
              x=group_list,
              y=return_life,
              marker=dict(color='rgb(158, 202, 225)')
      )]
  layout=go.Layout(
              title="Life Expectancy Comparison of AKC Dog Groups",
              xaxis=dict(
                title='Dog Groups',
                titlefont=dict(
                  family="Courier New, monospace",
                  size=18,
                  color='#E633FF'
                )
              ),
              yaxis=dict(
              title="Life Measured In Years",
              titlefont=dict(
                family="Courier New, monospace",
                size=18,
                color='#E633FF'
              )
              )
  )
  fig=go.Figure(data=data, layout=layout)
  py.plot(fig, filename='LifeExpectancy')



# plot_weights()
# plot_heights()
# plot_life_expectancy()

def master_groups_list():
  conn=sqlite3.connect(DBNAME)
  cur=conn.cursor()
  statement='''SELECT Name, Groups
  FROM Dogs
  JOIN Groups ON Groups.GroupName=Dogs.Groups
  ORDER BY Groups.Id'''
  cur.execute(statement)
  table_format=PrettyTable()
  table_format.field_names=["Name", "Group"]
  for row in cur:
    table_format.add_row(row)
  print(table_format)
  return None

def compare_dogs(input_1, input_2):
  conn=sqlite3.connect(DBNAME)
  cur=conn.cursor()
  input_1_list=[]
  input_2_list=[]
  statement1='''SELECT Name, [Rank], Height, Weight, LifeExpectancy
  FROM Dogs
  WHERE Name='''
  statement1= statement1 + '"' + input_1 + '"'
  cur.execute(statement1)
  for row in cur:
    rank1=int(row[1])
    input_1_list.append(rank1)
    height1=int(row[2])
    input_1_list.append(height1)
    weight1=int(row[3])
    input_1_list.append(weight1)
    life_expectancy1=int(row[4])
    input_1_list.append(life_expectancy1)

  statement2='''SELECT Name, [Rank], Height, Weight, LifeExpectancy
  FROM Dogs
  WHERE Name='''
  statement2= statement2 + '"' + input_2 + '"'
  cur.execute(statement2)
  for row in cur:
    rank2=int(row[1])
    input_2_list.append(rank2)
    height2=int(row[2])
    input_2_list.append(height2)
    weight2=int(row[3])
    input_2_list.append(weight2)
    life_expectancy2=int(row[4])
    input_2_list.append(life_expectancy2)
  # print(input_1_list)
  # print(input_2_list)
  trace1 = go.Bar(
    x=['Rank', 'Height', 'Weight', 'Life Expectancy'],
    y=input_1_list,
    name=input_1,
    marker=dict(color='rgb(158, 202, 225)')
    )
  trace2 = go.Bar(
    x=['Rank', 'Height', 'Weight', 'Life Expectancy'],
    y=input_2_list,
    name=input_2)

  data = [trace1, trace2]
  layout = go.Layout(
    barmode='group')

  fig = go.Figure(data=data, layout=layout)
  py.plot(fig, filename='comparison')
  return None


# compare_dogs("Irish Setter", "Ibizan Hound")


# Interactive portion
def interactive():
    prompt = ''' Hello, welcome to our interactive AKC dog information database.
    Menu:
        1. dog breed info -- Returns Information about one of our dogs in table format.
        2. avg height -- Returns a plot of the average heights of dogs based on their group
        3. avg weight -- Returns a plot of the average weights of our dogs based on their group
        3. avg life -- Returns a plot of the average life expectancy of our dogs based on their group
        4. groups -- Returns a table of the dogs in each group & a pie chart showing how many dogs are in each group
        5. compare -- Returns a plot comparing 2 dogs at a time (Rank, Height, Weight, Life Expectancy)
        6. exit -- exit the program'''
    response=""
    while response != "exit":
      print(prompt)
      response=input("Choose a menu option, please...")
      if response=="dog breed info":
        print('''Here are some example breeds, please input a breed for more info:
              Affenpinscher, Xoloitzcuintli, Irish Setter''')
        response=input("Choose a dog breed...")
        try:
          doggo_info=Dog_Info(response)
        except:
          print("Try again with another entry (Tip: Don't put a space after the dogs name)")
          response= input("Choose a dog breed...")
        pass
      elif response=="avg height":
        plot_heights()
        pass
      elif response=="avg weight":
        plot_weights()
        pass
      elif response == "avg life":
        plot_life_expectancy()
        pass
      elif response == "groups":
        master_groups_list()
        pass
      elif response == "compare":
        input_1=input("Enter the name of the first dog (with a capital letter)")
        input_2=input("Enter the name of the second dog (with a capital letter)")
        try:
          compare_dogs(input_1, input_2)
        except:
          print("Invalid response, try again")
        pass
      else:
        pass


if __name__ == "__main__":
    interactive()
