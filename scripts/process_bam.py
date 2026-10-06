import os
import pysam
import sys

# Get variables from environment
relative_SNP_position = int(os.getenv("relative_SNP_position"))
reference_allele = os.getenv("reference_allele")
alternate_allele = os.getenv("alternate_allele")

# Get the list of directories passed as arguments
bam_dirs = sys.argv[1:]

for bam_dir in bam_dirs:
    print(f"Processing directory: {bam_dir}")

    # Find the original Bismark BAM, ignoring BAMs created by this script
    bam_files = [
        os.path.join(bam_dir, f)
        for f in os.listdir(bam_dir)
        if f.endswith(".bam") and not f.endswith("_allele_reads.bam")
    ]

    if len(bam_files) == 0:
        print(f"No original Bismark BAM found in {bam_dir}, skipping...")
        continue

    if len(bam_files) > 1:
        print(f"Multiple input BAMs found in {bam_dir}:")
        for bam in bam_files:
            print(f"  {bam}")
        raise RuntimeError("Expected exactly one original Bismark BAM.")

    bam_file = bam_files[0]

    print(f"Processing BAM file: {bam_file}")

    # Initialize allele-specific BAM writers dynamically
    allele_files = {
        reference_allele: f"{bam_dir}/{reference_allele}_allele_reads.bam",
        alternate_allele: f"{bam_dir}/{alternate_allele}_allele_reads.bam",
    }

    # Open BAM file for reading and create output BAM files
    with pysam.AlignmentFile(bam_file, "rb") as bamfile, \
         pysam.AlignmentFile(allele_files[reference_allele], "wb", header=bamfile.header) as ref_writer, \
         pysam.AlignmentFile(allele_files[alternate_allele], "wb", header=bamfile.header) as alt_writer:

        # Process reads
        ref_count = 0
        alt_count = 0

        for read in bamfile:
            if read.is_unmapped:
                continue

            # Get the reference start position of the read (1-based)
            read_start_ref = read.reference_start + 1

            # Calculate the SNP position relative to the read (1-based in read sequence)
            relative_position = relative_SNP_position - read_start_ref + 1

            # Check if SNP position falls within the read
            if 1 <= relative_position <= read.query_length:
                # Extract the base from the read sequence
                snp_base = read.query_sequence[relative_position - 1]

                # Write read to appropriate BAM file based on the SNP base
                if snp_base == reference_allele:
                    ref_writer.write(read)
                    ref_count += 1
                elif snp_base == alternate_allele:
                    alt_writer.write(read)
                    alt_count += 1

    # Print the number of reads for each allele
    print(f"Reads supporting {reference_allele} allele: {ref_count}")
    print(f"Reads supporting {alternate_allele} allele: {alt_count}")
    print("BAM files for each allele have been created.\n")