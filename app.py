"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions


import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############

@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  app.logger.debug("Got a JSON request");
  #gathering info for calculation
  control= request.args.get('control', 0, type=int)
  brevdist=request.args.get('brevdist',type=int)
  units = request.args.get('units',type = str)
  start_time=request.args.get('starttime',type=str)
  start_date=request.args.get('startdate',type=str)
  
  bigstring = start_date + ' ' + start_time
  arrow_time_open = arrow.get(bigstring, 'YYYY/MM/DD HH:mm')
  arrow_time_close= arrow.get(bigstring, 'YYYY/MM/DD HH:mm')
  
  brev_list=[(200,15,34),(200,15,32),(200,15,30),(400,11.428,28),(300,13.333,26)]
  
  finished_close={200:13.5,300:20,400:27,600:40,1000:75}
  finished_open={200:5.8833333,300:9,400:12.1333333,600:18.8,1000:21.0833333}
  
  intopen = 0
  intclose = 0
  finished = "Race not yet finished"
  
  if (control < 0):
  	finished = "Not a valid control distance."
  	intopen = 0
  	intclose = 0
  if (units=='miles'):
  	control = control * 1.60934
  #race is finished 
  if (control == 0):
  	intclose += 1
  if (0 < control >= brevdist):
  	intopen  =finished_open[brevdist]
  	intclose =finished_close[brevdist]
  	finished = "Race is Finished!" 
  #control < brevdist
  elif 0 < control < brev_list[0][0]:
  	intopen += control/(brev_list[0][2])
  	intclose += control/(brev_list[0][1])
  else:
  	km_counter = control
  	for i in range(len(brev_list)): 
  		if (km_counter >= brev_list[i][0]):
  			km_counter = km_counter - brev_list[i][0]
  			intopen += (brev_list[i][0])/(brev_list[i][2])
  			intclose+= (brev_list[i][0])/(brev_list[i][1])
  			
  		elif(0 < km_counter <brev_list[i][0]):  
  			intopen += (km_counter)/(brev_list[i][2])
  			intclose += (km_counter)/(brev_list[i][1])
  			break
  	
  open_time = arrow_time_open.replace(hours =+ intopen)
  close_time = arrow_time_close.replace(hours =+ intclose)
  	
  returnstring = ("open: " + open_time.format("MM/DD HH:mm") + " close: "
  + close_time.format("MM/DD HH:mm"))
  
  rslt = {"times":returnstring, "finished": finished,} 
  return jsonify(result=rslt)


#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
