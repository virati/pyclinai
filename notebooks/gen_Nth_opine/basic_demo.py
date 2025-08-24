# %%
from dotenv import load_dotenv
import os
import dspy
from pyclinai.synthetic.notes import gen_note

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")


def main():
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=GEMINI_KEY, max_tokens=10000)
    dspy.configure(lm=lm)

    for nn in range(10):
        gen_note(
            "PATIENT is a 65 yo Male coming in with new onset left arm tremor with a family history of Parkinson's Disease.",
            updrs_score="UPDRS: 10",
            complexity=5,
            print_note=True,
        )


if __name__ == "__main__":
    main()
