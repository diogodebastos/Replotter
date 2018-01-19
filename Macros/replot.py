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





    
