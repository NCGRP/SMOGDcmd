Calculate G'st or D from a Genepop or Arlequin input file using Python.
Command line hacked version of Crawford's SMOGD.

usage:
./main_script.py datafile statdesired replicates

where,
datafile = path to the genepop or arlequin formatted data file
statdesired = name of desired output stat ("G_Hedrick", "D_Jost")
replicates = number of replicates for bootstrap analysis, use 0 to omit bootstrap

example: python -W ignore main_script.py genepop_test_file.txt G_Hedrick 0
         python -W ignore main_script.py arlequin_example_file.txt D_Jost 0
