#!/usr/bin/env python
#---coding:utf-8---

####################################################################
# File Name: linkerfilter.py
# Author: zxr
# mail: zhangxiaoran@picb.ac.cn 
# Created Time: Tue 19 Aug 2014 04:46:37 PM CST
 ####################################################################

import math, string
import sys, getopt
from datetime import datetime
from joblib import Parallel, delayed
import os, glob
def usage():
    print"-h --help useage()", '\n'
    print"-i inputfiles, should be separed by, and they should be  .fastq or .sam if you choose --nomap", '\n'
    print"-p pair inputfiles, should be separed by , and they should be  .fastq or .sam if you choose --nomap", '\n'
    print"-o outputdirs,should be separed by  default is ./ ", '\n'
    print"   the number of outdir is better equal the number of inputfiles.if not", '\n'
    print"   the results will divide into the dirs by turn", '\n' 
    print"-m mismatch number, default: 2", '\n'
    print"-n cpu number for a inputfile,  default:10", '\n'
    print"-s sample marker, one inputfile one marker, and they can be the same", '\n'
    print"-g --genome bowtie index, like $bowtie_index/mm9", '\n'
    print"-5 filter the sequence from the 5'-end", '\n'
    print"-3 filter the sequence from the 3'-end", '\n'
    print"-e --site the enzyme sites in Hic sequence result, shoule be separed by ,", '\n' 
    print"          like 5-G|TAC, should be enter GTA, default:GTA,CAT,CTA", '\n'
    print"--nodivide skep the step of dividing files", '\n'
    print"--nomap if you choose samfiles are inputfiles", '\n'
    print"--nosortsam if the samfiles are sorted! only use when you choose --nomap", '\n'
    print"-d --distance the cut off of the genome DNA fragment, default, 500", '\n'
    print"-r --noremove do not remove all the middle file like .sam .unmapped.fastq .fastq .bed or not, default:yes", '\n'
    print"--noadd do not add 1bp in the enzyme sites , default:yes", '\n'
def dividefiles(inputfile, pairfile, out_dir, smarker, filenum, leftend, rightend):

    marker=1 ## reads marker
    input=open(inputfile)
    pair=open(pairfile)
    line1=input.readline().rstrip()
    line2=pair.readline().rstrip()
    outputfile1=out_dir+"/"+smarker+"."+str(filenum)+".1.fastq"
    outputfile2=out_dir+"/"+smarker+"."+str(filenum)+".2.fastq"
    output1=open(outputfile1, 'w')
    output2=open(outputfile2, 'w')
    linenumber=0
    if rightend==0:
        while line1:
            if marker%4==1:
                newname1="@"+str(smarker)+":"+str(marker/4)+"/1"
                newname2="@"+str(smarker)+":"+str(marker/4)+"/2"
                output1.write(newname1+"\n")
                output2.write(newname2+"\n")
            elif marker%4==2:
                output1.write(line1[leftend:]+"\n")
                output2.write(line2[leftend:]+"\n")
            elif marker%4==3:
                newname1="+"
                newname2="+"
                output1.write(newname1+"\n")
                output2.write(newname2+"\n")
            elif marker%4==0:
                output1.write(line1[leftend:]+"\n")
                output2.write(line2[leftend:]+"\n")
            marker+=1
            line1=input.readline().rstrip()
            line2=pair.readline().rstrip()
    else:
        rightend=-1*rightend
        while line1:
            if marker%4==1:
                newname1="@"+str(smarker)+":"+str(marker/4)+"/1"
                newname2="@"+str(smarker)+":"+str(marker/4)+"/2"
                output1.write(newname1+"\n")
                output2.write(newname2+"\n")
            elif marker%4==2:
                output1.write(line1[leftend:rightend]+"\n")
                output2.write(line2[leftend:rightend]+"\n")
            elif marker%4==3:
                newname1="+"
                newname2="+"
                output1.write(newname1+"\n")
                output2.write(newname2+"\n")
            elif marker%4==0:
                output1.write(line1[leftend:rightend]+"\n")
                output2.write(line2[leftend:rightend]+"\n")
            marker+=1
            line1=input.readline().rstrip()
            line2=pair.readline().rstrip()
    input.close()
    pair.close()
    output1.close()
    output2.close()
    return outputfile1, outputfile2            
