from dotenv import load_dotenv
import os
import dspy
from pyclinai.synthetic.notes import gen_note

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")


def main():
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=GEMINI_KEY, max_tokens=10000)
    dspy.configure(lm=lm)

    gen_note(
        "PATIENT is a 55 yo Male smoker with no history of cancer complaining of a new tremor and cough.",
        updrs_score="UPDRS: 0",
        complexity=1,
    )
    gen_note(
        "PATIENT is a 23 yo Male smoker with no history of cancer complaining of a new tremor and chest pain.",
        updrs_score="UPDRS: 15",
        complexity=1,
    )

    gen_note(
        "PATIENT is a 23 yo Male smoker with no history of cancer complaining of a new tremor and chest pain.",
        updrs_score="UPDRS: 15",
        complexity=9,
    )


if __name__ == "__main__":
    main()
