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


@app.route("/Ops/<int:Or>")
@app.route("/Ops/<int:Or>/")
@crossdomain(origin='*')
def get_Ops(Or):
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab = "\"MB51\""
    d = dict(globals())
    d.update(locals())
    sql0="""WITH 
Ops as (SELECT *
FROM public."Coois_Ops_Archived")
,Cnt as (SELECT "Order","Oper./Act.",
Count("Entered by") as c
FROM public."AFRU" 
GROUP BY "Order", "Oper./Act.")
SELECT Ops."Oper./Act." as "Op",
Ops."Work cntr." as "WC",
Ops."Operation short text" as "Operation",
Ops."Op. Qty" as "Qty",
Ops."Act/Op.UoM" as "UoM",
Ops."System Status" as "Status",
Ops."Processing" as "Std_Hrs",
Ops."Conf. act. 3" as "Cnf_Hrs",
Cnt.c as cnt,
CASE WHEN (Cnt.c > 1) THEN 'inline-flex' ELSE 'none' END as c,
CASE WHEN (Cnt.c < 2) THEN 'inline-flex' ELSE 'none' END as cneg
FROM Ops INNER JOIN Cnt ON Ops."Order" = Cnt."Order" 
and Ops."Oper./Act." = Cnt."Oper./Act."
WHERE Ops."Op. Qty" > 1
AND Ops."Order" = %(Or)s
ORDER BY "Op";""" % d
    colla = []
    colla.append("Op")
    colla.append("WC")
    colla.append("Operation")
    colla.append("Qty")
    colla.append("UoM")
    colla.append("Status")
    colla.append("Std_Hrs")
    colla.append("Conf_Hrs")
    colla.append("cnt")
    colla.append("c")
    colla.append("cneg")
    #print sql0
    sql0=sql0 % globals()
    message = fetchViewAsJSON(sql0,colla)
    return message
#return render_template("postgres.html", postgres_data=postgres_info)    


@app.route("/Confs/<int:Or>")
@app.route("/Confs/<int:Or>/")
@crossdomain(origin='*')
def get_Confs(Or):
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab = "\"MB51\""
    d = dict(globals())
    d.update(locals())
    sql0="""SELECT "Order", "Oper./Act." as op, "Counter" as cnter, "Entered" as dat, "Entered by" as sso, "Plnt", "Confirmation text" as ctext, 
       "Activity to Conf. 2" as sp, "Activity to Conf. 3" as lb, "Activity to Conf. 4" as rw, 
       "Yield", "Scrap",  "Routing", "Type"
  FROM public."AFRU"
  WHERE "Order" = %(Or)s
ORDER BY op;""" % d
    colla = []
    colla.append("Order")
    colla.append("op")
    colla.append("cnter")
    colla.append("dat")
    colla.append("sso")
    colla.append("Plnt")
    colla.append("ctext")
    colla.append("sp")
    colla.append("lb")
    colla.append("rw")
    colla.append("Yield")
    colla.append("Scrap")
    colla.append("Routing")
    colla.append("Type")
    #print sql0
    sql0=sql0 % globals()
    message = fetchViewAsJSON(sql0,colla)
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


@app.route("/VarStats/<int:FW>")
@app.route("/VarStats/<int:FW>/")
@crossdomain(origin='*')
def get_VTP(FW):
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab2 = "\"MB51\""
    tab1 = "\"Variance\""
    d = dict(globals())
    d.update(locals())
    sql0="""WITH 
PVar as (SELECT *, ABS("Target/actual var#") as "Absolute" 
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
SELECT 
SUM( g.%(field106)s) as "netVar", 
SUM( g.%(field106)s)/ SUM( g.%(field104)s) as "varPercent", 
SUM( g.%(field105)s) as "ATo_Stock", 
SUM( g.%(field104)s) as "PTo_Stock",
SUM( g."Absolute") as "absVar"
FROM PVar g 
INNER JOIN MB h 
ON h.%(field17)s = g.%(field100)s;""" % d
    #print sql0
    colla = []
    colla.append("netVar")
    colla.append("varPercent")
    colla.append("ATo_Stock")
    colla.append("PTo_Stock")
    colla.append("absVar")
    
    #print sql0
    sql0=sql0 % globals()
    message = fetchViewAsJSON(sql0,colla)
    return message


