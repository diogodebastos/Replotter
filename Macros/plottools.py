import os
import ROOT
from replot import defaults




def getStackTot(stack):
    mc_hist = stack.GetHists().Last().Clone(stack.GetName()+"_tot_"  )
    mc_hist.Reset()
    mc_hist.Merge( stack.GetHists() )
    mc_hist.SetDirectory(0)
    return mc_hist




def getHistMax(hist):
  nBinX = hist.GetNbinsX()
  histMax= max( [(x,hist.GetBinContent(x)) for x in range(1, nBinX+1)] , key= lambda f: f[1] )
  return histMax

def getHistMin(hist,onlyPos=False):
  nBinX = hist.GetNbinsX()
  binContents = [ (x, hist.GetBinContent(x) ) for x in range(1, nBinX+1)]
  if onlyPos:
    binContents=filter( lambda x: x[1]>0, binContents )
  ret = min( binContents , key= lambda f: f[1] ) if binContents else [0,0]
  return ret


def makeLegendFromHists( hists, name="Legend", loc=[] , opt='f'):
    leg = ROOT.TLegend( *loc)
    leg.SetName(name)
    leg.SetFillColorAlpha(0,0.001)
    leg.SetBorderSize(0)
    for h in hists:
        opt_ = getattr(h,"legopt", opt) 
        leg.AddEntry( h, "#font[42]{%s}"%h.GetTitle(), opt_)
    return leg 


#def makeLegend( data=None, mc_stack=None, sig_stack=None, leg_location=None , nBkgInLeg=None, legx=[0.75, 0.95 ], legy=[0.7, 0.87 ]):
#    mc_hists   = list( reversed( mc_stack.GetHists() ) ) if mc_stack else None
#    data_hists = [data] if data else []
#    sig_hists  = list( sig_stack.GetHists() ) if isinstance( sig_stack, ROOT.THStack) else [sig_stack]
#    hists  = mc_hists + sig_hists + data_hists
#    nhists = len(hists)
#    from math import ceil
#    nBkgInLeg = nBkgInLeg if nBkgInLeg else nhists
#    nhists_   = nBkgInLeg * int( ceil(1.*nhists/nBkgInLeg) )
#    legx=legx[:]
#    legs=[]
#    legy_dens = (legy[1]-legy[0]) / float(nBkgInLeg)
#    if mc_hists:
#        subBkgLists = [ hists[x:x+nBkgInLeg] for x in range(0, nhists , nBkgInLeg) ]
#        #print subBkgLists
#        nBkgLegs = len(subBkgLists)
#        for i , subBkgList in enumerate( subBkgLists ):
#            legloc = [legx[0], legy[1]- len(subBkgList)*legy_dens  ,legx[1],legy[1]]
#            bkgLeg = makeLegendFromHists( [h for h in subBkgList if h in mc_hists], name='leg_%s'%i , loc = legloc )# [legx[0], newLegY0 ,legx[1],legy[1]] )
#            #print "==========================================================================="
#            #print bkgLeg, subBkgList, "\n" , legloc #[legx[0], newLegY0  , legx[1],legy[1]]
#            #print "==========================================================================="
#            legs.append(bkgLeg)
#            #legx = [ 2*legx[0] -legx[1] , legx[0]  ]
#            dx   = legx[1]-legx[0]
#            legx = [ legx[0]-1.*dx , legx[1]-dx  ]
#    if sig_stack:
#        for sig in sig_hists:
#            bkgLeg.AddEntry(sig, sig.GetTitle(), 'l')
#    if data:
#        bkgLeg.AddEntry( data, data.GetTitle(), 'lp')
#    return legs


