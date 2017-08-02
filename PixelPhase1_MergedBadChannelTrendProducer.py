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

n = 29696 # =18944+10752
n_bpix = 18944 # =(1536+3584+5632+8192)
n_fpix = 10752 # =(1792*3*2)

limit_cluster = 29696*100
nofClusters=100000000

countruns()
#print runs

ROOT.gROOT.SetBatch(True)

trendBPIXL1=TH1F("BPIX L1","BPIX L1",runs,0,runs)
trendBPIXL2=TH1F("BPIX L2","BPIX L2",runs,0,runs)
trendBPIXL3=TH1F("BPIX L3","BPIX L3",runs,0,runs)
trendBPIXL4=TH1F("BPIX L4","BPIX L4",runs,0,runs)
trendBPIX=TH1F("BPIX","BPIX",runs,0,runs)
trendFPIXR1DM3=TH1F("FPIX R1DM3","FPIX R1DM3",runs,0,runs)
trendFPIXR1DM2=TH1F("FPIX R1DM2","FPIX R1DM2",runs,0,runs)
trendFPIXR1DM1=TH1F("FPIX R1DM1","FPIX R1DM1",runs,0,runs)
trendFPIXR1DP1=TH1F("FPIX R1DP1","FPIX R1DP1",runs,0,runs)
trendFPIXR1DP2=TH1F("FPIX R1DP2","FPIX R1DP2",runs,0,runs)
trendFPIXR1DP3=TH1F("FPIX R1DP3","FPIX R1DP3",runs,0,runs)
trendFPIXR2DM3=TH1F("FPIX R2DM3","FPIX R2DM3",runs,0,runs)
trendFPIXR2DM2=TH1F("FPIX R2DM2","FPIX R2DM2",runs,0,runs)
trendFPIXR2DM1=TH1F("FPIX R2DM1","FPIX R2DM1",runs,0,runs)
trendFPIXR2DP1=TH1F("FPIX R2DP1","FPIX R2DP1",runs,0,runs)
trendFPIXR2DP2=TH1F("FPIX R2DP2","FPIX R2DP2",runs,0,runs)
trendFPIXR2DP3=TH1F("FPIX R2DP3","FPIX R2DP3",runs,0,runs)
trendFPIX=TH1F("FPIX","FPIX",runs,0,runs)
trend=TH1F("Pixel","Pixel",runs,0,runs)

trendBPIXL1.GetYaxis().SetTitle("# of Dead ROCs BPIXL1")
trendBPIXL2.GetYaxis().SetTitle("# of Dead ROCs BPIXL2")
trendBPIXL3.GetYaxis().SetTitle("# of Dead ROCs BPIXL3")
trendBPIXL4.GetYaxis().SetTitle("# of Dead ROCs BPIXL4")
trendBPIX.GetYaxis().SetTitle("% of Dead ROCs BPIX")
trendFPIXR1DM3.GetYaxis().SetTitle("# of Dead ROCs FPIXR1DM3")
trendFPIXR1DM2.GetYaxis().SetTitle("# of Dead ROCs FPIXR1DM2")
trendFPIXR1DM1.GetYaxis().SetTitle("# of Dead ROCs FPIXR1DM1")
trendFPIXR1DP1.GetYaxis().SetTitle("# of Dead ROCs FPIXR1DP1")
trendFPIXR1DP2.GetYaxis().SetTitle("# of Dead ROCs FPIXR1DP2")
trendFPIXR1DP3.GetYaxis().SetTitle("# of Dead ROCs FPIXR1DP3")
trendFPIXR2DM3.GetYaxis().SetTitle("# of Dead ROCs FPIXR2DM3")
trendFPIXR2DM2.GetYaxis().SetTitle("# of Dead ROCs FPIXR2DM2")
trendFPIXR2DM1.GetYaxis().SetTitle("# of Dead ROCs FPIXR2DM1")
trendFPIXR2DP1.GetYaxis().SetTitle("# of Dead ROCs FPIXR2DP1")
trendFPIXR2DP3.GetYaxis().SetTitle("# of Dead ROCs FPIXR2DP2")
trendFPIXR2DP3.GetYaxis().SetTitle("# of Dead ROCs FPIXR2DP3")
trendFPIX.GetYaxis().SetTitle("% of Dead ROCs FPIX")
trend.GetYaxis().SetTitle("% of Dead ROCs Pixel")

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

