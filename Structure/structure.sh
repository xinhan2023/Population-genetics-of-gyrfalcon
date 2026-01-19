plink --vcf Autosome.pass.chr.vcf.gz --recode --out autosome -aec --chr-set 40 --make-bed
king -b autosome.bed --kinship --prefix gyrfalcon
bcftools view -S unrelated.txt Autosome.pass.chr.vcf.gz -Oz -o unrelated.vcf.gz

vcftools --gzvcf unrelated.vcf.gz --recode --recode-INFO-all --stdout --minDP 10  --maxDP 100  --max-missing 0.3 --minGQ 10 |bgzip > Russiamac0.clean_depth10_mis0.3.vcf.gz
vcftools --gzvcf unrelated.vcf.gz --recode --recode-INFO-all --stdout --minDP 10  --maxDP 100  --max-missing 0.3 --mac 2 --minGQ 10 |bgzip > Russiamac2.clean_depth10_mis0.3.vcf.gz
vcftools --gzvcf unrelated.vcf.gz --recode --recode-INFO-all --stdout --minDP 10  --maxDP 100  --max-missing 0.3 --mac 1 --minGQ 10 |bgzip > Russiamac1.clean_depth10_mis0.3.vcf.gz

#het
plink \
	--vcf Russiamac0.clean_depth10_mis0.3.vcf.gz \
	--het \
	-aec \
	--chr-set 40 \
	--out Russia.clean_depth10_mis0.3.vcf.gz

#ROH
plink \
        --vcf Russiamac0.clean_depth10_mis0.3.vcf.gz \
        --homozyg \
	-aec \
	--chr-set 40 \
        --homozyg-kb 100 \
	--homozyg-snp 50 \
        --homozyg-window-missing 3 \
        --homozyg-window-snp 50 \
        --out Russiamac0.clean_depth10_mis0.3.vcf.gz

plink \
        --vcf Russiamac1.clean_depth10_mis0.3.vcf.gz \
        --homozyg \
        -aec \
        --chr-set 40 \
        --homozyg-kb 100 \
        --homozyg-snp 50 \
	--homozyg-window-missing 3 \
	--homozyg-window-snp 50 \
        --out Russiamac1.clean_depth10_mis0.3.vcf.gz
plink \
        --vcf Russiamac2.clean_depth10_mis0.3.vcf.gz \
        --homozyg \
        -aec \
        --chr-set 40 \
        --homozyg-kb 100 \
        --homozyg-snp 50 \
        --homozyg-window-snp 50 \
        --homozyg-window-missing 3 \
        --out Russiamac2.clean_depth10_mis0.3.vcf.gz

awk '$3 =="CDS" {print $1"\t"$4"\t"$5}' genes.gff > gene.bed

cat XPEHHselect.bed gene.bed > filter.bed
vcftools --gzvcf Russiamac0.clean_depth10_mis0.3.vcf.gz --exclude-bed filter.bed --recode --recode-INFO-all --stdout|gzip - > filter1.vcf.gz


zcat filter1.vcf.gz|awk '$0 !~/#/ {print $1"\t"$2}' > pos.txt
python getpos.py

vcftools --gzvcf filter1.vcf.gz --positions POS.bed --recode --recode-INFO-all --stdout|bgzip > filter2.vcf.gz

#tree
python vcf2phylip.py -i filter2.vcf.gz --output-prefix gyrfalcon -f
fasttree -nt -gtr gyrfalcon.min4.fasta > gyrfalcon.nwk


#pca and structure
plink --vcf filter2.vcf.gz --recode --out Gyr.3kb -aec --chr-set 40 --make-bed
for i in {2..5};do admixture -j2 -C 0.01 --cv Gyr.3kb.bed $i > admixture.log$i.out & echo ${i} ;done
plink  --allow-extra-chr --chr-set 40 --out gyrfalcon  --pca 10 \
  --set-missing-var-ids @:# --vcf filter2.vcf.gz --vcf-half-call missing
