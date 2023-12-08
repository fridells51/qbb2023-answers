Rscript runChicago.R raw/PCHIC_Data/GM_rep1.chinput,raw/PCHIC_Data/GM_rep2.chinput,raw/PCHIC_Data/GM_rep3.chinput output --design-dir raw/Design/ --en-feat-list raw/Features/featuresGM.txt --export-format washU_text


1.2

CTCF: This target is enriched. This makes sense because CTCF is a protein involved in the loop extrusion model
k4me1: this target is enriched. This makes sense because k4 methylation is involved in facultative repression of gene promoters and is found occupy repressed h3k27me3 promoters. It is likely that these regions are tightly wound around histones and form 3D interactions.
k4me3: this target is also enriched. H3k4me3 is an active histone mark, so this is a bit surprising to me. in my mind, genome interactions are associated with heterochromatin and inactive regions of the genome. However, it might be possible that this mark causes regions of the genome to interact with upstream enhancers that are spatially close by or interacting to promote transcription.
k27ac: this target is enriched. this is another active histone mark. I can only repeat what i said for the previous feature. this one is surprising to me.
k27me3: this target is neither enriched nor depleted. This is surprising to me as this is a constitutive mark that is crucial to development and silencing regions like centromeres. I'm very surprised this isn't enriched as there are many regions in the genome that undergo constitutive represseion. Perhaps these regions don't form higher-order looping structures.
k9me3: this target is enriched. This is another permanent, constitutive repression mark. It's commonly found in tandem repeat regions of the genome. These tandem repeat regions are likely forming higher-order DNA looping structures.

Top 6 bait-bait and top 6 bait-fragment



chr21	44582195	44849168	.	1000	50.99	.	0	chr21	44582195	44584504	AP001631.10	+	chr21	44845321	44849168	SIK1	+
chr20	17660712	17951709	.	909	46.35	.	0	chr20	17946510	17951709	MGME1;SNX5	+	chr20	17660712	17672229	RRBP1	+
chr20	44438565	44607204	.	837	42.69	.	0	chr20	44596299	44607204	FTLP1;ZNF335	+	chr20	44438565	44442365	UBE2C	+
chr20	17660712	17885496	.	836	42.67	.	0	chr20	17882598	17885496	RNU6-192P	+	chr20	17660712	17672229	RRBP1	+
chr21	26837918	26939577	.	782	39.91	.	0	chr21	26837918	26842640	snoU13	+	chr21	26926437	26939577	MIR155HG	+
chr20	24972345	25043735	.	771	39.33	.	0	chr20	24972345	24985047	APMAP	+	chr20	25036380	25043735	ACSS1	+
chr21	26797667	26939577	.	677	34.55	.	0	chr21	26926437	26939577	MIR155HG	+	chr21	26797667	26799364	.	-
chr20	55957140	56074932	.	646	32.94	.	0	chr20	55957140	55973022	RBM38;RP4-800J21.3	+	chr20	56067414	56074932	.	-
chr21	26790966	26939577	.	572	29.18	.	0	chr21	26926437	26939577	MIR155HG	+	chr21	26790966	26793953	.	-
chr20	5585992	5628028	.	566	28.9	.	0	chr20	5585992	5601172	GPCPD1	+	chr20	5625693	5628028	.	-
chr21	26793954	26939577	.	514	26.23	.	0	chr21	26926437	26939577	MIR155HG	+	chr21	26793954	26795680	.	-
chr20	5515866	5933156	.	511	26.08	.	0	chr20	5929472	5933156	MCM8;TRMT6	+	chr20	5515866	5523933	.	-



Yes it makes sense for this region to have a lot of CTCF interactions. CTCF forms higher order chromatin looping structures allowing for long distance genomic interactions. Based on the chromatin interactions bed file, we can see that these top hits interact with long distance enhancers, and thus it makes sense that there are CTCT peaks at these regions.
