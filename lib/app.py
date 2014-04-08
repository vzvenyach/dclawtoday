#!/usr/bin/env python

# USAGE
# 
# python app.py 
# 
# This generates a JSON object of each of the 3 courts' decisions and the Council's actions for the day

import urllib, urllib2
import datetime
import json
import os

def authenticate_API ():
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	top_level_url = "https://www.courtlistener.com/api/rest/v1/"
	password_mgr.add_password(None, top_level_url, 'vdavez','XaydidB15hpJ')
	handler = urllib2.HTTPBasicAuthHandler(password_mgr)
	opener = urllib2.build_opener(handler)
	urllib2.install_opener(opener)

def get_courts (court, date):
	out_data = []
	courts_url = "https://www.courtlistener.com/api/rest/v1/opinion/?court=" + court + "&date_filed__gte=" + date
	data = json.load(urllib2.urlopen(courts_url))

	for case in data["objects"]:
		out_data.append(case)

	# Loop through to get the rest of the decisions
	total_cases = data["meta"]["total_count"]
	i = 20
	while i < int(total_cases):
		new_url = "https://www.courtlistener.com" + data["meta"]["next"]
		data = json.load(urllib2.urlopen(new_url))
		for case in data["objects"]:
			out_data.append(case)
		i = i + 20
	return out_data

def get_measures (date):
	out_data = []
	measures_url = "https://api.opencivicdata.org/bills/?jurisdiction_id=ocd-jurisdiction/country:us/state:dc/legislature&apikey=e1b0f4a0c7b94f70aed6e6273c2a5b2c&updated_at__gt=" + date
	data = json.load(urllib2.urlopen(measures_url))
	for m in data["results"]:
		m_id = m["identifiers"][0]["identifier"]
		m_url = 'http://openstates.org/api/v1/bills/' + m_id + '?&apikey=e1b0f4a0c7b94f70aed6e6273c2a5b2c'
		m_data = json.load(urllib2.urlopen(m_url))
		out_data.append(m_data)
	return out_data

def write_to_file (date, data):
	f = open('../json/' + date + '.json', 'w')
	f.write(data)
	f.close

def main ():
	authenticate_API()
	date = datetime.date.today().isoformat()
#	date = "2014-04-03"
	data = []
	data.append({
		"court":"DCD",
		"decisions":get_courts("dcd", date)
		})
	data.append({
		"court":"CADC",
		"decisions":get_courts("cadc", date)
		})
	data.append({
		"court":"DCCA",
		"decisions":get_courts("dcca", date)
		})
	data.append({
		"council":"CDC",
		"measures": get_measures(date)
		})
	write_to_file(date, json.dumps({"date":date, "objects":data}, indent=2))

main()