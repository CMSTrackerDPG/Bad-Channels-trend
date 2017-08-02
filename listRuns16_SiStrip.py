#!/usr/bin/env python

import sys,ConfigParser,os,string,commands,time,xmlrpclib

from optparse import OptionParser
import json, csv

from rrapi import RRApi, RRApiError

parser=OptionParser()
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
parser.add_option("-m", "--min", dest="min", type="int", default=287178, help="Minimum run")
parser.add_option("-M", "--max", dest="max", type="int", default=999999, help="Maximum run")
parser.add_option("-d", "--dataset", dest="dataset", type="string", default="all", help="Datasets to take in RR")
parser.add_option("--daymin", dest="daymin", type="string", default="2017-01-01", help="Day of the first run")
parser.add_option("--daymax", dest="daymax", type="string", default="2018-01-01", help="Day of the last run")
parser.add_option("-y","--year", dest="year", type="int", default=2017, help="The year, data taken")
(options, args) = parser.parse_args()

RUNMINCFG=options.min
RUNMAXCFG=options.max
DATASETCFG=options.dataset
DAYMINCFG=options.daymin
DAYMAXCFG=options.daymax
YEAR=options.year

print DAYMINCFG

URL  = "http://runregistry.web.cern.ch/runregistry/"
api = RRApi(URL, debug = True)

if YEAR == 2017:
	if DATASETCFG == "all" or DATASETCFG == "Cosmics":
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "like %Cosmics17%", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Prompt%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_Cosmics = open('runlist_SiStrip_Cosmics.txt', 'w')
		file_Cosmics.write(RUN_DATA[7:]) #We cut the legend so  we just have the run number

	if DATASETCFG == "all" or DATASETCFG == "StreamExpressCosmics" :
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "like %Cosmics17%", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Express%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_StreamExpressCosmics = open('runlist_SiStrip_StreamExpressCosmics.txt', 'w')
		file_StreamExpressCosmics.write(RUN_DATA[7:])
		
	if DATASETCFG == "all" or DATASETCFG == "ZeroBias" :
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "Collisions17", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Prompt%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_ZeroBias = open('runlist_SiStrip_ZeroBias.txt', 'w')
		file_ZeroBias.write(RUN_DATA[7:])

	if DATASETCFG == "all" or DATASETCFG == "StreamExpress" :
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "Collisions17", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Express%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_StreamExpress = open('runlist_SiStrip_StreamExpress.txt', 'w')
		file_StreamExpress.write(RUN_DATA[7:])
elif YEAR == 2016:
	if DATASETCFG == "all" or DATASETCFG == "Cosmics":
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "Cosmics16", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Prompt%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_Cosmics = open('runlist_SiStrip_Cosmics.txt', 'w')
		file_Cosmics.write(RUN_DATA[7:]) #We cut the legend so  we just have the run number

	if DATASETCFG == "all" or DATASETCFG == "StreamExpressCosmics" :
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "Cosmics16", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Express%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_StreamExpressCosmics = open('runlist_SiStrip_StreamExpressCosmics.txt', 'w')
		file_StreamExpressCosmics.write(RUN_DATA[7:])
		
	if DATASETCFG == "all" or DATASETCFG == "ZeroBias" :
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "Collisions16", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Prompt%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_ZeroBias = open('runlist_SiStrip_ZeroBias.txt', 'w')
		file_ZeroBias.write(RUN_DATA[7:])

	if DATASETCFG == "all" or DATASETCFG == "StreamExpress" :
		RUN_DATA = api.data(workspace = 'TRACKER', table = 'runsummary', template = 'csv', columns = ['number'], filter = {"runClassName": "Collisions16", "number": ">= %d AND <= %d" %(int(RUNMINCFG),int(RUNMAXCFG)), "trackerPresent": "true", "tibtidReady": "true", "tobReady": "true","tecmReady": "true", "tecpReady": "true",  "datasets": {"rowClass": "org.cern.cms.dqm.runregistry.user.model.RunDatasetRowGlobal", "filter": {"datasetName": "like %Express%", "runCreated" : ">= %s AND <= %s" %(DAYMINCFG, DAYMAXCFG)}}},tag= 'LATEST')
		file_StreamExpress = open('runlist_SiStrip_StreamExpress.txt', 'w')
		file_StreamExpress.write(RUN_DATA[7:])
