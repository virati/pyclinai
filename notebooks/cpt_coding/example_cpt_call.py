#%%
%load_ext autoreload
%autoreload 2
#%%
from dotenv import load_dotenv
import os
import dspy
from pyclinai.synthetic.notes import gen_note
from pyclinai.coding.cpt import gen_cpt
from pyclinai.cost.mapping import map_cpt_to_cost
import numpy as np

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")


def main():
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=GEMINI_KEY, max_tokens=10000)
    dspy.configure(lm=lm)

    for ss in ['cough, tremor', 'chest pain, tremor', 'headache, dizziness']:
        note = gen_note(
            f"PATIENT is complaining of {ss}",
            complexity=np.random.randint(1, 10)
        )

        print(note)

        codes = gen_cpt(patient_note=note)
        print("CPT Code:", codes.cpt_code)
        print("ICD Code:", codes.icd_codes)
        print("HCPCS Code:", codes.hcpcs_code)
        print("DRG Code:", codes.ms_drg)

        cost_info = map_cpt_to_cost(cpt_code=codes.cpt_code, icd_codes=codes.icd_codes)
        print(cost_info)

if __name__ == "__main__":
    main()
