import pandas as pd


class LabAutomationPipeline:
    """Automates standard biochemistry calculations for laboratory datasets."""

    @staticmethod
    def calculate_molarity(mass_g, molecular_weight, volume_l):
        """Standard biochemistry formula: Molarity = moles / Liters"""
        if molecular_weight == 0 or volume_l == 0:
            return 0
        return round(mass_g / (molecular_weight * volume_l), 4)

    def process_batch_file(self, input_excel, output_excel):
        """Reads an input sheet, automates math across all rows, and exports results."""
        print(f"Reading laboratory spreadsheet: {input_excel}")

        df = pd.read_excel(input_excel)

        df['Calculated_Molarity_M'] = df.apply(
            lambda row: self.calculate_molarity(
                row['Mass_g'],
                row['Molecular_Weight_g_mol'],
                row['Volume_L']
            ), axis=1
        )

        df.to_excel(output_excel, index=False)
        print(f"Pipeline complete! Saved results to: {output_excel}\n")


if __name__ == "__main__":
    mock_lab_data = {
        "Compound": ["NaCl", "Glucose", "Tris-HCl"],
        "Mass_g": [5.84, 18.0, 121.1],
        "Molecular_Weight_g_mol": [58.44, 180.16, 121.14],
        "Volume_L": [1.0, 0.5, 0.25]
    }

    pd.DataFrame(mock_lab_data).to_excel("raw_lab_data.xlsx", index=False)

    pipeline = LabAutomationPipeline()
    pipeline.process_batch_file("raw_lab_data.xlsx", "completed_calculations.xlsx")

    final_df = pd.read_excel("completed_calculations.xlsx")
    print("--- Calculated Pipeline Output Data ---")
    print(final_df)
