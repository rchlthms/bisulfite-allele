# Bisulfite Allele Pipeline

A configurable pipeline for measuring allele-specific DNA methylation in targeted genomic regions using bisulfite-converted, nanopore-sequenced PCR products.

This pipeline is designed for small genomic regions, such as CpG islands upstream of genes, that contain a heterozygous SNP that can be used to distinguish the two alleles. PCR products generated from bisulfite-converted DNA are sequenced using Oxford Nanopore sequencing, and the resulting reads are analyzed separately for each allele.

The pipeline generates allele-specific reference sequences for the target region, aligns the sequencing reads to both allele-specific genomes, identifies reads supporting each allele based on the informative SNP, and uses Bismark to quantify DNA methylation at CpG sites within the region.

This targeted approach allows methylation patterns to be compared between alleles within specific genomic regions of interest, rather than requiring whole-genome bisulfite sequencing.

## How it works

The pipeline performs the following steps:

1. **Extract the target region** from the reference genome.
2. **Generate allele-specific reference sequences** by creating separate reference sequences containing the reference and alternate alleles at the informative SNP.
3. **Prepare the allele-specific genomes** for Bismark alignment.
4. **Trim and quality-check the sequencing reads** using Trim Galore and FastQC.
5. **Align the reads independently to both allele-specific genomes** using Bismark.
6. **Assign reads to alleles** based on the sequence observed at the informative SNP.
7. **Combine allele-specific alignments** while removing duplicate copies of reads assigned to the same allele in both genome alignments. Reads that align to both genomes are retained once rather than discarded.
8. **Extract DNA methylation information** using the Bismark methylation extractor.
9. **Generate allele-specific methylation files** that can be used to compare methylation between the two alleles.

## Installation

### 1. Clone the repository

Clone the repository and navigate into the project directory:

```bash
git clone git@github.com:rchlthms/bisulfite-allele.git
cd bisulfite-allele
```

### 2. Create the Conda environment

Create the pipeline environment using the provided `environment.yml` file:

```bash
conda env create -f environment.yml
```

### 3. Activate the environment

Activate the environment before running the pipeline:

```bash
conda activate bisulfite-allele-pipeline
```

### 4. Configure the pipeline

Copy `config/config.sh` to create your own configuration file. Update the reference genome path, target region, SNP information, sample names, and input directory to match your data.

Keep your personal configuration separate from the example configuration.

### 5. Run the pipeline

From the root of the repository, run:

```bash
./allele_methylation config/my_config.sh
```

The pipeline checks that the `bisulfite-allele-pipeline` Conda environment is active before proceeding. If the environment is not active, the script exits and displays instructions for activating it.

## Configuration reference

The pipeline is configured using a Bash configuration file. An example configuration is provided in `config/config.sh`.

Before running the pipeline, create a copy of the example configuration and edit it to match your data. For example:

```bash
cp config/config.sh config/my_config.sh
```

The configuration file defines the reference genome, target region, informative SNP, samples to analyse, and input and output directories.

### Reference genome

`reference_genome`

Path to the reference genome FASTA file used to extract the target region and generate the allele-specific reference sequences.

```bash
reference_genome="/path/to/reference_genome.fa"
```

Replace the example path with the path to your reference genome FASTA file. An absolute path is recommended to avoid ambiguity about file locations.

The pipeline uses `samtools` to index the reference genome if the index file does not already exist.

### Target region

`region_locus`

The genomic coordinates of the target region, specified in the format `chromosome:start-end`.

```bash
region_locus="chrX:150360000-150370000"
```

Replace these example coordinates with the genomic region you want to analyse. The coordinates must correspond to the reference genome specified by `reference_genome`.

The region is extracted from the reference genome using `samtools faidx`.

`region_name`

A short name used to identify the target region and name intermediate files and directories.

```bash
region_name="mamld_cpg"
```

Choose a descriptive name without spaces. This name is used when creating the allele-specific reference sequences and organizing intermediate files.

### Genomic coordinates

`first_position`

The genomic coordinate of the first base in the extracted target region.

```bash
first_position=150360000
```

This value is used to calculate the position of the informative SNP relative to the extracted region. It should match the start coordinate specified in `region_locus`.

`SNP_position`

The genomic coordinate of the informative SNP used to distinguish the two alleles.

```bash
SNP_position=150363776
```

This position must fall within the target region. The reference genome must contain the expected reference allele at this position.

The pipeline uses this coordinate to calculate the SNP's position within the extracted sequence and to identify reads supporting each allele.

### Alleles

`reference_allele`

The nucleotide present at the SNP position in the reference genome.

```bash
reference_allele="G"
```

`alternate_allele`

The alternative nucleotide at the informative SNP.

```bash
alternate_allele="T"
```

These values must represent the two alleles you want to distinguish. Use the appropriate nucleotide letters for your SNP.

The pipeline generates separate allele-specific reference sequences containing the reference and alternate alleles. Reads are subsequently assigned to alleles based on the nucleotide observed at the informative SNP.

### Samples

`samples`

An array containing the names of the samples to process.

```bash
samples=(
    "sample1"
    "sample2"
    "sample3"
)
```

Replace the example names with your sample identifiers. Each identifier must match the corresponding input FASTQ filename, excluding the `.fastq` extension.

For example, a sample named `sample1` must have an input file named `sample1.fastq` in the directory specified by `input_dir`.

Add or remove entries as needed. Each sample listed in this array will be processed using the same target region and SNP configuration.

The current pipeline expects single-end, uncompressed FASTQ files with the `.fastq` extension.

### Input and output directories

`input_dir`

The directory containing the input FASTQ files.

```bash
input_dir="/path/to/fastq_files"
```

Replace the example path with the directory containing your sequencing data. An absolute path is recommended.

`output_dir`

The directory used to store intermediate files generated during processing.

```bash
output_dir="work"
```

This includes extracted reference sequences, allele-specific genomes, trimmed reads, alignment files, merged BAM files, and methylation extractor outputs.

`results_dir`

The directory where the final allele-specific methylation coverage files are copied.

```bash
results_dir="results"
```

The pipeline creates this directory if it does not already exist.

The default values `work` and `results` are relative paths. When running the pipeline from the repository root, these directories will be created inside the project directory.

### Important considerations

- The reference genome, target region, SNP coordinates, and allele definitions must be consistent with one another.
- The informative SNP must lie within the target region and have the expected reference allele in the reference genome.
- The sample identifiers must match the input FASTQ filenames.
- The pipeline currently processes one target region and one informative SNP per configuration.
