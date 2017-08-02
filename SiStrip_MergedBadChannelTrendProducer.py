#!/usr/bin/python
from ROOT import TFile, gStyle, TCanvas, TH1F, TLegend
import re
import sys
import os.path
import ROOT

def countruns():
	global runs
	global runNumbers
	runlist=open(sys.argv[1],"r")
	for i in runlist:
		if i=="": continue
		runs=runs+1
		runNumbers.append(i)
	if runs==0:
		print "input file is empty"
		quit()

def SetHRange(h):
	h.SetTitle("Bad Channels "+ dataset + " " +str(runmin).strip(' \n')+"-"+str(runmax).strip(' \n'))
	hmax= h.GetMaximum()
	h.GetYaxis().SetRangeUser(0,hmax*1.2)

runs=0
runNumbers=[]
runtype=""
runmax=0
runmin=0
removeIndex=[]

n = 9316352

countruns()
#print runs

ROOT.gROOT.SetBatch(True)

trendTIB=TH1F("TIB","TIB",runs,0,runs)
trendTOB=TH1F("TOB","TOB",runs,0,runs)
trendTID=TH1F("TID","TID",runs,0,runs)
trendTEC=TH1F("TEC","TEC",runs,0,runs)
trend=TH1F("SiStrip","SiStrip",runs,0,runs)

trendTIB.GetYaxis().SetTitle("# of Bad Channels TIB")
trendTOB.GetYaxis().SetTitle("# of Bad Channels TOB")
trendTEC.GetYaxis().SetTitle("# of Bad Channels TEC")
trendTID.GetYaxis().SetTitle("# of Bad Channels TID")
trend.GetYaxis().SetTitle("% of Bad Channels SiStrip")

gStyle.SetHistFillColor(4)
gStyle.SetHistFillStyle(1)
gStyle.SetOptStat(0)


bin=0

totruns= len(runNumbers)
dataset=str(sys.argv[2])

print dataset

#Clean the missing tracker maps list
if os.path.isfile("list_missingTrackerMap_StreamExpressCosmics.txt") and dataset == "StreamExpressCosmics": os.remove("list_missingTrackerMap_StreamExpressCosmics.txt")
if os.path.isfile("list_missingTrackerMap_Cosmics.txt") and dataset == "Cosmics": os.remove("list_missingTrackerMap_Cosmics.txt")
if os.path.isfile("list_missingTrackerMap_StreamExpress.txt") and dataset == "StreamExpress": os.remove("list_missingTrackerMap_StreamExpress.txt")
if os.path.isfile("list_missingTrackerMap_ZeroBias1.txt") and dataset == "ZeroBias1": os.remove("list_missingTrackerMap_ZeroBias1.txt")

#if (dataset.find("Cosmics")>0):
# runtype="Cosmics"
#else:
# runtype="Beam"
#runtype="Cosmics"

if "Cosmics" in dataset:
	runtype="Cosmics"
else:
	runtype="Beam"


#runtype=str(sys.argv[3])

mean=0
year=2017

for index, k in enumerate(runNumbers):

	runshort=str(k)[:3]
	if (k < 287178):
		year=2016
	if (os.path.isfile("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/MergedBadComponents_run"+str(k).strip(' \n')+".txt")):
		tot=0
		tib=0 
		tob=0 
		tec=0 
		tid=0
		bin=bin+1
		#print bin
