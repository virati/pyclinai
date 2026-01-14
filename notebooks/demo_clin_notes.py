from dotenv import load_dotenv
import os
import dspy
from pyclinai.synthetic.notes import gen_note

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")


def main():
    lm = dspy.LM("gemini/gemini-2.5-flash", api_key=GEMINI_KEY, max_tokens=10000)
    dspy.configure(lm=lm)

    one_liners = [
        "PATIENT is a 55 yo Male smoker with no history of cancer complaining of a new tremor and cough.",
        "PATIENT is a 23 yo Male smoker with no history of cancer complaining of a new tremor and chest pain.",
        "PATIENT is a 23 yo Male smoker with no history of cancer complaining of a new tremor and chest pain.",
    ]
    complexity_level = 5

    for one_liner in one_liners:
        gen_note(
            one_liner,
            # updrs_score="UPDRS: 0",
            complexity=complexity_level,
            display_note=True,
        )


if __name__ == "__main__":
    main()
