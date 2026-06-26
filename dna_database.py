import sqlite3


class MolecularDatabase:
    """Creates and queries an indexed relational database for genomic datasets."""

    def __init__(self, db_name="biomedical_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Creates an structured table for storing localized gene expression records."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS genes (
                gene_id TEXT PRIMARY KEY,
                gene_name TEXT,
                chromosome TEXT,
                expression_level REAL,
                mutation_status TEXT
            )
        """)
        self.conn.commit()
        print("Database initialized: Table 'genes' structured successfully.")

    def insert_mock_data(self):
        """Populates relational records into the schema."""
        sample_genes = [
            ("G001", "BRCA1", "17", 45.2, "Mutant"),
            ("G002", "TP53", "17", 12.8, "Wild-Type"),
            ("G003", "EGFR", "7", 89.1, "Mutant"),
            ("G004", "MYC", "8", 5.4, "Wild-Type")
        ]

        self.cursor.executemany("""
            INSERT OR IGNORE INTO genes VALUES (?, ?, ?, ?, ?)
        """, sample_genes)
        self.conn.commit()
        print("Biomedical sample data populated successfully.")

    def query_high_expression_mutants(self):
        """Executes targeted SQL queries to retrieve highly expressed mutated genes."""
        print("\n--- Executing SQL Query: Active Mutant Biomarkers ---")
        self.cursor.execute("""
            SELECT gene_name, chromosome, expression_level 
            FROM genes 
            WHERE mutation_status = 'Mutant' AND expression_level > 20.0
        """)

        results = self.cursor.fetchall()
        for row in results:
            print(f"Target Gene: {row[0]} | Chromosome Location: Chr {row[1]} | Expression Level: {row[2]} FPKM")

    def close_connection(self):
        """Gracefully closes database read-write pipelines."""
        self.conn.close()


if __name__ == "__main__":
    db = MolecularDatabase()
    db.create_tables()
    db.insert_mock_data()
    db.query_high_expression_mutants()
    db.close_connection()
