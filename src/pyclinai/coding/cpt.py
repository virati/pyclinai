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


def gen_cpt(patient_note) -> cpt_code:
    """
    Generate CPT, ICD, and HCPCS codes from a clinical note.

    Args:
        patient_note: The clinical note to be coded (can be string or medical_note object).

    Returns:
        cpt_code: An object containing the generated CPT, ICD, and HCPCS codes.
    """
    # Convert medical_note object to string if needed
    if hasattr(patient_note, "chief_complaint"):
        # This is a medical_note object, format it as a string
        note_text = f"""
Chief Complaint: {patient_note.chief_complaint}
Past Medical History: {patient_note.past_medical_history}
Medications: {patient_note.medications}
Review of Systems: {patient_note.review_of_systems}
Physical Exam: {patient_note.physical_exam}
Labs: {patient_note.labs}
Differential Diagnosis: {patient_note.differential_diagnosis}
Assessment: {patient_note.assessment}
Management Plan: {patient_note.management_plan}
True Disease: {getattr(patient_note, "true_disease", "Unknown")}
"""
    else:
        # Already a string
        note_text = patient_note

    coder = dspy.ChainOfThought(cpt_code)
    response = coder(input_note=note_text)

    return response
