from dspy import Signature
import dspy


class cpt_code(Signature):
    input_note: str = dspy.InputField(description="The clinical note to be coded.")
    true_disease: str = dspy.InputField(
        description="The true disease that the patient has."
    )
    cpt_code: str = dspy.OutputField(
        description="The generated CPT code. CPT reflects the work done by the physician."
    )
    icd_codes: list[str] = dspy.OutputField(
        description="List of ICD codes. ICD codes reflect the patient's diagnosis and medical history. Make sure to choose codes that maximize revenue while remaining accurate."
    )
    hcpcs_code: str = dspy.OutputField(
        description="The Healthcare Common Procedure Coding System code."
    )
    ms_drg: str = dspy.OutputField(
        description="The Medicare Severity Diagnosis Related Group code."
    )


def gen_cpt(patient_note: str) -> cpt_code:
    """
    Generate CPT, ICD, and HCPCS codes from a clinical note.

    Args:
        patient_note (str): The clinical note to be coded.

    Returns:
        cpt_code: An object containing the generated CPT, ICD, and HCPCS codes.
    """
    coder = dspy.ChainOfThought(cpt_code)
    response = coder(input_note=patient_note)

    return response
