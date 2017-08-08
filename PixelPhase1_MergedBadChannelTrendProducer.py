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
def countruns(runfile,runtimesfile,runtype,dataset,year=2017):
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
        check_paths = [os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),dataset,'PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt')]
        if dataset == "ZeroBias1":
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'ZeroBias','PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt'))
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'PAMinimumBias1','PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt'))
        if dataset == "StreamExpress":
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'StreamExpressPA','PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt'))
        found_run = False
        for path in check_paths:
            if os.path.isfile(path): found_run = True
        if not found_run:
            runlist_missingTrackerMap = open('list_missingTrackerMap_Pixel_' + dataset + '.txt','a+')
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

#Format legend to display summary text
def FormatLegend(x1,y1,x2,y2,txt,txtsize):
    leg = TLegend(x1,y1,x2,y2)
    leg.SetHeader(txt)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0)
    return leg


runfile=sys.argv[1]
runtimesfile=sys.argv[2]
dataset=str(sys.argv[3])
#addtimelabels=int(sys.argv[4])

runtype="Cosmics" if "Cosmics" in dataset else "Beam"
year=2017
beamMode=False if "Cosmics" in dataset else True

#Clean the missing tracker maps list
if os.path.isfile("list_missingTrackerMap_Pixel_"+dataset+".txt") :
    os.remove("list_missingTrackerMap_Pixel_"+dataset+".txt")

runmax=0
runmin=0

n = 29696 # =18944+10752
n_bpix = 18944 # =(1536+3584+5632+8192)
n_fpix = 10752 # =(1792*3*2)

limit_cluster = 29696*100
nofClusters=100000000

#Get list of run numbers and durations
runNumbers,binedges,binsdict = countruns(runfile,runtimesfile,runtype,dataset,year)

totruns= len(runNumbers)

ROOT.gROOT.SetBatch(True)

gStyle.SetHistFillStyle(1)
gStyle.SetHistLineWidth(3)
gStyle.SetOptStat(0)

#Set up trend histograms
if DO_FIXED_BIN_WIDTH_PLOTS:
    trend_vs_run = {}
    trend_vs_run['BPix L1']    = TH1F("BPIX L1 vs run","BPIX L1;;# of Dead ROCs BPIXL1",totruns,0,totruns)
    trend_vs_run['BPix L2']    = TH1F("BPIX L2 vs run","BPIX L2;;# of Dead ROCs BPIXL2",totruns,0,totruns)
    trend_vs_run['BPix L3']    = TH1F("BPIX L3 vs run","BPIX L3;;# of Dead ROCs BPIXL3",totruns,0,totruns)
    trend_vs_run['BPix L4']    = TH1F("BPIX L4 vs run","BPIX L4;;# of Dead ROCs BPIXL4",totruns,0,totruns)
    trend_vs_run['BPix tot']   = TH1F("BPIX vs run","BPIX;;% of Dead ROCs BPIX",totruns,0,totruns)
    trend_vs_run['FPix R1DM3'] = TH1F("FPIX R1DM3 vs run","FPIX R1DM3;;# of Dead ROCs FPIXR1DM3",totruns,0,totruns)
    trend_vs_run['FPix R1DM2'] = TH1F("FPIX R1DM2 vs run","FPIX R1DM2;;# of Dead ROCs FPIXR1DM2",totruns,0,totruns)
    trend_vs_run['FPix R1DM1'] = TH1F("FPIX R1DM1 vs run","FPIX R1DM1;;# of Dead ROCs FPIXR1DM1",totruns,0,totruns)
    trend_vs_run['FPix R1DP1'] = TH1F("FPIX R1DP1 vs run","FPIX R1DP1;;# of Dead ROCs FPIXR1DP1",totruns,0,totruns)
    trend_vs_run['FPix R1DP2'] = TH1F("FPIX R1DP2 vs run","FPIX R1DP2;;# of Dead ROCs FPIXR1DP2",totruns,0,totruns)
    trend_vs_run['FPix R1DP3'] = TH1F("FPIX R1DP3 vs run","FPIX R1DP3;;# of Dead ROCs FPIXR1DP3",totruns,0,totruns)
    trend_vs_run['FPix R2DM3'] = TH1F("FPIX R2DM3 vs run","FPIX R2DM3;;# of Dead ROCs FPIXR2DM3",totruns,0,totruns)
    trend_vs_run['FPix R2DM2'] = TH1F("FPIX R2DM2 vs run","FPIX R2DM2;;# of Dead ROCs FPIXR2DM2",totruns,0,totruns)
    trend_vs_run['FPix R2DM1'] = TH1F("FPIX R2DM1 vs run","FPIX R2DM1;;# of Dead ROCs FPIXR2DM1",totruns,0,totruns)
    trend_vs_run['FPix R2DP1'] = TH1F("FPIX R2DP1 vs run","FPIX R2DP1;;# of Dead ROCs FPIXR2DP1",totruns,0,totruns)
    trend_vs_run['FPix R2DP2'] = TH1F("FPIX R2DP2 vs run","FPIX R2DP2;;# of Dead ROCs FPIXR2DP2",totruns,0,totruns)
    trend_vs_run['FPix R2DP3'] = TH1F("FPIX R2DP3 vs run","FPIX R2DP3;;# of Dead ROCs FPIXR2DP3",totruns,0,totruns)
    trend_vs_run['FPix tot']   = TH1F("FPIX vs run","FPIX;;% of Dead ROCs FPIX",totruns,0,totruns)
    trend_vs_run['Pixel']      = TH1F("Pixel vs run","Pixel;;% of Dead ROCs Pixel",totruns,0,totruns)