@app.route("/StockStats")
@app.route("/StockStats/")
@crossdomain(origin='*')
def get_VTStockStat():
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab2 = "\"MB51\""
    tab1 = "\"Variance\""
    d = dict(globals())
    d.update(locals())
    sql0="""WITH
MaxPst AS ( SELECT max("Pstng Date")::date as P
    FROM "public"."MB51"
),
PVar as (SELECT *
FROM "public"."Variance"
WHERE "WO" < 59999999
AND TRIM("Cost Element (Text)") IN ('Labor','Machine','Setup','Rework','Direct Material - OFT Hardware - 537', 'Other Purchase Mat & Svc HW/SW')
AND "Cost Elem#" > 0
AND "Total act#costs" > 0),
MB AS ( SELECT "Order", EXTRACT(WEEK FROM "Pstng Date") as "FW"
FROM "public"."MB51"
WHERE "Pstng Date" > ((SELECT P FROM MaxPst) - 56 - EXTRACT(DOW FROM (SELECT P FROM MaxPst))::integer )
AND "MvT"= '101'
AND "Order" IS NOT NULL
AND "Order" < 59999999
AND "Plnt" = '6400' ),
sec as (SELECT
prim."FW", 
SUM(prim."Stock") as "Stock"
FROM (SELECT h."Order", h."FW",
SUM( g."Total target costs") as "Stock"
FROM PVar g
INNER JOIN MB h
ON h."Order" = g."WO"
GROUP BY "Order","FW"
ORDER BY  "FW") prim
GROUP BY prim."FW"),
Smax as (SELECT MAX(sec."Stock") as F FROM sec )

SELECT sec."FW",
sec."Stock",
sec."Stock"/(SELECT F FROM Smax) as "Mpercent"
FROM sec;"""
    #print sql0
    colla = []
    colla.append("FW")
    colla.append("Stock")
    colla.append("Mpercent")
    #print sql0
    sql0=sql0 % globals()
    message = fetchViewAsJSON(sql0,colla)
    return message


@app.route("/Orders")
@app.route("/Orders/")
@crossdomain(origin='*')
def get_Order():
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    schem = "\"public\""
    tab2 = "\"MB51\""
    tab1 = "\"Variance\""
    d = dict(globals())
    d.update(locals())
    sql0="""WITH
MaxPst AS ( SELECT max("Pstng Date")::date as P
    FROM "public"."MB51"
),
PArch as (SELECT "Order"::numeric
FROM "public"."Coois_Ops_Archived"),
MB AS ( SELECT "Order", EXTRACT(WEEK FROM "Pstng Date") as "FW"
FROM "public"."MB51"
WHERE "Pstng Date" > ((SELECT P FROM MaxPst) - 56 - EXTRACT(DOW FROM (SELECT P FROM MaxPst))::integer )
AND "MvT"= '101'
AND "Order" IS NOT NULL
AND "Order" < 59999999
AND "Plnt" = '6400' )
SELECT
"Order"
FROM MB
WHERE "Order" NOT IN (SELECT "Order" FROM PArch)
GROUP BY "Order"
"""
    #print sql0
    colla = []
    colla.append("Order")
    #print sql0
    sql0=sql0 % globals()
    message = fetchViewAsJSON(sql0,colla)
    return message
    
    
