import kiff
from kiff.agents.base import BaseAgent
from pyclinai.synthetic.notes import gen_note


def main():
    agent = BaseAgent(base_model="gemini/gemini-2.5-flash")

    one_liners = [
        "PATIENT is a 35 yo Male smoker with no history of cancer complaining of a new tremor and cough.",
        "PATIENT is a 13 yo Male smoker with no history of cancer complaining of a new tremor and chest pain.",
        "PATIENT is a 63 yo Male smoker with no history of cancer complaining of a new tremor and chest pain.",
    ]
    complexity_level = 2

    for one_liner in one_liners:
        gen_note(
            agent,
            one_liner,
            # updrs_score="UPDRS: 0",
            complexity=complexity_level,
            display_note=True,
        )


if __name__ == "__main__":
    main()
