#!/usr/bin/python
from ROOT import TFile, gStyle, gPad, TCanvas, TH1F, TGraph, TLine, TLegend, TLatex
import sys
import os.path
import os
import time
import calendar
import ROOT
from array import array

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
        check_paths = [os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),dataset,'noisyPixelColumns.txt')]
        if dataset == "ZeroBias1":
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'ZeroBias','noisyPixelColumns.txt'))
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'PAMinimumBias1','noisyPixelColumns.txt'))
        if dataset == "StreamExpress":
            check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'StreamExpressPA','noisyPixelColumns.txt'))
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
    h.SetTitle("Noisy Columns "+ dataset + " " +str(runmin).strip(' \n')+"-"+str(runmax).strip(' \n'))
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
            ymax = h.GetMaximum() if h.GetMaximum() > 0 else gPad.GetUymax()
            line.DrawLine(h.GetXaxis().GetBinLowEdge(ibin),0,h.GetXaxis().GetBinLowEdge(ibin),ymax)
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

runtype="Cosmics" if "Cosmics" in dataset else "Beam"
year=2017
beamMode=False if "Cosmics" in dataset else True

#Clean the missing tracker maps list
if os.path.isfile("list_missingTrackerMap_Pixel_"+dataset+".txt") :
    os.remove("list_missingTrackerMap_Pixel_"+dataset+".txt")

runmax=0
runmin=0

#Get list of run numbers and durations
runNumbers,binedges,binsdict = countruns(runfile,runtimesfile,runtype,dataset,year)

totruns= len(runNumbers)

if totruns == 0:
    print "No runs (or TrackerMaps) found"
    sys.exit()

ROOT.gROOT.SetBatch(True)

gStyle.SetHistFillStyle(1)
gStyle.SetHistLineWidth(3)
gStyle.SetOptStat(0)

trend = {}
trend['BPixL1'] = TH1F("BPIX L1","BPIX L1;;# of noisy colums in BPIXL1",totruns,array('d',binedges))
trend['BPixL2'] = TH1F("BPIX L2","BPIX L2;;# of noisy colums in BPIXL2",totruns,array('d',binedges))
trend['BPixL3'] = TH1F("BPIX L3","BPIX L3;;# of noisy colums in BPIXL3",totruns,array('d',binedges))
trend['BPixL4'] = TH1F("BPIX L4","BPIX L4;;# of noisy colums in BPIXL4",totruns,array('d',binedges))
trend['BPix'] = TH1F("BPIX","BPIX;;# of noisy colums in BPIX",totruns,array('d',binedges))
trend['FPixp1'] = TH1F("FPIX +1","FPIX +1;;# of noisy colums in FPIX+1",totruns,array('d',binedges))
trend['FPixp2'] = TH1F("FPIX +2","FPIX +2;;# of noisy colums in FPIX+2",totruns,array('d',binedges))
trend['FPixp3'] = TH1F("FPIX +3","FPIX +3;;# of noisy colums in FPIX+3",totruns,array('d',binedges))
trend['FPixm1'] = TH1F("FPIX -1","FPIX -1;;# of noisy colums in FPIX-1",totruns,array('d',binedges))
trend['FPixm2'] = TH1F("FPIX -2","FPIX -2;;# of noisy colums in FPIX-2",totruns,array('d',binedges))
trend['FPixm3'] = TH1F("FPIX -3","FPIX -3;;# of noisy colums in FPIX-3",totruns,array('d',binedges))
trend['FPix'] = TH1F("FPIX","FPIX;;# of noisy colums in FPIX",totruns,array('d',binedges))
trend['Pixel'] = TH1F("Pixel","Pixel;;# of noisy colums in Pixel",totruns,array('d',binedges))

bin=0

mean=0
mean_bpix=0
mean_fpix=0

tot_time=0
mean_vs_time=0
mean_bpix_vs_time=0
mean_fpix_vs_time=0