def fillHistos(filename):
    global notEnoughClusters
    global limit_cluster
    global bin
    global mean_bpix
    global mean_fpix
    global mean
    nofClusters=0
    tot=0
    bpixl1=0
    bpixl2=0
    bpixl3=0
    bpixl4=0
    bpix=0
    fpixr1dm3=0
    fpixr1dm2=0
    fpixr1dm1=0
    fpixr1dp1=0
    fpixr1dp2=0
    fpixr1dp3=0
    fpixr2dm3=0
    fpixr2dm2=0
    fpixr2dm1=0
    fpixr2dp1=0
    fpixr2dp2=0
    fpixr2dp3=0
    fpix=0
    # Read DEAD ROC numbers from inputfile
    for line in filename: 
        if "Number of clusters=" in line:
            nofClusters =(line.split()[3])
    if float(nofClusters) < limit_cluster:
        notEnoughClusters = notEnoughClusters + 1
        return None #equivalent to a continue in the loop
    bin=bin+1
    #since we loop again on the file, we need to move to position 0 first
    filename.seek(0)
    for line in filename:
        if "BPix L1" in line:
            bpixl1=(line.split()[2])
        if "BPix L2" in line:
            bpixl2=(line.split()[2])
        if "BPix L3" in line:
            bpixl3=(line.split()[2])
        if "BPix L4" in line:
            bpixl4=(line.split()[2])
        if "FPix R1DM3" in line:
            fpixr1dm3=(line.split()[2])
        if "FPix R1DM2" in line:
            fpixr1dm2=(line.split()[2])
        if "FPix R1DM1" in line:
            fpixr1dm1=(line.split()[2])
        if "FPix R1DP1" in line:
            fpixr1dp1=(line.split()[2])
        if "FPix R1DP2" in line:
            fpixr1dp2=(line.split()[2])
        if "FPix R1DP3" in line:
            fpixr1dp3=(line.split()[2])
        if "FPix R2DM3" in line:
            fpixr2dm3=(line.split()[2])
        if "FPix R2DM2" in line:
            fpixr2dm2=(line.split()[2])
        if "FPix R2DM1" in line:
            fpixr2dm1=(line.split()[2])
        if "FPix R2DP1" in line:
            fpixr2dp1=(line.split()[2])
        if "FPix R2DP2" in line:
            fpixr2dp2=(line.split()[2])
        if "FPix R2DP3" in line:
            fpixr2dp3=(line.split()[2])                
        if "BPix tot" in line:
            bpix=(line.split()[2])
            mean_bpix+=float(bpix)
            mean+=float(bpix)
            tot+=float(bpix)
        if "FPix tot" in line:
            fpix=(line.split()[2])
            mean_fpix+=float(fpix)
            mean+=float(fpix)
            tot+=float(fpix)
    #print line
    # Setting bincontent of the histograms    
    trendBPIXL1.SetBinContent(bin,float(bpixl1));
    trendBPIXL1.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendBPIXL2.SetBinContent(bin,float(bpixl2));
    trendBPIXL2.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendBPIXL3.SetBinContent(bin,float(bpixl3));
    trendBPIXL3.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendBPIXL4.SetBinContent(bin,float(bpixl4));
    trendBPIXL4.GetXaxis().SetBinLabel(bin,str(k))
    #
    fract_bpix=100.*float(bpix)/n_bpix
    trendBPIX.SetBinContent(bin,fract_bpix);
    trendBPIX.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR1DM3.SetBinContent(bin,float(fpixr1dm3));
    trendFPIXR1DM3.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR1DM2.SetBinContent(bin,float(fpixr1dm2));
    trendFPIXR1DM2.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR1DM1.SetBinContent(bin,float(fpixr1dm1));
    trendFPIXR1DM1.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR1DP1.SetBinContent(bin,float(fpixr1dp1));
    trendFPIXR1DP1.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR1DP2.SetBinContent(bin,float(fpixr1dp2));
    trendFPIXR1DP2.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR1DP3.SetBinContent(bin,float(fpixr1dp3));
    trendFPIXR1DP3.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR2DM3.SetBinContent(bin,float(fpixr2dm3));
    trendFPIXR2DM3.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR2DM2.SetBinContent(bin,float(fpixr2dm2));
    trendFPIXR2DM2.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR2DM1.SetBinContent(bin,float(fpixr2dm1));
    trendFPIXR2DM1.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR2DP1.SetBinContent(bin,float(fpixr2dp1));
    trendFPIXR2DP1.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR2DP2.SetBinContent(bin,float(fpixr2dp2));
    trendFPIXR2DP2.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXR2DP3.SetBinContent(bin,float(fpixr2dp3));
    trendFPIXR2DP3.GetXaxis().SetBinLabel(bin,str(k))
    #
    fract_fpix=100.*float(fpix)/n_fpix
    trendFPIX.SetBinContent(bin,fract_fpix);
    trendFPIX.GetXaxis().SetBinLabel(bin,str(k))
    #
    fract=100.*float(tot)/n;
    trend.SetBinContent(bin,fract);
    trend.GetXaxis().SetBinLabel(bin,str(k))

    return bin

