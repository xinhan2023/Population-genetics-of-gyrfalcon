def psmc1(sample):
    with open(f'psmc1{sample}.sh','w') as f:
        f.write(f'''# !/bin/bash
# PBS    -N psmc{sample}
# PBS    -l nodes=1:ppn=1
# PBS    -q batch
# PBS    -V
export ref=fa
export road=BAM
export bcftools=bcftools
$bcftools mpileup -f $ref $road/{sample}.clean.sort.dedup.bam \\
	| $bcftools call -c - | vcfutils.pl vcf2fq -d 10 -D 100 | gzip > {sample}.fq.gz
export ROAD=psmc
$ROAD/utils/fq2psmcfa -q20 {sample}.fq.gz > {sample}.psmcfa
$ROAD/utils/splitfa {sample}.psmcfa > split.{sample}.psmcfa
$ROAD/psmc -N25 -t15 -r5 -p "4+25*2+4+6" -o {sample}.psmc {sample}.psmcfa
''')


from sys import argv
psmc1(argv[1])

