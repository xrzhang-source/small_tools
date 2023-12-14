#!/usr/bin/env python
#---coding:utf-8---

####################################################################
# File Name: cut_zero.py
# Author: zxr
# mail: zhangxiaoran@picb.ac.cn 
# Created Time: Tue 20 May 2014 03:31:48 PM CST
####################################################################

import math, string
import sys, getopt
import os
def usage():
    print( "-i inputfile", "\n")
    print( "-c rm clumons which are not to check , it shoule be separed by ', ', defalut none",'\n')
    print( "-t not to check the frist line, default yes", '\n')
    print( "--nk not to keep the title, only use it if you choose -t and want to rm the title in the output", '\n')
    print( "-o if you want to change the name, use it, if not , ignore it", '\n')
    print( "-z if you want to cut them from a zero value, use it, default:0.0", '\n')
    print( "-n if you want to rm n rows less than z value, use it ,default:all",'\n')
if __name__=="__main__":
    opts, args=getopt.getopt(sys.argv[1:], "hi:c:to:z:n:",["nk"] )
    input=""
    clu=[]
    top=2
    name=''
    zero=0.0
    nokeep=0
    nvalue="all"
    for op, value in opts:
        if op=="-h":
            usage()
            sys.exit()
        if op=="-i":
            input=value
            name=input
        if op=="-c":
            clu=value.split(",")
        if op=="-t":
            top=1
        if op=="-o":
            out=1
            name=value
        if op=="-z":
            zero=float(value)
        if op=="--nk":
            nokeep=1
        if op=="-n":
            nvalue=int(value)
    input=open(input)
    output=open("temp.txt", 'w')
    for line in input:
        mm=0
        if top==1:
            line2=line.rstrip('\n').split('\t')
            line1='\t'.join(line2)
            if nokeep==0:
                output.write(str(line1)+'\n')
            top+=1
            continue
        elif top>1:
            line=line.rstrip('\n').split('\t')
            if len(clu)==0:
                for i in range(0, len(line)):
                    if line[i].isdigit() == FALSE:
                        print ("warining!"+line+"\n")
                    elif float(line[i])<=zero:
                        mm+=1
                        continue
                    outdata='\t'.join(line)
                if nvalue=="all":
                    nvalue=len(line)
                if mm<nvalue:
                    output.write(str(outdata)+'\n')
                else:
                    continue
            else:
                for i in range (0, len(line)):
                    if str(i+1) in clu:
                        continue
                    else:
                        if float(line[i])<=zero:
                            mm+=1
                            continue
                        outdata='\t'.join(line)
                if nvalue=="all":
                    nvalue=(len(line)-len(clu))
                if mm<nvalue:
                    output.write(str(outdata)+'\n')
                else:
                    continue
    output.close()
    os.system("mv temp.txt "+str(name))

     
    