for index, k in enumerate(runNumbers):
    if beamMode:
        if  float(k) <= 280385 : runtype="BeamReReco23Sep"
        else : runtype="Beam"

    runshort=str(k)[:3]

    #print "/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"
    # if (os.path.isfile("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt")):
    if (os.path.isfile("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt")):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        fillHistos(file_in)
    
    elif dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data2017/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/ZeroBias/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/ZeroBias/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        fillHistos(file_in)
    
    elif dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data2017/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/PAMinimumBias1/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/PAMinimumBias1/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        fillHistos(file_in)
    
    elif dataset == "StreamExpress" and os.path.isfile("/data/users/event_display/Data2017/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/StreamExpressPA/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/StreamExpressPA/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt","r");
        fillHistos(file_in)
    
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
strleg_bpix="mean BPIX Dead ROCs= " + str(totfract_bpix)[:4] +"%"
totfract_fpix=100.*float(mean_fpix)/(n_fpix*totruns)
strleg_fpix="mean FPIX Dead ROCs= " + str(totfract_fpix)[:4] +"%"
totfract=100.*float(mean)/(n*totruns)
strleg="mean Pixel Dead ROCs= " + str(totfract)[:4] +"%"

print strleg_bpix
print strleg_fpix
print strleg


runmin=runNumbers[0]
runmax=runNumbers[totruns-1]

trend.GetXaxis().SetRange(1, totruns)
trendBPIXL1.GetXaxis().SetRange(1, totruns)
trendBPIXL2.GetXaxis().SetRange(1, totruns)
trendBPIXL3.GetXaxis().SetRange(1, totruns)
trendBPIXL4.GetXaxis().SetRange(1, totruns)
trendBPIX.GetXaxis().SetRange(1, totruns)
trendFPIXR1DM3.GetXaxis().SetRange(1, totruns)
trendFPIXR1DM2.GetXaxis().SetRange(1, totruns)
trendFPIXR1DM1.GetXaxis().SetRange(1, totruns)
trendFPIXR1DP1.GetXaxis().SetRange(1, totruns)
trendFPIXR1DP2.GetXaxis().SetRange(1, totruns)
trendFPIXR1DP3.GetXaxis().SetRange(1, totruns)
trendFPIXR2DM3.GetXaxis().SetRange(1, totruns)
trendFPIXR2DM2.GetXaxis().SetRange(1, totruns)
trendFPIXR2DM1.GetXaxis().SetRange(1, totruns)
trendFPIXR2DP1.GetXaxis().SetRange(1, totruns)
trendFPIXR2DP2.GetXaxis().SetRange(1, totruns)
trendFPIXR2DP3.GetXaxis().SetRange(1, totruns)
trendFPIX.GetXaxis().SetRange(1, totruns)