#.strip('\n')
#  file_in=open("sistrip_qtest_"+ str(k).strip('\n') +".log","r");
		file_in=open("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/MergedBadComponents_run"+str(k).strip(' \n')+".txt","r");
		for line in file_in:
			if "Tracker:" in line: 
				tot=(line.split()[3])
				tot=128*float(tot)
				mean+=float(tot)
				# print line 
			if "TIB:" in line: 
				tib =(line.split()[3])
				tib=128*float(tib)
				# print line 
			if "TOB:" in line:
				tob=(line.split()[3])
				tob=128*float(tob)
				# print line 
			if "TEC:" in line: 
				tec=(line.split()[3])
				tec=128*float(tec)
				# print line
			if "TID:" in line: 
				tid=(line.split()[3])
				tid=128*float(tid)
				# print line  


		trendTIB.SetBinContent(bin,float(tib));
		trendTIB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTOB.SetBinContent(bin,float(tob));
		trendTOB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTEC.SetBinContent(bin,float(tec));
		trendTEC.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTID.SetBinContent(bin,float(tid));
		trendTID.GetXaxis().SetBinLabel(bin,str(k))
		#
		fract=100.*float(tot)/n;
		trend.SetBinContent(bin,fract);
		trend.GetXaxis().SetBinLabel(bin,str(k))

	elif (dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/ZeroBias/MergedBadComponents_run"+str(k).strip(' \n')+".txt")):
		tot=0
		tib=0 
		tob=0 
		tec=0 
		tid=0
		bin=bin+1
		#print bin
		file_in=open("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/ZeroBias/MergedBadComponents_run"+str(k).strip(' \n')+".txt","r");
		for line in file_in:
			if "Tracker:" in line: 
				tot=(line.split()[3])
				tot=128*float(tot)
				mean+=float(tot)
				# print line 
			if "TIB:" in line: 
				tib =(line.split()[3])
				tib=128*float(tib)
				# print line 
			if "TOB:" in line:
				tob=(line.split()[3])
				tob=128*float(tob)
				# print line 
			if "TEC:" in line: 
				tec=(line.split()[3])
				tec=128*float(tec)
				# print line
			if "TID:" in line: 
				tid=(line.split()[3])
				tid=128*float(tid)
				# print line  


		trendTIB.SetBinContent(bin,float(tib));
		trendTIB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTOB.SetBinContent(bin,float(tob));
		trendTOB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTEC.SetBinContent(bin,float(tec));
		trendTEC.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTID.SetBinContent(bin,float(tid));
		trendTID.GetXaxis().SetBinLabel(bin,str(k))
		#
		fract=100.*float(tot)/n;
		trend.SetBinContent(bin,fract);
		trend.GetXaxis().SetBinLabel(bin,str(k))
	elif ( dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/PAMinimumBias1/MergedBadComponents_run"+str(k).strip(' \n')+".txt")):
		tot=0
		tib=0 
		tob=0 
		tec=0 
		tid=0
		bin=bin+1
		#print bin
		file_in=open("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/PAMinimumBias1/MergedBadComponents_run"+str(k).strip(' \n')+".txt","r");
		for line in file_in:
			if "Tracker:" in line: 
				tot=(line.split()[3])
				tot=128*float(tot)
				mean+=float(tot)
				# print line 
			if "TIB:" in line: 
				tib =(line.split()[3])
				tib=128*float(tib)
				# print line 
			if "TOB:" in line:
				tob=(line.split()[3])
				tob=128*float(tob)
				# print line 
			if "TEC:" in line: 
				tec=(line.split()[3])
				tec=128*float(tec)
				# print line
			if "TID:" in line: 
				tid=(line.split()[3])
				tid=128*float(tid)
				# print line  


		trendTIB.SetBinContent(bin,float(tib));
		trendTIB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTOB.SetBinContent(bin,float(tob));
		trendTOB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTEC.SetBinContent(bin,float(tec));
		trendTEC.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTID.SetBinContent(bin,float(tid));
		trendTID.GetXaxis().SetBinLabel(bin,str(k))
		#
		fract=100.*float(tot)/n;
		trend.SetBinContent(bin,fract);
		trend.GetXaxis().SetBinLabel(bin,str(k))
	elif ( dataset == "StreamExpress" and os.path.isfile("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/StreamExpressPA/MergedBadComponents_run"+str(k).strip(' \n')+".txt")):
		tot=0
		tib=0 
		tob=0 
		tec=0 
		tid=0
		bin=bin+1
		#print bin
		file_in=open("/data/users/event_display/Data"+str(year)+"/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/StreamExpressPA/MergedBadComponents_run"+str(k).strip(' \n')+".txt","r");
		for line in file_in:
			if "Tracker:" in line: 
				tot=(line.split()[3])
				tot=128*float(tot)
				mean+=float(tot)
				# print line 
			if "TIB:" in line: 
				tib =(line.split()[3])
				tib=128*float(tib)
				# print line 
			if "TOB:" in line:
				tob=(line.split()[3])
				tob=128*float(tob)
				# print line 
			if "TEC:" in line: 
				tec=(line.split()[3])
				tec=128*float(tec)
				# print line
			if "TID:" in line: 
				tid=(line.split()[3])
				tid=128*float(tid)
				# print line  


		trendTIB.SetBinContent(bin,float(tib));
		trendTIB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTOB.SetBinContent(bin,float(tob));
		trendTOB.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTEC.SetBinContent(bin,float(tec));
		trendTEC.GetXaxis().SetBinLabel(bin,str(k))
		#
		trendTID.SetBinContent(bin,float(tid));
		trendTID.GetXaxis().SetBinLabel(bin,str(k))
		#
		fract=100.*float(tot)/n;
		trend.SetBinContent(bin,fract);
		trend.GetXaxis().SetBinLabel(bin,str(k))

	else:

		runlist_missingTrackerMap = open('list_missingTrackerMap_SiStrip_' + dataset + '.txt','a+')
		runlist_missingTrackerMap.write(k)
		removeIndex.append(index)

for remove in reversed(removeIndex):
	# we remove in the reverse order to avoid changing the position of the item we will remove
	del runNumbers[remove] #remove this run from the actual list and update the totruns


totruns = totruns - len(removeIndex)

if totruns == 0:
    print "No runs (or TrackerMaps) found"
    sys.exit()


totfract=100.*float(mean)/(n*totruns)
strleg="mean BadChannels= " + str(totfract)[:4] +"%"

print strleg


runmin=runNumbers[0]
runmax=runNumbers[totruns-1]

trend.GetXaxis().SetRange(1, totruns)
trendTIB.GetXaxis().SetRange(1, totruns)
trendTOB.GetXaxis().SetRange(1, totruns)
trendTID.GetXaxis().SetRange(1, totruns)
trendTEC.GetXaxis().SetRange(1, totruns)



trendTIB.GetXaxis().LabelsOption("v")
trendTOB.GetXaxis().LabelsOption("v")
trendTID.GetXaxis().LabelsOption("v")
trendTEC.GetXaxis().LabelsOption("v")
trend.GetXaxis().LabelsOption("v")

if "ZeroBias" in dataset:
    dataset_str="Prompt-Reco Collisions"
elif "StreamExpressCosmics" in dataset:
    dataset_str="StreamExpress Cosmics"
elif "StreamExpress" in dataset:
    dataset_str="StreamExpress Collisions"
elif "Cosmics" in dataset:
    dataset_str="Prompt-Reco Cosmics"
else:
    dataset_str=dataset

Rleg=TLegend(0.30,0.30,0.9,0.6)
Rleg.SetHeader("#splitline{"+dataset_str+"}{"+strleg+"}")
Rleg.SetFillStyle(0)
Rleg.SetBorderSize(0)
Rleg.SetTextSize(0.1)

folder="/afs/cern.ch/user/c/cctrack/scratch0/Shifter_scripts/AutomaticBadChannelsTrends"

file = TFile(folder+"/SiStrip_MergedBadChannels_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".root", "RECREATE")


c_SiStrip = TCanvas("c_SiStrip","c_SiStrip",1,1,1800,800) 
c_SiStrip.SetGridx(True)
c_SiStrip.SetGridy(True)




#trend.SetFillColor(4)
SetHRange(trend)
trend.Draw()
Rleg.Draw()
c_SiStrip.SaveAs(folder+"/SiStrip_MergedBadChannelsTrends/MergedBadChannelsSiStrip_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_SiStrip.Write()

c_TIB = TCanvas("c_TIB","c_TIB",1,1,1800,800) 
c_TIB.SetGridx(True)
c_TIB.SetGridy(True)



#trendTIB.SetFillColor(4)
SetHRange(trendTIB)
trendTIB.Draw()
c_TIB.SaveAs(folder+"/SiStrip_MergedBadChannelsTrends/MergedBadChannelsTIB_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_TIB.Write()

c_TOB = TCanvas("c_TOB","c_TOB",1,1,1800,800) 
c_TOB.SetGridx(True)
c_TOB.SetGridy(True)




#trendTOB.SetFillColor(4)
SetHRange(trendTOB)
trendTOB.Draw()
c_TOB.SaveAs(folder+"/SiStrip_MergedBadChannelsTrends/MergedBadChannelsTOB_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_TOB.Write()

c_TEC = TCanvas("c_TEC","c_TEC",1,1,1800,800) 
c_TEC.SetGridx(True)
c_TEC.SetGridy(True)





#trendTEC.SetFillColor(4)
SetHRange(trendTEC)
trendTEC.Draw()
c_TEC.SaveAs(folder+"/SiStrip_MergedBadChannelsTrends/MergedBadChannelsTEC_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_TEC.Write()

c_TID = TCanvas("c_TID","c_TID",1,1,1800,800) 
c_TID.SetGridx(True)
c_TID.SetGridy(True)





#trendTID.SetFillColor(4)
SetHRange(trendTID)
trendTID.Draw()
c_TID.SaveAs(folder+"/SiStrip_MergedBadChannelsTrends/MergedBadChannelsTID_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_TID.Write()


