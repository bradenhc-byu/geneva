#To reduce the features
#java -cp ./weka.jar weka.filters.supervised.attribute.AttributeSelection -E "weka.attributeSelection.CfsSubsetEval -M" -S "weka.attributeSelection.BestFirst -D 1 -N 5" -i data/soybean.arff -o data/soybean2.arff

#To run the tests

# java -cp ./weka.jar weka.classifiers.rules.ZeroR -t "data/weather.nominal.arff" -v | grep "Correctly"

# and it will get you back "Correctly Classified Instances <tab> 9 <tab> 99%"
# or try findstr if grep does not work

#
from VariantInterpretationAnalysis.Definitions import DATA_DIR
import os
import subprocess
from subprocess import check_output
import subprocess

with open(DATA_DIR+"wekaClassifiers.txt") as f:
 for line in f:
  #"java -cp ./weka.jar "+line+ " -t data/weather.nominal.arff -v"
  print line[:-1]
  command = "java -cp ./weka.jar "+line[:-1]+ " -t data/weather.nominal.arff -v | findstr \"Correctly\" > tmp"
  #output = check_output(command, shell=True)
  os.system(command)
  with open("tmp") as g:
    for line2 in g:
        print line2 #This will be the accuracy
