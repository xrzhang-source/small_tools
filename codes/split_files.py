#!/usr/bin/env python
#---coding:utf-8---

####################################################################
# File Name: split_files.py
# Author: zxr
# mail: zhangxiaoran@picb.ac.cn 
# Created Time: Mon 25 Sep 2017 10:26:57 PM CST
####################################################################

import math, string
import sys, getopt

def usage():
    print ("-h --help useange()", "\n")
    print ("python 2 only", "\n")
    print ("-i: inputfile", "\n")
    print ("-o: outputfile index", "\n")
    print ("-c: markers columns, split by , ", "\n")
    print ("-k; not keep the markers in the result, defalut:yes", '\n')
    print ("-a: add the index before the markers in the file name, default:not", '\n')
    print ("-t: if the file have a title,choose it, default:not","\n")
    print ("-r: rm the title in the result files, default:not,only choose it when -t is choosed","\n")
if __name__=="__main__":
    opts, args=getopt.getopt(sys.argv[1:], "hi:o:c:katr", ["help"])
    input=""
    output=""
    cols=[]
    keep=1
    add_before=0
    cols2=[]
    title=0
    keeptitle=1
    for op, value in opts:
        if op in ("-h", "--help"):
            usage()
            sys.exit()
        if op=="-i":
            input=value
        if op=="-o":
            output=value
        if op=="-t":
            title=1
        if op=="-r":
            keeptitle=0
        if op=="-k":
            keep=0
        if op=="-a":
            add_before=1
        if op=="-c":
            cols=value.split(",")
            cols_number=len(cols)            
            for x in range(0, cols_number):
                cols2.append(int(cols[x])-1)
    inputfile=open(input, 'r')
    out={}
    #out_keys = list(out)
    a=1
    for line in inputfile:
        if title==1 and a==1:
            a+=1
            header=[]
            if keeptitle==0:
                continue
            else:
                line=line.rstrip().split()
                if keep==1:
                    header=line
                else:
                    for i in range(0, len(line)):
                        if i not in cols2:
                            header.append(line[i])
                continue
        line=line.rstrip().split()
        markers_list=[]
        makers=[0 for x in range(0, cols_number)]
        outline=[]
        if keep==1:
            outline=line
        for i in range(0, len(line)):
            if i in cols2:
                markers_list.append(line[i])
            elif keep==0:
                outline.append(line[i])
        markers_str="_".join(markers_list)
        if markers_str in out.keys():
        #if markers_str in out_keys:
            out[markers_str].append(outline)
        else:
            out.keys().append(markers_str)
            out[markers_str]=[]
            out[markers_str].append(outline)
    inputfile.close()
    for key in out.keys():
        if add_before==0:
            outname=output+"_"+key
        else:
            outname=key+"_"+output
        outfile=open(outname, 'w')
        if (keeptitle==1 and title==1):
            outfile.write(str("\t".join(header))+"\n")
        for i in range(0, len(out[key])):
            outfile.write(str("\t".join(out[key][i]))+"\n")
        outfile.close()
