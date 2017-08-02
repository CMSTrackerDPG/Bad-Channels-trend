#!/usr/bin/env bash

#--------------------------------------------------
# Instructions 
#--------------------------------------------------

if [[ $# -eq 0 ]]; then 
    printf "NAME\n\tBadChannelsTrendProducer.sh - Produce daily and weekly merged bad channels trend\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%-5s\n" "./BadChannelsTrendProducer.sh [OPTION] runlist.txt [DATASET]"
    printf "\nOPTIONS\n" 
    printf "\n\t%-5s  %-40s\n"  "1"  "do 1.1 (cleaning shifter folder) and 1.2 (creating BadChannels Trend)" 
    printf "\n\t%-5s  %-40s\n"  "1.1"  "completely clean up the shifter daily folder (http://vocms061.cern.ch/event_display/tmp/daily_badChannels/)" 
    printf "\n\t%-5s  %-40s\n"  "1.2"  "run 'MergedBadChannelTrendProducer.py' and store it in the shifter daily folder" 
    printf "\n\t%-5s  %-40s\n"  "2"  "copy the daily folder of the shifter in the weekly reports of Bad Channels Trends (Shift Leader only)" 
    printf "\nrunlist.txt\t%-5s (only for step 1.2)\n"
    printf "\n\t%-5s  %-40s\n"  "runlist.txt"  "Update this list with the new runs of the week where the tracker was ON" 
    printf "\nDATASET\t%-5s (only for step 1.2)\n"
    printf "\n\t%-5s  %-40s\n"  "Choose between : StreamExpress, ZeroBias, StreamExpressCosmics and Cosmics" 
    printf "\n\n"
    printf "/!\\ NB: if both runlist.txt and DATASET are not specified, the script will try ALL datasets with the runlist.txt in the current directory /!\\ \n\n"
fi

#--------------------------------------------------
# Reading arguments 
#--------------------------------------------------

step=$1     #variable that stores the step to run

runlist=$2  #variable that stores the address of the runlist to use
if [[ $runlist == "" ]]; then runlist="runlist.txt"; fi #if no option for the runlist is given, then look in the current directory

dataset=$3  #variable that stores the dataset to use

LOOPMODE=0
if [[ $dataset == "" ]]; then LOOPMODE=1; fi #if no dataset is specified, try them all

#--------------------------------------------------
# Global Variables
#--------------------------------------------------
#path variables
PREPATH=/data/users/event_display
DAILYPATH=$PREPATH/tmp/daily_badChannels
WEEKLYPATH=$PREPATH/weekly_badChannels
#arrays
MONTHS=(ZERO January February March April May June July August September October November December)
DATASETS=(StreamExpress ZeroBias StreamExpressCosmics Cosmics)
#Min run and Max run
sort $runlist > sorted_runlist.txt #not deleted right now, we will move it into each results directory and only delete it at the end
RUNMIN=$(sed -n '1p' sorted_runlist.txt)
RUNMAX=$(sed -e '$!d' sorted_runlist.txt)

################################################# STEPS 1.1 and 1.2
#elif [[ $step > 0.999 && $step < 2 ]]; then
if [[ $step > 0.999 && $step < 2 ]]; then
    if [[ $step == 1 || $step == 1.1 ]]; then   #shifter daily folder cleanup
        echo "ALL FILES IN THE DAILY SHIFTER FOLDER WILL BE LOST! [N/y]?"
        read answer
        if [[ $answer == "y" ]]; then
            echo "CLEANING UP..."
            echo "rm -rdf $DAILYPATH/*"
            rm -rdf $DAILYPATH/*
        fi
        printf "CLEANING DONE\n\n"
    fi  #end of step 1.1

    if [[ $step == 1 || $step == 1.2 ]]; then    #run MergedBadChannelTrendProducer
        echo "RUNNING THE SCRIPT BETWEEN RUNS $RUNMIN AND $RUNMAX"
        if [ "$CMSSW_BASE" == "" ]; then
            echo "Please set up a cmsenv (the same as the one used for Tracker maps generation)"
            exit 0
        fi       

        if [[ $LOOPMODE == 0 ]]; then
            echo "./MergedBadComponentsTrendProducer.py $runlist $dataset"
            mkdir -p  MergedBadChannelsTrends
            ./MergedBadChannelTrendProducer.py $runlist $dataset
            mkdir MergedBadChannelsTrends/${dataset}_from${RUNMIN}_to${RUNMAX}
            #the following line moves all the files in the correct directory, without moving directories themselves
            cp sorted_runlist.txt MergedBadChannelsTrends/runlist.txt
            mv MergedBadChannels*.root MergedBadChannelsTrends/.
            find MergedBadChannelsTrends/ -maxdepth 1 -type f -name '[!.]*' -exec mv -n {} MergedBadChannelsTrends/${dataset}_from${RUNMIN}_to${RUNMAX}/ \; 
            cd MergedBadChannelsTrends/${dataset}_from${RUNMIN}_to${RUNMAX}/ 
            perl ../../makeIndexForBadChannels.pl -c 2 -t ${dataset}_from${RUNMIN}_to${RUNMAX} #create the index for the html view
            cd ../..
        elif [[ $LOOPMODE == 1 ]]; then
            mkdir -p  MergedBadChannelsTrends
            echo "FINDING THE RIGHT DATASETS..."
            for eachDataset in "${DATASETS[@]}"
            do
                if nohup ./MergedBadChannelTrendProducer.py $runlist $eachDataset &>/dev/null ; then   #a lot of tricks to avoid having verbose when just testing if this script works
                    echo "./MergedBadComponentsTrendProducer.py $runlist $eachDataset"
                    ./MergedBadChannelTrendProducer.py $runlist $eachDataset
                    mkdir MergedBadChannelsTrends/${eachDataset}_from${RUNMIN}_to${RUNMAX}
                    cp sorted_runlist.txt MergedBadChannelsTrends/runlist.txt
                    mv MergedBadChannels*.root MergedBadChannelsTrends/.
                    find MergedBadChannelsTrends/ -maxdepth 1 -type f -name '[!.]*' -exec mv -n {} MergedBadChannelsTrends/${eachDataset}_from${RUNMIN}_to${RUNMAX}/ \; 
                    cd MergedBadChannelsTrends/${eachDataset}_from${RUNMIN}_to${RUNMAX}/ 
                    perl ../../makeIndexForBadChannels.pl -c 2 -t ${eachDataset}_from${RUNMIN}_to${RUNMAX} #create the index for the html view
                    cd ../..
                    fi
            done
        fi
    
        cp -r MergedBadChannelsTrends/* $DAILYPATH/.
        rm -r MergedBadChannelsTrends
        echo "THE FILES ARE STORED IN $DAILYPATH"
        echo "YOU CAN LOOK AT THEM AT : http://vocms061.cern.ch/event_display/tmp/daily_badChannels"
    
    fi  #end of step 1.2

################################################# STEP 2
elif [[ $step == 2 ]]; then     #copy the daily folder to the weekly folder to store the trends (shift leader)
    echo "CREATING THE WEEKLY TREND OF MERGED BAD CHANNELS"
    now="$(date +'%d/%m/%Y')"
    echo "CREATE THE REPORT FOR THE $now ? [N/y]"   #using automatic date
    read answer
    if [[ $answer == "y" ]]; then
        year="$(date +'%Y')"
        month="$(date +'%m')"
        day="$(date +'%d')"

    else    
        echo "PLEASE ENTER THE YEAR [$(date +'%Y')]"         #using custom date
        read year
        if [[ $year == "" ]]; then year="$(date +'%Y')"; fi    #if nothing is specified, assume the automatic date was ok
        echo "ENTER THE CURRENT MONTH [$(date +'%m')]"
        read month
        if [[ $month == "" ]]; then month="$(date +'%m')"; fi
        echo "ENTER THE CURRENT DAY [$(date +'%d')]"
        read day
        if [[ $day == "" ]]; then day="$(date +'%d')"; fi
        echo "CREATE THE REPORT FOR THE $day/$month/$year ? [N/y]"
        read answer
    fi

    daym1=$((day - 1))
    daym7=$((day - 7))

    if [[ $answer == "y" ]]; then #create the weekly report
        #create the year directory
        mkdir -p $WEEKLYPATH/$year
        #check if the month directory already exist, or create it
        if ls $WEEKLYPATH/$year/${MONTHS[$month]}* 1> /dev/null 2>&1; then
            month_directory="$(ls -d $WEEKLYPATH/$year/${MONTHS[$month]}*/)"   #here we store the actual current name of the month directory
        else
            mkdir $WEEKLYPATH/$year/${MONTHS[$month]}
            month_directory="$WEEKLYPATH/$year/${MONTHS[$month]}/"
        fi
        #check if a report already exist for the day. If it exists, delete it and create a new one. If not, just create a new one
        if ls $month_directory$daym7* 1> /dev/null 2>&1; then
            rm -rf $month_directory$daym7*
        fi
        mkdir $month_directory$daym7 #create the directory
        
        #copy the files from daily to weekly (with the index etc)
        cp -r $DAILYPATH/* $month_directory$daym7/.
        
        #now update the name of the day and month directories so it displays the run numbers contained in them
        #first, start with the days
        cd $month_directory$daym7/
        ls -d */ | grep -E -o "[0-9]+" | sort > ls_tmp.txt #in the directory, find the runmin and runmax
        day_runmin=$(sed -n '1p' ls_tmp.txt)
        day_runmax=$(sed -e '$!d' ls_tmp.txt)
        rm -f ls_tmp.txt
        mv ../$daym7 ../${daym7}_to${daym1}_from${day_runmin}_to${day_runmax}
        cd - 1> /dev/null 2>&1;
        #then do the same for the month directory
        cd $month_directory
        ls -d */ | grep -E -o "[0-9]+" | grep -E '(^|[^0-9])[0-9]{6}($|[^0-9])' |sort > ls_tmp.txt #in the directory find the runmin and runmax (only look at 6-digits numbers)
        month_runmin=$(sed -n '1p' ls_tmp.txt)
        month_runmax=$(sed -e '$!d' ls_tmp.txt)
        rm -f ls_tmp.txt
        if [ $month_directory != "$WEEKLYPATH/$year/${MONTHS[$month]}_from${month_runmin}_to${month_runmax}/" ]; then mv $month_directory $WEEKLYPATH/$year/${MONTHS[$month]}_from${month_runmin}_to${month_runmax} ; fi
        cd - 1> /dev/null 2>&1;
    fi  #end of step 2
        
################################################# UNKNOWN STEP
else    #option not found
    if [[ !($# -eq 0) ]]; then echo "UNKNOWN OPTION"; fi
fi


################################################# CLEANING NON NECESSARY FILES
rm sorted_runlist.txt
