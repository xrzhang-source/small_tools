#!/usr/bin/perl
#
use strict;
use warnings;

package Numcal;
require Exporter;

our @ISA=qw(Exporter);
our @EXPORT=qw(sum average mid diff max min fold std fano zscore tscore pearson lm ttest merge gini quarter1 quarter3);
our @VERSION=1.00;


#################usage####################
#sum    average	   mid    diff    fold    std   fano	   zscore    pearson#
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
#$one=one(@array)						# one of the element match the condition
#$all=all(@array)						# all of the element match the condition
#@lm=lm(\@array1,\@array2)    		# lm
#@gini=lm(@array)    		# gini
#$ttest=lm(\@array1,\@array2)    		# ttest
#################usage####################

#$sum=sum(@array)                       # sum of the array
sub sum{
	my $sum=0;
	$sum+=$_ for @_;
    $sum;
}

#$tscore=tscore(@array)                       # sum of the array
sub tscore{
    my @list=@_;
	my $max=max(@list);
    my $sum_t=0;
    for my $num(0..$#list){
        $sum_t+=1-($list[$num]/$max);
    }
    my $ts=$sum_t/$#list;
    return $ts;
}

#$average=average(@array)  #average num of the array
sub average{
	my $sum=0;
	$sum+=$_ for @_;
	my $count=@_;
    my $average=$sum/$count;
	$average;
}

#$mid=mid(@array)          # middle num of the array
sub mid{
	my @list=sort {$a<=>$b} @_;
	my $count=@list;
	my $mid;
	if($count==0){
		return 0;
		die "Kidding me?";
	}
	if ($count%2==1){
		$mid=$list[($count-1)/2];
	}
	elsif ($count%2==0){
		$mid=($list[$count/2-1]+$list[$count/2])/2;
	}
	$mid;
}

#$quarter1=quarter1(@array)          # 1/4 num of the array
sub quarter1{
	my @list=sort {$a<=>$b} @_;
	my $count=@list;
	my $quarter1;
	if($count==0){
		return 0;
		die "Kidding me?";
	}
    else{
		$quarter1=$list[int(($count-1)/4)+1];
	}
	$quarter1;
}
#$quarter3=quarter3(@array)          # 3/4 num of the array
sub quarter3{
	my @list=sort {$a<=>$b} @_;
	my $count=@list;
	my $quarter3;
	if($count==0){
		return 0;
		die "Kidding me?";
	}
    else{
		$quarter3=$list[int(($count-1)/4*3)];
	}
	$quarter3;
}


#$diff=diff(@array)         # maxnum-minnum
sub diff{
	my @list;
	for my $num(@_){
		next if $num=~/NULL/;
		push @list,$num;
	}
	my @sort_list=sort{$a<=>$b} @list;
	my $diff=$sort_list[-1]-$sort_list[0];
	$diff;
}

#$fold=fold(@array)         # maxnum/minnum
sub fold{
	my @sort_list=sort {$a<=>$b} @_;
	my $fold=($sort_list[-1]+1)/($sort_list[0]+1);
	$fold;
}

sub max{
	my @sort_list=sort {$a<=>$b} @_;
	my $max=$sort_list[-1];
	$max;
}

sub min{
	my @sort_list=sort {$a<=>$b} @_;
	my $min=$sort_list[0];
	$min;
}

#$std=std(@array)           # standard deviation of the array
sub std{
	my $average=average(@_);
	my $up=0;
	$up+=($_-$average)**2 for (@_);
	my $std=sqrt($up/($#_));
	return $std;
}

sub fano{
	my $average=average(@_);
	my $up=0;
	$up+=($_-$average)**2 for (@_);
	my $var=($up/($#_));
    my $fano=$var/$average;
	return $fano;
}

#@zscore=zscore(@array)     # transform to zscore
sub zscore{
	my $average=average(@_);
	my $up=0;
	$up+=($_-$average)**2 for (@_);
	my $std=sqrt($up/($#_));
	my @zscore;
	for (@_){
		my $zscore=($_-$average)/$std;
		push @zscore,$zscore;
	}
	return @zscore;
}

#$pearson=pearson(\@array1,\@array2)   # pearson correlation of array1 and array2, be sure the input is pointer format
sub pearson{
	my @a=(@_);
	my @array1=@{$a[0]};
	my @array2=@{$a[1]};
	my $avr1=average(@array1);
	my $avr2=average(@array2);
	my $up=0;
	my $down1=0;
	my $down2=0;
	for my $num(0..$#array1){
		$up+=($array1[$num]-$avr1)*($array2[$num]-$avr2);
		$down1+=($array1[$num]-$avr1)**2;
		$down2+=($array2[$num]-$avr2)**2;
	}
	my $pearson=$up/(sqrt($down1)*sqrt($down2));
	return $pearson;
}

sub lm{
	my @a=(@_);
	my @array1=@{$a[0]};
	my @array2=@{$a[1]};
	my $avr1=average(@array1);
	my $avr2=average(@array2);
	my $slope=0;
	my $intercept=0;
	for my $num (0..$#array1) {
		$slope+=($array1[$num]-$avr1)*($array2[$num]-$avr2);
		$intercept+=($array1[$num]-$avr1)**2;
	}
	$slope/=$intercept;
	$intercept=$avr2-$slope*$avr1;
	my @lm=($slope,$intercept);
	return @lm;
}

sub ttest{
	my @a=(@_);
	my @array1=@{$a[0]};
	my @array2=@{$a[1]};
	my $avr1=average(@array1);
	my $avr2=average(@array2);
    my $s1=std(@array1);
    my $s2=std(@array2);
    my $down=sqrt(($s1**2/($#array1+1)+$s2**2/($#array2+1))) if $s1!=$s2;
    $down=sqrt(sqrt(($#array1*($s1**2)+$#array2*($s2**2))/($#array1+$#array2)))*sqrt(1/($#array1+1)+(1/($#array2+1))) if $s1==$s2;
    my $ttest=($avr1-$avr2)/$down;
	return $ttest;
}


sub merge{
	my @a=(@_);
	my @sort_a=sort {$a<=>$b} @a;
	my $min=0;
	my $max=0;
	my @array;
	for my $num (0..$#sort_a-1){
		if ($sort_a[$num]!=$sort_a[$num+1]-1){
			$min=$sort_a[$num] if $min==0;
			$max=$sort_a[$num];
			my $loc=join " ",$min,$sort_a[$num];
			push @array,$loc;
			$loc=join " ",$sort_a[$#sort_a],$sort_a[$#sort_a] if $num==$#sort_a-1;
			push @array,$loc if $num==$#sort_a-1;
			$min=0;
		}
		elsif ($sort_a[$num]==$sort_a[$num+1]-1){
			$min=$sort_a[$num] if $min==0;
			my $loc=join " ",$min,$sort_a[$#sort_a] if $num==$#sort_a-1;
			push @array,$loc if $num==$#sort_a-1;
		}
	}
	return @array;
}

#$gini=gini(@array)           # gini index of the array
sub gini{
    my @array=@_;
    for my $num (0..$#array){
        $array[$num]+=0.0000001;
    }
    my @sort_array=sort{$a<=>$b} @array;
    my $sum_up=0;
    my $sum_down=0;
    my $count=1;
    for my $num(0..$#sort_array){
        $sum_up+=(2*$count-$#sort_array-2)*$sort_array[$num];
        my $sum_temp=(2*$count-$#sort_array-2);
        $sum_down+=$sort_array[$num];
        $count++;
    }
    my $gini=$sum_up/(($#sort_array+1)*$sum_down);
    return $gini;
}


1;
