#!/bin/bash
#PBS    -N Gather
#PBS    -l nodes=1:ppn=1
#PBS    -l mem=3G
#PBS    -q batch
#PBS    -V
export gatk=/public/software/gatk-4.0.7.0/gatk
# GatherVcfs
$gatk GatherVcfs -I autosome -O Autosome.vcf.gz
zcat Autosome.vcf.gz | awk '$0~/#/ || ($7 =="PASS"){print $0}' |bgzip > Autosome.pass.vcf.gz
