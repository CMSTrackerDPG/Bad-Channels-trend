#!/usr/bin/python
from ROOT import TFile, gStyle, TCanvas, TH1F, TGraph, TLine, TLegend, TLatex
import sys
import os.path
import os
import time
import calendar
import ROOT
from array import array

DO_FIXED_BIN_WIDTH_PLOTS = False
SHOW_LS = True

#Parse input files and get list of runs and their lengths
def countruns(runfile,runtimesfile,runtype,dataset,year):
    runNumbers = []
    binedges = []
    binsdict = {}
    #Get list of runs
    with open(runfile,"r") as f:
        runNumbers = [int(line) for line in f.readlines() if line != ""]

    #Check if tracker maps exist for all runs
    removeIndex = []
    for index, k in enumerate(runNumbers):
        runshort=str(k)[:3]
        if (k < 287178):
            year=2016
        check_paths = [os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),dataset,'MergedBadComponents_run'+str(k).strip(' \n')+'.txt')]
        if dataset == "ZeroBias1":
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'ZeroBias','MergedBadComponents_run'+str(k).strip(' \n')+'.txt'))
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'PAMinimumBias1','MergedBadComponents_run'+str(k).strip(' \n')+'.txt'))
        if dataset == "StreamExpress":
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'StreamExpressPA','MergedBadComponents_run'+str(k).strip(' \n')+'.txt'))
        found_run = False
        for path in check_paths:
            if os.path.isfile(path): found_run = True
        if not found_run:
            runlist_missingTrackerMap = open('list_missingTrackerMap_SiStrip_' + dataset + '.txt','a+')
            runlist_missingTrackerMap.write(str(k)+'\n')
            removeIndex.append(index)

    #If tracker maps don't exist, remove runs from list   
    for remove in reversed(removeIndex):
        # we remove in the reverse order to avoid changing the position of the item we will remove
        del runNumbers[remove] #remove this run from the actual list
    
    #Make sure there are runs to process
    if len(runNumbers) == 0:
        print "input file is empty"
        quit()

    #Fill array of bin edges based on lengths of runs
    binedges.append(0)
    with open(runtimesfile,"r") as f:
        line = f.readline().strip()
        runlist = line.lstrip('[').rstrip(']').split('],[')
        runtimesdict = {}
        for run in runlist:
            runnum = run.split(',')[0].strip('"')
            starttime = run.split(',')[1].strip('"').replace('_',' ')
            endtime = run.split(',')[2].strip('"').replace('_',' ')
            runtimesdict[int(runnum)] = [starttime,endtime]
        for run in runNumbers:
            if not runtimesdict.has_key(run):
                print "didn\'t find run %d in run times list!" % run
                quit()
            start_epoch = int(calendar.timegm(time.strptime(runtimesdict[run][0], '%Y-%m-%d %H:%M:%S')))
            end_epoch = int(calendar.timegm(time.strptime(runtimesdict[run][1], '%Y-%m-%d %H:%M:%S')))
            runlength = end_epoch - start_epoch
            binedges.append(binedges[-1] + runlength)
            binsdict[run] = (runtimesdict[run][0], runtimesdict[run][1])

    return runNumbers,binedges,binsdict

#Set histogram range and add title
def SetHRange(h,dataset,runmin,runmax):
    h.SetTitle("Bad Channels "+ dataset + " " +str(runmin).strip(' \n')+"-"+str(runmax).strip(' \n'))
    hmax= h.GetMaximum()
    h.GetYaxis().SetRangeUser(0,hmax*1.2)

