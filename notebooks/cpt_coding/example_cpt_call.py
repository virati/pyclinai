#!/usr/bin/env python3
"""
Example script demonstrating PyClinAI CPT coding functionality.
"""

import os
import random
from dotenv import load_dotenv
import dspy

from pyclinai.synthetic.notes import gen_note, print_note
from pyclinai.coding.cpt import gen_cpt
from pyclinai.cost.mapping import map_cpt_to_cost


def main():
    """Main function demonstrating CPT coding workflow."""
    # Load environment variables
    load_dotenv()

    gemini_key = os.getenv("GEMINI_KEY")
    if not gemini_key:
        print("Error: GEMINI_KEY environment variable not set")
        return

    # Configure DSPy with Gemini model
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=gemini_key, max_tokens=10000)
    dspy.configure(lm=lm)

    # Test cases for different patient symptoms
    symptoms_list = ["cough, tremor", "chest pain, tremor", "headache, dizziness"]

    for symptoms in symptoms_list:
        print(f"\n{'=' * 60}")
        print(f"Processing case: {symptoms}")
        print(f"{'=' * 60}")

        # Generate synthetic medical note
        note = gen_note(
            f"PATIENT is complaining of {symptoms}", complexity=random.randint(1, 10)
        )

        # Print the generated note in a readable format
        print_note(note)

        # Generate medical codes from the note
        codes = gen_cpt(patient_note=note)
        print(f"\nGenerated Codes:")
        print(f"CPT Code: {codes.cpt_code}")
        print(f"ICD Codes: {codes.icd_codes}")
        print(f"HCPCS Code: {codes.hcpcs_code}")
        print(f"DRG Code: {codes.ms_drg}")

        # Map codes to cost information
        cost_info = map_cpt_to_cost(cpt_code=codes.cpt_code, icd_codes=codes.icd_codes)
        print(f"\nCost Information:")
        print(f"Estimated Cost: ${cost_info.cost}")
        print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
