for year in {17,18}; do
  
  YEAR=20${year}
  echo $YEAR

#  python replot.py --isPAPERorMVAorCC=mva --plot_path=/home/t3cms/dbastos/LSTORE/Stop4Body_RunII/nTuples${year}_nanoAOD_v2021-10-15/DataMC-ss-fix/Presel_LepPt_syncPlot.root --output_dir=plots${YEAR} --output_name=Presel_LepPt_${YEAR}
#  python replot.py --isPAPERorMVAorCC=mva --plot_path=/home/t3cms/dbastos/LSTORE/Stop4Body_RunII/nTuples${year}_nanoAOD_v2021-10-15/DataMC-ss-fix/Presel_Met_syncPlot.root --output_dir=plots${YEAR} --output_name=Presel_Met_${YEAR}

  for i in {1..8}; do 
    #python replot.py --isPAPERorMVAorCC=mva --plot_path=/home/t3cms/dbastos/LSTORE/Stop4Body_RunII/DDE${YEAR}_fix_24bins_noNegWatSR_unblind_bdt${i}0/PreselectionMVA_BDT_syncPlot.root --output_dir=plots${YEAR} --output_name=${YEAR}_dm${i}0_PreselectionMVA_BDT --opt=BDT
    python replot.py --isPAPERorMVAorCC=mva --plot_path=/lstore/cms/dbastos/REPOS/Stop4Body-nanoAOD/CMSSW_8_0_14/src/UserCode/Stop4Body-nanoAOD/Macros/FinalTablesYieldUnc_unblinded_plots/${YEAR}/plotDM${i}0_syncPlot.root --output_dir=plots${YEAR} --output_name=plotDM${i}0 --opt=BDT
    #mv plots${YEAR}/PreselectionMVA_BDT_syncPlot.pdf plots${YEAR}/${YEAR}_dm${i}0_PreselectionMVA_BDT.pdf
  done
done
