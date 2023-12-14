#!/usr/bin/env python
#---coding:utf-8---

####################################################################
# File Name: merge_profile.py
# Author: zxr
# mail: zhangxiaoran@picb.ac.cn 
# Created Time: Sun 27 Apr 2014 05:16:38 PM CST
####################################################################

import math, string
import sys, getopt
import os
import pandas as pd
import argparse

import pandas as pd
import argparse

def merge_files(input_file, plus_files, output_file, separator='\t', c1=0, c2=1):
    # Read input and plus files
    input_df = pd.read_csv(input_file, sep=separator, header=None)
    plus_df_list = [pd.read_csv(file, sep=separator, header=None) for file in plus_files.split(',')]

    # Convert the merging columns to the same data type (string)
    input_df[c1] = input_df[c1].astype(str)
    for plus_df in plus_df_list:
        plus_df[c2] = plus_df[c2].astype(str)

    # Merge dataframes based on specified columns
    merged_df = input_df.copy()
    for plus_df in plus_df_list:
        merged_df = pd.merge(merged_df, plus_df, how='left', left_on=c1, right_on=c2)

    # Fill missing values with 0
    merged_df = merged_df.fillna(0)

    # Save the merged dataframe to the output file
    merged_df.to_csv(output_file, index=False, sep=separator, header=None)

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Merge different files based on specified columns.')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-p', '--plusfiles', required=True, help='Comma-separated list of plus files')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-s', '--separator', default='\t', help='Separator for the input and plus files')
    parser.add_argument('-c1', '--column_input', type=int, default=0, help='Column number for merging in the input file')
    parser.add_argument('-c2', '--column_plus', type=int, default=1, help='Column number for merging in plus files')

    # Parse command line arguments
    args = parser.parse_args()

    # Call the merge function with provided arguments
    merge_files(args.input, args.plusfiles, args.output, args.separator, args.column_input, args.column_plus)


