import defaults
import getplots

def getPlotOption( plot_path ):
    import os
    pname = os.path.basename(plot_path)
    tags = [tag for tag in defaults.plot_options.keys() if tag in pname.lower()]
    bdtplot = re.findall(r"DeltaM\d\d",plot_path)
    if tags:
        assert len(tags)==1, "Not sure which plot option to use for %s, %s"%(pname, default.plot_options )
        return " --opt=%s "%tags[0]
    elif bdtplot:
        assert len(bdtplot)==1
        dm = bdtplot[0].replace("DeltaM","DM")
        return "  --opt=%s "%dm
    elif "fit_b" in pname:
        sigtag_ = 'T2bW' if 'T2bW' in pname else ''
        return " --opt=CCres%s "%sigtag_
    else:
        return ""

def runFuncInParal( func, args , nProc = 15 ):
    import multiprocessing 
    #nProc=1
    if nProc >1:
        pool         =   multiprocessing.Pool( processes = nProc )
        results      =   pool.map( func , args)
        pool.close()
        pool.join()
    else:
        results = map(func,args)
    return results

if __name__=='__main__':

    cc_plots_dir  = "/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/8025_mAODv2_v7/80X_postProcessing_v1/EPS17_v0/ForPaper_v5/LepGood_lep_lowpt_Jet_def_SF_STXSECFIX_PU_TTIsr_Wpt_TrigEff_lepSFFix/DataBlind/presel/extras/"
    mva_plots_dir = "/afs/cern.ch/user/c/cbeiraod/public/Stop4Body/temp/"
    output_dir    = "/afs/hephy.at/user/n/nrad/www/SUS17005/forFR/"
    #output_dir    = "/afs/hephy.at/user/n/nrad/www/ForPaper/"
    #output_dir    = "/afs/hephy.at/user/n/nrad/www/SUS17005/forPAS/"
    
    import glob
    import os
    import re    

    cc_plots  = glob.glob(cc_plots_dir+"/*.root")
    mva_plots = glob.glob(mva_plots_dir +"/*.root")
    mva_plots += glob.glob( mva_plots_dir +"/Delta*/*.root")
    cc_plots  += glob.glob("./new_plots/fit_b_WithSigs.root") 
    cc_plots  += glob.glob("./new_plots/fit_b_WithSigs_T2bW.root") 
    
    command_tmp = "python replot/replot.py --isMVAorCC=%s --plot_path=%s --output_dir=%s"
    
    commands = []
    mva_plots = []
    #cc_plots = cc_plots[-1:]

    for plt in cc_plots:
        if not ("leppt.root" in plt.lower() or "Lepmt.root" in plt or 'fit_b_' in plt): continue
        plot_option = getPlotOption(plt) 
        command = command_tmp%("cc", plt, output_dir +"/CC/" ) + plot_option
        commands.append(command)
    
    for plt in mva_plots:
        plot_option = getPlotOption(plt) 
        deltam = re.findall(r"DeltaM\d\d",plt)
        if deltam:
            deltam = deltam[0].replace("DeltaM","_DM")
        else: 
            deltam = ""
        pltname = os.path.basename(plt)[:-5] 
        pltname = pltname.replace("_syncPlot","").replace("PreselectionMVA","PreselMVA_") + deltam 
        #pltname = pltnmae.replace("_highDM_","").replace("_lowDM_","")
        command = command_tmp%("mva", plt, output_dir +"/MVA/" ) +plot_option +" --output_name=%s"%pltname
        commands.append(command)
    
    
    for c in commands:
        print c
    #runFuncInParal( os.system, commands )
    
    
    

