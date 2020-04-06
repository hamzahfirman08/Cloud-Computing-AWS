#! /usr/bin/python3

# Author: Hamzah Firman
# Assignment: Project 5
# Class: CSC 346 / Dr.Lewis
# Date: 03/05/2020
import cgi
import cgitb
# Reads POST / PUT data from JSON Files
import sys
# Sends back a JSON objects to the Client
import json
# MySQL DB and passwords
import MySQLdb
import passwords
# Accessing the environment variables
import os 


cgitb.enable()

print("Status: 200 OK")
print("Content-Type: text/html")
print()
# Creates Connection to the DB using 'username'
# and 'password' in passwords.py

conn = MySQLdb.connect(host   = passwords.SQL_HOST,
                       user   = passwords.SQL_USER,
                       passwd = passwords.SQL_PASSWD,
                       db     = "csc_346_proj_5")


## ------ TERMINAL RUNS ------ 

# FIRST: Checks if PATH_INFO variable exist
if "PATH_INFO" in os.environ:
  # This is the 'SUBSET' of the path ( anything after the 'root' path)
  curr_path = os.environ["PATH_INFO"]
else:
  # Sets it to a Default slash '/'. Allows it to be used in the script
  curr_path = "/"

def handle_pets_GET(curr_path):
  # --- GET operation
  # GET Logic goes here
  # Commits all changes to the DB
  #conn.commit() 

  print("Status: 200 OK")
  print("Content-Type: application/json")
  print()

  cursor = conn.cursor()

  if curr_path == "/":
    # Parsing through a table 
    cursor.execute("SELECT * FROM pets")

    # FUNCTION: Getting the results from a SELECT operation above. 
    # RETURN: a list (possibly empty) of tuples. Each tuple is a 
    # record, and each element in the tuple a field
    results = cursor.fetchall()

    # FUNCTION: Close the cursor (deactivated). However, the connection 
    # object - adn the transaction - stay open 

    cursor.close()
    all_people  = []

    for row in results:
      json_data = { 'id': None, 'name': None, 'breed': None, 'favorite_food': None}
      count = 0
      for data in json_data:
        json_data[data] = row[count]
        count += 1
      json_data['link'] = 'http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/pets/' + str(json_data['id'])

      json_data['owner_link'] = 'http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/pets/' + str(row[4])
      all_people.append(json_data)
    print(json.dumps(all_people, indent=2))

  else:
    ID = curr_path.lstrip('/')
    # Parsing through a table 
    cursor.execute("SELECT * FROM pets WHERE" + " id="+ ID)

    # FUNCTION: Getting the results from a SELECT operation above. 
    # RETURN: a list (possibly empty) of tuples. Each tuple is a 
    # record, and each element in the tuple a field
    results = cursor.fetchall()

    # FUNCTION: Close the cursor (deactivated). However, the connection 
    # object - adn the transaction - stay open 

    cursor.close()

     # FUNCTION: Converting Pyhton Object to JSON using JSON library
    # First
    # Parses thtough the list of tuples which generated from DB
    # Then, append each record to their associated fields using 
    # Dictonary 
    person  = []


    json_data = { 'id': results[0][0], 'name': results[0][1], 'breed': results[0][2], 'favorite_food': results[0][3]}
    json_data['link'] = 'http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/pets/' + str(json_data['id'])
    json_data['owner_link'] = 'http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/pets/' + str(results[0][4])
    person.append(json_data)
    print(json.dumps(person, indent=2))


  # FUNCTION: Converting Pyhton Object to JSON using JSON library
  # First
  # Parses thtough the list of tuples which generated from DB
  # Then, append each record to their associated fields using 
  # Dictonary 