#Add vertical lines showing boundaries between runs
def AddRunBoundaries(h,addlabels=False):
    line = TLine()
    line.SetLineStyle(3)
    tl = TLatex()
    tl.SetTextSize(0.025)
    tl.SetTextAlign(33)
    tl.SetTextAngle(90)
    tl2 = TLatex()
    tl2.SetTextSize(0.025)
    tl2.SetTextAlign(31)
    tl2.SetTextAngle(90)
    axislength = h.GetXaxis().GetBinUpEdge(h.GetNbinsX()) - h.GetXaxis().GetBinLowEdge(1)
    for ibin in range(1,h.GetNbinsX()+1):
        if ibin>1:
            line.DrawLine(h.GetXaxis().GetBinLowEdge(ibin),0,h.GetXaxis().GetBinLowEdge(ibin),h.GetMaximum())
        if addlabels:
            tl.DrawLatex(h.GetXaxis().GetBinLowEdge(ibin)+0.005*axislength,0.01,"#splitline{%s }{  %s }" % (binsdict[runNumbers[ibin-1]][0].split()[0],binsdict[runNumbers[ibin-1]][0].split()[1]))
            tl2.DrawLatex(h.GetXaxis().GetBinUpEdge(ibin)-0.01*axislength,0.01,"#splitline{%s }{  %s }" % (binsdict[ibin-1][1].split()[0],binsdict[ibin-1][1].split()[1]))

#Format x-axis and suppress some labels if needed to avoid overcrowding
def FormatAxis(h,nbins,variable=False,maxlabels=60):
    h.GetXaxis().SetRange(1, nbins)
    h.GetXaxis().LabelsOption("v")
    h.GetXaxis().SetTickLength(0.)
    labelSpacing = round(nbins/float(maxlabels),0)
    labelCounter = -1
    totalLength = h.GetXaxis().GetBinUpEdge(nbins) - h.GetXaxis().GetBinLowEdge(1)
    lastLabel = 0.0
    for ibin in range(1,nbins+1):
        labelCounter += 1
        if variable:
            if (h.GetXaxis().GetBinCenter(ibin) - lastLabel)/float(totalLength) < 1./float(maxlabels):
                h.GetXaxis().SetBinLabel(ibin,"")
            else:
                lastLabel = h.GetXaxis().GetBinCenter(ibin)
        else:
            if nbins > maxlabels and labelCounter%labelSpacing != 0:
                h.GetXaxis().SetBinLabel(ibin,"")


runfile=sys.argv[1]
runtimesfile=sys.argv[2]
dataset=str(sys.argv[3])
#addtimelabels=int(sys.argv[4])

runtype="Cosmics" if "Cosmics" in dataset else "Beam"
year=2017

#Clean the missing tracker maps list
if os.path.isfile("list_missingTrackerMap_SiStrip_"+dataset+".txt") :
    os.remove("list_missingTrackerMap_SiStrip_"+dataset+".txt")

runmax=0
runmin=0

n = 9316352

#Get list of run numbers and durations
runNumbers,binedges,binsdict = countruns(runfile,runtimesfile,runtype,dataset,year)

totruns=len(runNumbers)

if totruns == 0:
    print "No runs (or TrackerMaps) found"
    sys.exit()

print dataset

ROOT.gROOT.SetBatch(True)

gStyle.SetHistFillStyle(1)
gStyle.SetHistLineWidth(3)
gStyle.SetOptStat(0)

#Set up trend histograms
if DO_FIXED_BIN_WIDTH_PLOTS:
    trend_vs_run = {}
    trend_vs_run['TIB'] = TH1F("TIB vs run","TIB;;# of Bad Channels TIB",totruns,0,totruns)
    trend_vs_run['TOB'] = TH1F("TOB vs run","TOB;;# of Bad Channels TOB",totruns,0,totruns)
    trend_vs_run['TID'] = TH1F("TID vs run","TID;;# of Bad Channels TID",totruns,0,totruns)
    trend_vs_run['TEC'] = TH1F("TEC vs run","TEC;;# of Bad Channels TEC",totruns,0,totruns)
    trend_vs_run['SiStrip'] = TH1F("SiStrip vs run","SiStrip;;% of Bad Channels SiStrip",totruns,0,totruns)

