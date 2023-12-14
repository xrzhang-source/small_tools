#!/usr/bin/env perl
#########################################################################
# File Name: HTcount2RPKM.pl
# Author: Rui
# mail: dongruipicb@gmail.com
# Created Time: Wed 04 Jan 2017 09:50:23 AM CST
#########################################################################

use strict;
use warnings;
use Getopt::Long;
use Overlap;

sub usage {
	print <<"END_USAGE";
Usage: perl $0
	--htcount 
	--gtf 
	--total	 total mapped reads/fragment 
	--output 
END_USAGE
	exit;
}

my ($htcount,$gtf,$total,$output);
GetOptions (
	'htcount=s'=>\$htcount,
	'gtf=s'=>\$gtf,
	'total=s'=>\$total,
	'output=s'=>\$output,
) or usage();
usage() if (!$htcount or !$gtf or !$output);

print "Warning!!! No total reads input, counts in all genes from gtf will be used.\n" if !$total;
open my $gtf_in,"$gtf";
my %hash_gtf;
while (<$gtf_in>){
    next if $_=~/\#/;
	chomp;
	my @loc=split;
	my @F=split(/gene_name/,$_);
	my @gene_id=split(/\;/,$F[1]);
	$gene_id[0]=~s/\"| //g;
	my $loc=join "\t",@loc[0,3,4];
	push @{$hash_gtf{$gene_id[0]}},$loc;
}
close $gtf_in;
###calculate gene length###
my %hash_length;
for my $key(keys %hash_gtf){
	my $gene_length;
	my %hash_judge;
	my @loc=@{$hash_gtf{$key}};
	for my $loc(@loc){
		my @seq_loc=split(/\t/,$loc);
		$hash_judge{$seq_loc[0]}=1;
	}
	my @judge=keys %hash_judge;
	if ($#judge==0){
		my @overlap_array;
		for my $loc(@loc){
			my @seq_loc=split(/\t/,$loc);
			push @overlap_array,[@seq_loc[1,2]];
		}
		$gene_length=overlap(@overlap_array);
		$hash_length{$key}=$gene_length;
	}
}
######

open my $htcount_in,"$htcount";
my %hash_count;
my $sum=0;
while (<$htcount_in>){
	chomp;
	next if $_=~/lines|SAM line|SAM alignment|^__/i;
	my @F=split;
	$sum+=$F[1] if !$total;
	$hash_count{$F[0]}=$F[1];
}
my @test=keys %hash_count;

close $htcount_in;
open my $out_file,">$output";

for my $keys(keys %hash_count){
    next if !$hash_length{$keys} or $hash_length{$keys}==0;
	my $rpkm=$hash_count{$keys}/$hash_length{$keys}/$sum*1000000000 if !$total;
	$rpkm=$hash_count{$keys}/$hash_length{$keys}/$total*1000000000 if $total;
	print $out_file "$keys\t$rpkm\n";
}
close $out_file;
