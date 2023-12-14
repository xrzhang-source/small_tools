#!/usr/bin/env python
#---coding:utf-8---

####################################################################
# File Name: commom_culomn.py
# Author: zxr
# mail: zhangxiaoran@picb.ac.cn 
# Created Time: Wed 30 Apr 2014 02:31:09 PM CST
####################################################################

import math, string
import sys, getopt
import os, glob

def usage():
    print ("commom_column.py inputfile1 inputfile2 column number1 column_number2")
    print ("\n")
if __name__=="__main__":
    if len(sys.argv[1:])==0:
        usage()
    elif len(sys.argv[1:])==4:
        input1=sys.argv[1]
        input2=sys.argv[2]
        col1=int(sys.argv[3])-1
        col2=int(sys.argv[4])-1
        p1, f1=os.path.splitext(input1)
        p2, f2=os.path.splitext(input2)
        output1="common_"+p1+"_"+p2+".txt"
        output2="unique_"+p1+f1
        output3="unique_"+p2+f2
        data1={}
        input1=open(input1)
        output1=open(output1, 'w')
        output2=open(output2, 'w')
        output3=open(output3, 'w')
        for line in input1:
            line=line.rstrip().split()
            data1[line[col1]]='\t'.join(line)
        input1.close()
        data2={}
        input2=open(input2)
        for line in input2:
            line1=line.rstrip().split()
            line2='\t'.join(line1[0:col2]+line1[col2+1:])
            data2[line1[col2]]='\t'.join(line1)
            if line1[col2] in data1.keys():
                output1.write(str(data1[line1[col2]])+'\t'+str(line2)+'\n' )
            else:
                output3.write(str(data2[line1[col2]])+'\n')
        for key in data1.keys():
            if key in data2.keys():
                continue
            else:
                output2.write(data1[key]+'\n')
            
        input2.close()
        output1.close()
        output2.close()
        output3.close()

    else:
        print("There is something wrong in your parameter, print common_column.py to see the useage", '\n')

