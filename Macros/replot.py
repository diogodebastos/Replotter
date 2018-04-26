#!/usr/bin/env python
import defaults # it is important defaults is imported first 
import getplots
import plottools 
import sys
import os

defaults.tdrstyle.setTDRStyle()
plot_styles = defaults.plot_styles

import argparse
parser = argparse.ArgumentParser( description= "Arguments for replotting")
parser.add_argument('--plot_path'       , help='Path to the root file plot')
parser.add_argument('--output_dir'      , help='Output dir for png, pdf, root')
parser.add_argument('--output_name'     , help='Output name. if not give same name as input will be used')
parser.add_argument('--isMVAorCC'       , choices=['mva','cc'] , help='')
parser.add_argument('--opt'        , choices=defaults.plot_options.keys() )

args = parser.parse_args()
plot_path = args.plot_path
output_dir = args.output_dir
plot_options = defaults.plot_options[args.opt] if args.opt else {}

plot_defaults = plot_options.get("defaults",{})
for pdef, pdefval in plot_defaults.items():
    setattr(defaults,pdef,pdefval)

cms_lumi_defaults = plot_options.get("CMS_lumi",{})
for opt, optval in cms_lumi_defaults.items():
    setattr(defaults.CMS_lumi,opt,optval)

def replot( isMVAorCC, plot_path, output_dir, plot_options={}):
    assert isMVAorCC in ['mva','cc']
    
    plot_root_file = os.path.basename( plot_path )
    
    if not plot_root_file.endswith(".root"):
        raise Exception("--plot_path needs to be path to a MVA or CC root file. Instead it was %s"%plot_path)
    plot_name = os.path.splitext( plot_root_file )[0]

    if isMVAorCC=='cc':
        plot_dict = getplots.getCCplot( plot_path )
    if isMVAorCC=='mva':
        plot_dict = getplots.getMVAplot( plot_path )

    data, mc_stack, sig_stack = plot_dict["Data"], plot_dict["mcStack"], plot_dict["sigStack"]
    mc_stack  = getplots.fixHistsStyles( mc_stack  , plot_styles )
    data      = getplots.fixHistsStyles( data      , plot_styles )
    sig_stack = getplots.fixHistsStyles( sig_stack , plot_styles , reorder=False)
    leg       = plottools.makeLegend( data, mc_stack, sig_stack  , nBkgInLeg=defaults.nBkgInLeg , legx=defaults.legx, legy=defaults.legy )
    plot_ret  = plottools.drawNiceDataPlot( data, mc_stack, sig_stack, saveDir=output_dir, name=plot_name , leg=leg , options = plot_options)

    data.SetDirectory(0)
    print data.GetDirectory()
    print plot_dict.values(), leg, plot_ret
    for x in plot_dict.values():
        if hasattr(x, 'SetDirectory'):
            x.SetDirectory(0)
    return (plot_dict, leg, plot_ret)



