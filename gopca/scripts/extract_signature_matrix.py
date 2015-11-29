#!/usr/bin/env python2.7

# Copyright (c) 2015 Florian Wagner
#
# This file is part of GO-PCA.
#
# GO-PCA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License, Version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Script to extract the GO-PCA signature matrix as a tab-delimited text file.
"""

import sys
import argparse

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

from genometools import misc
from gopca import common

def get_argument_parser():

    description='Extract the GO-PCA signatures matrix as a tab-delimited ' + \
        'text file.'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-g','--gopca-file',required=True,
            help='The GO-PCA output file (in pickle format).')
    parser.add_argument('-o','--output-file',required=True,
            help='The output file.')

    parser.add_argument('-i','--invert-signature-order',action='store_true',
            help = 'If set, invert the ordering of the signatures.')
    parser.add_argument('--sample-cluster-metric', default='euclidean',
            help = 'Metric used for clustering the samples')
    parser.add_argument('--disable-sample-clustering', action='store_true',
            help = 'Disable sample clustering.')

    return parser

def main(args=None):

    if args is None:
        parser = get_argument_parser()
        args = parser.parse_args()

    gopca_file = args.gopca_file
    output_file = args.output_file
    invert_signature_order = args.invert_signature_order
    sample_cluster_metric = args.sample_cluster_metric
    disable_sample_clustering = args.disable_sample_clustering

    logger = misc.configure_logger(__name__)

    output = common.read_gopca_output(gopca_file)
    
    signatures = output.signatures
    labels = [sig.get_label(include_id=False) for sig in signatures]
    samples = list(output.samples)
    S = output.S

    # clustering of rows (signatures)
    order_rows = common.cluster_signatures(S,invert=invert_signature_order)
    S = S[order_rows,:]
    labels = [labels[idx] for idx in order_rows]

    if not disable_sample_clustering:
        # clustering of columns (samples)
        #distxy = squareform(pdist(S.T, metric='euclidean'))
        distxy = squareform(pdist(S.T, metric=sample_cluster_metric))
        R = dendrogram(linkage(distxy, method='average'),no_plot=True)
        order_cols = np.int64([int(l) for l in R['ivl']])
        S = S[:,order_cols]
        samples = [samples[j] for j in order_cols]

    common.write_expression(output_file,labels,samples,S)
    logger.info('Wrote %d signatures to "%s".', len(signatures),output_file)

    return 0

if __name__ == '__main__':
    return_code = main()
    sys.exit(return_code)
