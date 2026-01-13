#!/usr/bin/env python3
"""
Simple test script to verify PyClinAI package functionality.
"""

import os
from dotenv import load_dotenv
import dspy

from pyclinai.synthetic.notes import gen_note
from pyclinai.coding.cpt import gen_cpt
from pyclinai.cost.mapping import map_cpt_to_cost


def test_basic_functionality():
    """Test basic functionality of the PyClinAI package."""
    # Load environment variables
    load_dotenv()

    gemini_key = os.getenv("GEMINI_KEY")
    if not gemini_key:
        print("Error: GEMINI_KEY environment variable not set")
        return False

    # Configure DSPy
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=gemini_key, max_tokens=10000)
    dspy.configure(lm=lm)

    try:
        # Test note generation
        print("Testing note generation...")
        note = gen_note("Patient complains of headache", complexity=3)
        print(f"✓ Note generated successfully")

        # Test CPT coding
        print("Testing CPT coding...")
        codes = gen_cpt(patient_note=note)
        print(f"✓ CPT code generated: {codes.cpt_code}")

        # Test cost mapping
        print("Testing cost mapping...")
        cost_info = map_cpt_to_cost(cpt_code=codes.cpt_code, icd_codes=codes.icd_codes)
        print(f"✓ Cost mapped: ${cost_info.cost}")

        print("\n✅ All tests passed! PyClinAI package is working correctly.")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    test_basic_functionality()