def makeLegend( data=None, mc_stack=None, sig_stack=None, leg_location=None , nBkgInLeg=None, legx=[0.75, 0.95 ], legy=[0.7, 0.87 ]):
    mc_hists   = list( reversed( mc_stack.GetHists() ) ) if mc_stack else None
    data_hists = [data] if data else []
    sig_hists  = list( sig_stack.GetHists() ) if isinstance( sig_stack, ROOT.THStack) else [sig_stack]
    #hists  = data_hists + mc_hists + sig_hists #+ data_hists
    hists  = mc_hists + data_hists + sig_hists #+ data_hists
    #if defaults.bigLeg:
    #    hists  = mc_hists + data_hists + sig_hists #+ data_hists
    #else:
    #    hists  = data_hists + mc_hists + sig_hists #+ data_hists
    nhists = len(hists)
    from math import ceil
    nBkgInLeg = nBkgInLeg if nBkgInLeg else nhists
    nhists_   = nBkgInLeg * int( ceil(1.*nhists/nBkgInLeg) )
    legx=legx[:]
    legs=[]
    legy_dens = (legy[1]-legy[0]) / float(nBkgInLeg)
    for h in mc_hists:
        h.legopt='f'
    for h in sig_hists:
        h.legopt='l'
    for h in data_hists:
        h.legopt='ep'
    if mc_hists:
        subBkgLists = [ hists[x:x+nBkgInLeg] for x in range(0, nhists , nBkgInLeg) ]
        #print subBkgLists
        nBkgLegs = len(subBkgLists)
        isLastCol = False
        for i , subBkgList in enumerate( subBkgLists ):
            legloc = [legx[0], legy[1]- len(subBkgList)*legy_dens  ,legx[1],legy[1]]
            #bkgLeg = makeLegendFromHists( [h for h in subBkgList if h in mc_hists], name='leg_%s'%i , loc = legloc )# [legx[0], newLegY0 ,legx[1],legy[1]] )
            bkgLeg = makeLegendFromHists( subBkgList, name='leg_%s'%i , loc = legloc )# [legx[0], newLegY0 ,legx[1],legy[1]] )
            #print "==========================================================================="
            #print bkgLeg, subBkgList, "\n" , legloc #[legx[0], newLegY0  , legx[1],legy[1]]
            #print "==========================================================================="
            bkgLeg.SetMargin(0.2)
            if isLastCol:
                bkgLeg.SetMargin(0.15)
            legs.append(bkgLeg)
            #legx = [ 2*legx[0] -legx[1] , legx[0]  ]
            if isLastCol: 
                break
            isLastCol = i == len(subBkgLists)-2
            dx   = legx[1]-legx[0]
            #f__   = 0.08 if defaults.bigLeg else (isLastCol)*0.1
            #f_   = getattr(defaults, 'legMultiColFact', f__ )
            offsets = getattr( defaults, 'legMultiColOffsets', False )
            if not offsets:
                offset1, offset2 = [0,0]
            else:
                offset1, offset2 = offsets[i]
                
            print offset1,offset2, isLastCol
            legx = [ legx[0] - dx - offset2 , legx[1] - dx -offset1  ]
            print legx
    #if sig_stack:
    #    for sig in sig_hists:
    #        bkgLeg.AddEntry(sig, sig.GetTitle(), 'l')
    #if data:
    #    bkgLeg.AddEntry( data, data.GetTitle(), 'lp')
    return legs


def makeCanvasPads(    c1Name="canvas",  c1ww=defaults.canvas_width, c1wh=defaults.canvas_height,
                       p1Name="pad1", p1M=defaults.pad1_loc , p1Gridx=False, p1Gridy=False,
                       p2Name="pad2", p2M=defaults.pad2_loc, p2Gridx=False, p2Gridy=False,
                       joinPads=True,
                       func=None
                    ):
  c = ROOT.TCanvas(c1Name,c1Name,c1ww,c1wh)

  pad1 = ROOT.TPad(p1Name, p1Name, *p1M)
  pad1.SetBottomMargin(0)  # joins upper and lower plot
  if p1Gridx: pad1.SetGridx()
  if p1Gridy: pad1.SetGridy()

  # Lower ratio plot is pad2
  c.cd()  # returns to main canvas before defining pad2
  pad2 = ROOT.TPad(p2Name, p2Name, *p2M)

  if joinPads: pad2.SetTopMargin(0)  # joins upper and lower plot
  pad2.SetBottomMargin(0.3)
  if p2Gridx: pad2.SetGridx()
  if p2Gridy: pad2.SetGridy()
  if func:
    func(pad1,pad2)
  pad1.Draw()
  pad2.Draw()
  return c, pad1, pad2