trend = {}
trend['BPix L1']    = TH1F("BPIX L1","BPIX L1;;# of Dead ROCs BPIXL1",totruns,array('d',binedges))
trend['BPix L2']    = TH1F("BPIX L2","BPIX L2;;# of Dead ROCs BPIXL2",totruns,array('d',binedges))
trend['BPix L3']    = TH1F("BPIX L3","BPIX L3;;# of Dead ROCs BPIXL3",totruns,array('d',binedges))
trend['BPix L4']    = TH1F("BPIX L4","BPIX L4;;# of Dead ROCs BPIXL4",totruns,array('d',binedges))
trend['BPix tot']   = TH1F("BPIX","BPIX;;% of Dead ROCs BPIX",totruns,array('d',binedges))
trend['FPix R1DM3'] = TH1F("FPIX R1DM3","FPIX R1DM3;;# of Dead ROCs FPIXR1DM3",totruns,array('d',binedges))
trend['FPix R1DM2'] = TH1F("FPIX R1DM2","FPIX R1DM2;;# of Dead ROCs FPIXR1DM2",totruns,array('d',binedges))
trend['FPix R1DM1'] = TH1F("FPIX R1DM1","FPIX R1DM1;;# of Dead ROCs FPIXR1DM1",totruns,array('d',binedges))
trend['FPix R1DP1'] = TH1F("FPIX R1DP1","FPIX R1DP1;;# of Dead ROCs FPIXR1DP1",totruns,array('d',binedges))
trend['FPix R1DP2'] = TH1F("FPIX R1DP2","FPIX R1DP2;;# of Dead ROCs FPIXR1DP2",totruns,array('d',binedges))
trend['FPix R1DP3'] = TH1F("FPIX R1DP3","FPIX R1DP3;;# of Dead ROCs FPIXR1DP3",totruns,array('d',binedges))
trend['FPix R2DM3'] = TH1F("FPIX R2DM3","FPIX R2DM3;;# of Dead ROCs FPIXR2DM3",totruns,array('d',binedges))
trend['FPix R2DM2'] = TH1F("FPIX R2DM2","FPIX R2DM2;;# of Dead ROCs FPIXR2DM2",totruns,array('d',binedges))
trend['FPix R2DM1'] = TH1F("FPIX R2DM1","FPIX R2DM1;;# of Dead ROCs FPIXR2DM1",totruns,array('d',binedges))
trend['FPix R2DP1'] = TH1F("FPIX R2DP1","FPIX R2DP1;;# of Dead ROCs FPIXR2DP1",totruns,array('d',binedges))
trend['FPix R2DP2'] = TH1F("FPIX R2DP2","FPIX R2DP2;;# of Dead ROCs FPIXR2DP2",totruns,array('d',binedges))
trend['FPix R2DP3'] = TH1F("FPIX R2DP3","FPIX R2DP3;;# of Dead ROCs FPIXR2DP3",totruns,array('d',binedges))
trend['FPix tot']   = TH1F("FPIX","FPIX;;% of Dead ROCs FPIX",totruns,array('d',binedges))
trend['Pixel']      = TH1F("Pixel","Pixel;;% of Dead ROCs Pixel",totruns,array('d',binedges))