def mapping(noadd, input, mis, cpu, genome, sites, resites, rmmiddle):
    pre=os.path.splitext(input)[0]
    output=pre+'_0.sam'
    logs=pre+'.log'
    en_log=pre+'.enzyme.log'
    command="bowtie "+genome+" -q "+input+" -p "+str(cpu)+" -n "+str(mis)+" -m 1"+" -S "+output+" 2>"+logs  
    os.system(command)
    site_number={}
    if noadd==1:
        for site in sites:
            for resite in resites:
                key=site+resite
                if key not in site_number.keys():
                    site_number[key]=[0, len(site), len(resite)]
    else:
        for site in sites:
            for resite in resites:
                key1=site+"A"+resite
                key2=site+"T"+resite
                key3=site+"C"+resite
                key4=site+"G"+resite
                if key1 not in site_number.keys():
                    site_number[key1]=[0, len(site), len(resite)]
                if key2 not in site_number.keys():
                    site_number[key2]=[0, len(site), len(resite)]
                if key3 not in site_number.keys():
                    site_number[key3]=[0, len(site), len(resite)]
                if key4 not in site_number.keys():
                    site_number[key4]=[0, len(site), len(resite)]
    samfile=pre+".sam"
    unmapfile=pre+"_unmapped.fastq"
    unmapfilename=unmapfile
    unmapfile=open(unmapfile, 'w')
    samfile=open(samfile, 'w')
    newmis=0
    for newmis in range(0, mis+1):
        tempfile=os.path.splitext(output)[0]+"_"+str(newmis)+".fastq"
        output2=pre+"_"+str(newmis)+"mis.sam"
        readin=open(output)
        temp=open(tempfile, 'w')
        if newmis==0:
            for line in readin:
                line=line.rstrip()
                if line[0][0]=="@":
                    samfile.write(line+'\n')
                    continue
                else:
                    line=line.split()
                    if line[1]=="4":
                        cut=-1
                        for twosite in site_number.keys():
                            havesite=0
                            sitelen=site_number[twosite][1]
                            resitelen=site_number[twosite][2]
                            cut=int(line[9].find(twosite, 20))
                            if cut==-1:
                                cut=int(line[9].find(twosite))
                                if cut==-1:
                                    continue
                            else:
                                if noadd==1:
                                    site_number[line[9][cut:cut+sitelen+resitelen]][0]+=1
                                    if cut+sitelen>18:
                                        temp.write("@"+line[0]+"\n")
                                        temp.write(line[9][0:cut+sitelen]+"\n")
                                        temp.write("+"+"\n")
                                        temp.write(line[10][0:cut+sitelen]+'\n')
                                    if len(line[9][cut+sitelen:])>=20:
                                        temp.write("@"+line[0]+"\n")
                                        temp.write(line[9][cut+sitelen:]+"\n")
                                        temp.write("+"+"\n")
                                        temp.write(line[10][cut+sitelen:]+'\n')
                                else :
                                    site_number[line[9][cut:cut+sitelen+resitelen+1]][0]+=1
                                    if cut+sitelen>18:
                                        temp.write("@"+line[0]+"\n")
                                        temp.write(line[9][0:cut+sitelen]+"\n")
                                        temp.write("+"+"\n")
                                        temp.write(line[10][0:cut+sitelen]+'\n')
                                    if len(line[9][cut+sitelen+1:])>=20:
                                        temp.write("@"+line[0]+"\n")
                                        temp.write(line[9][cut+sitelen+1:]+"\n")
                                        temp.write("+"+"\n")
                                        temp.write(line[10][cut+sitelen+1:]+'\n')
                                break
                        if cut==-1:
                            unmapfile.write("@"+line[0]+"\n")
                            unmapfile.write(line[9]+"\n")
                            unmapfile.write("+"+"\n")
                            unmapfile.write(line[10]+"\n")
                    else:
                        samfile.write('\t'.join(line)+'\n')
        else:
            for line in readin:
                line=line.rstrip()
                if line[0][0]=="@":
                    continue
                else:
                    line=line.split()
                    if line[1]=="4":
                        temp.write("@"+line[0]+"\n")
                        temp.write(line[9]+"\n")
                        temp.write("+"+"\n")
                        temp.write(line[10]+"\n")
                    else:
                        samfile.write('\t'.join(line)+'\n')
        readin.close()
        temp.close()
        print"The second mapping of "+str(newmis)+" mismatch is starting....", '\n'
        command2="bowtie "+genome+" -q "+tempfile+" -p "+str(cpu)+" -n "+str(newmis)+" -m 1"+" -S "+output2+" 2>>"+logs  
        os.system(command2)
        print"The second mapping of "+str(newmis)+" mismatch is finished", '\n'
        os.system("rm "+output+" -f")
        os.system("rm "+tempfile+" -f")
        output=output2
    readin2=open(output2)
    en_log=open(en_log, 'w')
    for key in site_number.keys():
        en_log.write(key+"\t"+str(site_number[key][0])+'\n')
    en_log.close()
    for line in readin2:
        line=line.rstrip()
        if line[0][0]=="@":
            continue
        else:
            line=line.split()
            if line[1]=="4":
                unmapfile.write("@"+line[0]+"\n")
                unmapfile.write(line[9]+"\n")
                unmapfile.write("+"+"\n")
                unmapfile.write(line[10]+"\n")
            else:
                samfile.write('\t'.join(line)+'\n')
    os.system("rm "+output2+" -f")
    readin2.close()
    samfile.close()
    unmapfile.close()
    if rmmiddle==1:
        os.system("rm "+unmapfilename+" -f")

