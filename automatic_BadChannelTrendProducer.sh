#!/usr/bin/env bash

if [[ $# -eq 0 ]]; then
    printf "NAME\n\t automatic_BadChannelTrendProducer.sh - Produce merged bad channels trend\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%-5s\n" "./automatic_BadChannelTrendProducer.sh [DETECTOR] [MODES] [OPTIONS]"
    printf "\nDETECTOR\n"
    printf "\n\t%-5s  %-40s\n"  "all"  "produce trends for both SiStrip and Pixel."
    printf "\n\t%-5s  %-40s\n"  "SiStrip"  "produce trends for SiStrip only."
    printf "\n\t%-5s  %-40s\n"  "Pixel"  "produce trends for Pixel only."
    printf "\nMODES\n"
    printf "\n\t%-5s  %-40s\n"  "all"  "produce all the trends for the CURRENT week, month and year."
    printf "\n\t%-5s  %-40s\n"  "week"  "produce the weekly trend"
    printf "\n\t%-5s  %-40s\n"  "month"  "produce the monthly trend for the month in [OPTIONS] (default: current month)"
    printf "\n\t%-5s  %-40s\n"  "year"  "produce the yearly trend for the year in [OPTIONS] (default: current year)"
    printf "\nOPTIONS\t%-5s (only for 'month' and 'year' modes)\n"
    printf "\n\t%-5s  %-40s\n"  "if in 'month' mode"  "add the number of the month (January = 01; February = 02; etc) to be produced"
    printf "\n\t%-5s  %-40s\n"  "if in 'year' mode"  "add the number of the year (2016...)"
    printf "\n\t%-5s  %-40s\n"  ""
    printf "\n\n"
fi

#cosmetics
#WARN="\033[1;33;5;7mWARN\033[0;m"

#dates
now="$(date +'%d/%m/%Y')"
year="$(date +'%Y')"
month="$(date +'%m')"
day="$(date +'%d')"
dayofweek="$(date +'%u')" #1 if Monday, 2 if Tuesday... 7 if Sunday

detector=$1
mode=$2
option=$3

MONTHLIST=" 01 02 03 04 05 06 07 08 09 10 11 12 "
YEARLIST=" 2016 2017 " #FIXME PLEASE UPDATE THIS CHECK LIST TO ALLOW OTHER GENERATION THAN 2016 !! JUST ADD THE WANTED YEAR!! E.G. " 2016 2017 " (the empty spaces are important !!!}
MONTHS=(ZERO January February March April May June July August September October November December)


#--------------------------------------------------
# Every day, produce the daily report for the  the last week + the number of in this week (until yesterday)
#--------------------------------------------------
#Daily-1: Produce the runlist.txt for all datasets for the current days in week + last week
#firstday=$(date -d "-6days-${dayofweek}days" +'%Y-%m-%d') #this is the specific format needed for the run registry

if [ $# -ne 0 ] && [ "$CMSSW_BASE" == "" ]; then
    echo "Please set up a cmsenv (the same as the one used for Tracker maps generation - see instructions)"
    exit 0
fi

if [[ $mode == "all" || $mode == "week" ]]; then

    echo "Cleaning old runlists..."
    rm runlist_*.txt    
    rm list_missingTrackerMap_*.txt

    firstday=$(date -d "-7days" +'%Y-%m-%d') #this is the specific format needed for the run registry
    lastday=$(date +'%Y-%m-%d') 
    if [[ $detector == "all" || $detector == "SiStrip" ]]; then
        python listRuns16_SiStrip.py --daymin $firstday --daymax $lastday
    fi
    if [[ $detector == "all" || $detector == "Pixel" ]]; then
        python listRuns16_Pixel.py --daymin $firstday --daymax $lastday
    fi

    find -type f -empty -delete #remove empty files
    if ! ls runlist_*.txt 1> /dev/null 2>&1; then
        echo "No runs in this time period - the weekly directory on vocms061 wil be empty"
        mkdir -p /data/users/event_display/MergedBadChannels
        mkdir -p /data/users/event_display/MergedBadChannels/$year
        mkdir -p /data/users/event_display/MergedBadChannels/$year/Weekly
        #if [[ $detector == "all" || $detector == "SiStrip" ]] ; then mkdir -p /data/users/event_display/MergedBadChannels/$year/Weekly/SiStrip ; fi
        #if [[ $detector == "all" || $detector == "Pixel" ]] ; then mkdir -p /data/users/event_display/MergedBadChannels/$year/Weekly/Pixel ; fi
        if [[ $detector == "all" || $detector == "SiStrip" ]] ; then rm -rf /data/users/event_display/MergedBadChannels/$year/Weekly/SiStrip/ ; fi
        if [[ $detector == "all" || $detector == "Pixel" ]] ; then rm -rf /data/users/event_display/MergedBadChannels/$year/Weekly/Pixel/ ; fi
        exit 0
    fi

    ls runlist_*.txt > ls.txt
    read -a runlists -d '\n' < ls.txt
    rm -f ls.txt
    echo "Step 1 done"
    #Daily-2: produce it in the daily report
    sh BadChannelTrendProducer_automaticYes.sh 1.1 #clean the daily reports
    echo "Cleaning done"
    for eachRunlist in "${runlists[@]}"
    do
        if [[ $eachRunlist == *"StreamExpressCosmics"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpressCosmics"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpressCosmics
        elif [[ $eachRunlist ==  *"Cosmics"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist Cosmics"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist Cosmics
        elif [[ $eachRunlist == *"StreamExpress"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpress"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpress
        elif [[ $eachRunlist == *"ZeroBias"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist ZeroBias1"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist ZeroBias1
        fi
    done

    #moving from tmp to the weekly
    mkdir -p /data/users/event_display/MergedBadChannels
    mkdir -p /data/users/event_display/MergedBadChannels/$year
    mkdir -p /data/users/event_display/MergedBadChannels/$year/Weekly
    if [[ $detector == "all" || $detector == "SiStrip" ]] ; then rm -rf /data/users/event_display/MergedBadChannels/$year/Weekly/SiStrip/ ; fi
    if [[ $detector == "all" || $detector == "Pixel" ]] ; then rm -rf /data/users/event_display/MergedBadChannels/$year/Weekly/Pixel/ ; fi
    cp -r /data/users/event_display/tmp/daily_badChannels/* /data/users/event_display/MergedBadChannels/$year/Weekly/.

fi
if [[ $mode == "all" || $mode == "month" ]]; then

    if [[ $option == "" ]]; then
        monthOption=$month
    elif [[ $MONTHLIST == *" $option "* ]]; then
        monthOption=$option
    else
        echo "Not a correct month number - should be 01 or 02 or... 12 (the 0 matters)"
        exit 0
    fi
    monthOptionIndex=$((10#$monthOption)) #The number entered (01, 04...) starts with a 0. This is (unfortunatly) the bash convention to write octal numbers. This line is therefore here to convert those numbers in decimal numbers.
#    echo "mode= $mode"
#    echo "option= $option"
#    echo "monthOption= $monthOption"
#    echo "monthOptionIndex"

    echo "Cleaning old runlists..."
    rm runlist_*.txt
    rm list_missingTrackerMap_*.txt
 
    firstday="${year}-${monthOption}-01"
    lastday=$(date -d "$firstday +1month -1day" +'%Y-%m-%d') #the daily report produces the trend for the last week + everything in the current week until yesterday
    if [[ $detector == "all" || $detector == "SiStrip" ]]; then
        python listRuns16_SiStrip.py --daymin $firstday --daymax $lastday
    fi
    if [[ $detector == "all" || $detector == "Pixel" ]]; then
        python listRuns16_Pixel.py --daymin $firstday --daymax $lastday
    fi


    find -type f -empty -delete #remove empty files
    if ! ls runlist_*.txt 1> /dev/null 2>&1; then
        echo "No runs in this time period"
        exit 0
    fi

    ls runlist_*.txt > ls.txt
    read -a runlists -d '\n' < ls.txt
    rm -f ls.txt

    #Daily-2: produce it in the daily report
    sh BadChannelTrendProducer_automaticYes.sh 1.1 #clean the daily reports
    for eachRunlist in "${runlists[@]}"
    do
        if [[ $eachRunlist == *"StreamExpressCosmics"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpressCosmics"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpressCosmics
        elif [[ $eachRunlist ==  *"Cosmics"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist Cosmics"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist Cosmics
        elif [[ $eachRunlist == *"StreamExpress"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpress"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpress
        elif [[ $eachRunlist == *"ZeroBias"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist ZeroBias1"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist ZeroBias1
        fi
    done

    #moving from tmp to the weekly
    mkdir -p /data/users/event_display/MergedBadChannels
    mkdir -p /data/users/event_display/MergedBadChannels/$year
    mkdir -p /data/users/event_display/MergedBadChannels/$year/${monthOption}_${MONTHS[${monthOptionIndex}]}/
    if [[ $detector == "all" || $detector == "SiStrip" ]]; then rm -rf /data/users/event_display/MergedBadChannels/$year/${monthOption}_${MONTHS[${monthOptionIndex}]}/SiStrip ; fi
    if [[ $detector == "all" || $detector == "Pixel" ]]; then rm -rf /data/users/event_display/MergedBadChannels/$year/${monthOption}_${MONTHS[${monthOptionIndex}]}/Pixel ; fi
    cp -r /data/users/event_display/tmp/daily_badChannels/* /data/users/event_display/MergedBadChannels/$year/${monthOption}_${MONTHS[${monthOptionIndex}]}/.

fi
if [[ $mode == "all" || $mode == "year" ]]; then

    if [[ $option == "" ]]; then
        yearOption=$year

    elif [[ $YEARLIST == *" $option "* ]]; then
        yearOption=$option
    else
        echo "Not a correct year number, the authorized years are : $YEARLIST "
        exit 0
    fi

    echo "Cleaning old runlists..."
    rm runlist_*.txt
    rm list_missingTrackerMap_*.txt
 
    firstday="${yearOption}-01-01"
    #lastday=$(date +'%Y-%m-%d') 
    lastday="${yearOption}-12-31"
    if [[ $detector == "all" || $detector == "SiStrip" ]]; then
        python listRuns16_SiStrip.py --daymin $firstday --daymax $lastday
    fi
    if [[ $detector == "all" || $detector == "Pixel" ]]; then
        python listRuns16_Pixel.py --daymin $firstday --daymax $lastday
    fi



    find -type f -empty -delete #remove empty files
    if ! ls runlist_*.txt 1> /dev/null 2>&1; then
        echo "No runs in this time period"
        exit 0
    fi

    ls runlist_*.txt > ls.txt
    read -a runlists -d '\n' < ls.txt
    rm -f ls.txt

    #Daily-2: produce it in the daily report
    sh BadChannelTrendProducer_automaticYes.sh 1.1 #clean the daily reports
    for eachRunlist in "${runlists[@]}"
    do
        if [[ $eachRunlist == *"StreamExpressCosmics"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpressCosmics"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpressCosmics
        elif [[ $eachRunlist ==  *"Cosmics"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist Cosmics"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist Cosmics
        elif [[ $eachRunlist == *"StreamExpress"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpress"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist StreamExpress
        elif [[ $eachRunlist == *"ZeroBias"* ]]; then
            echo "sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist ZeroBias1"
            sh BadChannelTrendProducer_automaticYes.sh 1.2 $eachRunlist ZeroBias1
        fi
    done

    #moving from tmp to the weekly
    mkdir -p /data/users/event_display/MergedBadChannels
    mkdir -p /data/users/event_display/MergedBadChannels/$yearOption
    mkdir -p /data/users/event_display/MergedBadChannels/$yearOption/Summary/
    if [[ $detector == "all" || $detector == "SiStrip" ]]; then rm -rf /data/users/event_display/MergedBadChannels/$yearOption/Summary/SiStrip ; fi
    if [[ $detector == "all" || $detector == "Pixel" ]]; then rm -rf /data/users/event_display/MergedBadChannels/$yearOption/Summary/Pixel ; fi
    cp -r /data/users/event_display/tmp/daily_badChannels/* /data/users/event_display/MergedBadChannels/$yearOption/Summary/.

fi


# Log of the missing tracker maps
if [[ $# -ne 0 ]]; then
    if ls list_missingTrackerMap_*.txt 1> /dev/null 2>&1; then
        #echo "$WARN WARNING : Some tracker maps are missing"
        echo "WARNING : Some tracker maps are missing"
        echo "WARNING : Please check list_missingTrackerMap_*.txt and produce those tracker maps. Then reload this script."
        echo "WARNING : Please note that the list named as 'ZeroBias1' contains the datasets ZeroBias, ZeroBias1 and PAMinimumBias1."
        echo "WARNING : Identically, the StreamExpress datasets contains also the StreamExpressPA dataset."
    fi
fi
