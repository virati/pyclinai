from dotenv import load_dotenv
import os
import dspy
from pyclinai.synthetic.notes import gen_note

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")


def main():
    lm = dspy.LM(
        "gemini/gemini-2.5-flash-preview-04-17", api_key=GEMINI_KEY, max_tokens=6000
    )
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


def ask_question(question: str):
    prepend = "You are a medical expert specializing in mental health. You will answer questions about Deep Brain Stimulation for Depression."
    prepend = "You are a medical student just learning about Deep Brain Stimulation for Depression. You will answer questions about it, but they'll be fantastical and not very accurate."

    qa = dspy.Predict("question : str -> response : str")
    response = qa(question=f"{prepend} What is Deep Brain Stimulation for Depression?")

    print(response.response)


if __name__ == "__main__":
    main()
