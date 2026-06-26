import os
import pandas as pd
from Bio.PDB import MMCIFParser, PDBList


class BioFileReader:
    """Base Parent Class demonstrating OOP Inheritance for fetching bio-files."""

    def __init__(self):
        self.pdbl = PDBList()

    def download_file(self, pdb_id):
        print(f"Connecting to Protein Data Bank... Fetching: {pdb_id}")
        return self.pdbl.retrieve_pdb_file(pdb_id, file_format="mmCif", pdir=".")


class AdvancedStructuralModeler(BioFileReader):
    """Child Class inheriting from BioFileReader to parse 3D coordinates."""

    def __init__(self):
        super().__init__()
        # Encapsulation: Protect the parser instance variable
        self._parser = MMCIFParser(QUIET=True)

    def extract_alpha_carbons(self, cif_file):
        print(f"Processing structural coordinates from: {cif_file}")
        structure = self._parser.get_structure("protein_target", cif_file)

        ca_data = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    if "CA" in residue:
                        ca_atom = residue["CA"]
                        coord = ca_atom.get_coord() 

                        ca_data.append({
                            "Chain_ID": chain.id,
                            "Amino_Acid": residue.get_resname(),
                            "Residue_ID": residue.id,
                            "Vector_X": round(float(coord[0]), 3),
                            "Vector_Y": round(float(coord[1]), 3),
                            "Vector_Z": round(float(coord[2]), 3)
                        })

        return pd.DataFrame(ca_data)


if __name__ == "__main__":
    modeler = AdvancedStructuralModeler()

    downloaded_filename = modeler.download_file("1A8G")

    df_structure = modeler.extract_alpha_carbons(downloaded_filename)

    print("\n--- Advanced OOP Structural Matrix Analysis Complete ---")
    print(df_structure.head(10))

    if os.path.exists(downloaded_filename):
        os.remove(downloaded_filename)