def sortsam(samfile, cpu, nosortsam, outdir, nomapping, rmmiddle):
    filename=os.path.splitext(samfile)[0]
    filetype=os.path.splitext(samfile)[1]
    if nomapping==1:
        filename=outdir+"/"+filename
        #if not os.path.exists(outdir):## check the out_dir, and make it if there is not such a dir
         #   os.makedirs(outdir)
    bamfile=filename+"temp.bam"
    bamfile2=filename+".bam"
    if filetype==".sam":
        os.system("samtools view -b -o "+bamfile+" -@ "+str(cpu)+" -q 30 "+samfile)
    elif filetype==".bam":
        bamfile=samfile
    if nosortsam==0:
        os.system("samtools sort -n -O bam -@ "+str(cpu)+" -o "+bamfile2+" -T "+filename+" "+bamfile)
        os.system("rm -f "+bamfile)
    else:
        bamfile2=bamfile
    if rmmiddle==1:
        os.system("rm -f "+samfile)
    #os.system("bamToBed -i "+bamfile2+" >"+filename+".bed")
    #if rmmiddle==1:
    #    os.system("rm -f "+bamfile2)
def forpair(bamAfile, bamBfile, dis, cpu):
    pre=os.path.splitext(bamAfile)[0][0:-2]
    bamfile=pre+"_merge.bam"
    bedfile=pre+".bed"
    os.system("samtools merge "+bamfile+" "+bamAfile+" "+bamBfile+" -@ "+str(cpu)+" -f -n")
    os.system("bamToBed -i "+bamfile+" >"+bedfile)
    intrafile=pre+"_intra.bed"
    interfile=pre+"_inter.txt"
    toonearfile=pre+"_genome_DNA.txt"
    logfile=pre+"_forpair.log"
    intranum=0
    internum=0
    toonearnum=0
    pairnum=0
    bedA=open(bedfile)
    line1=bedA.readline().rstrip().split()
    intra=open(intrafile, 'w')
    inter=open(interfile, 'w')
    toonear=open(toonearfile, 'w')
    log=open(logfile, 'w')
    biaspair=0
    title=0
    A=[]
    sameid=[]
    sameid2=[]
    lastid=''
    B=0
    while line1:
        id1=int(line1[3].split('/')[0].split(':')[-1])
        if title==0:
            lastid=id1
            sameid.append(line1[0:3])
            title+=1    
            line1=bedA.readline().rstrip().split()
            continue
        else:
            if id1 == lastid:
                sameid.append(line1[0:3])
                line1=bedA.readline().rstrip().split()
                B=1
                continue
            elif id1 >lastid:
                B=0
            
                if len(sameid)>1:
                    #print sameid, '\n'
                    A=[]
                    for i in range(0, (len(sameid)-1)):
                        for j in range(i+1, len(sameid)):
                            pairnum+=1
                            if sameid[i][0]==sameid[j][0]:
                                if abs(int(sameid[i][1])-int(sameid[j][1]))<dis:
                                    toonearnum+=1
                                    left=min(int(sameid[i][1]), int(sameid[j][1]))
                                    right=max(int(sameid[i][1]), int(sameid[j][1]))
                                    toonear.write(str(left)+'\t'+sameid[i][0]+'\t'+str(right)+'\n')
                                    if i not in A:
                                        A.append(i)
                    for i in range(0, len(sameid)):
                        if i in A:
                            continue
                        else:
                            sameid2.append(sameid[i])
                    #print sameid2, '\n'
                    #print A, '\n'
                    if len(sameid2)>1:
                        for i in range(0, (len(sameid2)-1)):
                            for j in range(i+1, len(sameid2)):
                                biaspair+=1
                                if sameid2[i][0]==sameid2[j][0]:
                                    intranum+=1
                                    left=min(int(sameid2[i][1]), int(sameid2[j][1]))
                                    right=max(int(sameid2[i][1]), int(sameid2[j][1]))
                                    intra.write(str(left)+'\t'+sameid2[i][0]+'\t'+str(right)+'\n')
                                else:
                                    internum+=1
                                    inter.write('\t'.join(sameid2[i][0:3])+'\t'+'\t'.join(sameid2[j][0:3])+'\n')
                        biaspair-=1
                sameid=[]
                sameid2=[]
                sameid.append(line1[0:3])
                lastid=id1
                line1=bedA.readline().rstrip().split()
            else:
                print"bed file is not sorted!", '\n'
    if B==1:
        if len(sameid)>1:
            for i in range(0, (len(sameid)-1)):
                for j in range(i+1, len(sameid)):
                    pairnum+=1
                    if sameid[i][0]==sameid[j][0]:
                        if abs(int(sameid[i][1])-int(sameid[j][1]))<dis:
                            toonearnum+=1
                            left=min(int(sameid[i][1]), int(sameid[j][1]))
                            right=max(int(sameid[i][1]), int(sameid[j][1]))
                            toonear.write(str(left)+'\t'+sameid[i][0]+'\t'+str(right)+'\n')
                            A.append(i)
            for i in range(0, len(sameid)):
                if i in A:
                    continue
                else:
                    sameid2.append(sameid[i])
            if len(sameid2)>1:
                for i in range(0, (len(sameid2)-1)):
                    for j in range(i+1, len(sameid2)):
                        biaspair+=1
                        if sameid2[i][0]==sameid2[j][0]:
                            intranum+=1
                            left=min(int(sameid2[i][1]), int(sameid2[j][1]))
                            right=max(int(sameid2[i][1]), int(sameid2[j][1]))
                            intra.write(str(left)+'\t'+sameid2[i][0]+'\t'+str(right)+'\n')
                        else:
                            internum+=1
                            inter.write('\t'.join(sameid2[i][0:3])+'\t'+'\t'.join(sameid2[j][0:3])+'\n')

    intra.close()
    inter.close()
    toonear.close()
    log.write("Reads paired successfully: "+str(pairnum)+'\n')
    log.write("Reads of that are bias pair are: "+str(biaspair)+'\n')
    readleft=intranum+internum
    rmratio='%.2f' % (float(readleft)*100/float(pairnum))
    log.write("Reads are left are: "+str(readleft)+'\n')
    log.write("Kept ratio is(%): "+str(rmratio)+'\n')
    log.write("Intra reads number: "+str(intranum)+'\n')
    log.write("Inter reads number: "+str(internum)+'\n')
    log.write("Reads are too near: "+str(toonearnum)+'\n')
    log.close()
    #os.system("rm -f "+bedAfile)
