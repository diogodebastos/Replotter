import glob
import os
import ROOT
import plottools
from replot import defaults
import colorsys

sigs_to_use = defaults.sigs_to_use #( (500,490), (500,470), (500,420) )
mvaUncertainty = defaults.mvaUncertainty

def getSigMasses( signame ):
    import re
    masses = re.findall(".*(\d\d\d).*(\d\d\d).*", signame)
    if masses:
        return tuple([int(x) for x in masses[0]])
    else:
        return False



def getMVAplot( root_file):
    tf = ROOT.TFile(root_file)
    hists = dict(   [ (x.GetName(), getattr(tf, x.GetName())) for x in tf.GetListOfKeys()] )
    hists['sigStack'] = ROOT.THStack("sigStack","sigStack")
    sig_hists    = [h for h in hists.values() if getSigMasses(h.GetTitle()) ]
    sigs_to_use_ = [ h for h in sig_hists if getSigMasses(h.GetTitle()) in sigs_to_use ]
    #hists['mcError'] = hists['']
    hists['mcSum_orig'] = hists['mcSum'].Clone()
    if mvaUncertainty == "syst" or mvaUncertainty == "env":
      if mvaUncertainty == "syst":
        mc_err_atone   = hists['relativeSystematicUncertainties'].Clone()
      else:
        mc_err_atone   = hists['relativeSystematicUncertaintiesEnvelope'].Clone()
      hists['mcSum'].Sumw2()
      mc_err_atone.Sumw2()
      for ib in range( 1,mc_err_atone.GetNbinsX()+1 ):
        mc_err_atone.SetBinContent(ib,1)

      if getattr(defaults, "addMVASysts", True ) :
        hists['mcSum'] = hists['mcSum'] * mc_err_atone

    if not sigs_to_use_:
        sigs_to_use_ = sig_hists

    for htitle,h in hists.items(): 
        #print htitle, h.GetName()
        try:
            h.SetDirectory(0)
        except:
            pass
    for sig_hist in sigs_to_use_:
        hists['sigStack'].Add( sig_hist )
    return hists

def fixHistStyle( hist, plot_styles ):
    MVA_name_map  ={
                     'DY + Jets': 'DY',
                     'Multiboson': 'VV',
                     'Multijet': 'QCD',
                     'Single Top': 'SingleTop',
                     'W + Jets': 'WJets',
                     'Z(#nu#nu) + jets': 'ZInv',
                     't#bar{t}': 'TTbar',
                     't#bar{t}X': 'TTX' , 
                     'Data'     :  'Data', 
                  }
    #MVA_name_map  ={'DYJets': 'DY',
    #               'QCD': 'QCD',
    #               'SingleTop': 'SingleTop',
    #               'VV': 'VV',
    #               'WJets': 'WJets',
    #               'ZInv': 'ZInv',
    #               'ttbar_lep': 'TTbar',
    #               'ttx': 'TTX'}
    CC_name_map = {
                    'ttX':                       'TTX',
                    'VV':                        'VV',
                    'QCD':                       'QCD',
                    'Singletop':                 'SingleTop',
                    'Zrightarrownunu+jets':      'ZInv',
                    'Zgamma*+jets':              'DY',
                    'TT':                        'TTbar',
                    #'TTJets':                    'TTbar',
                    #'TT_1l':                     'TTbar',
                    #'TT_2l':                     'TTbar',
                    'WJets':                     'WJets',
                "DataBlind":                     "Data" , 

                    'data' :                    "Data",
                    "Others":                   "Rare", 
                "Fakes":                        "Nonprompt",
                    

                  }
    import re
    hname    = hist.GetName()
    htitle   = hist.GetTitle()
    isSignal = getSigMasses(hname)#re.findall(".*(\d\d\d).*(\d\d\d).*", hname)
    #isCCplot = re.findall( r"(.*?)_presel_.*", hname ) 
    isCCplot = [x for x in CC_name_map if x in hname]
    #print hname, htitle, isCCplot
    if isCCplot:
        assert len(isCCplot)==1, isCCplot
        new_name = CC_name_map.get( isCCplot[0] , None )
        if new_name : hist.SetName(new_name)
    elif isSignal:
        masses   = isSignal
        new_name = masses #"s_%s_%s"%masses
        if new_name : hist.SetName("s_%s_%s"%masses)
        if not new_name in plot_styles:
            hist.SetTitle( defaults.sig_label%masses )
    else:
        new_name = MVA_name_map.get( htitle , None)
        if new_name : hist.SetName( new_name)
    #hist.SetTitle(new_name)
    plot_info = plot_styles.get(new_name,{})
    if not plot_info:
        print "##################### no plot info found for plot:", hname, htitle, new_name
    for opt, optval in plot_info.items():
        if hasattr( hist, opt):
            if 'color' in opt.lower():
                if isinstance( optval, (tuple,list) ):
                    optval = ROOT.TColor.GetColor( * colorsys.hsv_to_rgb( *optval) )
                if isinstance( optval, str ) and optval.startswith("#"):
                    optval = ROOT.TColor.GetColor( optval )
            getattr(hist,opt)(optval)



