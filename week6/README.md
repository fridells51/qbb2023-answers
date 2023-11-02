# Command to generate top2 pcs
plink2 --vcf gwas_data/genotypes.vcf --make-bed --out genotypes
plink2 --bfile genotypes --pca 10 --out pca_genotypes
cut -f3,4 pca_genotypes.eigenvec > top2pcs

# Command to generate allele freqs
plink2 --bfile genotypes --freq --out allele_frequencies
awk '{print $2, $5, $6}' allele_frequencies.afreq > allele_frequencies.txt

# Command to generate gwas results
plink --vcf genotypes.vcf --linear --pheno phenotype.txt --covar pca.eigenvec --allow-no-sex --out phenotype_gwas_results


I found for GS phenotype, that ZNF826 is the associated gene for the hg18 build. According to NCBI, ZNF826 is a pseudogene that may enable DNA-binding transcription activity. However, given what I know about zinc finger genes, the sequencing technology of 2006 is not able to fully characterize these genes because they are massive and contain lots of repetitive sequences. This gene is surrounded by other putative ZNF protein sequences, and it is believed that this is a highly structural section of the genome.

I found for the CB phenotype, the DIP2B gene which is involved in DNA methylation. It's possible that an aberrant methylation state can lead to a disease phenotype.