print dataset

bin=0
bin_time=0

mean=0
mean_bpix=0
mean_fpix=0

tot_time=0
mean_vs_time=0
mean_bpix_vs_time=0
mean_fpix_vs_time=0

notEnoughClusters=0

#Loop over runs
for index, k in enumerate(runNumbers):
    if beamMode:
        if  float(k) <= 280385 : runtype="BeamReReco23Sep"
        else : runtype="Beam"
    runshort=str(k)[:3]

    #Find correct tracker map file
    file_path = ''
    check_paths = [os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),dataset,'PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt')]
    if dataset == "ZeroBias1":
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'ZeroBias','PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt'))
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'PAMinimumBias1','PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt'))
    if dataset == "StreamExpress":
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'StreamExpressPA','PixZeroOccROCs_run'+str(k).strip(' \n')+'.txt'))
    for path in check_paths:
        if os.path.isfile(path):
            file_path = path
            break
    if file_path == '':
        'Print didn\'t find tracker maps for run number ',str(k),'\!'
        sys.exit()

    tot=0
    bin_time=bin_time+1

    with open(file_path,'r') as file_in:
        contents = file_in.readlines()

    #Read DEAD ROC numbers from input file
    found_line = False
    for line in contents: 
       if "Number of clusters=" in line:
            nofClusters =(line.split()[3])
            found_line = True
    if float(nofClusters) < limit_cluster or not found_line:
        notEnoughClusters = notEnoughClusters + 1
	continue

    bin=bin+1

    #Parse file contents
    for subdet in trend.keys():
	if subdet == 'Pixel':
	    continue
	ndeadroc = 0
	for line in contents:
	    if line.startswith(subdet):
	        ndeadroc = line.split()[2]
        if subdet == 'BPix tot':
            mean_bpix+=float(ndeadroc)
            mean_bpix_vs_time+=float(ndeadroc)*(binedges[bin_time]-binedges[bin_time-1])
            tot+=float(ndeadroc)
            mean+=float(ndeadroc)
            mean_vs_time+=float(ndeadroc)*(binedges[bin_time]-binedges[bin_time-1])
            fract_bpix=100.*float(ndeadroc)/n_bpix
            if DO_FIXED_BIN_WIDTH_PLOTS:
                trend_vs_run[subdet].SetBinContent(bin,fract_bpix)
                trend_vs_run[subdet].GetXaxis().SetBinLabel(bin,str(k))
            trend[subdet].SetBinContent(bin,fract_bpix)
            trend[subdet].GetXaxis().SetBinLabel(bin,str(k))
        elif subdet == 'FPix tot':
            mean_fpix+=float(ndeadroc)
            mean_fpix_vs_time+=float(ndeadroc)*(binedges[bin_time]-binedges[bin_time-1])
            tot+=float(ndeadroc)
            mean+=float(ndeadroc)
            mean_vs_time+=float(ndeadroc)*(binedges[bin_time]-binedges[bin_time-1])
            fract_fpix=100.*float(ndeadroc)/n_fpix
	    if DO_FIXED_BIN_WIDTH_PLOTS:
                trend_vs_run[subdet].SetBinContent(bin,fract_fpix)
                trend_vs_run[subdet].GetXaxis().SetBinLabel(bin,str(k))
            trend[subdet].SetBinContent(bin,fract_fpix)
            trend[subdet].GetXaxis().SetBinLabel(bin,str(k))
        else:
	    if DO_FIXED_BIN_WIDTH_PLOTS:
                trend_vs_run[subdet].SetBinContent(bin,float(ndeadroc))
                trend_vs_run[subdet].GetXaxis().SetBinLabel(bin,str(k))
            trend[subdet].SetBinContent(bin,float(ndeadroc))
            trend[subdet].GetXaxis().SetBinLabel(bin,str(k))
    tot_time += (binedges[bin_time]-binedges[bin_time-1])
    fract=100.*float(tot)/n;
    if DO_FIXED_BIN_WIDTH_PLOTS:
        trend_vs_run['Pixel'].SetBinContent(bin,fract);
        trend_vs_run['Pixel'].GetXaxis().SetBinLabel(bin,str(k))
    trend['Pixel'].SetBinContent(bin,fract)
    trend['Pixel'].GetXaxis().SetBinLabel(bin,str(k))


