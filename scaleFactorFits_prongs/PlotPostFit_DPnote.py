#!/usr/bin/python
import os
import sys

def replace_steer(PathRootFile, PlotName, year):
    PathPlots="/afs/desy.de/user/s/schwarzd/Plots/TopTagging/PostFit_prongs/"+year+"/"
    if year == "2018":
        filename="/nfs/dust/cms/user/schwarzd/SFramePlotter_TopTagging/toptagging_prongs"
    if year == "2017":
        filename="/nfs/dust/cms/user/schwarzd/SFramePlotter_TopTagging/toptagging_prongs_2017"
    if year == "2016":
        filename="/nfs/dust/cms/user/schwarzd/SFramePlotter_TopTagging/toptagging_prongs_2016"
    oldfile = open(filename+".steer",'r')       # open file for read
    newfile = open("toptagging_prongs_temp.steer", 'w') # create new file to write

    pattern1 = "fCycleName"
    pattern2 = "fOutputPsFile"
    for line in oldfile:
        line = line.strip('\r\n')  # it's always a good behave to strip what you read from files

        # if line matches a pattern, replace the line
        if pattern1 in line:
            line = 'fCycleName = "' + PathRootFile+'";'
        if pattern2 in line:
            line = 'fOutputPsFile = "'+PathPlots+PlotName+'.ps";'
        newfile.write(line + '\n')

    # close both files
    oldfile.close()
    newfile.close()

    # now rename file to replace original
    # os.rename(filename+"_temp.steer", filename+".steer")

####### MAIN
year = "2018"
if len(sys.argv) > 1:
    year = sys.argv[1]

PathPlots="/afs/desy.de/user/s/schwarzd/Plots/TopTagging/PostFit_prongs/"+year+"/"
PathRootFile= "/afs/desy.de/user/s/schwarzd/Plots/TopTagging/fitResults_FSR_f_prongs/"+year+"/mass_sub/"
rootname=PathRootFile+"Hists_incl_PUPPI_sys_wp2.root"
plotname="PostFit_incl_PUPPI_sys_wp2"
replace_steer(rootname, plotname, year)
os.system("/nfs/dust/cms/user/schwarzd/SFramePlotter_TopTagging/bin/Plots -f toptagging_prongs_temp.steer")

os.chdir(PathPlots)
os.system("epstopdf PostFit_incl_PUPPI_sys_wp2_Main_Mass_pass.eps")
os.system("epstopdf PostFit_incl_PUPPI_sys_wp2_Main_Mass_fail.eps")
