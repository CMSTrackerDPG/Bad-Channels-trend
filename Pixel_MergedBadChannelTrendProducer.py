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

n = 15840 #= (2560-256) + (4096-256) + (5632-256) + 4320
n_bpix = 11520
n_fpix = 4320

limit_cluster = 15840*100
nofClusters=100000000

countruns()
#print runs

ROOT.gROOT.SetBatch(True)

trendBPIXL1=TH1F("BPIX L1","BPIX L1",runs,0,runs)
trendBPIXL2=TH1F("BPIX L2","BPIX L2",runs,0,runs)
trendBPIXL3=TH1F("BPIX L3","BPIX L3",runs,0,runs)
trendBPIX=TH1F("BPIX","BPIX",runs,0,runs)
trendFPIX=TH1F("FPIX","FPIX",runs,0,runs)
trend=TH1F("Pixel","Pixel",runs,0,runs)

trendBPIXL1.GetYaxis().SetTitle("# of Bad Channels BPIXL1")
trendBPIXL2.GetYaxis().SetTitle("# of Bad Channels BPIXL2")
trendBPIXL3.GetYaxis().SetTitle("# of Bad Channels BPIXL3")
trendBPIX.GetYaxis().SetTitle("% of Bad Channels BPIX")
trendFPIX.GetYaxis().SetTitle("% of Bad Channels FPIX")
trend.GetYaxis().SetTitle("% of Bad Channels Pixel")

gStyle.SetHistFillColor(4)
gStyle.SetHistFillStyle(1)
gStyle.SetOptStat(0)


bin=0

totruns= len(runNumbers)
print totruns
dataset=str(sys.argv[2])

print dataset

#Clean the missing tracker maps list
if os.path.isfile("list_Pixel_missingTrackerMap_StreamExpressCosmics.txt") and dataset == "StreamExpressCosmics": os.remove("list_Pixel_missingTrackerMap_StreamExpressCosmics.txt")
if os.path.isfile("list_Pixel missingTrackerMap_Cosmics.txt") and dataset == "Cosmics": os.remove("list_Pixel_missingTrackerMap_Cosmics.txt")
if os.path.isfile("list_Pixel missingTrackerMap_StreamExpress.txt") and dataset == "StreamExpress": os.remove("list_Pixel_missingTrackerMap_StreamExpress.txt")
if os.path.isfile("list_Pixel_missingTrackerMap_ZeroBias1.txt") and dataset == "ZeroBias1": os.remove("list_Pixel_missingTrackerMap_ZeroBias1.txt")

#if (dataset.find("Cosmics")>0):
# runtype="Cosmics"
#else:
# runtype="Beam"
#runtype="Cosmics"



if "Cosmics" in dataset:
    runtype="Cosmics"
    beamMode=False
else:
    runtype="Beam"
    beamMode=True

mean=0
mean_bpix=0
mean_fpix=0

notEnoughClusters=0

for index, k in enumerate(runNumbers):
    if beamMode:
        if  float(k) <= 280385 : runtype="BeamReReco23Sep"
        else : runtype="Beam"

    runshort=str(k)[:3]

    #print "/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"
    if (os.path.isfile("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt")):
        tot=0
        bpixl1=0
        bpixl2=0
        bpixl3=0
        bpix=0
        fpix=0
        #print bin
