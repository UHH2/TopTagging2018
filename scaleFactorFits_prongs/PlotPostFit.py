#!/usr/bin/python
import os

def replace_steer(PathRootFile, PlotName):
    PathPlots="/afs/desy.de/user/s/schwarzd/Plots/TopTagging/PostFit_prongs/"
    filename="/nfs/dust/cms/user/schwarzd/SFramePlotter_TopTagging/toptagging_prongs"
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


def write_latex(PathPlots,ptbins_PUPPI, ptbins_HOTVR, jets, uncerts, wps_PUPPI, wps_HOTVR):
    outfile = open(PathPlots+"PostFitLatex.tex","w")
    outfile.write("\\documentclass[aspectratio=169]{beamer}\n")
    outfile.write("\\usepackage[english]{babel}\n")
    outfile.write("\\usepackage{graphicx} \n")
    outfile.write("\\usepackage{epstopdf}\n")
    outfile.write("\\usetheme{Copenhagen}\n")
    outfile.write("\\usecolortheme{beaver}\n")
    outfile.write("\\begin{document}\n")
    for jet in jets:
        if "HOTVR" in jet:
            wps = wps_HOTVR
            ptbins = ptbins_HOTVR
        if "PUPPI" in jet:
            wps = wps_PUPPI
            ptbins = ptbins_PUPPI
        for wp in wps:
            for unc in uncerts:
                # begin new frame
                outfile.write("%--------------------------------------------\n")
                outfile.write("\\begin{frame}\n")
                wpname = wp
                if "_btag" in wpname:
                    wpname = wpname.replace("_btag", " btag")
                outfile.write("\\frametitle{"+jet+", "+wpname+", "+unc+"}\n")
                outfile.write("\\begin{columns}\n")
                plotwidth = 1.0/len(ptbins)
                for pt in ptbins:
                    # first convert eps to pdf
                    filename = "PostFit_"+pt+"_"+jet+"_"+unc+"_"+wp+"_Main_Mass_pass"
                    os.system("epstopdf "+filename+".eps")
                    # 1st figure: pass
                    outfile.write("\\begin{column}{"+str(plotwidth)+"\\textwidth}\n")
                    outfile.write("\\begin{figure}\n")
                    outfile.write("\\includegraphics[width=\\textwidth]{")
                    outfile.write(filename+".pdf")
                    outfile.write("} \n")
                    outfile.write("\\end{figure}\n")
                    # first convert eps to pdf
                    filename = "PostFit_"+pt+"_"+jet+"_"+unc+"_"+wp+"_Main_Mass_fail"
                    os.system("epstopdf "+filename+".eps")
                    # 2nd figure: fail
                    outfile.write("\\begin{figure}\n")
                    outfile.write("\\includegraphics[width=\\textwidth]{")
                    outfile.write(filename+".pdf")
                    outfile.write("} \n")
                    outfile.write("\\end{figure}\n")
                    outfile.write("\\end{column}\n")
                # end frame
                outfile.write("\\end{columns}\n")
                outfile.write("\\end{frame}\n")
    #end document
    outfile.write("\\end{document}")
    outfile.close()



####### MAIN
PathPlots="/afs/desy.de/user/s/schwarzd/Plots/TopTagging/PostFit_prongs/"
PathRootFile= "/afs/desy.de/user/s/schwarzd/Plots/TopTagging/fitResults_FSR_f_prongs/mass_sub/"
ptbins_PUPPI = ["300to400", "400to480", "480to600", "600"]
ptbins_HOTVR = ["200to250", "250to300", "300to400", "400to480", "480to600", "600"]
jets = ["PUPPI", "HOTVR"]
# jets = ["HOTVR"]
# uncerts = ["stat"]
uncerts = ["stat", "sys"]
wps_PUPPI = ["wp1", "wp2", "wp3", "wp4", "wp5", "wp1_btag", "wp2_btag", "wp3_btag", "wp4_btag", "wp5_btag"]
wps_HOTVR = [""]

for jet in jets:
    if "HOTVR" in jet:
        wps = wps_HOTVR
        ptbins = ptbins_HOTVR
    if "PUPPI" in jet:
        wps = wps_PUPPI
        ptbins = ptbins_PUPPI
    for pt in ptbins:
        for unc in uncerts:
            for wp in wps:
                rootname=PathRootFile+"Hists_"+pt+"_"+jet+"_"+unc+"_"+wp+".root"
                plotname="PostFit_"+pt+"_"+jet+"_"+unc+"_"+wp
                replace_steer(rootname, plotname)
                os.system("/nfs/dust/cms/user/schwarzd/SFramePlotter_TopTagging/bin/Plots -f toptagging_prongs_temp.steer")

print "creating latex document..."
os.chdir(PathPlots)
write_latex(PathPlots, ptbins_PUPPI, ptbins_HOTVR, jets, uncerts, wps_PUPPI, wps_HOTVR)
os.system("pdflatex PostFitLatex.tex")
