#!/usr/bin/env python
#---coding:utf-8---

####################################################################
# File Name: extend_form_summit.py
# Author: zxr
# mail: zhangxiaoran@picb.ac.cn 
# Created Time: Tue 05 Jan 2016 03:22:12 PM CST
####################################################################

import math, string
import sys, getopt

def usage():
    print("-h --help useange()", "\n")
    print("-i: inputfile", "\n")
    print("-o: outputfile", "\n")
    print("-g: chromsize file", '\n')
    print("-l: length, the length of the whole peak, default=0, ", '\n')
    print("-f: the float percentange to extend of the whole peak, default:use -l", '\n')
    print("-s: the col number of the summit, default:none", '\n')
    print("-m: the col number of the summit is the length from the start end, default:not", '\n')
    print("-e: extend half of -l from the start and end, default:not", '\n')
    print("-t: the input file have a header in the frist line, default:not", '\n')
    print("-k: keep the input file have a header in the frist line, default:not", '\n')
    print("-d: the result can be different length if start is less than 0 and max more than the chrome size, default:not","\n")
if __name__=="__main__":
    opts, args=getopt.getopt(sys.argv[1:], "hi:o:g:l:s:mef:tkd", ["help"])
    input=""
    output=""
    genome=""
    length=0
    summit=0
    sumcol=0
    mode=0
    middle=0
    extendto=0
    fp=0.0
    usef=0
    title=0
    keep=0
    A=0
    odd=0
    difflen=0
    for op, value in opts:
        if op in ("-h", "--help"):
            usage()
            sys.exit()
        if op=="-i":
            input=value
        if op=="-o":
            output=value
        if op=="-g":
            genome=value
        if op=="-l":
            length=int(value)
        if op=="-s":
            summit=1
            sumcol=int(value)-1
        if op=="-m":
            mode=1
        if op=="-e":
            extendto=1
        if op=="-f":
            fp=float(value)
            usef=1
        if op=="-t":
            title=1
        if op=="-k":
            keep=1
        if op=="-d":
            difflen=1
    chromsize={}
    genomefile=open(genome)
    
    if usef==0:
        half=int(length/2)
        if length%2==1:
            odd=1
    for line in genomefile:
        line=line.rstrip().split()
        chromsize[line[0]]=int(line[1])
    input=open(input)
    output=open(output, 'w')
    for line in input:
        if title==1 and A==0:
            A+=1
            if keep==0:
                continue
            else:
                output.write(line)
                continue
        line=line.rstrip().split()
        max=chromsize[line[0]]
        wholelen=int(line[2])-int(line[1])
        
        if extendto==0:
            if summit==1:
                if mode==1:
                    middle=int(line[sumcol])+int(line[1])
                else:
                    middle=int(line[sumcol])
            else:
                middle=(int(line[1])+int(line[2]))/2
            if usef==0:
                left=int(middle-half)
                right=int(middle+half+odd)
            else:
                half=int(wholelen*fp)
                left=int(middle-half)
                right=int(middle+half)
        else:
            if usef==0:
                left=int(line[1])-half
                right=int(line[2])+half+odd
            else:
                half=int(wholelen*fp)
                left=int(line[1])-half
                right=int(line[2])+half
        if left<0:
            left=0
            if difflen==0:
                right=length
        elif right>max:
            right=max
            if difflen==0:
                if usef==0:
                    left=max-length
                    if left<0:
                        left=0
        other=[]
        if len(line)==3: 
            output.write(line[0]+"\t"+str(left)+"\t"+str(right)+"\n")
        else:
            other=line[3:]
            otherstr='\t'.join(other)
            output.write(line[0]+"\t"+str(left)+"\t"+str(right)+"\t"+otherstr+"\n")
    input.close()
    output.close()