#Loop over runs
for index, k in enumerate(runNumbers):
    if beamMode:
        if  float(k) <= 280385 : runtype="BeamReReco23Sep"
        else : runtype="Beam"

    runshort=str(k)[:3]

    #Find correct tracker map file
    file_path = ''
    check_paths = [os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),dataset,'noisyPixelColumns.txt')]
    if dataset == "ZeroBias1":
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'ZeroBias','noisyPixelColumns.txt'))
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'PAMinimumBias1','noisyPixelColumns.txt'))
    if dataset == "StreamExpress":
        check_paths.append(os.path.join('/data/users/event_display/Data'+str(year),runtype,runshort,str(k).strip(' \n'),'StreamExpressPA','noisyPixelColumns.txt'))
    for path in check_paths:
        if os.path.isfile(path):
            file_path = path
            break
    if file_path == '':
        print 'Didn\'t find tracker maps for run number ',str(k),'!'
        #sys.exit()
	bin=bin+1
	continue

    with open(file_path,'r') as file_in:
        contents = file_in.readlines()

    bin=bin+1

    totals = [float(line.split()[3]) for line in contents if "TOTAL IN LAYER" in line]
    if len(totals) != 10:
           continue
    #this is the order of the entries in the file
    trend['BPixL4'].SetBinContent(bin,totals[0])
    trend['FPixp1'].SetBinContent(bin,totals[1])
    trend['FPixp2'].SetBinContent(bin,totals[2])
    trend['FPixp3'].SetBinContent(bin,totals[3])
    trend['BPixL1'].SetBinContent(bin,totals[4])
    trend['BPixL2'].SetBinContent(bin,totals[5])
    trend['BPixL3'].SetBinContent(bin,totals[6])
    trend['FPixm2'].SetBinContent(bin,totals[7])
    trend['FPixm3'].SetBinContent(bin,totals[8])
    trend['FPixm1'].SetBinContent(bin,totals[9])
    bpix = totals[4] + totals[5] + totals[6] + totals[0]
    fpix = totals[1] + totals[2] + totals[3] + totals[9] + totals[7] + totals[8]
    tot = bpix + fpix
    trend['BPix'].SetBinContent(bin,bpix)
    trend['FPix'].SetBinContent(bin,fpix)
    trend['Pixel'].SetBinContent(bin,tot)
    mean_bpix += bpix
    mean_bpix_vs_time += bpix*(binedges[bin] - binedges[bin-1])
    mean_fpix += fpix
    mean_fpix_vs_time += fpix*(binedges[bin] - binedges[bin-1])
    mean += tot
    mean_vs_time += tot*(binedges[bin] - binedges[bin-1])
    tot_time += (binedges[bin]-binedges[bin-1])

    for hist in trend.values():
	hist.GetXaxis().SetBinLabel(bin,str(k))


runmin=runNumbers[0]
runmax=runNumbers[totruns-1]

totfract_bpix_time=1.*float(mean_bpix_vs_time)/(tot_time)
strleg_bpix_time="mean = " + str(totfract_bpix_time)[:4] 
totfract_fpix_time=1.*float(mean_fpix_vs_time)/(tot_time)
strleg_fpix_time="mean = " + str(totfract_fpix_time)[:4] 
totfract_time=1.*float(mean_vs_time)/(tot_time)
strleg_time="mean = " + str(totfract_time)[:4] 

totfract_bpix=1.*float(mean_bpix)/(totruns)
strleg_bpix="mean = " + str(totfract_bpix)[:4] 
totfract_fpix=1.*float(mean_fpix)/(totruns)
strleg_fpix="mean = " + str(totfract_fpix)[:4] 
totfract=1.*float(mean)/(totruns)
strleg="mean = " + str(totfract)[:4] 

print strleg_bpix_time
print strleg_fpix_time
print strleg_time