def fixHistsStyles( stack, plot_styles, reorder = True):
    hists = stack.GetHists() if isinstance( stack, ROOT.THStack ) else ( stack if isinstance(stack,(list,tuple)) else [stack])
    for h in hists:
        fixHistStyle( h, plot_styles)
        #print h.GetTitle()
    #orderfunc = lambda h: h.Integral()
    #new_stack = stack
    new_stack = reorderStack( stack , key = lambda h: defaults.hists_order.index(h.GetName()) ) if reorder else stack
    #order = ["QCD", "TTX","ZInv","VV","SingleTop","DY","TTbar","WJets"]
    #new_hists  = sorted( mc_stack.GetHists() ,  key=lambda h: order.index( h.GetName() ) )
    #new_stack = ROOT.THStack("mcStack", "mcStack")
    #for h in new_hists: new_stack.Add(h)
    return new_stack


def niceRegionName(r):
    ret = r.replace("sr","SR").replace("cr","CR").replace("vl","VL").replace("l","L").replace("v","V").replace("h","H").replace("m","M")
    if "VL" in ret:
        ret = "VL"#"[3.5-5)"
    elif "L" in ret:
        ret = "L"#"[5-12)"
    elif "M" in ret:
        ret = "M"#"[12-20)"
    elif "H" in ret:
        ret = "H"#"[20-30)"
    return ret



def getCCplot( root_file ) :
    #print "\n\n " , root_file
    filename = os.path.basename( root_file )
    basename = os.path.splitext( filename )[0]
    tf = ROOT.TFile(root_file)    
    first_key = tf.GetListOfKeys()[0].GetName()
    canv = getattr(tf, first_key)
    if not isinstance( canv, ROOT.TCanvas): raise Exception("Canvas not found.. instead got this (%s)"%canv)
    pads = plottools.getCanvPrims( canv ) 
    hists = []
    hists = map( plottools.getCanvPrims , pads ) 
    objs = {
            "mcStack" :  hists[0][1].Clone("mcStack"),
            "mc_err"   :  hists[0][2].Clone("mc_err"),
            "Data"     :  hists[0][3].Clone(),
            "sigStack_":  hists[0][4].Clone("sigStack_"),
           }
    #print objs
    for o in objs.values():
        if hasattr(o,"SetDirectory") :
            o.SetDirectory(0)
    
    hists = objs['mcStack']
    mc_stack = ROOT.THStack("mcStack",'mcStack')
    first = False
    for h in hists:
        hname = h.GetName()
        if "TT_" in hname:
            if not first:
                first = h
                first.SetName( hname.replace("TT_1l_","TT_").replace("TT_2l_","TT_") )
            else:
                first.Add(h)
                mc_stack.Add( first )
        else:
            mc_stack.Add( h ) 
    objs['mcStack'] = mc_stack
    objs['mcSum'] = plottools.getStackTot( objs["mcStack"] )
    mc_total = objs['mcSum']

    if 'fit_' in root_file:
        for i in range(1, mc_total.GetNbinsX()+1):
            mc_total.GetXaxis().SetBinLabel( i , niceRegionName(mc_total.GetXaxis().GetBinLabel(i)) )
            mc_total.GetXaxis().LabelsOption("H")
            #mc_total.GetXaxis().SetTitle("p_{T}(l) [GeV]")
            mc_total.GetXaxis().SetTitle("p_{T}(l) Category")

    sig_stack_all = objs['sigStack_']
    
    sighists = [h for h in sig_stack_all.GetHists() if getSigMasses(h.GetName()) in sigs_to_use  ]
    if len(sighists) == len(sigs_to_use):
        sig_stack = ROOT.THStack("sigStack","sigStack")
        for h in sorted( sighists, key=lambda x:x.GetName() , reverse = True):
            sig_stack.Add(h)
        objs['sigStack']=sig_stack
    else:
        objs['sigStack'] = objs['sigStack'].Clone('sigStack')
        

    

    
    



    #print objs
    return objs




def reorderStack( stack, key = lambda h: h.Integral(), reverse=False):
    if not isinstance(stack, ROOT.THStack):
        return stack
    new_hists = sorted( stack.GetHists() ,  key=key, reverse=reverse )
    new_stack = ROOT.THStack(stack.GetName(), stack.GetTitle())
    for h in new_hists: new_stack.Add(h)
    return new_stack



print defaults.plot_opt
print defaults.plot_option

if __name__=='__main__' and False:

    plots_dir = "trunk/plots"
    output_dir = "plots2/"
    CC_plots_dir = os.path.join( plots_dir, "CC" )
    
    CC_plots =  glob.glob( CC_plots_dir +"/presel_*.root" )

    root_file = CC_plots[0]
    
    ret = map( getCCplot , CC_plots )
    print ret
    
    cc_plot_name = "LepPt"
    cc_plot_path = "trunk/plots/CC/presel_LepPt.root"
    print cc_plot_path
    cc_plot = getCCplot( cc_plot_path )
    data, mc_stack, sig_stack = cc_plot["Data"], cc_plot["mcStack"], cc_plot["sigStack"]
    mc_stack = fixHistsStyles( mc_stack, plot_styles )
    mc_stack.SetMinimum(0.1)
    cc_plot_ret = plottools.drawNiceDataPlot( data, mc_stack, sig_stack, saveDir="./output/", name=cc_plot_name )



