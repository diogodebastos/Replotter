import CMS_lumi
import tdrstyle
import ROOT
##
## Hist Names and Style
##
from copy import deepcopy
import colorsys

    


addMVASysts = True  # Option to include uncertainties from relativeSystematicUncertainties to MVA hists 
    


sigs_to_use = ( 
                (500,490), 
             #  (500,470), 
                (500,420),
              )  ## use these sigs of available 


mvaUncertainty = "syst"



 


error_fill_style = 3013
#error_fill_style = 3144
#ROOT.gStyle.SetHatchesSpacing(0.01)
#ROOT.gStyle.SetHatchesLineWidth(1)

plot_styles = {
               "WJets":        { 'SetFillColor': (0.28, 0.60, 0.90) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'W + jets'},
               "TTbar":        { 'SetFillColor': (0.63, 0.80, 1.00) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'t#bar{t}'},
               "SingleTop":    { 'SetFillColor': (0.56, 0.50, 0.80) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'Single t'},
               "VV":           { 'SetFillColor': (0.25, 0.90, 0.45) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'Diboson'},
               "ZInv":         { 'SetFillColor': (0.13, 1.00, 1.00) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'Z#rightarrow#nu#nu + jets'},
               "DY":           { 'SetFillColor': (0.77, 0.60, 1.00) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'Z/#gamma* + jets'},
               "QCD":          { 'SetFillColor': (0.85, 1.00, 0.40) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'QCD multijet'},
               "TTX":          { 'SetFillColor': (0.55, 0.40, 1.20) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'t#bar{t}X'},
               "Rare":        { 'SetFillColor': (0.13, 1.00, 1.00) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'Rare'},
               "Nonprompt":   { 'SetFillColor': (0.77, 0.60, 1.00) , 'SetLineWidth': 0, 'SetLineStyle': 1 ,'SetTitle':'Nonprompt'},
                } 
    
plot_styles.update( {
               "Data":         { 'SetMarkerSize':0.8, 'SetMarkerStyle':20, 'SETBAADSF':123 , 'SetTitle':'Data'},
                })

sig_colors = {
                (475,465) : ROOT.kRed,
                (500,480) : ROOT.kRed,
                (550,520) : ROOT.kRed,
                (550,510) : ROOT.kRed,
                (525,475) : ROOT.kRed,
                (525,465) : ROOT.kRed,
                (525,455) : ROOT.kRed,
                #(300,270) : 617,
                #(375,365) : 600,
                (500,420) : ROOT.kRed,
                (500,490) : (0.66, 0.8, 1.4),
                #(500,470) : ROOT.kBlue,
             }
#tilde{t}
#sig_label  = "T2tt(%s,%s)"
#sig_label  = "m(#tilde{t}, #tilde{#chi}^{0})=(%s, %s)"
#sig_label  = "m_{#tilde{t}} = %s, m_{#tilde{#chi}^{0}} = %s"
#sig_label  = "m(#tilde{t}) = %s, m(#tilde{#chi}^{0}) = %s"
#sig_label  = "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow b f f' #tilde{#chi}^{0}_{1} (%s,%s)"
#sig_label  = "T2t*t*(%s,%s)"
#sig_label  = "#tilde{t} #rightarrow b f f' #tilde{#chi}^{0}_{1} (%s,%s)"

sig_label  = "#tilde{t}_{1} #rightarrow b f f' #tilde{#chi}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#lower[0.2]{#scale[0.85]{_{1}}}} (%s,%s)"


#
_t2bw=False
if _t2bw:
    stop   = "#tilde{t}_{1}"
    lsp    = "#lower[-0.20]{#tilde{#chi}}#lower[-0.1]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
    #m_stop = "m(%s) [GeV]"%stop
    #chargino = "#lower[-0.2]{#tilde{#chi}}#lower[-0.1]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
    chargino  = "#lower[-0.20]{#tilde{#chi}}#lower[-0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}"
    sig_label = "{stop} #rightarrow {chargino} b, {chargino} #rightarrow f f' {lsp} (%s,%s)".format(stop=stop, antistop=stop, chargino=chargino, lsp=lsp)

for sigmasses, sig_color in sig_colors.items():
    plot_styles[sigmasses] = { 'SetLineColor':sig_color, 'SetLineWidht':2  , 'SetTitle': sig_label%sigmasses }


