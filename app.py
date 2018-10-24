from flask import Flask, render_template, request, \
    jsonify, make_response, Response
from flask_httpauth import HTTPBasicAuth
import md5
from functools import wraps
from nameko.standalone.rpc import ServiceRpcProxy
import psycopg2.extras
import os
import json
import psycopg2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests
from fieldsLocal import *
import sys, pprint
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

pOrt = int(os.getenv("PORT", 3000))
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

auth = HTTPBasicAuth()

APPLICATION_NAME = "Farnborough Back End Application"

#Connect to Database and create database session
app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route("/")   
@app.route("/status")
def get_status():
    conn = Connect()
    if(conn.closed==0):
        stronga = "Connection is up and running"
    else:
        stronga = "Connection did not succeed"
    return stronga

@app.route("/vcap")
def get_vcap():
    message = os.environ["VCAP_SERVICES"]
    return message

    
@app.route("/MB")
@crossdomain(origin='*')
def get_con():
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab = "\"MB51\""
    sql0="SELECT * FROM %s.%s LIMIT 10" % (schem,tab)
    sql0=sql0 % globals()
    message = fetchAsJSON(sql0)
    return message
#return render_template("postgres.html", postgres_data=postgres_info)

@app.route("/MBAlt")
@crossdomain(origin='*')
def get_conA():
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab = "\"MB51\""

    
    sql0="SELECT * FROM %s.%s LIMIT 10" % (schem,tab)
    sql0=sql0 % globals()
    message = fetchAsJSON(sql0)
    return message

    
@app.route("/VTStock/<int:FW>")
@app.route("/VTStock/<int:FW>/")
@crossdomain(origin='*')
def get_VTS(FW):
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab2 = "\"MB51\""
    tab1 = "\"Variance\""
    d = dict(globals())
    d.update(locals())
    sql0="""WITH 
PVar as (SELECT * 
FROM %(schem)s.%(tab1)s
WHERE %(field100)s < 59999999 
AND TRIM(%(field102)s) IN ('Labor','Machine','Setup','Rework','Direct Material - OFT Hardware - 537', 'Other Purchase Mat & Svc HW/SW') 
AND %(field101)s > 0 
AND %(field105)s > 0),    
MB AS (    SELECT * 
FROM %(schem)s.%(tab2)s 
WHERE EXTRACT(YEAR FROM %(field12)s) = EXTRACT(YEAR FROM current_date) 
AND EXTRACT(WEEK FROM %(field12)s) = %(FW)f 
AND %(field8)s= '101' 
AND %(field17)s IS NOT NULL    
AND %(field6)s = '6400' )    
SELECT SUM( g.%(field105)s) as "To_Stock" 
FROM Pvar g 
INNER JOIN MB h ON h.%(field17)s = g.%(field100)s;""" % d
    colla = []
    colla.append("To_Stock")
    #print sql0
    sql0=sql0 % globals()
    message = fetchViewAsJSON(sql0,colla)
    return message
    
@app.route('/MB/<int:FW>')
@app.route('/MB/<int:FW>/')
@crossdomain(origin='*')
def get_MB_weekly(FW):

    schem = "\"public\""
    tab = "\"MB51\""
    d = dict(globals())
    d.update(locals())
    sql0="SELECT * FROM %(schem)s.%(tab)s WHERE %(field12)s > current_date-2 LIMIT 10 " % d
    sql0=sql0 % globals()
    message = fetchAsJSON(sql0)
    return message

def Connect():
    if os.getenv("VCAP_SERVICES") is None:
        conn_string = "host='localhost' dbname='postgres' user='postgres' password='postgres'"
        connection = psycopg2.connect(conn_string)
    else:
        print "------------------------------------------------"
        print os.environ["VCAP_SERVICES"]
        print "------------------------------------------------"
        j = json.loads(os.environ["VCAP_SERVICES"])
        kl = j["postgres-2.0"][0]
        connection = psycopg2.connect(
                database=kl["credentials"]["database"],
                user=kl["credentials"]["username"],
                password=kl["credentials"]["password"],
                host=kl["credentials"]["hostname"],
            )
    return connection
    
def fetchViewAsJSON(stringSQL, columnList):
    print "Starting fetch"
    conn = Connect()   
    cursor = conn.cursor()
    cursor.execute(stringSQL)
    postgres_data = cursor.fetchall()
#    col_names = [desc[0] for desc in cursor.description]
#    print "----------------------------------"
#    print col_names
#    print "----------------------------------"
    returnString = ""
    for rows in postgres_data:
        k = {}
        cnt = 0
        if not (len(rows) < len(columnList)):
  #          print "-----------------------------------"
  #          print "Row was long enough"
  #          print "-----------------------------------"
            for l in columnList:
 #               print "Current Column Name: " + str(l)
 #               print "Current Value: " + str(rows[cnt]).replace(",","")
 #               print "Current Counter: " + str(cnt)
                k[l] = str(rows[cnt]).decode('utf-8','ignore').encode("utf-8").replace(",","").replace("'","")
                cnt += 1
        
        
        data = json.dumps(k, separators=(',', ':')) 
 #       print "-----------------------------------"
 #       print data
        returnString += "," + data
    returnString = "[" + returnString[1:len(returnString)] + "]"
    return returnString 
 
def fetchAsJSON(stringSQL):
    print "Starting fetch"
    conn = Connect()   
    cursor = conn.cursor()
    cursor.execute(stringSQL)
    postgres_data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
#    print "----------------------------------"
#    print col_names
#    print "----------------------------------"
    returnString = ""
    for rows in postgres_data:
        k = {}
        cnt = 0
        if not (len(rows) < len(col_names)):
#            print "-----------------------------------"
#            print "Row was long enough"
#            print "-----------------------------------"
            for l in col_names:
 #               print "Current Column Name: " + str(l)
 #               print "Current Value: " + str(rows[cnt]).replace(",","")
  #              print "Current Counter: " + str(cnt)
                k[l] = str(rows[cnt]).decode('utf-8','ignore').encode("utf-8").replace(",","").replace("'","")
                cnt += 1
        data = json.dumps(k, separators=(',', ':')) 
        returnString += "," + data
    returnString = "[" + returnString[1:len(returnString)] + "]"
    return returnString

        
    
    

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  #app.context = ('server.crt', 'server.key')
  app.run(host = '0.0.0.0', port = pOrt, threaded=True)
