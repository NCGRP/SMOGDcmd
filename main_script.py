#!/usr/bin/env python
# encoding: utf-8
"""
popgen_format_parsers.py

Created by Nicholas Crawford on 2009-02-14.
Copyright (c) 2009 Boston Univeristy. All rights reserved.

Modified by Patrick Reeves 1-16-2016 for command line use.
"""
from numpy import *
from scipy import stats   # for calculating harmonic mean
import re
from Jost_Stats_Calc import *
#from bootstrap import Bootstrap
import genotype_file_parsers as gfp
#import pprint as pp
import sys


def main(argv):	
	
	fp = open(sys.argv[1]) #open the data file, specified as argument 1
	data = fp.read()
	statdesired = sys.argv[2]
	numb_of_replicates = int(sys.argv[3]) #get the number of replicates from the command line

	data = data.strip()												# get data
	file_info = gfp.determine_file_type(data)					# determine file type (e.g. mac, linux, PC)
	lines = data.split(file_info[0])									# splits on file type endings (e.g., \r\n or \n or \r)
	
	#  PROCESS DATA, FIND UNIQUE ALLELES
	#
	# 	Basic format of processed data:
	# [   [u'Locus 1', u'Locus 2'],
	#     [u'Species_w_20_loci', u'SpeciesB', u'SpeciesA'],
	#     [   [   [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'001001', u'001001'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002'],
	#             [u'002002', u'002002']],
	#	etc.. 
	
	
	
	# pick appropriate file parser
	if file_info[1] == 'Arlequin':										
		processed_data = gfp.arlequin_parser(lines)
		
	if file_info[1] == 'unknown':
		processed_data = gfp.genepop_parser(lines)
	
	#print "processed_data:"
	#print processed_data
	
	
	# process data, etc.
	empty_dict = create_empty_dictionaries_of_unique_alleles(processed_data)  # create empty dictionaries of alleles in each locus
	
	allele_counts = generate_allele_counts(processed_data[0], processed_data[1], processed_data[2], empty_dict)
	
	population_sizes = generate_population_sizes(processed_data[2], processed_data[1], processed_data[0])		# dictionary of population sizes
	
	frequencies = generate_frequencies(processed_data, allele_counts)
	
	#pp.pprint(frequencies)
	
	results = fstats(frequencies, processed_data[1], processed_data[0], population_sizes)

	
	
	#mean_D = mean_D_across_loci(results[1])
	
	#bootstrap_results = Bootstrap(processed_data, numb_of_replicates)
	
	#pairwise_stats = generate_pairwise_stats(processed_data[0], processed_data[1], processed_data[2])
	
	#calculate only the desired statistic specified at the command line
	n = float(len(processed_data[1])) #n (or K), the number of populations, can be calculated by counting the number of population names
	mean_statdesired = mean_across_loci(results[1], statdesired, n)

	
	#return abbreviated results
	#print results[1]
	#print "mean_D = ", mean_D
	#print statdesired, " = ", mean_statdesired
	print mean_statdesired
	
	#return (results, bootstrap_results, mean_D)
	
	# create urls and files:
	#fstats_url = update_csv_file('fstats',results[0])
	
	#fstats_est_url = update_csv_file('est_stats',results[1])
	
	#bootstrap_url = update_csv_file('bootstrap_results',bootstrap_results)
	
	#matrix_url = update_csv_file('pairwise_matrices',pairwise_stats[0])
	
	#dest_matrix_url = update_csv_file('dest_matrices',pairwise_stats[1])
	
	#return (results, bootstrap_results, (fstats_url,fstats_est_url,bootstrap_url, matrix_url, dest_matrix_url), mean_D)
	return (statdesired)

if __name__ == "__main__":
   main(sys.argv[1:])