trendBPIXL1.GetXaxis().LabelsOption("v")
trendBPIXL2.GetXaxis().LabelsOption("v")
trendBPIXL3.GetXaxis().LabelsOption("v")
trendBPIXL4.GetXaxis().LabelsOption("v")
trendBPIX.GetXaxis().LabelsOption("v")
trendFPIXR1DM3.GetXaxis().LabelsOption("v")
trendFPIXR1DM2.GetXaxis().LabelsOption("v")
trendFPIXR1DM1.GetXaxis().LabelsOption("v")
trendFPIXR1DP1.GetXaxis().LabelsOption("v")
trendFPIXR1DP2.GetXaxis().LabelsOption("v")
trendFPIXR1DP3.GetXaxis().LabelsOption("v")
trendFPIXR2DM3.GetXaxis().LabelsOption("v")
trendFPIXR2DM2.GetXaxis().LabelsOption("v")
trendFPIXR2DM1.GetXaxis().LabelsOption("v")
trendFPIXR2DP1.GetXaxis().LabelsOption("v")
trendFPIXR2DP2.GetXaxis().LabelsOption("v")
trendFPIXR2DP3.GetXaxis().LabelsOption("v")
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


c_BPIXL4 = TCanvas("c_BPIXL4","c_BPIXL4",1,1,1800,800)
c_BPIXL4.SetGridx(True)
c_BPIXL4.SetGridy(True)




#trendBPIXL4.SetFillColor(4)
SetHRange(trendBPIXL4)
trendBPIXL4.Draw()
c_BPIXL4.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsBPIXL4_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL4.Write()


c_FPIXR1DM3 = TCanvas("c_FPIXR1DM3","c_FPIXR1DM3",1,1,1800,800)
c_FPIXR1DM3.SetGridx(True)
c_FPIXR1DM3.SetGridy(True)




#trendFPIXR1DM3.SetFillColor(4)
SetHRange(trendFPIXR1DM3)
trendFPIXR1DM3.Draw()
c_FPIXR1DM3.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR1DM3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR1DM3.Write()


c_FPIXR1DM2 = TCanvas("c_FPIXR1DM2","c_FPIXR1DM2",1,1,1800,800)
c_FPIXR1DM2.SetGridx(True)
c_FPIXR1DM2.SetGridy(True)




#trendFPIXR1DM2.SetFillColor(4)
SetHRange(trendFPIXR1DM2)
trendFPIXR1DM2.Draw()
c_FPIXR1DM2.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR1DM2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR1DM2.Write()

c_FPIXR1DM1 = TCanvas("c_FPIXR1DM1","c_FPIXR1DM1",1,1,1800,800)
c_FPIXR1DM1.SetGridx(True)
c_FPIXR1DM1.SetGridy(True)




#trendFPIXR1DM1.SetFillColor(4)
SetHRange(trendFPIXR1DM1)
trendFPIXR1DM1.Draw()
c_FPIXR1DM1.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR1DM1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR1DM1.Write()


c_FPIXR1DP1 = TCanvas("c_FPIXR1DP1","c_FPIXR1DP1",1,1,1800,800)
c_FPIXR1DP1.SetGridx(True)
c_FPIXR1DP1.SetGridy(True)




#trendFPIXR1DP1.SetFillColor(4)
SetHRange(trendFPIXR1DP1)
trendFPIXR1DP1.Draw()
c_FPIXR1DP1.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR1DP1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR1DP1.Write()


