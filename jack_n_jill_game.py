   #! /usr/bin/python3

import cgi
import cgitb
import random
cgitb.enable()

#BEFORE THE 'PLAY' BUTTON IS PRESS
# Starting scores for Jack and Jill
starting_scores_jack = 100
starting_scores_jill = 100
# Impact after hits and healed 
hp_jack = 0
hp_jill = 0
heal_jill = 0
# Gone up and down 
gone_up = 0
gone_down = 0

print("Status: 200 OK")
print("Content-Type: text/html")
print()

print("""<html>
  
        <head>
                <title>Jack and Jill Game</title>
        </head>
        <body> """)

storage = cgi.FieldStorage()
# Play a brand new game (Not a 'Replay')
# Values are randomized 
if "gone_up" not in storage:
      print("""<center>
          <h1><b>Welcome to The<font color='blue'>Jack</font> and <font color='pink'>Jill</font> Game</b></h1>""")
                      # 'Play' - Reloads the page and passes all the hidden variables
                      # The hidden varibles are:
                      #   1.) Hit Points 
                      #   2.) Healing Points 
                      #   3.) # of gone up 
                      #   4.) # of gone down 
      print(f"""<p><form action="jj_game" method=get>
                  <input type=hidden name=starting_scores_jack value={starting_scores_jack}>
                  <input type=hidden name=starting_scores_jill value={starting_scores_jill}>
                  <input type=hidden name=gone_up value={gone_up +1}>
                  <input type=hidden name=gone_down value={gone_down +1}>
                  <input type=submit value="Play">
              </form></p>
           </center>""")

# AFTER THE 'PLAY' BUTTON IS PRESSED
# Once all varibales passed in then this condition will be executed.
else:
  print("""<center>
          <h1><b>We shall see how long they can survive</b></h1>
          </center>""")
  starting_scores_jack = storage["starting_scores_jack"].value
  starting_scores_jill = storage["starting_scores_jill"].value
  # Random numbers
  hp_rando_jack = random.randint(10,50)
  hp_rando_jill = random.randint(10,50)
  heal_rando_jill = random.randint(1,10)
  # Numbers of when they gone up and down
  gone_up = int(storage["gone_up"].value)
  gone_down = int(storage["gone_down"].value)
  # Impact after hits and healed 
  hp_jack = int(storage["starting_scores_jack"].value) - hp_rando_jack
  hp_jill = int(storage["starting_scores_jill"].value) - hp_rando_jill
  heal_jill = hp_jill + heal_rando_jill

# Let the game begin! 
#
# Jack and Jill have gone to the top of the hill
# Current scores: 100 for both
print("""<h3><i>"Once upon a time . . ."</i><h3>""")
print("""<h3><i> "Jack and Jill are up on the hill to fetch a pail of water</i><b><font color='green'> [""",
  str(gone_up),"""times]</font></b></h3>""")
print("<h2> Scores: </h2>")
print("""<p><table border=3>
                <tr>
                <th><font color='blue'>Jack's Score:""",str(starting_scores_jack),"""</font></th>
                <th><font color='pink'>Jill's Score:""",str(starting_scores_jill), """</font></th>
                </tr>""")
# Jack and Jill tumbles down the hill
# Damages are being applied 
# Current Scores: 100 - (Random numbers between 1 and 10)
print("""</table></p>
                <h3><i>"Oh no . . . "</i></h3>
                <h3><i>"They have tumbled down the hill</i><b><font color='green'> [""", str(gone_down),"""times]</font></b></h3>""")
print("""<h3><font color='red'>CRASH!</font></h3>
                <h2> Scores: </h2>
                <p><table border=3>
                        <tr>""")
# Hit points  

print("<th><font color='blue'> Jack's Score:",str(hp_jack),
  "</font></th>")
print("<th><font color='pink'> Jill's Score:",str(hp_jill),
  "</font></th>")
print("""<tr>
                </table></p>
                <p><table> """)
# Jill is healing up from the fall
# Check the following: If Jack's and Jill'sscore is 0, then game is over, otherwise
# starts from 100 again (Reload the page)
print("""<h3><i>"Meanwhile, Jill is healing herself"</i></h3>""")
print("""<h2> Scores: </h2>
                <p><table border=3>
                        <tr>""")
# Jill is healed
print("<th><font color='blue'> Jack's Score:",str(hp_jack),"</font></th>")
print("<th><font color='pink'> Jill's Score:",str(heal_jill),"</font></th>")
print("""<tr>
                </table></p>""")

if hp_jack and heal_jill <= 0:
  print("<h1><b>REST IN PEACE <font color='blue'>JACK</font> AND <font color='pink'>JILL</font></b></h1>")
  print("""<p><form action="jj_game" method=get>
    <input type=submit value="Play Again">
  </form></p>""")
# They are alive and their current scores get passed on to the next game as their
# starting scores.
else:
    print(f"""<p><form action="jj_game" method=get>
    <input type=hidden name=starting_scores_jack value={hp_jack}>
    <input type=hidden name=starting_scores_jill value={heal_jill}>
    <input type=hidden name=gone_up value={gone_up + 1}>
    <input type=hidden name=gone_down value={gone_down + 1}>
    <input type=submit value="Continue">
        </form></p>""")

