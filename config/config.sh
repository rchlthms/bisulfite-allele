# Reference genome
reference_genome="path/to/reference_genome.fa"

# Region containing the SNP
region_locus="chrX:150360000-150370000"
region_name="mamld_cpg"

# Coordinates
first_position=150360000
SNP_position=150363776

# Alleles
reference_allele="G"
alternate_allele="T"

# Samples
samples=(
    "sample1"
    "sample2"
    "sample3"
)

# Input and output locations
input_dir="path/to/fastq_files"
output_dir="work"
results_dir="results"
