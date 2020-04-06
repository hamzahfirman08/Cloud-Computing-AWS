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

# print("Status: 200 OK")
# print("Content-Type: text/html")
# print()
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

def handle_people_GET(curr_path):
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
    cursor.execute("SELECT * FROM customers")

    # FUNCTION: Getting the results from a SELECT operation above. 
    # RETURN: a list (possibly empty) of tuples. Each tuple is a 
    # record, and each element in the tuple a field
    results = cursor.fetchall()

    # FUNCTION: Close the cursor (deactivated). However, the connection 
    # object - adn the transaction - stay open 

    cursor.close()
    all_people  = []

    for row in results:
      json_data = { 'id': None, 'first_name': None, 'last_name': None, 'address': None }
      count = 0
      for data in json_data:
        json_data[data] = row[count]
        count += 1
      json_data['link'] = 'http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/people/' + str(json_data['id'])
      all_people.append(json_data)
    print(json.dumps(all_people, indent=2))
  else:
    num = curr_path.lstrip('/')
    # Parsing through a table 
    cursor.execute("SELECT * FROM customers WHERE" + " id="+ str(num))

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
    # Dictonary ]

    json_data = { 'id': results[0][0], 'first_name': results[0][2], 'last_name': results[0][3] , 'address':results[0][4]}
    json_data['link'] = 'http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/people/' + str(results[0][0])
    print(json.dumps(person, indent=2))



# # --- POST operation --- 
def handle_people_POST():
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
      if data == "first_name" or data == "address":
        check += "Y"
      elif data == "last_name":
        check += "N"
    if "Y" in check:
      if check == "YY":
        # JSON individual Data
        first_name = pyhton_obj['first_name']
        address = pyhton_obj['address']
        cursor.execute("INSERT INTO customers(first_name, address) VALUES("+'"'+ first_name + '"'+ ", "+'"'+address+'"'+");")
      elif check == "YNY":
        # JSON individual Data
        first_name = pyhton_obj['first_name']
        last_name = pyhton_obj['last_name']
        address = pyhton_obj['address']
        cursor.execute("INSERT INTO customers(first_name, last_name, address) VALUES("+'"'+ first_name + '"'+ ", "+'"'+last_name+'"'+", "+'"'+address+'"'+");")
      else:
        x = 1/0

    count = cursor.rowcount

    cursor.close()
    conn.commit()


    print("Status: 302 Redirect")
    print("Location: http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/vet-clinic/people")
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
def handle_people_DELETE(curr_path):
  try:
    ID = curr_path.lstrip('/')
    # JSON individual Data

    cursor = conn.cursor()


    # FUNCTION: Parses through Pyhton Dict/Obj
    if cursor.execute("DELETE FROM customers WHERE"+ " id=" + ID):

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
if curr_path.startswith('/') or curr_path == "/people/":
    if os.environ["REQUEST_METHOD"] == "GET":
      handle_people_GET(curr_path)
    elif os.environ["REQUEST_METHOD"] == "POST":
      handle_people_POST()
    elif os.environ["REQUEST_METHOD"] == "DELETE":
      handle_people_DELETE(curr_path)
    else:
      not_found_page()

      # Raise helpes to re-raise the caught exception. cgitb will 
      # catc