plot_options = {
                  'mt':  {'xtitle':"M_{T}(l, p_{T}^{miss}) [GeV]",
                          'defaults':{
                                      'legMultiColOffsets' : [ [0.01, 0.06] ],
                                      'xtitle_offset' : 1.1,
                                     }
                          },

                'leppt': {'xtitle':"p_{T}(l) [GeV]",
                          'defaults':{
                                      'bigLeg'   : False,
                                      'legx'     : [0.78 , 0.95 ]       ,
                                      'legy'     : [0.72 , 0.89 ]      ,
                                      'nBkgInLeg':  4                 , 
                                     }
                         },

                'CCres': {
                           'ytitle_r': "Data/pred.",
                           'ymax':1E4,
                           'defaults':{
                                     'xtitle_size': 0.05,
                                     'nBkgInLeg': 4 ,
                                     'hists_order' : ["Rare", "Nonprompt", "TTbar","WJets"],
                                     #'legx':[0.71,  0.91 ],
                                     #'legy':[0.7,  0.89 ],
                                     'legx':[0.8,  1.0 ],
                                     'legy':[0.7,  0.89 ],
                                     'ymin':0.1,
                                     'ratio_range':[0,2.1],

                                     'canvas_width'  :  1300 , 
                                     'canvas_height' :  800 , 

                                     'ytitle_offset' : 0.7,

                                     'xtitle_offset' : 1.0,
                                     'xtitle_r_factor': 0.8 , 
                                     'ytitle_r_offset_factor':1.0,
                                     },
                           'CMS_lumi':{
                                        'cmsTextSize':1.4,
                                       }
                         },
                'BDT': { 
                        'defaults':{
                                    'ratio_range':[0.1,2.1],
                                    'mvaUncertainty':"syst",
                                   }
                },
                'BDTEnv': { 
                         'defaults':{
                                     'ratio_range':[0.1,2.1],
                                     'mvaUncertainty':"env",
                                    }
                },
                'BDTStat': { 
                         'defaults':{
                                     'ratio_range':[0.1,2.1],
                                     'mvaUncertainty':"stat",
                                    }
                },
                'MVAEnv': { 
                         'defaults':{
                                     'mvaUncertainty':"env",
                                    }
                },
                'MVAStat': { 
                         'defaults':{
                                     'mvaUncertainty':"stat",
                                    }
                }
            }


plot_options['CCresT2bW'] = deepcopy( plot_options['CCres'] )
plot_options['CCresT2bW']['defaults'].update({
                                               'legx':[0.8,1.00],
                                               #'legMultiColFact': 0.1
                                             })
plot_options['CCresT2bW']['CMS_lumi'].update({
                                               'writeExtraText':True,
                                               'extraText':'Supplementary',
                                                
                                             })


plot_opt = ""

plot_option = plot_options.get( plot_opt , {} )

##
## Canvas Info
##


canvas_width  =  800
canvas_height =  800

pad1_loc      =  [0, 0.3, 1, 1.0]
pad2_loc      =  [0, 0.00, 1, 0.3]

ymin   = 1

xtitle_size = 0.05#4
xtitle_offset = 1.15

ytitle_r    = "Data#kern[0.6]{/}#kern[0.13]{M}C"
ytitle_size = 0.06
ytitle_offset = 1.0 #1.25

ratio_range = [0.4,1.6]

#xtitle_r_offset_factor = 0.80

#legend

#legx = [0.75,0.93 ]
#legy = [0.75, 0.89 ]
#nBkgInLeg = 4 # determines number of legend columns


## bigger leg
bigLeg = True
legx = [0.72,0.92 ]
legy = [0.55, 0.89 ]
nBkgInLeg = 8 # determines number of legend columns
legMultiColOffsets = [ [0,0], [0.01, 0.1] ]
    
#else:
#    legx = [0.75,0.98 ] 
#    legy = [0.65, 0.89 ] 
#    nBkgInLeg = 6 # determines number of legend columns
#    legMultiColOffsets = [ [0,0], [0,0.6] ]

hists_order = ["TTX", "QCD","DY", "ZInv","VV","SingleTop","TTbar","WJets"]
#hists_order = ["Rare", "Nonprompt", "TTbar","WJets"]


## CMS_Lumi
lumi = 35.9
energy = 13
iPosX  = 11 ## 0: CMS logo outside, 10: CMS logo inside


CMS_lumi.cmsText     = "CMS";
CMS_lumi.cmsTextFont   = 61

CMS_lumi.writeExtraText = False
CMS_lumi.extraText   = "Preliminary"
CMS_lumi.extraOverCmsTextSize = 0.5

#CMS_lumi.extraTextFont = 52

CMS_lumi.lumiTextSize     = 0.6
CMS_lumi.lumiTextOffset   = 0.15

CMS_lumi.cmsTextSize      = 1.2 #0.75
CMS_lumi.cmsTextOffset    = 0.15

CMS_lumi.relPosX    = 0.045
CMS_lumi.relPosY    = 0.035
CMS_lumi.relExtraDY = 1