@app.route("/VarChart")
@app.route("/VarChart/")
@crossdomain(origin='*')
def get_VTChart():
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    sql0="""WITH
MaxPst AS ( SELECT max("Pstng Date")::date as P
    FROM "public"."MB51"
),
PVar as (SELECT *
FROM "public"."Variance"
WHERE "WO" < 59999999
AND TRIM("Cost Element (Text)") IN ('Labor','Machine','Setup','Rework','Direct Material - OFT Hardware - 537', 'Other Purchase Mat & Svc HW/SW')
AND "Cost Elem#" > 0
AND "Total act#costs" > 0),
MB AS ( SELECT "Order", EXTRACT(WEEK FROM "Pstng Date") as "FW"
FROM "public"."MB51"
WHERE "Pstng Date" > ((SELECT P FROM MaxPst) - 56 - EXTRACT(DOW FROM (SELECT P FROM MaxPst))::integer )
AND "MvT"= '101'
AND "Order" IS NOT NULL
AND "Order" < 59999999
AND "Plnt" = '6400' )
Select 
sec."FW",
SUM(NV) as negVariance,
SUM(PV) as posVariance,
(SUM(NV)+SUM(PV))/SUM("Stock") as varpercent
FROM (SELECT
prim."FW", 
CASE WHEN prim."netVar" > 0 THEN prim."netVar" ELSE 0 END as NV, 
CASE WHEN prim."netVar" < 0 THEN prim."netVar" ELSE 0 END as PV, 
prim."Stock"
FROM (SELECT h."Order", h."FW",
SUM( g."Target/actual var#") as "netVar",
SUM( g."Total target costs") as "Stock"
FROM PVar g
INNER JOIN MB h
ON h."Order" = g."WO"
GROUP BY "Order","FW"
ORDER BY  "FW","netVar") prim
) sec
GROUP BY "FW";"""


    colla = []
    colla.append("FW")
    colla.append("negVariance")
    colla.append("posVariance")
    colla.append("varpercent")
    message = fetchViewAsJSON(sql0,colla)
    return message
    
    
@app.route("/VarTab/<int:FW>")
@app.route("/VarTab/<int:FW>/")
@crossdomain(origin='*')
def get_VTTable(FW):
    conn = Connect()       
    #print conn
    cursor = conn.cursor()
    d = dict(globals())
    d.update(locals())
    sql0="""WITH MB AS (    SELECT * 
FROM "public"."MB51" 
WHERE EXTRACT(YEAR FROM "Pstng Date") = EXTRACT(YEAR FROM current_date) 
AND EXTRACT(WEEK FROM "Pstng Date") = %(FW)s 
AND "MvT"= '101' 
AND "Order" IS NOT NULL    
AND "Plnt" = '6400' ),
PVar as (SELECT * 
FROM "public"."Variance" 
WHERE "WO" < 59999999 
AND TRIM("Cost Element (Text)") IN ('Labor','Machine','Setup','Rework','Direct Material - OFT Hardware - 537', 'Other Purchase Mat & Svc HW/SW') 
AND "Cost Elem#" > 0 
AND "Total act#costs" > 0)

SELECT  
SUM(g."Target/actual var#")*-1 as Sum_Var
,SUM(g."Other Purchased")*-1 as "External Services"
,SUM(g."Rework")*-1 as "Rework"
,SUM(g."Direct Material")*-1 as "Direct Material"
,SUM(g."Labor")*-1 as "Labor"
,h."Material Description"
,h."Material"
,g."WO"
FROM (
SELECT *,
CASE "Cost Element (Text)" 
WHEN 'Labor' THEN "Target/actual var#"
ELSE 0 END as "Labor"
,CASE "Cost Element (Text)" 
WHEN 'Machine' THEN "Target/actual var#"
ELSE 0 END as "Machine"
,CASE "Cost Element (Text)" 
WHEN 'Setup' THEN "Target/actual var#"
ELSE 0 END as "Setup"
,CASE "Cost Element (Text)" 
WHEN 'Rework' THEN "Target/actual var#"
ELSE 0 END as "Rework"
,CASE "Cost Element (Text)" 
WHEN 'Direct Material - OFT Hardware - 537' THEN "Target/actual var#"
ELSE 0 END as "Direct Material"
,CASE "Cost Element (Text)" 
WHEN 'Other Purchase Mat & Svc HW/SW' THEN "Target/actual var#"
ELSE 0 END as "Other Purchased" 
FROM PVar) g
INNER JOIN MB h
ON h."Order" = g."WO" 
WHERE  g."WO" < 59999999
GROUP BY g."WO", h."Material", h."Material Description"
ORDER BY Sum_Var asc
 """  % d
    colla = []
    colla.append("Sum_Var")
    colla.append("External Services")
    colla.append("Rework")
    colla.append("Direct Material")
    colla.append("Labor")
    colla.append("Material Description")
    colla.append("Material")
    colla.append("WO")  
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
