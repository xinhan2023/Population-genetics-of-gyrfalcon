def load_name_list(name_file):
	nameList = []
	with open(name_file) as f:
		for name in f:
			nameList.append(name.strip())
	return nameList
def produce(nameList):
	for i in nameList:
		with open(f'{i}_SNP.sh','w') as f:								
			f.write(f'''#!/bin/bash
#PBS    -N {i}
#PBS    -l nodes=1:ppn=3
#PBS    -q batch
#PBS    -V
export gatk=gatk
export ref=*.fa
$gatk --java-options \"-XX:ParallelGCThreads=3 -Xmx20g -Djava.io.tmpdir=temp\" CombineGVCFs \\
	-R $ref \\
	-V {i}.list \\
	-O {i}.merge.g.vcf.gz
   
$gatk --java-options \"-XX:ParallelGCThreads=3 -Xmx20g -Djava.io.tmpdir=temp/\" GenotypeGVCFs \\
	-R $ref \\
	-G StandardAnnotation -new-qual \\
	-V {i}.merge.g.vcf.gz \\
	-O {i}.vcf.gz
   
$gatk --java-options \"-XX:ParallelGCThreads=3 -Xmx40g -Djava.io.tmpdir=temp/\" SelectVariants \\
	-R $ref \\
	-V {i}.vcf.gz \\
	--select-type-to-include SNP \\
	-O {i}.raw.SNP.vcf.gz

$gatk --java-options \"-XX:ParallelGCThreads=3 -Xmx40g -Djava.io.tmpdir=temp/\" VariantFiltration \\
	-R $ref \\
	-V {i}.raw.SNP.vcf.gz \\
	--filter-expression "DP < (1/3 sum DP) || DP > (3 sum DP) || QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 || SOR > 3.0" \\
	--filter-name filtered \\
	-O {i}.filter.SNP.vcf.gz

$gatk --java-options \"-XX:ParallelGCThreads=3 -Xmx40g -Djava.io.tmpdir=temp/\" SelectVariants \\
	-R $ref \\
	-V {i}.filter.SNP.vcf.gz \\
	--select-type-to-include SNP \\
	-restrict-alleles-to BIALLELIC \\
	--remove-unused-alternates \\
	--exclude-non-variants \\
	--exclude-filtered true \\
	-O {i}.clean.SNP.vcf.gz
''')
def main():
    import sys
    nameList = load_name_list(sys.argv[1])
    produce(nameList)
main()
