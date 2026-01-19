vcftools --gzvcf unrelated.vcf.gz --recode --recode-INFO-all --stdout --minDP 10  --maxDP 100 \
    --minQ 30 --minGQ 20 |bgzip > clean1_depth10.vcf.gz
vcftools --gzvcf clean1_depth10.vcf.gz --exclude-bed gyr.newchr.cds --recode --recode-INFO-all --stdout|bgzip >clean2_depth10.vcf.gz

bcftools view -S Chukotka clean2_depth10.vcf.gz -Oz -o Chukotka.vcf.gz
bcftools view -S Yamal clean2_depth10.vcf.gz -Oz -o Yamal.vcf.gz
bcftools view -S Kola clean2_depth10.vcf.gz -Oz -o Kola.vcf.gz

plink --vcf Chukotka.vcf.gz --out Chukotka -aec --chr-set 40 --recode
plink --vcf Yamal.vcf.gz --out Yamal -aec --chr-set 40 --recode
plink --vcf Kola.vcf.gz --out Kola -aec --chr-set 40 --recode

sh script_GONE.sh Chukotka
sh script_GONE.sh Yamal
sh script_GONE.sh Kola