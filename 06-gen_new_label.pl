#!/usr/bin/perl

use 5.18.2;
use strict;
use warnings;

my (@all_time, @sheng, @yun, @gen_label, @gen_phone);

#system ("rm -rf label/new-01");
#system ("mkdir -p label/new-01");
#system ("rm -rf interval");
#system ("mkdir -p interval");

#+++++++++++++++++++++依次读取每个文件+++++++++++++++++++++

my ($read_file_path,$file_name);

while ($read_file_path = glob "interval/*.interval"){		#获取路径下所有文件路径；

	if ($read_file_path =~ m/1[0-9]{5,6}/){		#提取文件名；

		$file_name = $&;
		say "Start processing file $file_name.";
		#&revise_interval($file_name);
		&read_time_from_yinsu($file_name);
		&read_interval_yinsu($file_name);
		&read_label_from_gen($file_name);
		&gen_label($file_name);
		
		(@all_time, @sheng, @yun, @gen_label, @gen_phone) = ();
		
	}
}

#+++++++++++++++++++++++生成标注信息+++++++++++++++++++++++++

sub gen_label{
	
	my $label_file_name = $_[0];
	open (OUTPUT_new_LABEL, '>', "label/new-01/$label_file_name.lab")||die("Can not open label/new-01/$label_file_name.lab!$!\n");
	my (@label_array,$label_new_list);		#以数组方式储存标注信息，最后转化为标注list；

	my $syllable_num = 0;		#计数器，音节信息；
	my $phoneme_num = 0;		#计数器，音素信息；
	
#	print join "\t", @gen_phone;
#	print "\n";
#	print join "\t", @sheng;
#	print "\n";
#	print join "\t", @yun;
#	print "\n";
#	print join "\n", @gen_label;
#	print "\n";

	#@all_time——音素级; @sheng——音节级; @gen_label——音节级;

	for ($syllable_num = 0; $syllable_num <= $#sheng; $syllable_num++){
			if ($phoneme_num == 0){
				$label_array[0] = 0;
				$label_array[1] = $all_time[$phoneme_num];
			} elsif ($phoneme_num == $#all_time) {
				$label_array[0] = $all_time[$phoneme_num-1];
				$label_array[1] = $all_time[$phoneme_num];
		        } else {
				$label_array[0] = $all_time[$phoneme_num-1];
				$label_array[1] = $all_time[$phoneme_num];
				$label_array[2] = $all_time[$phoneme_num+1];
			}
			
			if ($sheng[$syllable_num] =~ m/nil|sil|sp|rr|zero/){
				$label_new_list = "$label_array[0] $label_array[1] -$yun[$syllable_num]+$gen_label[$syllable_num]\n";
				#$label_new_list = "$label_array[0] $label_array[1] -$gen_label[$syllable_num]\n";
				print OUTPUT_new_LABEL $label_new_list;
				$phoneme_num++;
			} else {
				$label_new_list = "$label_array[0] $label_array[1] -$sheng[$syllable_num]+$gen_label[$syllable_num]\n";
				#$label_new_list = "$label_array[0] $label_array[2] -$gen_label[$syllable_num]\n";
				print OUTPUT_new_LABEL $label_new_list;
				$phoneme_num++;
				$label_new_list = "$label_array[1] $label_array[2] -$yun[$syllable_num]+$gen_label[$syllable_num]\n";
				#$label_new_list = "$label_array[0] $label_array[2] -$gen_label[$syllable_num]\n";
				print OUTPUT_new_LABEL $label_new_list;
				$phoneme_num++;
			} 			
	}
	close OUTPUT_new_LABEL;
}

#+++++++++++++读取gen_label文件，提取音节标注信息+++++++++++++++++++++

sub read_label_from_gen{

	my $yinsu_file_name = $_[0];
	open (FILE_GEN_LABEL, "label/old/$yinsu_file_name.lab")||die("Can not open label/old/$yinsu_file_name.lab!$!\n");
	
	my ($INPUT_LABEL);
	
	while ($INPUT_LABEL = <FILE_GEN_LABEL>){		#逐行输入文本文件；
		$INPUT_LABEL =~ s/\s+//g;
		$INPUT_LABEL =~ s/^\d+//g;
		$INPUT_LABEL =~ s/^-//g;
		
		$INPUT_LABEL =~ s/sp\+nil/sp\+sp/g;
		$INPUT_LABEL =~ s/sp-nil/sp-sp/g;
		$INPUT_LABEL =~ s/sil\+nil/sil\+sil/g;
		$INPUT_LABEL =~ s/sil-nil/sil-sil/g;
		$INPUT_LABEL =~ s/_x\/B:/_0\/B:/g;
		$INPUT_LABEL =~ s/\@x\/C:/\@0\/C:/g;
		$INPUT_LABEL =~ s/\|x\/D:/\|0\/D:/g;
		$INPUT_LABEL =~ s/D:x#x\$x\@x=x-x&x_x\@x-x/D:0#0\$0\@0=0-0&0_0\@0-0/g;
		$INPUT_LABEL =~ s/E:x&x\^x\|x-x!x\^x\+x!x#x/E:0&0\^0\|0-0!0\^0\+0!0#0/g;

		if ($INPUT_LABEL =~ m/nil|sil|sp|rr|([a-zA-Z]{1,5})/){
			push @gen_phone,$&;
		}
		push @gen_label,$INPUT_LABEL;
	}
	close FILE_GEN_LABEL;
}


