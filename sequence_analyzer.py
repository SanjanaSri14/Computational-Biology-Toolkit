import os
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction


class SequenceWrangler:
    """An Object-Oriented tool to parse and analyze genomic data files."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.records = []

    def ensure_file_exists(self):
        """Automatically creates the sample FASTA file if it is missing."""
        if not os.path.exists(self.file_path):
            print(f"Creating sample file: {self.file_path}...")
            sample_data = (
                ">sample_gene_1 BRCA1 segment sequence\n"
                "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAA\n"
                "ATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGAC\n"
                ">sample_gene_2 TP53 segment sequence\n"
                "ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCA\n"
                "GACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCGCTTGGTCTGGCCCACTGA\n"
            )
            with open(self.file_path, "w") as f:
                f.write(sample_data)

    def load_data(self):
        """Loads sequences using Biopython."""
        self.records = list(SeqIO.parse(self.file_path, "fasta"))
        print(f"Successfully loaded {len(self.records)} sequence(s).\n")

    def generate_summary(self):
        """Calculates metrics and wraps data into a Pandas DataFrame."""
        data_list = []
        for record in self.records:
            metrics = {
                "Sequence_ID": record.id,
                "Length_BP": len(record.seq),
                "GC_Content_Pct": round(gc_fraction(record.seq) * 100, 2)
            }
            data_list.append(metrics)

        return pd.DataFrame(data_list)


if __name__ == "__main__":
    wrangler = SequenceWrangler(file_path="test.fasta")

    wrangler.ensure_file_exists()

    wrangler.load_data()
    df = wrangler.generate_summary()
    print(df)

