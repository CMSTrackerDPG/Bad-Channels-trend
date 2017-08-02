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
    h.SetTitle("Noisy Columns "+ dataset + " " +str(runmin).strip(' \n')+"-"+str(runmax).strip(' \n'))
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
trendFPIXp1=TH1F("FPIX +1","FPIX +1",runs,0,runs)
trendFPIXp2=TH1F("FPIX +2","FPIX +2",runs,0,runs)
trendFPIXp3=TH1F("FPIX +3","FPIX +3",runs,0,runs)
trendFPIXm1=TH1F("FPIX -1","FPIX -1",runs,0,runs)
trendFPIXm2=TH1F("FPIX -2","FPIX -2",runs,0,runs)
trendFPIXm3=TH1F("FPIX -3","FPIX -3",runs,0,runs)
trendFPIX=TH1F("FPIX","FPIX",runs,0,runs)
trend=TH1F("Pixel","Pixel",runs,0,runs)

trendBPIXL1.GetYaxis().SetTitle("# of noisy colums in BPIXL1")
trendBPIXL2.GetYaxis().SetTitle("# of noisy colums in BPIXL2")
trendBPIXL3.GetYaxis().SetTitle("# of noisy colums in BPIXL3")
trendBPIXL4.GetYaxis().SetTitle("# of noisy colums in BPIXL4")
trendBPIX.GetYaxis().SetTitle("# of noisy colums in BPIX")
trendFPIXp1.GetYaxis().SetTitle("# of noisy colums in FPIX+1")
trendFPIXp2.GetYaxis().SetTitle("# of noisy colums in FPIX+2")
trendFPIXp3.GetYaxis().SetTitle("# of noisy colums in FPIX+3")
trendFPIXm1.GetYaxis().SetTitle("# of noisy colums in FPIX-1")
trendFPIXm2.GetYaxis().SetTitle("# of noisy colums in FPIX-2")
trendFPIXm3.GetYaxis().SetTitle("# of noisy colums in FPIX-3")
trendFPIX.GetYaxis().SetTitle("# of noisy colums in FPIX")
trend.GetYaxis().SetTitle("# of noisy colums in Pixel")

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
    fpixp1=0
    fpixp2=0
    fpixp3=0
    fpixm1=0
    fpixm2=0
    fpixm3=0
    fpix=0
    # Read double columns numbers from inputfile
    #for line in filename: 
    #    if "Number of clusters=" in line:
    #        nofClusters =(line.split()[3])
    #if float(nofClusters) < limit_cluster:
    #    notEnoughClusters = notEnoughClusters + 1
    #    return None #equivalent to a continue in the loop
    bin=bin+1
    #since we loop again on the file, we need to move to position 0 first
    #filename.seek(0)
    position_counter =0
    for line in filename:
        if "TOTAL IN LAYER" in line:
#                bpixl4=re.findall('([0-9]+)$', line)	    
            if position_counter == 0:
                 bpixl4=(line.split()[3])
            elif position_counter == 1:
                 fpixp1=(line.split()[3])
            elif position_counter == 2:
                 fpixp2=(line.split()[3])
            elif position_counter == 3:
                 fpixp3=(line.split()[3])
            elif position_counter == 4:
                 bpixl1=(line.split()[3])
            elif position_counter == 5:
                 bpixl2=(line.split()[3])
            elif position_counter == 6:
                 bpixl3=(line.split()[3])
            elif position_counter == 7:
                 fpixm2=(line.split()[3])
            elif position_counter == 8:
                 fpixm3=(line.split()[3])
            elif position_counter == 9:
                 fpixm1=(line.split()[3])
                 bpix=float(bpixl1)+float(bpixl2)+float(bpixl3)+float(bpixl4)
		 mean_bpix += float(bpix)
		 fpix=float(fpixp1)+float(fpixp2)+float(fpixp3)+float(fpixm1)+float(fpixm2)+float(fpixm3)
		 mean_fpix += float(fpix)
		 tot=float(bpix)+float(fpix)
		 mean += float(tot)
            position_counter = position_counter + 1
    

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
    trendBPIX.SetBinContent(bin,float(bpix));
    trendBPIX.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXp1.SetBinContent(bin,float(fpixp1));
    trendFPIXp1.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXp2.SetBinContent(bin,float(fpixp2));
    trendFPIXp2.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXp3.SetBinContent(bin,float(fpixp3));
    trendFPIXp3.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXm1.SetBinContent(bin,float(fpixm1));
    trendFPIXm1.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXm2.SetBinContent(bin,float(fpixm2));
    trendFPIXm2.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIXm3.SetBinContent(bin,float(fpixm3));
    trendFPIXm3.GetXaxis().SetBinLabel(bin,str(k))
    #
    trendFPIX.SetBinContent(bin,float(fpix));
    trendFPIX.GetXaxis().SetBinLabel(bin,str(k))
    #
    trend.SetBinContent(bin,float(tot));
    trend.GetXaxis().SetBinLabel(bin,str(k))

    return bin