totruns = totruns - notEnoughClusters

if totruns == 0:
    print "No runs (or TrackerMaps) found"
    sys.exit()


runmin=runNumbers[0]
runmax=runNumbers[totruns-1]

totfract_bpix_time=100.*float(mean_bpix_vs_time)/(n_bpix*tot_time)
strleg_bpix_time="mean BPIX Dead ROCs = " + str(totfract_bpix_time)[:4] +"%"
totfract_fpix_time=100.*float(mean_fpix_vs_time)/(n_fpix*tot_time)
strleg_fpix_time="mean FPIX Dead ROCs = " + str(totfract_fpix_time)[:4] +"%"
totfract_time=100.*float(mean_vs_time)/(n*tot_time)
strleg_time="mean Pixel Dead ROCs = " + str(totfract_time)[:4] +"%"

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

Rleg_time = {}
Rleg_time['BPix tot'] = FormatLegend(0.2,0.3,0.8,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_bpix_time+"}",txtsize=0.1)
Rleg_time['FPix tot'] = FormatLegend(0.2,0.3,0.8,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_fpix_time+"}",txtsize=0.1)
Rleg_time['Pixel'] = FormatLegend(0.2,0.3,0.8,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_time+"}",txtsize=0.1)

#Setup x axis
for subdet in trend.keys():
    FormatAxis(trend[subdet],totruns,True)

#Calculate unit of time for legend
totalLength = trend['Pixel'].GetXaxis().GetBinUpEdge(totruns) - trend['Pixel'].GetXaxis().GetBinLowEdge(1)
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

file = TFile(folder+"/Pixel_MergedBadChannels_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".root", "RECREATE")

#Format and plot trend vs time histograms
for subdet,hist in trend.iteritems():
    c = TCanvas("c_"+subdet,"c_"+subdet,1,1,1800,800)
    c.SetGridy(True)
    SetHRange(hist,dataset,runmin,runmax)
    hist.Draw()
    if Rleg_time.has_key(subdet):
	Rleg_time[subdet].Draw()
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
    c.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannels"+subdet.replace(" ","")+"_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
    c.Write()



if DO_FIXED_BIN_WIDTH_PLOTS:
    #Setup x axis
    for subdet in trend_vs_run.keys():
        FormatAxis(trend_vs_run[subdet],totruns)

    totfract_bpix=100.*float(mean_bpix)/(n_bpix*totruns)
    strleg_bpix="mean BPIX Dead ROCs= " + str(totfract_bpix)[:4] +"%"
    totfract_fpix=100.*float(mean_fpix)/(n_fpix*totruns)
    strleg_fpix="mean FPIX Dead ROCs= " + str(totfract_fpix)[:4] +"%"
    totfract=100.*float(mean)/(n*totruns)
    strleg="mean Pixel Dead ROCs= " + str(totfract)[:4] +"%"

    Rleg = {}
    Rleg['BPix tot'] = FormatLegend(0.3,0.3,0.9,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_bpix+"}",txtsize=0.1)
    Rleg['FPix tot'] = FormatLegend(0.3,0.3,0.9,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_fpix+"}",txtsize=0.1)
    Rleg['Pixel'] = FormatLegend(0.3,0.3,0.9,0.9,txt="#splitline{"+dataset_str+"}{"+strleg+"}",txtsize=0.1)

    #Format and plot trend vs run histograms
    for subdet,hist in trend_vs_run.iteritems():
        c = TCanvas("c_vsrun_"+subdet,"c_vsrun_"+subdet,1,1,1800,800)
        c.SetGridy(True)
        SetHRange(hist,dataset,runmin,runmax)
        hist.Draw()
        if Rleg.has_key(subdet):
    	    Rleg[subdet].Draw()
        AddRunBoundaries(hist)
        c.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannels"+subdet.replace(" ","")+"_vsrun_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
        c.Write()

