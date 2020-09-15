#! /usr/bin/python3


# ===== IMPORTS =====
import cgi
import cgitb
# Reads POST data from JSON Files
import sys
# Sends back a JSON objects to the Client
import json
# MySQL DB and passwords
import MySQLdb
import passwords
# Accessing the environment variables
import os 

# Max number of Data in MySQL DB
MAX = 20

cgitb.enable()

# ===== MySQL CONNECTION =====
#Creates Connection to the DB using 'username'
# and 'password' in passwords.py
conn = MySQLdb.connect(host   = passwords.SQL_HOST,
                       user   = passwords.SQL_USER,
                       passwd = passwords.SQL_PASSWD,
                       db     = "csc_346_proj_6")


# ===== APACHE: 'PATH_INFO'=====

# CONDITIONS: Checks if PATH_INFO variable exist
if "PATH_INFO" in os.environ:
  # This is the 'SUBSET' of the path ( anything after the 'root' path)
  curr_path = os.environ["PATH_INFO"]
else:
  # Sets it to a Default slash '/'. Allows it to be used in the script
  curr_path = "/"

# ===== GET Operation =====
# FUNCTION: Calls other functions associated to the functionality of GET operation 
def handle_webhook_GET():
  check_max()
  print_data()

# FUNCTION: If the current number of messages exceeds the defined MAX, it deletes old messages. 
def check_max():
  #===== MySQL DB =====

  cursor = conn.cursor()

  # ===== MySQL: SELECT Operation =====
  # Parses through a table 
  cursor.execute("SELECT id FROM webhook ORDER BY time")

  # FUNCTION: Getting the results from a SELECT operation above. 
  # RETURN: a list (possibly empty) of tuples. Each tuple is a 
  # record, and each element in the tuple a field
  results = cursor.fetchall()

  # FUNCTION: Close the cursor (deactivated). However, the connection 
  # object - adn the transaction - stay open
   
  # Parses through the 'result' (list of data)
  cursor.close()
  msg_id = 0
  count = 0 
  for data in results:
    msg_id = data[0]
    if msg_id > MAX:
      count += 1

      #===== MySQL: DELETE Operation =====
      cursor = conn.cursor()
      
      # Parsing through a table 
      cursor.execute("DELETE FROM webhook WHERE id=" + str(count)+";")

      # FUNCTION: Close the cursor (deactivated). However, the connection 
      # object - adn the transaction - stay open
      
      # Parses through the 'result' (list of data)
      cursor.close()
           
# FUNCTION: Prints MySQL data to a static HTML on a web-browser 
def print_data():
  # GET Logic goes here
  # Commits all changes to the DB
  #conn.commit() 

  #===== HTTP Header: 200 OK =====
  print("Status: 200 OK")
  print("Content-Type: text/html")
  print()

  #===== MySQL DB =====

  cursor = conn.cursor()


  # Parsing through a table 
  cursor.execute("SELECT * FROM webhook")

  # FUNCTION: Getting the results from a SELECT operation above. 
  # RETURN: a list (possibly empty) of tuples. Each tuple is a 
  # record, and each element in the tuple a field
  results = cursor.fetchall()

  # FUNCTION: Close the cursor (deactivated). However, the connection 
  # object - adn the transaction - stay open 

  cursor.close()

  print("""<html> 
              <body>
              <table border=1>
              <tr><td><b>Time</b></td> <td><b>Payload</b></td> </tr>""")
  for data in results:
    time = str(data[1])
    message = str(data [2])
    print("""   <tr>
                    <td>""" + time + """</td>
                    <td><div><pre>""" + message + """</pre></div></td>
                </tr>""")
  print("""</table></body></html>""")

# ===== POST operation =====
# FUNCTION: Performs a POST operation by inserting user input into the MySQL DB 
def handle_webhook_POST():
    try:
      # 'input_data': Reads the text on which been sent on the terminal
      input_data = sys.stdin.read()
      if len(input_data) == 0:
        x = 1/0
      try:
        # If input is a JSON Formatted 
        #
        if json.loads(input_data):
          # ==== MySQL ====
          # MySQL cursor
          cursor = conn.cursor()
          pyhton_obj = json.loads(input_data)
          list_obj = []
          list_obj.append(pyhton_obj)
          
          # MySQL Operation: INSERT 
          # 'cursor.execute': Adds a new record to the 'csc_346_proj_6' database
          cursor.execute("INSERT INTO webhook(time, message) VALUES(NOW(), " + '"' + str(list_obj) + '"'+");")
          count = cursor.rowcount

          # Close the cursor 
          cursor.close()
          # Commit the transaction
          conn.commit()
          
          #===== HTTP Header: 302 REDIRECT =====
          print("Status: 302 Redirect")
          print("Location: http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/project6/webhook")
          print()

      except:
        # If the input is a String type 
        #
        # #===== MySQl DB =====
        # MySQL cursor
        cursor = conn.cursor()

        # MySQL Operation: INSERT 
        # FUNCTION: Adds a new record to the 'csc_346_proj_6' database
        cursor.execute("INSERT INTO webhook(time, message) VALUES(NOW(), " + '"' + input_data + '"'+");")
        count = cursor.rowcount

        # Close the cursor 
        cursor.close()
        # Commit the transaction
        conn.commit()
        
        #===== HTTP Header: 302 REDIRECT =====
        print("Status: 302 Redirect")
        print("Location: http://ec2-54-237-92-183.compute-1.amazonaws.com/cgi-bin/project6/webhook")
        print()
     
    except ZeroDivisionError:

    #===== HTTP Header: 200 OK =====
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

#  ===== NOT FOUND 404 page =====
def not_found_page():
    #===== HTTP Header: 404 NOT FOUND =====
    print("Status: 404 Not Found")
    print("Content-Type: text/html")
    print()

# ===== APACHE: 'REQUEST_METHOD' =====
# CONDITIONS: Checks if 'curr_path' matches with existed URLS
if curr_path.startswith('/') or curr_path == "/webhook/":
    if os.environ["REQUEST_METHOD"] == "POST":
      handle_webhook_POST()
    elif os.environ["REQUEST_METHOD"] == "GET":
      handle_webhook_GET()
    else:
      not_found_page()