for index, k in enumerate(runNumbers):
    if beamMode:
        if  float(k) <= 280385 : runtype="BeamReReco23Sep"
        else : runtype="Beam"

    runshort=str(k)[:3]

    #print "/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt"
    # if (os.path.isfile("/data/users/event_display/Data2016/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/PixZeroOccROCs_run"+str(k).strip(' \n')+".txt")):
    if (os.path.isfile("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/noisyPixelColumns.txt")):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/" + dataset + "/noisyPixelColumns.txt","r");
        fillHistos(file_in)
    
    elif dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data2017/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/ZeroBias/noisyPixelColumns.txt"):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/ZeroBias/noisyPixelColumns.txt","r");
        fillHistos(file_in)
    
    elif dataset == "ZeroBias1" and os.path.isfile("/data/users/event_display/Data2017/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/PAMinimumBias1/noisyPixelColumns.txt"):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/PAMinimumBias1/noisyPixelColumns.txt","r");
        fillHistos(file_in)
    
    elif dataset == "StreamExpress" and os.path.isfile("/data/users/event_display/Data2017/"+runtype+"/"+runshort+"/"+str(k).strip(' \n')+"/StreamExpressPA/noisyPixelColumns.txt"):
        file_in=open("/data/users/event_display/Data2017/" + runtype + "/" + runshort + "/"+str(k).strip(' \n')+"/StreamExpressPA/noisyPixelColumns.txt","r");
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

totfract_bpix=1.*float(mean_bpix)/(totruns)
strleg_bpix="mean = " + str(totfract_bpix)[:4] 
totfract_fpix=1.*float(mean_fpix)/(totruns)
strleg_fpix="mean = " + str(totfract_fpix)[:4] 
totfract=1.*float(mean)/(totruns)
strleg="mean = " + str(totfract)[:4] 

print strleg_bpix
print strleg_fpix
print strleg

#Mean doesn't mean (haha) a lot for the moment, so let's remove it.
strleg_bpix=""
strleg_fpix=""
strleg=""

runmin=runNumbers[0]
runmax=runNumbers[totruns-1]

trend.GetXaxis().SetRange(1, totruns)
trendBPIXL1.GetXaxis().SetRange(1, totruns)
trendBPIXL2.GetXaxis().SetRange(1, totruns)
trendBPIXL3.GetXaxis().SetRange(1, totruns)
trendBPIXL4.GetXaxis().SetRange(1, totruns)
trendBPIX.GetXaxis().SetRange(1, totruns)
trendFPIXp1.GetXaxis().SetRange(1, totruns)
trendFPIXp2.GetXaxis().SetRange(1, totruns)
trendFPIXp3.GetXaxis().SetRange(1, totruns)
trendFPIXm1.GetXaxis().SetRange(1, totruns)
trendFPIXm2.GetXaxis().SetRange(1, totruns)
trendFPIXm3.GetXaxis().SetRange(1, totruns)
trendFPIX.GetXaxis().SetRange(1, totruns)



trendBPIXL1.GetXaxis().LabelsOption("v")
trendBPIXL2.GetXaxis().LabelsOption("v")
trendBPIXL3.GetXaxis().LabelsOption("v")
trendBPIXL4.GetXaxis().LabelsOption("v")
trendBPIX.GetXaxis().LabelsOption("v")
trendFPIXp1.GetXaxis().LabelsOption("v")
trendFPIXp2.GetXaxis().LabelsOption("v")
trendFPIXp3.GetXaxis().LabelsOption("v")
trendFPIXm1.GetXaxis().LabelsOption("v")
trendFPIXm2.GetXaxis().LabelsOption("v")
trendFPIXm3.GetXaxis().LabelsOption("v")
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

