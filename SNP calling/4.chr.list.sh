for i in `cat name`
do
	for chr in  `cat chrom` 
	do
		ls -l SNP/01/${i}_${chr}.g.vcf.gz | gawk '{print $9}' |sort |uniq >> ${chr}.list
	done
done

