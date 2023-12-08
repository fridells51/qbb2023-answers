import sys

def convert_to_ucsc(washu, baitmap, output):
    # make a dict to lookup if frag is bait or not
    bait_dict = {}
    with open(baitmap, 'r') as bm:
        for line in bm:
            fields = line.strip().split('\t')
            # need to match chr nomenclature
            chrom = str('chr' + fields[0])
            start_pos = int(fields[1])
            end_pos = int(fields[2])
            gene_name = fields[4]
            bait_dict[(chrom, start_pos, end_pos)] = gene_name

    with open(washu, 'r') as cf, open(output, 'w') as ucscf:
        # track header
        ucscf.write('track type=interact name="pCHIC" description="Chromatin interactions" useScore=on maxHeightPixels=200:100:50 visibility=full\n')

        for line in cf:
            fields = line.strip().split('\t')

            frag1_info = fields[0].split(',')
            frag2_info = fields[1].split(',')
            strength = float(fields[2])

            chrom1, start1, end1 = frag1_info[0], int(frag1_info[1]), int(frag1_info[2])
            chrom2, start2, end2 = frag2_info[0], int(frag2_info[1]), int(frag2_info[2])

            # lookup in baitmap dict
            frag1 = bait_dict.get((chrom1, start1, end1), '.')
            frag2 = bait_dict.get((chrom2, start2, end2), '.')

            # if the first fragment is bait, then just flip the variables so we don't have to write a bunch of ifs
            if frag1 == '.':
                frag1, frag2 = frag2, frag1
                start1, start2 = start2, start1
                end1, end2 = end2, end1

            # cut -f3 output_washU_text.txt | sort -n > sorted_strengths
            # I used this code to find the max strength of the scores to be 50.99
            max_strength = 50.99
            ucsc_score = int(strength / max_strength * 1000)

            # write what we can for now excluding the last 2 cols
            ucscf.write(f"{chrom1}\t{min(start1, start2)}\t{max(end1, end2)}\t.\t{ucsc_score}\t{strength}\t.\t0\t{chrom1}\t{start1}\t{end1}\t{frag1}\t+\t{chrom2}\t{start2}\t{end2}\t")

            # we need to consider the case that they are both bait fragments in which case follow the directions
            if frag1 != '.' and frag2 != '.':
                ucscf.write(f"{frag2}\t+\n")
            else:
                ucscf.write('.\t-\n')
if __name__ == "__main__":
    washu = sys.argv[1]
    baitmap = sys.argv[2]
    output= sys.argv[3]
    convert_to_ucsc(washu, baitmap, output)