file = TFile(folder+"/Pixel_NoisyColumns_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".root", "RECREATE")


c_Pixel = TCanvas("c_Pixel","c_Pixel",1,1,1800,800)
c_Pixel.SetGridx(True)
c_Pixel.SetGridy(True)




#trend.SetFillColor(4)
SetHRange(trend)
trend.Draw()
Rleg.Draw()
c_Pixel.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsPixel_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_Pixel.Write()

c_BPIX = TCanvas("c_BPIX","c_BPIX",1,1,1800,800)
c_BPIX.SetGridx(True)
c_BPIX.SetGridy(True)



#trendBPIX.SetFillColor(4)
SetHRange(trendBPIX)
trendBPIX.Draw()
Rleg_bpix.Draw()
c_BPIX.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsBPIX_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIX.Write()

c_FPIX = TCanvas("c_FPIX","c_FPIX",1,1,1800,800)
c_FPIX.SetGridx(True)
c_FPIX.SetGridy(True)



#trendFPIX.SetFillColor(4)
SetHRange(trendFPIX)
trendFPIX.Draw()
Rleg_fpix.Draw()
c_FPIX.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsFPIX_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIX.Write()



c_BPIXL1 = TCanvas("c_BPIXL1","c_BPIXL1",1,1,1800,800)
c_BPIXL1.SetGridx(True)
c_BPIXL1.SetGridy(True)




#trendBPIXL1.SetFillColor(4)
SetHRange(trendBPIXL1)
trendBPIXL1.Draw()
c_BPIXL1.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsBPIXL1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL1.Write()


c_BPIXL2 = TCanvas("c_BPIXL2","c_BPIXL2",1,1,1800,800)
c_BPIXL2.SetGridx(True)
c_BPIXL2.SetGridy(True)




#trendBPIXL2.SetFillColor(4)
SetHRange(trendBPIXL2)
trendBPIXL2.Draw()
c_BPIXL2.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsBPIXL2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL2.Write()


c_BPIXL3 = TCanvas("c_BPIXL3","c_BPIXL3",1,1,1800,800)
c_BPIXL3.SetGridx(True)
c_BPIXL3.SetGridy(True)




#trendBPIXL3.SetFillColor(4)
SetHRange(trendBPIXL3)
trendBPIXL3.Draw()
c_BPIXL3.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsBPIXL3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL3.Write()


c_BPIXL4 = TCanvas("c_BPIXL4","c_BPIXL4",1,1,1800,800)
c_BPIXL4.SetGridx(True)
c_BPIXL4.SetGridy(True)




#trendBPIXL4.SetFillColor(4)
SetHRange(trendBPIXL4)
trendBPIXL4.Draw()
c_BPIXL4.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsBPIXL4_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_BPIXL4.Write()


c_FPIXp1 = TCanvas("c_FPIXp1","c_FPIXp1",1,1,1800,800)
c_FPIXp1.SetGridx(True)
c_FPIXp1.SetGridy(True)




#trendFPIXp1.SetFillColor(4)
SetHRange(trendFPIXp1)
trendFPIXp1.Draw()
c_FPIXp1.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsFPIXp1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXp1.Write()


c_FPIXp2 = TCanvas("c_FPIXp2","c_FPIXp2",1,1,1800,800)
c_FPIXp2.SetGridx(True)
c_FPIXp2.SetGridy(True)




#trendFPIXp2.SetFillColor(4)
SetHRange(trendFPIXp2)
trendFPIXp2.Draw()
c_FPIXp2.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsFPIXp2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXp2.Write()

c_FPIXp3 = TCanvas("c_FPIXp3","c_FPIXp3",1,1,1800,800)
c_FPIXp3.SetGridx(True)
c_FPIXp3.SetGridy(True)




#trendFPIXp3.SetFillColor(4)
SetHRange(trendFPIXp3)
trendFPIXp3.Draw()
c_FPIXp3.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsFPIXp3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXp3.Write()


c_FPIXm1 = TCanvas("c_FPIXm1","c_FPIXm1",1,1,1800,800)
c_FPIXm1.SetGridx(True)
c_FPIXm1.SetGridy(True)




#trendFPIXm1.SetFillColor(4)
SetHRange(trendFPIXm1)
trendFPIXm1.Draw()
c_FPIXm1.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsFPIXm1_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXm1.Write()


c_FPIXm2 = TCanvas("c_FPIXm2","c_FPIXm2",1,1,1800,800)
c_FPIXm2.SetGridx(True)
c_FPIXm2.SetGridy(True)




#trendFPIXm2.SetFillColor(4)
SetHRange(trendFPIXm2)
trendFPIXm2.Draw()
c_FPIXm2.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsFPIXm2_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXm2.Write()


c_FPIXm3 = TCanvas("c_FPIXm3","c_FPIXm3",1,1,1800,800)
c_FPIXm3.SetGridx(True)
c_FPIXm3.SetGridy(True)




#trendFPIXm3.SetFillColor(4)
SetHRange(trendFPIXm3)
trendFPIXm3.Draw()
c_FPIXm3.SaveAs(folder+"/Pixel_NoisyColumnsTrends/Pixel_NoisyColumnsFPIXm3_"+str(runmin).strip(' \n')+"_"+str(runmax).strip(' \n')+".png")
c_FPIXm3.Write()


