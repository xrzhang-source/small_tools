# small tools

These are small tools for NGS data analysis by Xiaoran Zhang(xrzhang0525@gmail.com)

###package/tools dependency

python2.7+, 
Perl


## Installation

Download the code and add the codes to your PATH.

##tutorial

### this is a small tool for paired two big files by the same index. 

```
bedForPair.py -h

-h useange()

-i inputfile, merged filename,sorted by the name

-o outputfile, file name

-c columon, number,default=4
```

### this is a small tool to got common data from two files by the same index
```
commom_column.py inputfile1 inputfile2 column number1 column_number2
```
### this is a small tool to trim matrix with a threshold of the min value
```
cut_zero.py -h

-i inputfile

-c rm clumons which are not to check , it shoule be separed by ', ', defalut none

-t not to check the frist line, default yes

--nk not to keep the title, only use it if you choose -t and want to rm the title in the output

-o if you want to change the name, use it, if not , ignore it

-z if you want to cut them from a zero value, use it, default:0.0

-n if you want to rm n rows less than z value, use it ,default:all
```
### this is a small tool to extend peaks bed files from the summit 
```
extend_from_summit.py -h

-h --help useange()

-i: inputfile

-o: outputfile

-g: chromsize file

-l: length, the length of the whole peak, default=0,

-f: the float percentange to extend of the whole peak, default:use -l

-s: the col number of the summit, default:none

-m: the col number of the summit is the length from the start end, default:not

-e: extend half of -l from the start and end, default:not

-t: the input file have a header in the frist line, default:not

-k: keep the input file have a header in the frist line, default:not

-d: the result can be different length if start is less than 0 and max more than the chrome size, default:not
```
### this is a small tool to merge files by the same index, it will keep all the index from the inputfile.
```
merge_profile.py -h

usage:merge_profile.py -i inputfile -p plusfile1, plusfile2, ..., plusfilen -o outputfile

-n ( if you want sort you can choose this parameter,  by the n column, default :not sort, and if you sort , you'd better choose -b 1 )

   if you choose -n, do only one merge_profile.py in one folder

-b (1 or 2, 1 rm the frist row, 2 not, and default :2)

-k if you choose it, means you choose -b 1 and keep a new sample header like gene_name 1 2 3... in the result, default:not

-c cut this column in the result, default: none

-1 the column of the key in inputfile, default: 1

-2 the column of the key in plusfile, default: 1
```
### this is a small tool to merge big files.
numpy >= 1.17.3
```
merge_profile_bigdata.py -h
usage: merge_profile_bigdata.py [-h] -i INPUT -p PLUSFILES -o OUTPUT
                                [-s SEPARATOR] [-c1 COLUMN_INPUT]
                                [-c2 COLUMN_PLUS]

Merge different files based on specified columns.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file path
  -p PLUSFILES, --plusfiles PLUSFILES
                        Comma-separated list of plus files
  -o OUTPUT, --output OUTPUT
                        Output file path
  -s SEPARATOR, --separator SEPARATOR
                        Separator for the input and plus files
  -c1 COLUMN_INPUT, --column_input COLUMN_INPUT
                        Column number for merging in the input file
  -c2 COLUMN_PLUS, --column_plus COLUMN_PLUS
                        Column number for merging in plus files
```
### this is a small tool for split a file to different files by one index
```
split_files.py -h
-h --help useange()

python 2 only

-i: inputfile

-o: outputfile index

-c: markers columns, split by ,

-k; not keep the markers in the result, defalut:yes

-a: add the index before the markers in the file name, default:not

-t: if the file have a title,choose it, default:not

-r: rm the title in the result files, default:not,only choose it when -t is choosed
```
### this is a perl package for a gene expression table: #sum    average    mid    diff    fold    std   fano       zscore    pearson#
```
#$sum=sum(@array)                       # sum of the array
#$average=average(@array)               # average num of the array
#$mid=mid(@array)                       # middle num of the array
#$quarter1=quarter1(@array)               # 1/4 num of the array
#$quarter3=quarter3(@array)               # 3/4 num of the array
#$diff=diff(@array)                     # maxnum-minnum
#$fold=fold(@array)                     # maxnum/minnum
#$min=min(@array)                       # min
#$max=max(@array)                       # max
#$std=std(@array)                       # standard deviation of the array
#$fano=fano(@array)                       # standard deviation of the array
#@zscore=zscore(@array)                 # transform to zscore
#$pearson=pearson(\@array1,\@array2)    # pearson correlation of array1 and array2, be sure the input is pointer format
#$one=one(@array)                                               # one of the element match the condition
#$all=all(@array)                                               # all of the element match the condition
#@lm=lm(\@array1,\@array2)              # lm
#@gini=lm(@array)               # gini
#$ttest=lm(\@array1,\@array2)                   # ttest
```

Contact: xrzhang0525@gmail.com 