if __name__ == '__main__':

 
    #output = replot( args.isMVAorCC, args.plot_path, args.output_dir )

    plot_root_file = os.path.basename( plot_path )
    
    if not plot_root_file.endswith(".root"):
        raise Exception("--plot_path needs to be path to a MVA or CC root file. Instead it was %s"%plot_path)
    plot_name = os.path.splitext( plot_root_file )[0] if not args.output_name else args.output_name

    if args.isMVAorCC=='cc':
        plot_dict = getplots.getCCplot( plot_path )
    if args.isMVAorCC=='mva':
        plot_dict = getplots.getMVAplot( plot_path )

    data, mc_stack, sig_stack, mc_tot  = plot_dict["Data"], plot_dict["mcStack"], plot_dict["sigStack"], plot_dict["mcSum"]
    mc_stack  = getplots.fixHistsStyles( mc_stack  , plot_styles )
    data      = getplots.fixHistsStyles( data      , plot_styles )
    sig_stack = getplots.fixHistsStyles( sig_stack , plot_styles , reorder = False)
    leg       = plottools.makeLegend( data, mc_stack, sig_stack  , nBkgInLeg=defaults.nBkgInLeg , legx=defaults.legx, legy=defaults.legy )
    plot_ret  = plottools.drawNiceDataPlot( data, mc_stack, sig_stack, mc_total=mc_tot, saveDir=args.output_dir, name=plot_name , leg=leg, options=plot_options )

    #if plot_options.has_key('objectsToDraw'):
    #    objectsToDraw = plot_options['objectsToDraw']

    if 'CCres' in args.opt:
        #draw lines
        import ROOT
        import numpy as np
        y0 = 0 
        def drawVLine( x, y ,s,w=3):
            l=ROOT.TLine( x,0.01,x,y0+y)
            l.SetLineColor( ROOT.kGray+2) 
            l.SetLineWidth( w ) 
            l.SetLineStyle( s ) 
            l.Draw()
            return l
        
        def drawTLatex( x,y, text, font=42):
            tl = ROOT.TLatex( x,y0+y, text)
            tl.SetTextAlign(23)
            #tl.SetTextFont(12)
            tl.SetTextFont(font)
            tl.SetTextSize(0.04)
            tl.SetTextColor ( ROOT.kBlack)
            #tl.SetTextAngle( 45 )
            tl.Draw()
            return tl

        c,p1,p2 = plot_ret[0]
        #p2.SetBottomMargin(0.4)
        #c.SetBottomMargin(0.4)
        #p2.RedrawAxis()
        #p2.Update()
        p1.cd()
        spaces = [  4,  4,  4,  4,  3,  3   ]
        sizes  = [ 2.5 , 3 , 2.5, 3, 2.5 , 3.5 ]
        #styles = [ 7 , 9 , 7, 9, 7 , 1 ]
        styles = [ 3 , 7 , 3, 7, 3 , 9 ]
        locs   = np.cumsum( spaces*2 )
        ls=[]
        p1.SetTicks(1,0)
        p2.SetTicks(1,0)
        labels = [ "MTa", "", "MTb", "","MTc", "" ]
        #labels = [ "M_{T} < 60 GeV", "", "60 < M_{T} < 95 GeV", "","M_{T} > 95 GeV", "" ]  
        opt1=True
        if opt1:
            labels = [
                   #[ "M_{T}",""]*6 , 
                   #[ "<60 GeV", "", "60-95 GeV", "",">95 GeV" ,""] *2,

                   #[ "SR1a", "", "SR1b", "","SR1c", "" ]  + [ "SR2a", "", "SR2b", "","SR2c", "" ],
                   [ "", "", "SR1", "","" ,""] + [ "", "", "SR2", "","" ,""],
                   [ "M_{T} < 60", "", "60 < M_{T} < 95", ""," M_{T} > 95" ,""] *2,
                  ]
        else:
            labels = [
                   [ "SR1a", "", "SR1b", "","SR1c", "" ]  + [ "SR2a", "", "SR2b", "","SR2c", "" ],
                  ]

        labels += [
                   [ "C_{T1}(X)             ", "C_{T1}(Y)             ", "C_{T1}(X)             ", "C_{T1}(Y)             ","C_{T1}(X)          " ,"C_{T1}(Y)          "] +
                   [ "C_{T2}(X)             ", "C_{T2}(Y)             ", "C_{T2}(X)             ", "C_{T2}(Y)             ","C_{T2}(X)          " ,"C_{T2}(Y)          "] ,
                  ]
        #labels = [  "#splitline{M_{T}}{<60 GeV}" , "" ,
        #            "#splitline{M_{T}}{60-95 GeV}" , "" ,
        #            "#splitline{M_{T}}{>95 GeV}" , "" ,
        #         ]
        
        #loc_size_style= zip( locs, sizes*2, styles*2 , *labels)
        loc_size_style= zip( locs, sizes*2, styles*2 , *labels)
        for vals in loc_size_style[:]:
            if opt1:
                x,y,s,l1,l2,l3 = vals
            else:
                x,y,s,l2,l3 = vals
            y_ =10**(0+y)

            if opt1:
                ls.append( drawTLatex( x, 10**3.65, l1 , 62) ) 
                ls.append( drawTLatex( x, 10**3.27, l2) ) 
                ls.append( drawTLatex( x, 10**2.85, l3) ) 
            else:
                ls.append( drawTLatex( x, 10**3.35, l2, 62) ) 
                ls.append( drawTLatex( x, 10**2.90, l3) ) 
                
            if s and not vals == loc_size_style[-1]:
                ls.append( drawVLine(x,y_,s) ) 
                p2.cd() 
                ls.append( drawVLine(x,2,s) ) 
                p1.cd() 
        output_name = output_dir +"/" + plot_name
        if opt1:
            c.SaveAs(output_name +".png")
            c.SaveAs(output_name +".pdf")
            c.SaveAs(output_name +".root")
        else:
            c.SaveAs(output_name +"_v2.png")
            c.SaveAs(output_name +"_v2.pdf")
            c.SaveAs(output_name +"_v2.root")

