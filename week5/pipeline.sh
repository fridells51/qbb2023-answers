#!/bin/bash

for file in hw-data/*.fastq
do
bwa mem -t 4 -R "@RG\tID:${file}\tSM:${file}" \
    hw-data/sacCer3.fa \
    ${file} ${file} > ${file}.SAM
done


for file in hw-data/*.SAM
do
    samtools sort ${file} -o ${file}.bam
    samtools index -b ${file}.bam
done

freebayes -p 1 --fasta-reference sacCer3.fa --bam-list bam_list --genotype-qualities > all.vcf


vcffilter -f "QUAL > 20" all.vcf > filtered.vcf


vcfallelicprimitives filtered.vcf -k > decomposed.vcf

SnpEff R64-1-1.105 decomposed.vcf