#+++++++++++++读取interval文件，修改interval格式+++++++++++++++++++++

sub revise_interval{

	my $yinsu_file_name = $_[0];
	open (FILE_YINSU, "interval-01/$yinsu_file_name.TextGrid")||die("Can not open interval-01/$yinsu_file_name.TextGrid!$!\n");
	open (OUTPUT_INTERVAL, '>', "interval/$yinsu_file_name.interval")||die("Can not open interval/$yinsu_file_name.interval!$!\n");
	
	my $i = 0; my ($INPUT_YINSU,$LAST_STRING);
	
	while ($INPUT_YINSU = <FILE_YINSU>){		#逐行输入文本文件；
		$INPUT_YINSU =~ s/^\s+//g;	
		if ($i > 14){				#从第n行开始匹配；
			unless ($INPUT_YINSU =~ /interval/){
				$INPUT_YINSU =~ s/^xmin = //g;
				$INPUT_YINSU =~ s/^xmax = //g;
				$INPUT_YINSU =~ s/^text = //g;
				print OUTPUT_INTERVAL $INPUT_YINSU;	
			}
		} else {
			print OUTPUT_INTERVAL $INPUT_YINSU;
		}
		$i++;		#计数器，累计读取文件行数；
	}

	close OUTPUT_INTERVAL;
	close FILE_YINSU;
}


#+++++++++++++读取interval文件，提取时间（音素）+++++++++++++++++++++

sub read_time_from_yinsu{

	my $yinsu_file_name = $_[0];
	open (FILE_YINSU, "interval/$yinsu_file_name.interval")||die("Can not open interval/$yinsu_file_name.interval!$!\n");
	
	my $i = 0; my ($INPUT_YINSU,$LAST_STRING);
	
	while ($INPUT_YINSU = <FILE_YINSU>){		#逐行输入文本文件；
		if ($i > 12){				#从第n行开始匹配；
			$INPUT_YINSU =~ s/\s+//g;
			if ($INPUT_YINSU =~ m/nil|sil|sp|rr|([a-zA-Z]{1,5})/){	#匹配音素截止时间单元；
				$LAST_STRING *= 10000000; 
				$LAST_STRING = int($LAST_STRING);
				push @all_time,$LAST_STRING;			#前一字符串为所有音素截止时间；截止时间存入数组；
			}
			$LAST_STRING = $INPUT_YINSU;	#暂存当前字符串；
		}
		$i++;		#计数器，累计读取文件行数；
	}
	close FILE_YINSU;
}

#+++++++++++++++读取interval文件，提取声韵母+++++++++++++++++++++

sub read_interval_yinsu{

	my $yinsu_file_name = $_[0];
	open (FILE_YINSU, "interval/$yinsu_file_name.interval")||die("Can not open interval/$yinsu_file_name.interval!$!\n");

	my $i = 0; my ($INPUT_YINSU,$LAST_YINSU); 
	
	while ($INPUT_YINSU = <FILE_YINSU>){		#逐行输入文本文件；
		if ($i > 12){				#从第n行开始匹配；
			$INPUT_YINSU =~ s/\s+//g;	
			if ($INPUT_YINSU =~ m/"sil"|"sp"/){
				if ($INPUT_YINSU =~ m/"sil"/){
					$LAST_YINSU = $INPUT_YINSU;
					push @sheng,"sil";
					push @yun,"sil";
				} else {
					$LAST_YINSU = $INPUT_YINSU;
					push @sheng,"sp";
					push @yun,"sp";
				}
			} elsif ($INPUT_YINSU =~ m/"[a-z]{1,5}"/){	#匹配是否为声母；
				if ($INPUT_YINSU =~ m/"rr"/){
					$LAST_YINSU = $INPUT_YINSU;
					$INPUT_YINSU =~ s/"//g;
					push @sheng,"rr";
					push @yun,"rr";
				} else {
					$LAST_YINSU = $INPUT_YINSU;
					$INPUT_YINSU =~ s/"//g;
					push @sheng,$INPUT_YINSU;
				}
			} elsif ($INPUT_YINSU =~ m/"[a-z]{1,5}\d+"|[A-Z]{4}\d+/){	#匹配是否为韵母；
				if ($LAST_YINSU =~ m/"sil"|"sp"|"rr"/){		#若前一音素为静音，为零声母；
					$LAST_YINSU = $INPUT_YINSU;
					$INPUT_YINSU =~ s/"//g;
					$INPUT_YINSU =~ s/\d//g;
					push @sheng,"zero";
					push @yun,$INPUT_YINSU;
				} elsif ($LAST_YINSU =~ m/"[a-z]{1,5}"/){	#若前一音素为声母，正常；
					$LAST_YINSU = $INPUT_YINSU;
					$INPUT_YINSU =~ s/"//g;
					$INPUT_YINSU =~ s/\d//g;
					push @yun,$INPUT_YINSU;
				} elsif ($LAST_YINSU =~ m/"[a-z]{1,5}\d+"|[A-Z]{4}\d+/){	#若前一音素为韵母，为零声母；
					$LAST_YINSU = $INPUT_YINSU;
					$INPUT_YINSU =~ s/"//g;
					$INPUT_YINSU =~ s/\d//g;
					push @sheng,"zero";
					push @yun,$INPUT_YINSU;
				}
			} else { if ($INPUT_YINSU =~ m/"/) {say "$INPUT_YINSU can not be classified!"}}
		}
		$i++;		#计数器，累计读取文件行数；
	}
	
	close FILE_YINSU;
}