trend = {}
trend['TIB'] = TH1F("TIB","TIB;;# of Bad Channels TIB",totruns,array('d',binedges))
trend['TOB'] = TH1F("TOB","TOB;;# of Bad Channels TOB",totruns,array('d',binedges))
trend['TID'] = TH1F("TID","TID;;# of Bad Channels TID",totruns,array('d',binedges))
trend['TEC'] = TH1F("TEC","TEC;;# of Bad Channels TEC",totruns,array('d',binedges))
trend['SiStrip'] = TH1F("SiStrip","SiStrip;;% of Bad Channels SiStrip",totruns,array('d',binedges))


bin=0
mean=0
mean_vs_time=0
tot_time=0

#Loop over runs
for index, k in enumerate(runNumbers):
    runshort=str(k)[:3]
    if (k < 287178):
        year=2016

    #Find correct tracker map file
    file_path = ''
    check_paths = [os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),dataset,'MergedBadComponents_run'+str(k).strip(' \n')+'.txt')]
    if dataset == "ZeroBias1":
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'ZeroBias','MergedBadComponents_run'+str(k).strip(' \n')+'.txt'))
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'PAMinimumBias1','MergedBadComponents_run'+str(k).strip(' \n')+'.txt'))
    if dataset == "StreamExpress":
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'StreamExpressPA','MergedBadComponents_run'+str(k).strip(' \n')+'.txt'))
    for path in check_paths:
        if os.path.isfile(path):
            file_path = path
            break
    if file_path == '':
        'Print didn\'t find tracker maps for run number ',str(k),'\!'
        sys.exit()

    bin=bin+1
    with open(file_path,'r') as file_in:
        contents = file_in.readlines()

    #Parse file contents
    for subdet in trend.keys():
        if subdet == 'SiStrip':
            line = [line for line in contents if line.startswith('Tracker:')][0]
            nchannels = 128*float(line.split()[3])
            mean += float(nchannels)
            mean_vs_time += float(nchannels)*(binedges[bin]-binedges[bin-1])
            tot_time += (binedges[bin]-binedges[bin-1])
            fract=100.*float(nchannels)/n  #Fraction of bad channels
            if DO_FIXED_BIN_WIDTH_PLOTS:
                trend_vs_run[subdet].SetBinContent(bin,fract)
                trend_vs_run[subdet].GetXaxis().SetBinLabel(bin,str(k))
            trend[subdet].SetBinContent(bin,fract)
            trend[subdet].GetXaxis().SetBinLabel(bin,str(k))
        else:
            line = [line for line in contents if line.startswith(subdet+':')][0]
            nchannels = 128*float(line.split()[3])
            if DO_FIXED_BIN_WIDTH_PLOTS:
                trend_vs_run[subdet].SetBinContent(bin,float(nchannels))
                trend_vs_run[subdet].GetXaxis().SetBinLabel(bin,str(k))
            trend[subdet].SetBinContent(bin,float(nchannels))
            trend[subdet].GetXaxis().SetBinLabel(bin,str(k))


runmin=runNumbers[0]
runmax=runNumbers[totruns-1]

totfract_time=100.*float(mean_vs_time)/(n*tot_time)
strleg_time="mean BadChannels = " + str(totfract_time)[:4] +"%"

dataset_str = ""
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

Rleg_time=TLegend(0.30,0.30,0.9,0.6)
Rleg_time.SetHeader("#splitline{"+dataset_str+"}{"+strleg_time+"}")
Rleg_time.SetFillStyle(0)
Rleg_time.SetBorderSize(0)
Rleg_time.SetTextSize(0.08)

#Setup x axis
for subdet in trend.keys():
    FormatAxis(trend[subdet],totruns,True)

