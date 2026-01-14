# %%
# %load_ext autoreload
# %autoreload 2
# %%
from dotenv import load_dotenv
import os
import dspy
from pyclinai.synthetic.notes import gen_note
import numpy as np

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")


def gen_note_loop(meta_params=None):
    if (
        meta_params
        and "complexity_level" in meta_params
        and meta_params["complexity_level"] is not None
    ):
        complexity_level = meta_params["complexity_level"]
    # need to handle metaparams better

    generated_notes = []
    for nn in range(2):
        complexity_level = np.random.randint(1, 11)
        updrs_score = np.random.randint(1, 11)
        generated_notes.append(
            gen_note(
                "PATIENT is a 65 yo Male coming in with new onset left arm tremor with a family history of Parkinson's Disease.",
                complexity=complexity_level,
                display_note=True,
            )
        )

    return generated_notes


def main():
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=GEMINI_KEY, max_tokens=10000)
    dspy.configure(lm=lm)

    gen_note_loop()


if __name__ == "__main__":
    main()
