#USAGE:python 01.py name chrom
import itertools
from sys import argv
def chromosome(chrom):
    with open(chrom) as f:
        chromosomes = [line.strip() for line in f]
    return chromosomes

def load_name_list(name_file):
    nameList = []
    with open(name_file) as f:
        for name in f:
            nameList.append(name.strip())
    return nameList


def produce(nameList,CHROM):
    for n in nameList:
        for chrom in CHROM:
            with open(f'{n}_{chrom}_gv.sh','w') as f:
                f.write(f'''#!/bin/sh
#PBS    -N {chrom}_{n}
#PBS    -l nodes=1:ppn=1
#PBS    -q batch
#PBS    -V
export gatk=gatk
export BAM=BAM
export ref=*.fa
$gatk --java-options \"-XX:ParallelGCThreads=3 -Xmx10g -Djava.io.tmpdir=temp/\" HaplotypeCaller \\
	-R $ref \\
	-ERC GVCF \\
	-L {chrom} \\
	-I $BAM/{n}.clean.sort.dedup.bam \\
	-O {n}_{chrom}.g.vcf.gz
''')
def main():
    nameList = load_name_list(argv[1])
    CHROM = chromosome(argv[2])
    produce(nameList,CHROM)
main()


