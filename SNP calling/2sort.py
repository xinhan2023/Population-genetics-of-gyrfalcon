import sys

file1 = sys.argv[1]

with open(f'{file1}.sh', "w") as f1:
	f1.write(f'''#!/bin/bash
#PBS    -N {file1}
#PBS    -l nodes=1:ppn=8
#PBS    -l mem=40g
#PBS    -q batch
#PBS    -V
PICARD=picard.jar
ref=gyr.newchr.fa
samtools=samtools
road=./
bwa=bwa
fastp -i {file1}_1.fq.gz -I {file1}_2.fq.gz -o clean_1.fq.gz -O clean_2.fq.gz -q 15 --adapter_sequence AAGTCGGAGGCCAAGCGGTCTTAGGAAGACAA \\
	--adapter_sequence_r2 AAGTCGGATCGTAGCCATGTCGTTCTGTGAGCCAAGGAGTTG -f 2 -t 2 -M 10 -l 30 -W 30
$bwa mem -t 8 -M -R "@RG\\\\tID:{file1}\\\\tLB:{file1}\\\\tPL:ILLUMINA\\\\tSM:{file1}" $ref $road/{file1}/clean_1.fq.gz $road/{file1}/clean_2.fq.gz | $samtools view -bS - > {file1}.bam

java -Djava.io.tmpdir=temp -Xmx40g -jar $PICARD SortSam \\
	I={file1}.bam \\
	O={file1}.sort.bam \\
	SORT_ORDER=coordinate

java -Djava.io.tmpdir=temp -Xmx40g -jar $PICARD MarkDuplicates \\
	I={file1}.sort.bam \\
	O={file1}.clean.sort.dedup.bam \\
	M={file1}.clean.sort.dedup.text \\
	CREATE_INDEX=true \\
	VALIDATION_STRINGENCY=LENIENT \\
	REMOVE_DUPLICATES=true 
''')