#.strip('\n')
#  file_in=open("sistrip_qtest_"+ str(k).strip('\n') +".log","r");
        file_in=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in:
            if "Number of clusters" in line:
                nofClusters =(line.split()[3])
        if nofClusters < limit_cluster:
            notEnoughClusters = notEnoughClusters + 1
            continue
        bin=bin+1
        file_in2=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in2:
            if "BPix L1:" in line:
                bpixl1 =(line.split()[2])
                #print line
            if "BPix L2:" in line:
                bpixl2=(line.split()[2])
                #print line
                bpixl3=(line.split()[2])
                #print line
            if "BPix tot:" in line:
                bpix=(line.split()[2])
                tot+=float(bpix)
                mean_bpix+=float(bpix)
                mean+=float(bpix)
                #print line
                #print bpix
            if "FPix tot:" in line:
                fpix=(line.split()[2])
                tot+=float(fpix)
                mean_fpix+=float(fpix)
                mean+=float(fpix)
                #print line


        trendBPIXL1.SetBinContent(bin,float(bpixl1));
        trendBPIXL1.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL2.SetBinContent(bin,float(bpixl2));
        trendBPIXL2.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL3.SetBinContent(bin,float(bpixl3));
        trendBPIXL3.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_bpix=100.*float(bpix)/n_bpix
        trendBPIX.SetBinContent(bin,fract_bpix);
        trendBPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_fpix=100.*float(fpix)/n_fpix
        trendFPIX.SetBinContent(bin,fract_fpix);
        trendFPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract=100.*float(tot)/n;
        trend.SetBinContent(bin,fract);
        trend.GetXaxis().SetBinLabel(bin,str(k))


    elif dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data2016/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/ZeroBias/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"):

        tot=0
        bpixl1=0
        bpixl2=0
        bpixl3=0
        bpix=0
        fpix=0
        #print bin
        file_in=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/ZeroBias/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in:
            if "Number of clusters=" in line:
                nofClusters =(line.split()[3])
        if float(nofClusters) < limit_cluster:
            notEnoughClusters = notEnoughClusters + 1
            continue
        bin=bin+1
        file_in2=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/ZeroBias/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in2:
            if "BPix L1:" in line:
                bpixl1 =(line.split()[2])
                #print line
            if "BPix L2:" in line:
                bpixl2=(line.split()[2])
                #print line
            if "BPix L3:" in line:
                bpixl3=(line.split()[2])
                #print line
            if "BPix tot:" in line:
                bpix=(line.split()[2])
                tot+=float(bpix)
                mean_bpix+=float(bpix)
                mean+=float(bpix)
                #print line
                #print bpix
            if "FPix tot:" in line:
                fpix=(line.split()[2])
                tot+=float(fpix)
                mean_fpix+=float(fpix)
                mean+=float(fpix)
                #print line

        trendBPIXL1.SetBinContent(bin,float(bpixl1));
        trendBPIXL1.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL2.SetBinContent(bin,float(bpixl2));
        trendBPIXL2.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL3.SetBinContent(bin,float(bpixl3));
        trendBPIXL3.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_bpix=100.*float(bpix)/n_bpix
        trendBPIX.SetBinContent(bin,fract_bpix);
        trendBPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_fpix=100.*float(fpix)/n_fpix
        trendFPIX.SetBinContent(bin,fract_fpix);
        trendFPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract=100.*float(tot)/n;
        trend.SetBinContent(bin,fract);
        trend.GetXaxis().SetBinLabel(bin,str(k))
    elif dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data2016/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/PAMinimumBias1/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"):

        tot=0
        bpixl1=0
        bpixl2=0
        bpixl3=0
        bpix=0
        fpix=0
        #print bin
        file_in=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/PAMinimumBias1/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in:
            if "Number of clusters=" in line:
                nofClusters =(line.split()[3])
        if float(nofClusters) < limit_cluster:
            notEnoughClusters = notEnoughClusters + 1
            continue
        bin=bin+1
        file_in2=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/PAMinimumBias1/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in2:
            if "BPix L1:" in line:
                bpixl1 =(line.split()[2])
                #print line
            if "BPix L2:" in line:
                bpixl2=(line.split()[2])
                #print line
            if "BPix L3:" in line:
                bpixl3=(line.split()[2])
                #print line
            if "BPix tot:" in line:
                bpix=(line.split()[2])
                tot+=float(bpix)
                mean_bpix+=float(bpix)
                mean+=float(bpix)
                #print line
                #print bpix
            if "FPix tot:" in line:
                fpix=(line.split()[2])
                tot+=float(fpix)
                mean_fpix+=float(fpix)
                mean+=float(fpix)
                #print line

        trendBPIXL1.SetBinContent(bin,float(bpixl1));
        trendBPIXL1.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL2.SetBinContent(bin,float(bpixl2));
        trendBPIXL2.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL3.SetBinContent(bin,float(bpixl3));
        trendBPIXL3.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_bpix=100.*float(bpix)/n_bpix
        trendBPIX.SetBinContent(bin,fract_bpix);
        trendBPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_fpix=100.*float(fpix)/n_fpix
        trendFPIX.SetBinContent(bin,fract_fpix);
        trendFPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract=100.*float(tot)/n;
        trend.SetBinContent(bin,fract);
        trend.GetXaxis().SetBinLabel(bin,str(k))
    elif dataset == "StreamExpress" and os.path.isfile("/data/users/event_display/Data2016/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/StreamExpressPA/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"):

        tot=0
        bpixl1=0
        bpixl2=0
        bpixl3=0
        bpix=0
        fpix=0
        #print bin
        file_in=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/StreamExpressPA/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in:
            if "Number of clusters=" in line:
                nofClusters =(line.split()[3])
        if float(nofClusters) < limit_cluster:
            notEnoughClusters = notEnoughClusters + 1
            continue
        bin=bin+1
        file_in2=open("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/StreamExpressPA/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        for line in file_in2:
            if "BPix L1:" in line:
                bpixl1 =(line.split()[2])
                #print line
            if "BPix L2:" in line:
                bpixl2=(line.split()[2])
                #print line
            if "BPix L3:" in line:
                bpixl3=(line.split()[2])
                #print line
            if "BPix tot:" in line:
                bpix=(line.split()[2])
                tot+=float(bpix)
                mean_bpix+=float(bpix)
                mean+=float(bpix)
                #print line
                #print bpix
            if "FPix tot:" in line:
                fpix=(line.split()[2])
                tot+=float(fpix)
                mean_fpix+=float(fpix)
                mean+=float(fpix)
                #print line

        trendBPIXL1.SetBinContent(bin,float(bpixl1));
        trendBPIXL1.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL2.SetBinContent(bin,float(bpixl2));
        trendBPIXL2.GetXaxis().SetBinLabel(bin,str(k))
        #
        trendBPIXL3.SetBinContent(bin,float(bpixl3));
        trendBPIXL3.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_bpix=100.*float(bpix)/n_bpix
        trendBPIX.SetBinContent(bin,fract_bpix);
        trendBPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract_fpix=100.*float(fpix)/n_fpix
        trendFPIX.SetBinContent(bin,fract_fpix);
        trendFPIX.GetXaxis().SetBinLabel(bin,str(k))
        #
        fract=100.*float(tot)/n;
        trend.SetBinContent(bin,fract);
        trend.GetXaxis().SetBinLabel(bin,str(k))


    else:

        runlist_missingTrackerMap = open('list_missingTrackerMap_Pixel_' + dataset + '.txt','a+')
        runlist_missingTrackerMap.write(k)
        removeIndex.append(index)

for remove in reversed(removeIndex):
    # we remove in the reverse order to avoid changing the position of the item we will remove
    del runNumbers[remove] #remove this run from the actual list and update the totruns

totruns = totruns - len(removeIndex) - notEnoughClusters

if totruns == 0:
    print "No runs (or TrackerMaps) found"
    sys.exit()

totfract_bpix=100.*float(mean_bpix)/(n_bpix*totruns)
strleg_bpix="mean BPIX BadChannels= " + str(totfract_bpix)[:4] +"%"
totfract_fpix=100.*float(mean_fpix)/(n_fpix*totruns)
strleg_fpix="mean FPIX BadChannels= " + str(totfract_fpix)[:4] +"%"
totfract=100.*float(mean)/(n*totruns)
strleg="mean Pixel BadChannels= " + str(totfract)[:4] +"%"

print strleg_bpix
print strleg_fpix
print strleg


runmin=runNumbers[0]
runmax=runNumbers[totruns-1]

trend.GetXaxis().SetRange(1, totruns)
trendBPIXL1.GetXaxis().SetRange(1, totruns)
trendBPIXL2.GetXaxis().SetRange(1, totruns)
trendBPIXL3.GetXaxis().SetRange(1, totruns)
trendBPIX.GetXaxis().SetRange(1, totruns)
trendFPIX.GetXaxis().SetRange(1, totruns)



trendBPIXL1.GetXaxis().LabelsOption("v")
trendBPIXL2.GetXaxis().LabelsOption("v")
trendBPIXL3.GetXaxis().LabelsOption("v")
trendBPIX.GetXaxis().LabelsOption("v")
trendFPIX.GetXaxis().LabelsOption("v")
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



Rleg_bpix=TLegend(0.30,0.30,0.9,0.9)
Rleg_bpix.SetHeader("#splitline{"+dataset_str+"}{"+strleg_bpix+"}")
Rleg_bpix.SetFillStyle(0)
Rleg_bpix.SetBorderSize(0)
Rleg_bpix.SetTextSize(0.1)

Rleg_fpix=TLegend(0.30,0.30,0.9,0.9)
Rleg_fpix.SetHeader("#splitline{"+dataset_str+"}{"+strleg_fpix+"}")
Rleg_fpix.SetFillStyle(0)
Rleg_fpix.SetBorderSize(0)
Rleg_fpix.SetTextSize(0.1)

Rleg=TLegend(0.30,0.30,0.9,0.9)
Rleg.SetHeader("#splitline{"+dataset_str+"}{"+strleg+"}")
Rleg.SetFillStyle(0)
Rleg.SetBorderSize(0)
Rleg.SetTextSize(0.1)


folder="/afs/cern.ch/user/c/cctrack/scratch0/Shifter_scripts/AutomaticBadChannelsTrends"

file = TFile(folder+"/Pixel_MergedBadChannels_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".root", "RECREATE")


c_Pixel = TCanvas("c_Pixel","c_Pixel",1,1,1800,800)
c_Pixel.SetGridx(True)
c_Pixel.SetGridy(True)




#trend.SetFillColor(4)
SetHRange(trend)
trend.Draw()
Rleg.Draw()
c_Pixel.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsPixel_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_Pixel.Write()

c_BPIX = TCanvas("c_BPIX","c_BPIX",1,1,1800,800)
c_BPIX.SetGridx(True)
c_BPIX.SetGridy(True)



#trendBPIX.SetFillColor(4)
SetHRange(trendBPIX)
trendBPIX.Draw()
Rleg_bpix.Draw()
c_BPIX.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsBPIX_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIX.Write()

c_FPIX = TCanvas("c_FPIX","c_FPIX",1,1,1800,800)
c_FPIX.SetGridx(True)
c_FPIX.SetGridy(True)



#trendFPIX.SetFillColor(4)
SetHRange(trendFPIX)
trendFPIX.Draw()
Rleg_fpix.Draw()
c_FPIX.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIX_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIX.Write()



c_BPIXL1 = TCanvas("c_BPIXL1","c_BPIXL1",1,1,1800,800)
c_BPIXL1.SetGridx(True)
c_BPIXL1.SetGridy(True)




#trendBPIXL1.SetFillColor(4)
SetHRange(trendBPIXL1)
trendBPIXL1.Draw()
c_BPIXL1.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsBPIXL1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL1.Write()


c_BPIXL2 = TCanvas("c_BPIXL2","c_BPIXL2",1,1,1800,800)
c_BPIXL2.SetGridx(True)
c_BPIXL2.SetGridy(True)




#trendBPIXL2.SetFillColor(4)
SetHRange(trendBPIXL2)
trendBPIXL2.Draw()
c_BPIXL2.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsBPIXL2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL2.Write()


c_BPIXL3 = TCanvas("c_BPIXL3","c_BPIXL3",1,1,1800,800)
c_BPIXL3.SetGridx(True)
c_BPIXL3.SetGridy(True)




#trendBPIXL3.SetFillColor(4)
SetHRange(trendBPIXL3)
trendBPIXL3.Draw()
c_BPIXL3.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsBPIXL3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL3.Write()