#def drawCMSHeader( preliminary = "", lumi = 35.9, lxy = [0.16,0.915], rxy=[0.77,0.915], textR="%0.1f fb^{-1} (13 TeV)", cmsinside=True):
#    isPaper = preliminary.lower() in ['paper','']
#    latex = ROOT.TLatex()
#    latex.SetNDC()
#    latex.SetTextSize(0.04)
#    font=52
#    latex.SetTextFont(font)
#    #latexTextL = "#font[%s]{CMS %s}"%(font, preliminary)
#    #latexTextL = "CMS %s"%(preliminary)
#    cmstextsize = 0.08 if isPaper else 0.06
#    cmstext = "#font[61]{CMS}"
#    if not cmsinside:
#        latexTextL = cmstext
#        if preliminary:
#            latexTextL += "  #font[%s]{%s}"%(font,preliminary)
#        latex.DrawLatex(lxy[0],lxy[1],  latexTextL)
#    else:
#        textCMSlarge = ROOT.TLatex()
#        textCMSlarge.SetNDC()
#        textCMSlarge.SetTextSize(cmstextsize)
#        textCMSlarge.SetTextAlign(13)   
#        textCMSlarge.SetTextFont(42)
#        textCMSlarge.DrawLatex(0.20,0.85, cmstext)
#
#        if preliminary:
#            prelim = "#font[%s]{%s}"%(font,preliminary)
#            textPrelimlarge = ROOT.TLatex()
#            textPrelimlarge.SetNDC()
#            textPrelimlarge.SetTextSize(0.06*0.6)
#            textPrelimlarge.SetTextAlign(13)   
#            textPrelimlarge.SetTextFont(42)
#            textPrelimlarge.DrawLatex(0.21,0.78, prelim)
#
#       
#    if "%" in textR:
#        textR      = textR%lumi
#    latexTextR = "#font[42]{%s}"%(textR)
#    #latexTextR = "#font[%s]{%0.1f fb^{-1} (13 TeV)}"%(lumi)
#    latex.DrawLatex(rxy[0],rxy[1],  latexTextR)


def getDataMCRatios( data_hist, mc_hist ):
    import array as ar
    efill = defaults.error_fill_style
    ecolor = 13#defaults.error_fill_color
    
    if type(mc_hist) == ROOT.THStack :
        stack = mc_hist.Clone("stack")
        mc_hist = stack.GetHists().Last().Clone("mc_hist" )
        mc_hist.Reset()
        mc_hist.Merge( stack.GetHists() )
        

    unity = mc_hist.Clone( "IAmOne" )
    unity.SetLineColor(1)
    unity.SetLineWidth(1)
    unity.SetFillColor(0)
    nBins = unity.GetNbinsX()
    mc_noe = mc_hist.Clone( "mc_noerror" )
    #mc_noe.Sumw2(0)
    mc_noe.SetError(ar.array( "d",[0]*(nBins+1) ) ) 
    
    mc_e = mc_hist.Clone( "mc_error" )
    mc_e.Divide(mc_noe)
    mc_e.SetFillStyle(efill)
    #mc_e.SetLineColor( ecolor )
    mc_e.SetFillColor( ecolor -1)
    mc_e.SetMarkerSize(0)

    for ib in range( nBins+1 ):
        unity.SetBinContent(ib, 1)
        unity.SetBinError(ib, 0)

    data_ratio = data_hist.Clone( "data_ratio"  )
    data_ratio.Divide( mc_noe )

    mc_eb = mc_hist.Clone("mc_errorbar" )
    mc_eb.SetFillStyle( efill )
    mc_eb.SetLineColor( ecolor )
    mc_eb.SetMarkerSize(0)
    mc_eb.SetFillColor( ecolor )
    #mc_eb.SetFillColor(ROOT.kBlue-5)

    ROOT.gStyle.SetHatchesSpacing(0.01)
    ROOT.gStyle.SetHatchesLineWidth(1)

    ret = [data_ratio, mc_e, mc_eb , unity, mc_noe]
    for x in ret: x.SetDirectory(0)
    return ret



