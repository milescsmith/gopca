#!/usr/bin/env python2.7

import sys
import argparse
import cPickle as pickle

from gopca import common

def read_args_from_cmdline():
	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-g','--gopca-file',required=True)
	parser.add_argument('-o','--output-file',required=True)

	return parser.parse_args()

def main(args=None):

	if args is None:
		args = read_args_from_cmdline()

	gopca_file = args.gopca_file
	output_file = args.output_file

	result = None
	with open(gopca_file,'rb') as fh:
		result = pickle.load(fh)
	
	signatures = result.signatures
	labels = [sig.get_pretty_format() for sig in signatures]
	samples = list(result.samples)
	S = result.S
	common.write_expression(output_file,labels,samples,S)

	return 0

if __name__ == '__main__':
	return_code = main()
	sys.exit(return_code)