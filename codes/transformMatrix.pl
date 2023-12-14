#!/usr/bin/env perl
#########################################################################
# File Name: circ_Alu_count.pl
# Author: Rui
# mail: dongruipicb@gmail.com
# Created Time: Thu 28 Aug 2014 09:47:03 PM CST
#########################################################################

use strict;
use warnings;
use Getopt::Long;

sub usage {
    print <<"END_USAGE";
Usage: perl $0
    --in  
    --sep
END_USAGE
        exit;
}

my ($in,$sep);
GetOptions (
        'in=s'=>\$in,
        'sep=s'=>\$sep,
) or usage();
usage() if (!$in);

#$sep="\t" if (!$sep);
open my $file_in,"$in";
my $i=0;
my @data;
while(<$file_in>){
    chomp;
    my @line;
    if (!$sep){
        @line=split(/\t/,$_);
    }
    else{
        @line=split(/$sep/,$_);
    }
    for my $k(0 .. $#line){
        $data[$k][$i]=$line[$k];
    }
    $i++;
}
close $file_in;
for (@data){
    if (!$sep){
        print join("\t",@{$_}),"\n";
    }
    else{
        print join($sep,@{$_}),"\n";
    }
}