def drawNiceDataPlot( data_hist, mc_stack, sig_stack = None ,mc_total = None, options={} , saveDir = "./" , name = "plot", leg= None):
    """
           mc_total can be given in order to propegate errors fully, otherwise errors in mc_stack will be added in quad
    """

    canv = []
    ratios = [] 
    uq    = name+"_"
    #print uq

    if not mc_total:
        mc_total = mc_stack.GetHists()[0].Clone( "total"+"_"+uq)
        mc_total.Reset()
        mc_total.Merge( mc_stack.GetHists() )

    canv_hw=(800,800)
    canv  = makeCanvasPads() 
    #print canv
    canv[1].cd()
    setLogY = options.get('logy',1)
    canv[1].SetLogy( setLogY )

    ratios = getDataMCRatios( data_hist  , mc_total )
    data_ratio , mc_e, mc_eb, unity, mc_noe = ratios
    ymax = max( getHistMax( mc_noe )[1] , getHistMax( data_hist )[1] )
    #if sig_stack:
    #    ymin = min( [getHistMin( mc_stack.GetHists().First() )[1] , getHistMax( data_hist )[1] , ])
    #else:
    #    ymin = min( [getHistMin( mc_stack.GetHists().First() )[1] , getHistMax( data_hist )[1] , getHistMax( sig_stack.GetHists().First() )[1] ])
    ymin = options.get('ymin', defaults.ymin )
    extras = [mc_stack]
    #print '---------------', mc_stack
    #mc_stack.Print("all")
    #mc_eb.Draw("E2")

    # Recreating the stack here for some reason because ROOT segfaults if I use mc_stack ( no clue why! )
    stack = ROOT.THStack( mc_stack.GetTitle() + "2", mc_stack.GetName() )  
    for h in mc_stack.GetHists():
        h.SetDirectory(0)
        stack.Add(h)
        #print h.Draw("same")
    mc_stack = stack
    #
    ymax = options.get("ymax",ymax) 
    mc_stack.Draw("hist")
    ytitle = options.get( "ytitle", "Events")
    mc_stack.GetYaxis().SetTitle( ytitle )
    mc_stack.GetYaxis().SetTitleOffset(  getattr( defaults, "ytitle_offset", 1.0 ) )
    mc_stack.SetMaximum(ymax* ( 1.5 + 15*setLogY) )
    mc_stack.SetMinimum( ymin )
    mc_eb.Draw("E2same")
    #mc_e.Print("all")
    if sig_stack:
        dOptSig = "same hist"
        if isinstance( sig_stack, ROOT.THStack ):
            dOptSig += " nostack"
        sig_stack.Draw(dOptSig)
    #drawCMSHeader()
    data_hist.Draw("sameE0X0")

    if leg:
        leg = [leg] if not type(leg) in [list, tuple] else leg
        for l in leg:
            l.Draw()

    ## draw ratio
    ytitle_r = options.get( "ytitle_r", getattr(defaults, "ytitle_r", "Data/MC") )
    #ytitle_size = options.get("ytitle_size", 0.12 )
    #ytitle_offset = options.get("ytitle_offset", 0.5)
    xtitle = options.get( "xtitle", getattr(defaults, "xtitle", None))
    canv[2].cd()
    unity.Draw() 
    unity.GetYaxis().SetTitle(       ytitle_r ) 
    #unity.GetYaxis().SetTitleSize(   ytitle_size )  
    #unity.GetYaxis().SetTitleOffset( ytitle_offset )
    #unity.GetYaxis().SetLabelSize( unity.GetYaxis().GetLabelSize()*2)
    if xtitle: unity.GetXaxis().SetTitle( xtitle )
    unity.SetNdivisions(505, "y")
    nBinsX = unity.GetNbinsX()
    xsize = canv_hw[0]/( nBinsX +1)/180. #180 scale is arbitrary (but emperical!)
    xsize = min([0.12, xsize])
    unity.GetXaxis().SetLabelSize( xsize )
    #unity.GetXaxis().LabelsOption("v")
    mc_e.Draw("E2same")
    mc_e.Draw("E2same")
    data_ratio.Draw("E0X0p same")
    #data_ratio.SetMaximum(2)
    #data_ratio.SetMinimum(0)
    #degTools.saveCanvas( canv[0], saveDir , name)
    canv = list(canv)
    canv[1],canv[2] = adjustRatioPadTitleSizes( canv[1], canv[2] )
    canv = tuple(canv)

    defaults.CMS_lumi.CMS_lumi(canv[1], defaults.lumi, defaults.energy , defaults.iPosX) 
    canv[1].Update()
    canv[2].Update()
    if saveDir:
        if not os.path.isdir( saveDir ):
            os.makedirs( saveDir ) 
        save_path = os.path.join( saveDir, name )
        canv[0].SaveAs( save_path +".root")
        canv[0].SaveAs( save_path +".pdf")
        canv[0].SaveAs( save_path +".png")

        #canv[0].SetGrayscale(1)
        #canv[0].SaveAs( save_path +"_bw.pdf")
        #canv[0].SaveAs( save_path +"_bw.png")
        
    return canv, ratios, mc_stack