# # --- POST operation --- 
def handle_pets_POST():
  try:
    # FUNCTION: Read the text on which been sent on the terminal
    input_data = sys.stdin.read()
    # Returns a Pyhton object
    pyhton_obj = json.loads(input_data)

    # MySQL DB: INSERT operation
    # MySQL cursor
    cursor = conn.cursor()

    check = ""

    for data in pyhton_obj.keys():
      if data == "name" or data == "customerID":
        check += "D"
      elif data == "breed":
        check += "B"
      elif data == "favorite_food":
        check += "F"

    if "D" in check:
      if check == "DD":
        # JSON individual Data
        dog_name = pyhton_obj['name']
        cus_id = pyhton_obj['customerID']
        cursor.execute("INSERT INTO pets(name, customerID) VALUES("+'"'+ dog_name + '"'+ ", "+'"'+str(cus_id)+'"'+");")

      elif len(check) >= 3:
        if check == "DBD":
          # JSON individual Data
          dog_name = pyhton_obj['name']
          a_breed = pyhton_obj['breed']
          cus_id = pyhton_obj['customerID']

          cursor.execute("INSERT INTO pets(name, breed, customerID) VALUES("+'"'+ dog_name + '"'+ ", "+'"'+a_breed+'"'+", "+'"'+ str(cus_id)+'"'+");")

        elif check == "DFD":
          # JSON individual Data
          dog_name = pyhton_obj['name']
          favorite_food = pyhton_obj['favorite_food']
          cus_id = pyhton_obj['customerID']

          cursor.execute("INSERT INTO pets(name, favorite_food, customerID) VALUES("+'"'+ dog_name + '"'+ ", "+'"'+favorite_food+'"'+", "+'"'+ str(cus_id)+'"'+");")

        else:
          # JSON individual Data
          dog_name = pyhton_obj['name']
          a_breed = pyhton_obj['breed']
          favorite_food = pyhton_obj['favorite_food']
          cus_id = pyhton_obj['customerID']

          cursor.execute("INSERT INTO pets(name, breed, favorite_food, customerID) VALUES("+'"'+ dog_name + '"'+ ", "+'"'+a_breed+'"'+", "+'"'+ favorite_food+'"'+", "+'"'+ str(cus_id)+'"'+");")

      else:
        x = 1/0

    count = cursor.rowcount
    cursor.close()
    conn.commit()

    print("Status: 302 Redirect")
    print("Location: http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/pets")
    print()
     
  except ZeroDivisionError:
    # Prints any exception errors to the browser as an HTML page
    # which caused by cgitb 
    print("Status: 200 OK")
    print("Content-Type: text/html")
    print()

    print("""<html>

        <body> <h1> YOU NEED MORE INFORMATION! </h1>
        </body>
        </html>""")

    # Raise helpes to re-raise the caught exception. cgitb will 
    # catch it next
    raise 


#  --- DELETE operation ---
def handle_pets_PUT(curr_path):
  try:
    splitted = curr_path.split('/')
    cus_id = splitted[0]
    pet_id = splitted[1]
    name   = splitted[2]
    # JSON individual Data

    cursor = conn.cursor()

    # FUNCTION: Parses through Pyhton Dict/Obj
    if cursor.execute("UPDATE pets SET" + "name="+ name +"WHERE id="+ str(ID) + ", "+"customerID="+str(cus_id)+");"):

        # FUNCTION: Return the number of rows were effected 
      count = cursor.rowcount

      cursor.close()
      conn.commit()
    else:
      not_found_page()
      # POST Logic goes here

      # Commits all changes to the DB
      #conn.commit() 

    print("Status: 302 Redirect")
    print("Location: http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/people")
    print()

     
  except:
      # Prints any exception errors to the browser as an HTML page
      # which caused by cgitb 
      print("Status: 200 OK")
      print("Content-Type: text/html")
      print()

      # Raise helpes to re-raise the caught exception. cgitb will 
#       # catc
#  --- NOT FOUND 404 page --- 
def not_found_page():
    print("Status: 404 Not Found")
    print("Content-Type: text/html")
    print()


# SECOND: Checks if 'curr_path' matches with existed URLS
if curr_path.startswith('/') or curr_path == "/pets/":
    if os.environ["REQUEST_METHOD"] == "GET":
      handle_pets_GET(curr_path)
    elif os.environ["REQUEST_METHOD"] == "POST":
      handle_pets_POST()
    elif os.environ["REQUEST_METHOD"] == "PUT":
      handle_pets_PUT(curr_path)
    else:
      not_found_page()

      # Raise helpes to re-raise the caught exception. cgitb will 
      # catc