c_FPIXR1DP2 = TCanvas("c_FPIXR1DP2","c_FPIXR1DP2",1,1,1800,800)
c_FPIXR1DP2.SetGridx(True)
c_FPIXR1DP2.SetGridy(True)




#trendFPIXR1DP2.SetFillColor(4)
SetHRange(trendFPIXR1DP2)
trendFPIXR1DP2.Draw()
c_FPIXR1DP2.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR1DP2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR1DP2.Write()


c_FPIXR1DP3 = TCanvas("c_FPIXR1DP3","c_FPIXR1DP3",1,1,1800,800)
c_FPIXR1DP3.SetGridx(True)
c_FPIXR1DP3.SetGridy(True)




#trendFPIXR1DP3.SetFillColor(4)
SetHRange(trendFPIXR1DP3)
trendFPIXR1DP3.Draw()
c_FPIXR1DP3.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR1DP3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR1DP3.Write()


c_FPIXR2DM3 = TCanvas("c_FPIXR2DM3","c_FPIXR2DM3",1,1,1800,800)
c_FPIXR2DM3.SetGridx(True)
c_FPIXR2DM3.SetGridy(True)




#trendFPIXR2DM3.SetFillColor(4)
SetHRange(trendFPIXR2DM3)
trendFPIXR2DM3.Draw()
c_FPIXR2DM3.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR2DM3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR2DM3.Write()


c_FPIXR2DM2 = TCanvas("c_FPIXR2DM2","c_FPIXR2DM2",1,1,1800,800)
c_FPIXR2DM2.SetGridx(True)
c_FPIXR2DM2.SetGridy(True)




#trendFPIXR2DM2.SetFillColor(4)
SetHRange(trendFPIXR2DM2)
trendFPIXR2DM2.Draw()
c_FPIXR2DM2.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR2DM2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR2DM2.Write()

c_FPIXR2DM1 = TCanvas("c_FPIXR2DM1","c_FPIXR2DM1",1,1,1800,800)
c_FPIXR2DM1.SetGridx(True)
c_FPIXR2DM1.SetGridy(True)




#trendFPIXR2DM1.SetFillColor(4)
SetHRange(trendFPIXR2DM1)
trendFPIXR2DM1.Draw()
c_FPIXR2DM1.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR2DM1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR2DM1.Write()


c_FPIXR2DP1 = TCanvas("c_FPIXR2DP1","c_FPIXR2DP1",1,1,1800,800)
c_FPIXR2DP1.SetGridx(True)
c_FPIXR2DP1.SetGridy(True)




#trendFPIXR2DP1.SetFillColor(4)
SetHRange(trendFPIXR2DP1)
trendFPIXR2DP1.Draw()
c_FPIXR2DP1.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR2DP1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR2DP1.Write()


c_FPIXR2DP2 = TCanvas("c_FPIXR2DP2","c_FPIXR2DP2",1,1,1800,800)
c_FPIXR2DP2.SetGridx(True)
c_FPIXR2DP2.SetGridy(True)




#trendFPIXR2DP2.SetFillColor(4)
SetHRange(trendFPIXR2DP2)
trendFPIXR2DP2.Draw()
c_FPIXR2DP2.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR2DP2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR2DP2.Write()


c_FPIXR2DP3 = TCanvas("c_FPIXR2DP3","c_FPIXR2DP3",1,1,1800,800)
c_FPIXR2DP3.SetGridx(True)
c_FPIXR2DP3.SetGridy(True)




#trendFPIXR2DP3.SetFillColor(4)
SetHRange(trendFPIXR2DP3)
trendFPIXR2DP3.Draw()
c_FPIXR2DP3.SaveAs(folder+"/Pixel_MergedBadChannelsTrends/Pixel_MergedBadChannelsFPIXR2DP3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXR2DP3.Write()