#Mean doesn't mean (haha) a lot for the moment, so let's remove it.
strleg_bpix_time=""
strleg_fpix_time=""
strleg_time=""
strleg_bpix=""
strleg_fpix=""
strleg=""

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
Rleg_time['BPix'] = FormatLegend(0.3,0.3,0.9,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_bpix_time+"}",txtsize=0.1)
Rleg_time['FPix'] = FormatLegend(0.3,0.3,0.9,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_fpix_time+"}",txtsize=0.1)
Rleg_time['Pixel'] = FormatLegend(0.3,0.3,0.9,0.9,txt="#splitline{"+dataset_str+"}{"+strleg_time+"}",txtsize=0.1)

#Setup x axis
for subdet in trend.keys():
    FormatAxis(trend[subdet],totruns,True)

#Calculate unit of time for legend
totalLength = trend['Pixel'].GetXaxis().GetBinUpEdge(totruns) - trend['Pixel'].GetXaxis().GetBinLowEdge(1)
leg_time = TLatex()
leg_time.SetTextSize(0.03)
lsLength = 23.3
leg_time_scale = 500.*lsLength
leg_time_str = '500 LS'
if leg_time_scale > 0.5*totalLength:
    leg_time_scale = 50.*lsLength
    leg_time_str = '50 LS'
elif leg_time_scale < 0.05*totalLength:
    leg_time_scale = 5000.*lsLength
    leg_time_str = '5000 LS'

'''
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
'''

folder = os.getcwd()

file = TFile(folder+"/Pixel_NoisyColumns_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".root", "RECREATE")

#Format and plot trend vs time histograms
for subdet,hist in trend.iteritems():
    c = TCanvas("c_"+subdet,"c_"+subdet,1,1,1800,800)
    c.SetGridy(True)
    SetHRange(hist,dataset,runmin,runmax)
    hist.Draw()
    if Rleg_time.has_key(subdet):
	Rleg_time[subdet].Draw()
    AddRunBoundaries(hist)
    c.Update()
    ymax = hist.GetMaximum() if hist.GetMaximum() > 0 else gPad.GetUymax()
    leg_time_bkg = TGraph(5)
    leg_time_bkg.SetPoint(0,0.15,1.0*ymax)
    leg_time_bkg.SetPoint(1,0.15,0.9*ymax)
    #leg_time_bkg.SetPoint(2,0.15+5.5*(totalLength/20.0),0.9*ymax)
    #leg_time_bkg.SetPoint(3,0.15+5.5*(totalLength/20.0),1.0*ymax)
    leg_time_bkg.SetPoint(2,0.15+totalLength/10.0+2.5*(leg_time_scale),0.9*ymax)
    leg_time_bkg.SetPoint(3,0.15+totalLength/10.0+2.5*(leg_time_scale),1.0*ymax)
    leg_time_bkg.SetPoint(4,0.15,1.0*ymax)
    leg_time_bkg.SetFillColor(10)
    leg_time_bkg.SetFillStyle(1001)
    leg_time_gr = TGraph(4)
    leg_time_gr.SetPoint(0,0.15+totalLength/20.0,0.97*ymax)
    leg_time_gr.SetPoint(1,0.15+totalLength/20.0,0.95*ymax)
    #leg_time_gr.SetPoint(2,0.15+2*(totalLength/20.0),0.95*ymax)
    #leg_time_gr.SetPoint(3,0.15+2*(totalLength/20.0),0.97*ymax)
    leg_time_gr.SetPoint(2,0.15+totalLength/20.0+leg_time_scale,0.95*ymax)
    leg_time_gr.SetPoint(3,0.15+totalLength/20.0+leg_time_scale,0.97*ymax)
    leg_time_bkg.Draw('F')
    leg_time_gr.Draw('L')
    #leg_time.DrawLatex(0.15 + 2.25*(totalLength/20.0),0.95*ymax,time_str)
    leg_time.DrawLatex(0.15 + totalLength/20.0 + 1.25*(leg_time_scale),0.95*ymax,leg_time_str)
    c.RedrawAxis()
    c.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumns"+subdet+"_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
    c.Write()

