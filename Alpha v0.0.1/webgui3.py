#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb


# global variables
speriod=(15*60)-1
dbname='/home/pi/windlog.db'



# print the HTTP header
def printHTTPheader():
    print "Content-type: text/html\n\n"



# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    
    

    print "</head>"


# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(interval):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM windlog")
    else:
        curs.execute("SELECT * FROM windlog WHERE date>datetime('now','-%s hours')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows


# convert rows from database into a javascript table

# print the javascript to generate the chart
# pass the table generated from the database info




# print the div that contains the graph


# connect to the db and show some stats
# argument option is the number of hours
def show_stats(option):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if option is None:
        option = str(6)

    curs.execute("SELECT date,max(mph) FROM windlog WHERE date>datetime('now','-%s day') AND date<=datetime('now')" % option)
    rowmax=curs.fetchone()
    rowstrmax="{0}&nbsp&nbsp&nbsp{1} MPH".format(str(rowmax[0]),str(rowmax[1]))

#    curs.execute("SELECT date,min(mph) FROM windlog WHERE date>datetime('now','-%s day') AND date<=datetime('now')" % option)
#    rowmin=curs.fetchone()
#    rowstrmin="{0}&nbsp&nbsp&nbsp{1}MPH".format(str(rowmin[0]),str(rowmin[1]))

    curs.execute("SELECT avg(mph) FROM windlog WHERE date>datetime('now','-%s day') AND date<=datetime('now')" % option)
    rowavg=curs.fetchone()


    print "<hr>"


#    print "<h2>Minumum Wind-Speed&nbsp</h2>"
#    print rowstrmin
    print "<h2>Maximum Wind-Speed</h2>"
    print rowstrmax
    print "<h2>Average Wind-Speed</h2>"
    print "%.3f" % rowavg+" MPH"

    print "<hr>"

    print "<h2>In the last 20 seconds:</h2>"
    print "<table>"
    print "<tr><td><strong>Date/Time</strong></td><td><strong>Wind-Speed</strong></td></tr>"

    rows=curs.execute("SELECT * FROM windlog WHERE date>datetime('now','-20 second') AND date<=datetime('now')")
    for row in rows:
        rowstr="<tr><td>{0}&emsp;&emsp;</td><td>{1}"" MPH""</td></tr>".format(str(row[0]),str(row[1]))
        print rowstr
    print "</table>"

    print "<hr>"

    conn.close()




def print_time_selector(option):

    print """<form action="/cgi-bin/webgui3.py" method="POST">
        Show the Wind-Speed logs for  
        <select name="timeinterval">"""


    if option is not None:

        
	if option == "6":
            print "<option value=\"1\" selected=\"selected\">the last 1 hours</option>"
        else:
            print "<option value=\"1\">the last 1 hours</option>"

        if option == "12":
            print "<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
        else:
            print "<option value=\"6\">the last 6 hours</option>"

        if option == "365":
            print "<option value=\"365\" selected=\"selected\">the last 8760 hours</option>"
        else:
            print "<option value=\"365\">the last 365 hours</option>"

	
    else:
        print """<option value="1">the last 1 hours</option>
            <option value="365">the last 365 hours</option>
		<option value="365" selected="selected">the last 365 hours</option>"""

    print """        </select>
        <input type="submit" value="Display">
    </form>"""


# check that the option is valid
# and not an SQL injection
def validate_input(option_str):
    # check that the option string represents a number
    if option_str.isalnum():
        # check that the option is within a specific range
        if int(option_str) > 0 and int(option_str) <= 6:
            return option_str
        else:
            return None
    else: 
        return None


#return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return validate_input (option)
    else:
        return None




# main function
# This is where the program starts 
def main():

    cgitb.enable()

    # get options that may have been passed to this script
    option=get_option()

    if option is None:
        option = str(6)

    # get data from the database
    records=get_data(option)

    # print the HTTP header
    printHTTPheader()

    

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
   

    # print the page body
    print "<body>"
    print "<h1>Raspberry Pi Wind-Speed Logger</h1>"
    print "<hr>"
    print_time_selector(option)
    
    show_stats(option)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()