#Calculate unit of time for legend
totalLength = trend['SiStrip'].GetXaxis().GetBinUpEdge(totruns) - trend['SiStrip'].GetXaxis().GetBinLowEdge(1)
leg_time = TLatex()
leg_time.SetTextSize(0.03)
time_unit = tot_time/20.
m,s = divmod(time_unit,60)
h,m = divmod(m,60)
d,h = divmod(h,24)
time_str = ''
if SHOW_LS:
    time_str = '%3.0f LS' % (time_unit/23.3)
elif d > 0:
    time_str = '%4.1f days' % (time_unit/(3600.*24))
elif h > 0:
    time_str = '%d h, %d m, %3.1f s' % (h,m,(time_unit - (3600.*h + 60.*m)))
elif m > 0:
    time_str = '%d m, %3.1f s' % (m,(time_unit - (60.*m)))
else:
    time_str = '%3.1f seconds' % (time_unit)

folder=os.getcwd()

file = TFile(folder+"/SiStrip_MergedBadChannels_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".root", "RECREATE")

#Format and plot trend vs time histograms
for subdet,hist in trend.iteritems():
    c = TCanvas("c_"+subdet,"c_"+subdet,1,1,1800,800)
    c.SetGridy(True)
    SetHRange(hist,dataset,runmin,runmax)
    hist.Draw()
    if subdet == 'SiStrip':
        Rleg_time.Draw()
    AddRunBoundaries(hist)
    ymax = hist.GetMaximum()
    leg_time_bkg = TGraph(5)
    leg_time_bkg.SetPoint(0,0.15,1.0*ymax)
    leg_time_bkg.SetPoint(1,0.15,0.9*ymax)
    leg_time_bkg.SetPoint(2,0.15+5.5*(totalLength/20.0),0.9*ymax)
    leg_time_bkg.SetPoint(3,0.15+5.5*(totalLength/20.0),1.0*ymax)
    leg_time_bkg.SetPoint(4,0.15,1.0*ymax)
    leg_time_bkg.SetFillColor(10)
    leg_time_bkg.SetFillStyle(1001)
    leg_time_gr = TGraph(4)
    leg_time_gr.SetPoint(0,0.15+totalLength/20.0,0.97*ymax)
    leg_time_gr.SetPoint(1,0.15+totalLength/20.0,0.95*ymax)
    leg_time_gr.SetPoint(2,0.15+2*(totalLength/20.0),0.95*ymax)
    leg_time_gr.SetPoint(3,0.15+2*(totalLength/20.0),0.97*ymax)
    leg_time_bkg.Draw('F')
    leg_time_gr.Draw('L')
    leg_time.DrawLatex(0.15 + 2.25*(totalLength/20.0),0.95*ymax,time_str)
    c.RedrawAxis()
    c.SaveAs(folder+"/SiStrip_MergedBadChannelsTrends/MergedBadChannels"+subdet+"_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
    c.Write()

if DO_FIXED_BIN_WIDTH_PLOTS:
    #Setup x axis
    for subdet in trend_vs_run.keys():
        FormatAxis(trend_vs_run[subdet],totruns)
    
    totfract=100.*float(mean)/(n*totruns)
    strleg="mean BadChannels= " + str(totfract)[:4] +"%"
    
    Rleg=TLegend(0.30,0.30,0.9,0.6)
    Rleg.SetHeader("#splitline{"+dataset_str+"}{"+strleg+"}")
    Rleg.SetFillStyle(0)
    Rleg.SetBorderSize(0)
    Rleg.SetTextSize(0.1)
    
    #Format and plot trend vs run histograms
    for subdet,hist in trend_vs_run.iteritems():
        c = TCanvas("c_vsrun_"+subdet,"c_vsrun_"+subdet,1,1,1800,800)
        c.SetGridy(True)
        SetHRange(hist,dataset,runmin,runmax)
        hist.Draw()
        if subdet == 'SiStrip':
            Rleg.Draw()
        AddRunBoundaries(hist)
        c.SaveAs(folder+"/SiStrip_MergedBadChannelsTrends/MergedBadChannels"+subdet+"_vsrun_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
        c.Write()

