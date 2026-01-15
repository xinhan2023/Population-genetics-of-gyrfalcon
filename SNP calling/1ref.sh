#!/bin/sh
#PBS    -N ref
#PBS    -l nodes=1:ppn=2
#PBS    -q batch
bwa=/software/bwa/bwa-0.7.17/bwa
picard=/software/picard.jar

iTools Fatools regenerate -InPut gyr_scaffold.fa -OutPut gyr.newchr.fa -InsertN 500 -Length 30000000 -NoOutgz
$bwa index gyr.newchr.fa -p gyr.newchr.fa
java -Djava.io.tmpdir=temp -Xmx4g -jar $picard CreateSequenceDictionary \
	R=gyr.newchr.fa \
	O=gyr.newchr.dict
samtools faidx gyr.newchr.fa