def getCanvPrims( canv , doClone=True):
    if doClone:
        ret= [canv.GetPrimitive( x.GetName() ).Clone() for x in canv.GetListOfPrimitives() ]
    else:
        ret= [canv.GetPrimitive( x.GetName() ) for x in canv.GetListOfPrimitives() ]
    for x in ret:
        if hasattr(x,"SetDirectory"): x.SetDirectory(0)
    return ret

def getCanvFirstHist( canv , doClone=False):
    prims = getCanvPrims(canv, doClone=doClone)
    hist_types = [ROOT.TH1D, ROOT.TH2D, ROOT.TH1F, ROOT.TH2F ]
    for p in prims:
        if isinstance(p, ROOT.THStack ):
            return p.GetHists().First()
        if any( [isinstance( p, htype) for htype in hist_types ] ):
            return p
    
    

def adjustRatioPadTitleSizes(pad1,pad2):
    h1=getCanvFirstHist( pad1, doClone=False)
    h2=getCanvFirstHist( pad2, doClone=False)
    pads_ratio = pad1.GetAbsHNDC() / pad2.GetAbsHNDC()
    #print pads_ratio 
    #print h1.GetYaxis().GetTitleOffset() , h2.GetYaxis().GetTitleOffset()

    h1.GetXaxis().SetTitleSize( getattr( defaults, "xtitle_size", 0.06 ) )
    h1.GetXaxis().SetLabelSize( getattr( defaults, "xtitle_size", 0.06 ) )
    h1.GetXaxis().SetTitleOffset( getattr( defaults, "xtitle_offset", 0.001 ) )

    h1.GetYaxis().SetTitleSize(   getattr( defaults, "ytitle_size", 0.06 ) )
    h1.GetYaxis().SetLabelSize(   getattr( defaults, "ytitle_size", 0.06 ) )
    h1.GetYaxis().SetTitleOffset( getattr( defaults, "ytitle_offset", 1.25 ) )
    h1.Modify()

    xtitle_r_factor = getattr( defaults, "xtitle_r_factor", 0.8)
    ytitle_r_offset_factor  = getattr( defaults, "ytitle_r_offset_factor" , 1.0 )
    h2.GetXaxis().SetTitleSize(  h1.GetXaxis().GetTitleSize()      * pads_ratio )
    h2.GetXaxis().SetLabelSize(  h1.GetXaxis().GetLabelSize()  * pads_ratio )
    h2.GetXaxis().SetTitleOffset(  h1.GetXaxis().GetTitleOffset()   )
    h2.GetXaxis().SetLabelOffset(0.01)
    
    h2.GetYaxis().SetTitleSize(  h1.GetYaxis().GetTitleSize()      * pads_ratio )
    h2.GetYaxis().SetTitleOffset(  h1.GetYaxis().GetTitleOffset()  / pads_ratio * ytitle_r_offset_factor)
    h2.GetYaxis().SetLabelSize(  h1.GetYaxis().GetLabelSize()  * pads_ratio * xtitle_r_factor)
    h2.GetYaxis().SetLabelOffset(0.01)
     
    h2.GetYaxis().SetRangeUser(*defaults.ratio_range)

    #print h1.GetXaxis().GetLabelOffset() , h2.GetXaxis().GetLabelOffset()
    print  h1.GetYaxis().GetLabelSize(), h2.GetYaxis().GetLabelSize()
    #print  h2.GetXaxis().GetTitleSize()

    return pad1, pad2