def deverse(site):
    resite=''
    for i in range(0, len(site)):
        if site[i]=="A":
            resite+='T'
        elif site[i]=="T":
            resite+='A'
        elif site[i]=="C":
            resite+='G'
        elif site[i]=="G":
            resite+='C'
    resite=resite[::-1]
    return resite
def number_trans(innumber):
    outstr=''
    while innumber/1000>=1:
        out=innumber%1000
        innumber=innumber/1000
        if len(str(out))==2:
            outstr=','+"0"+str(out)+outstr
        elif len(str(out))==1:
            outstr=','+"00"+str(out)+outstr
        else:
            outstr=','+str(out)+outstr
    outstr=str(innumber)+outstr
    return outstr
if __name__=="__main__":
    opts, args=getopt.getopt(sys.argv[1:], "hi:p:m:n:o:s:g:5:3:e:d:r", ["help", "genome=", "site=", "nomap", "nosortsam", "distance=", "noremove", "noadd", "nodivide"])
    inputfiles=[]
    pairfiles=[]
    smarkers=[]
    output=""
    mis=2
    m=1
    nodivide=0
    leftend=0
    rightend=0
    out_dir="." 
    out_dirs=[","]
    smarker="s"
    tt=datetime.now()
    cpu=10
    genome="$bowtie_index"+"hg19"
    cys=[]
    sites=['GTA', 'CAT', 'CTA']
    nomapping=0
    notosortsam=0
    dis=500
    rmmiddle=1
    noadd=0
    for op, value in opts:
        if op in ("-h", "--help"):
            usage()
            sys.exit()
        if op=="-i":
            inputfiles=value.split(',')
        if op=="-p":
            pairfiles=value.split(',')
        if op=="-m":
            mis=int(value)
        if op=="-n":
            cpu=int(value)
        if op=="-o":
            out_dirs=value.split(',')
        if op=="-s":
            smarkers=value.split(',')
        if op in ("-g", "--genome"):
            genome=value
        if op=="-5":
            leftend=int(value)
        if op=="-3":
            rightend=int(value)
        if op in ("-e", "--site"):
            sites=value.split(',')
        if op=="--nomap":
            nomapping=1
        if op=="--nosortsam":
            notosortsam=1
        if op in ("-d", "--distance"):
            dis=int(value)
        if op in ("-r", "--noremove"):
            rmmiddle=0
        if op =="--noadd":
            noadd=1
        if op =="--nodivide":
            nodivide=1
    outdirsmarkers=[]
    if len(inputfiles)==len(pairfiles):
        if len(inputfiles)%len(out_dir)!=0:
                print "Warning! There must be some mistakes in -o parametre!!", '\n'
        else:
            for out_dir in (out_dirs):
                if not os.path.exists(out_dir):## check the out_dir, and make it if there is not such a dir
                    os.makedirs(out_dir)
                logssummary=out_dir+"/summary.log"
                logssummary=open(logssummary, 'w')
            newout_dirs=out_dirs*(len(inputfiles)/len(out_dirs))
            all_outdirs=newout_dirs*2

            for i in range(0, len(inputfiles)):
                fullmarker=newout_dirs[i]+"/"+smarkers[i]
                outdirsmarkers.append(fullmarker)
            if nomapping==0 and len(inputfiles)==len(smarkers):
                print "Analysis start......", '\n'
                if nodivide==0:
                    r=Parallel(n_jobs=len(inputfiles))(delayed(dividefiles)(inputfiles[i], pairfiles[i], newout_dirs[i], smarkers[i], i, leftend, rightend) for i in range(0, len(inputfiles)))
                resites=[]
                resite=''
                for site in sites:
                    resite=deverse(site)
                    resites.append(resite)
                A, B=zip(*r)
                all=A+B
                
                ss=datetime.now()-tt
                print "The time caused is : ", ss, '\n'
                
                print"Mapping start......", '\n'
                Parallel(n_jobs=len(all))(delayed(mapping)(noadd, all[i],mis, cpu,genome, sites, resites, rmmiddle) for i in range(0, len(all)))
                ss=datetime.now()-tt
                print "The time caused is : ", ss, '\n'
                
                maplog=''
                allreadsnumber=0
                s1mappednumber=0
                s2mappednumber=0
                s1mappedratio=0
                s2mappedratio=0
                for in1 in A:
                    pre=os.path.splitext(in1)[0]
                    maplog=pre+'.log'
                    maplogs=open(maplog)
                    linenum=0
                    sign_for_line1=0
                    for line in maplogs:
                        line=line.rstrip().split(":")
                        if line[0]=="# reads processed" and sign_for_line1==0:
                            allreadsnumber+=int(line[1].split(" ")[1])
                            sign_for_line1+=1
                        elif line[0]=="# reads with at least one reported alignment":
                            s1mappednumber+=int(line[1].split(" ")[1])
                        else:
                            continue
                s1mappedratio=float(s1mappednumber)*100/float(allreadsnumber)
                strallreadsnumber=number_trans(allreadsnumber)
                strs1mappednumber=number_trans(s1mappednumber)
                for in2 in B:
                    pre=os.path.splitext(in2)[0]
                    maplog=pre+'.log'
                    maplogs=open(maplog)
                    linenum=0
                    for line in maplogs:
                        line=line.rstrip().split(":")
                        if line[0]=="# reads with at least one reported alignment":
                            s2mappednumber+=int(line[1].split(" ")[1])
                        else:
                            continue
                s2mappedratio=float(s2mappednumber)*100/float(allreadsnumber)
                strs2mappednumber=number_trans(s2mappednumber)
                logssummary.write("ALL reads number"+"\t"+"S1 mapped number"+"\t"+"S1 mapped ratio(%)"+"\t"+"S2 mapped number"+"\t"+"S2 mapped ratio(%)"+"\n")
                logssummary.write(strallreadsnumber+"\t"+strs1mappednumber+"\t"+str('%.2f'%(s1mappedratio))+"\t"+strs2mappednumber+"\t"+str('%.2f'%(s2mappedratio))+"\n"+"\n")
                if rmmiddle==1:
                    for i in range(0, len(A)):
                        print "rm "+A[i]+" -f"+'\n'
                        os.system("rm "+A[i]+" -f")
                        print "rm "+B[i]+" -f"+'\n'
                        os.system("rm "+B[i]+" -f")
                samAs=[]
                samBs=[]
                for i in range(0, len(inputfiles)):
                    samA=newout_dirs[i]+"/"+smarkers[i]+"."+str(i)+".1.sam"
                    samB=newout_dirs[i]+"/"+smarkers[i]+"."+str(i)+".2.sam"
                    samAs.append(samA)
                    samBs.append(samB)
            elif nomapping==0 and len(inputfile)!=len(smarkers):
                print"Warning!There must be some mistakes in -s parametre!", '\n'
            else:
                samAs=inputfiles
                samBs=pairfiles
            allsams=samAs+samBs
            Parallel(n_jobs=len(allsams))(delayed(sortsam)(allsams[i], cpu, notosortsam, all_outdirs[i], nomapping, rmmiddle) for i in range(0, len(allsams)))
            #print"Samfiles are sorted and converted to bedfiles!",'\n' 
            print"Samfiles are sorted !",'\n' 
            ss=datetime.now()-tt
            print "The time caused is : ", ss, '\n'
                
                
            bamAfiles=[]
            bamBfiles=[]
            for i in range(0, len(samAs)):
                if nomapping==1:
                    bedA=newout_dirs[i]+"/"+os.path.splitext(samAs[i])[0]+".bam"
                    bedB=newout_dirs[i]+"/"+os.path.splitext(samBs[i])[0]+".bam"
                else:
                    bamA=os.path.splitext(samAs[i])[0]+".bam"
                    bamB=os.path.splitext(samBs[i])[0]+".bam"
                bamAfiles.append(bamA)
                bamBfiles.append(bamB)
            Parallel(n_jobs=len(bamAfiles))(delayed(forpair)(bamAfiles[i], bamBfiles[i], dis, cpu) for i in range(0, len(bamAfiles)))
            print"Pairing is finished!", '\n'
            ss=datetime.now()-tt
            print "The time caused is : ", ss, '\n'
            allpairednumber=0
            allbiaspairnumber=0
            allleftnumber=0
            allkeptratio=0
            allintranumber=0
            allinternumber=0
            allselfnumber=0
            for bamAfile in bamAfiles:
                pre=os.path.splitext(bamAfile)[0][0:-2]
                logfile=pre+"_forpair.log"
                pairlog=open(logfile)
                pairednumbers=0
                m=0
                for line in pairlog:
                    line=line.rstrip().split(': ')
                    pairednumbers=line[1]
                    if m%7==0:
                        allpairednumber+=int(pairednumbers)
                    elif m%7==1:
                        allbiaspairnumber+=int(pairednumbers)
                    elif m%7==2:
                        allleftnumber+=int(pairednumbers)
                    elif m%7==4:
                        allintranumber+=int(pairednumbers)
                    elif m%7==5:
                        allinternumber+=int(pairednumbers)
                    m+=1
            allkeptratio='%.2f'%(float(allleftnumber)*100/float(allpairednumber))
            logssummary.write("All paired"+"\t"+"Bias paired"+"\t"+"After removed genome DNA"+"\t"+"Kept ratio(%)"+"\t"+"Intra pets"+"\t"+"Inter pets"+"\n")
            logssummary.write(number_trans(allpairednumber)+"\t"+number_trans(allbiaspairnumber)+"\t"+number_trans(allleftnumber)+"\t"+str(allkeptratio)+"\t"+number_trans(allintranumber)+"\t"+number_trans(allinternumber)+"\n")
            markers=list(set(outdirsmarkers))
            for i in range(0, len(markers)):
                os.system("cat "+markers[i]+".*_intra.bed |awk '{if (!seen[$0]++){print $0;}}' >"+markers[i]+"_intra.bed")
                os.system("rm -f "+markers[i]+".*_intra.bed")
                #os.system("sort -k2,2 -k1,1n -k3,3n "+markers[i]+"_intra.bed >"+markers[i]+"_intra_sorted.bed")
                os.system("cat "+markers[i]+".*_inter.txt |awk '{if (!seen[$0]++){print $0;}}' >"+markers[i]+"_inter.txt")
                os.system("rm -f "+markers[i]+".*_inter.txt")
                #os.system("sort -k1,1 -k4,4 -k2,2n -k5,5n "+markers[i]+"_inter.txt >"+markers[i]+"_inter_sorted.txt")
                os.system("wc -l "+markers[i]+"_intra.bed >"+markers[i]+"_rmdup.txt")
                os.system("wc -l "+markers[i]+"_inter.txt >>"+markers[i]+"_rmdup.txt")
                duplog=open(markers[i]+"_rmdup.txt")
                alldupnumber=[]
                for line in duplog:
                    line=line.rstrip().split()
                    alldupnumber.append(line[0])
                if allintranumber>0 :
                    intrakeptratio='%.2f'%(float(alldupnumber[0])/float(allintranumber))
                else :
                    intrakeptratio="0.00"
                if allinternumber>0:
                    interkeptratio='%.2f'%(float(alldupnumber[1])/float(allinternumber))
                else:
                    interkeptratio="0.00"
                logssummary.write("\n")
                logssummary.write("Unique intra pets"+"\t"+"Kept ratio(%)"+"\t"+"Unique inter pets"+"\t"+"Kept ratio(%)"+"\n")
                logssummary.write(number_trans(int(alldupnumber[0]))+"\t"+intrakeptratio+"\t"+number_trans(int(alldupnumber[1]))+"\t"+interkeptratio+"\n")
                if rmmiddle==1:
                    os.system("rm -f "+markers[i]+"_inter.txt")
                    os.system("rm -f "+markers[i]+"_intra.bed")
                    os.system("rm -f "+markers[i]+"_rmdup.txt")
            print "All are done!", '\n'
            ss=datetime.now()-tt
            print "The time caused is : ", ss, '\n'

    else:
        print"The files must be paired!!", '\n'
    logssummary.close()
