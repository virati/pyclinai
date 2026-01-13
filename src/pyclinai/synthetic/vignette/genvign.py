import dspy
from typing import Union
from pathlib import Path
from pathlib import PurePath
from typing import Optional

from multimethod import multimethod


class Vignette(dspy.Signature):
    disease: str = dspy.InputField(desc="The disease to generate a vignette for.")
    patient_characteristics: str = dspy.InputField(
        desc="Characteristics of the patient, potentially including age, sex, and relevant medical history."
    )
    vignette: str = dspy.OutputField(
        desc="A concise clinical vignette describing a patient's presentation, including symptoms, duration, and any relevant context. Add in personality and work-related details that may or may not be relevant to disease itself."
    )


@multimethod
def gen_vignette(disease: str, patient_characteristics: Optional[str] = None) -> str:
    vignette_gen = dspy.Predict(Vignette)
    if patient_characteristics is None:
        patient_characteristics = "Median Person to have the disease"

    response = vignette_gen(
        disease=disease, patient_characteristics=patient_characteristics
    )
    return response.vignette


@multimethod
def gen_vignette():
    pass
