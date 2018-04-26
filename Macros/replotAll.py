import os,subprocess,ROOT
import pickle
import re
import time

def listDir(path):
  p = subprocess.Popen(['ls',path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  return out.split()

def runReplotter(inDir, file, opt, suffix, dryRun):
  list = ["python", "replot.py", "--isMVAorCC=mva", "--output_dir="+inDir, "--plot_path="+inDir+"/"+file]
  if opt is not None:
    list = list + ["--opt="+opt]

  if dryRun:
    print "Run the following:", list
  else:
    p = subprocess.call(["cp", inDir + "/" + file, inDir + "/bak.root"])
    p = subprocess.call(list)
    renameOutput(inDir, file, suffix, dryRun)
    p = subprocess.call(["mv", inDir + "/bak.root", inDir + "/" + file])
  return

def renameOutput(inDir, file, suffix, dryRun):
  if dryRun:
    return
  baseName = file[:-5]
  for extension in [".root", ".pdf", ".png"]:
    p = subprocess.call(["mv", inDir + "/" + baseName + extension, inDir + "/" + baseName + "_" + suffix + extension])
  return

def replot(inDir, dryRun):
  itemList = listDir(inDir)
  dirList = []
  fileList = []

  for item in itemList:
    if os.path.isdir(inDir + "/" + item):
      dirList.append(inDir + "/" + item)
    if os.path.isfile(inDir + "/" + item):
      if item[-14:] == "_syncPlot.root":
        fileList.append(item)

  for file in fileList:
    isBDT = False
    bdtName = "BDT"
    if file[-18:-13] == "_BDT_":
      isBDT = True
      tree = (inDir).split("/")
      for node in tree:
        if node[:6] == "DeltaM":
          bdtName = "BDT" + node[6:]

    opt = "MVA"
    if isBDT:
      opt = bdtName
    runReplotter(inDir, file, opt, "syst", dryRun)

    opt = "MVAEnv"
    if isBDT:
      opt = bdtName + "Env"
    runReplotter(inDir, file, opt, "envelope", dryRun)

    opt = "MVAStat"
    if isBDT:
      opt = bdtName + "Stat"
    runReplotter(inDir, file, opt, "stat", dryRun)

  for dir in dirList:
    replot(dir, dryRun)

  return

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description='Process the command line options')
  parser.add_argument('-i', '--inDirectory', required=True, help='Name of the input directory')
  parser.add_argument('-d', '--dryRun', action='store_true', help='Do a dry run (i.e. do not actually run the potentially dangerous commands but print them to the screen)')

  args = parser.parse_args()

  if not args.dryRun:
    print "You did not enable dry run. You are on your own!"

  if not os.path.isdir(args.inDirectory):
    parser.error('The given input directory must be a directory')

  replot(args.inDirectory, args.dryRun)
