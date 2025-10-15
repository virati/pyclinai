import dspy
from typing import Union
from pathlib import Path
from pathlib import PurePath


class medical_note(dspy.Signature):
    role: str = dspy.InputField(desc="The role of the person writing the note.")
    is_inpatient: bool = dspy.InputField(
        desc="Whether the patient is an inpatient or outpatient. If inpatient, the note should be more detailed and include more information about the hospital course."
    )
    one_liner: str = dspy.InputField(
        desc="A one-liner describing the patient's main complaint."
    )
    complexity: int = dspy.InputField(
        desc="The complexity of the case, on a scale from 1 to 10, where 1 is the least complex and 10 is the most complex. The more complex the case, the more the details of the note will deviate from the typical presentation for the given gold_updrs score."
    )
    chief_complaint: str = dspy.OutputField(
        desc="A concise summary of the patient's chief complaint. How long the symptoms have been present and the patient's age must be included. Be sure to factor in the complexity score in determining the chief complaint."
    )
    past_medical_history: str = dspy.OutputField(
        desc="At least four paragraphs, each with at least three sentences, detailing the patient's past medical history. First paragraph should focus on the symptoms in the CC, and broaden to ask for symptoms typically associated. Second paragraph should focus on history of any/all illnesses. Third paragraph should focus on family history. Final paragraph should include occupation, socioeconomic factors, and any quirky components of the interaction with the patient."
    )
    medications: str = dspy.OutputField(
        desc="A list of the patient's current medications, without dosages and frequencies. Be sure to include medications related and unrelated to the one_liner."
    )
    review_of_systems: str = dspy.OutputField()
    physical_exam: str = dspy.OutputField(
        desc="A detailed physical exam of the patient, including any relevant findings from the review of systems. Break down by all systems, including neurological, cardiovascular, respiratory, gastrointestinal, musculoskeletal, and any other relevant systems. Each system should be described in detail, including any abnormalities or findings that may be relevant to the patient's condition."
    )
    labs: str = dspy.OutputField(
        desc="Just provide a list of the labs, not the results, that are relevant to the patient's condition. Make sure it's formatted in a list with newlines between each lab."
    )
    differential_diagnosis: str = dspy.OutputField(
        desc="Provide a list of the top 5 diagnoses that are consistent with the symptoms and other findings in the history."
    )
    assessment: str = dspy.OutputField(
        desc="A detailed medical assessment of the patient's condition, including any relevant findings from the review of systems and labs."
    )
    management_plan: str = dspy.OutputField(
        desc="A comprehensive management plan for the patient, including any recommended treatments, follow-up appointments, and lifestyle modifications."
    )
    severity: int = dspy.OutputField(
        desc="A severity score from 1 to 10, where 1 is the least severe and 10 is the most severe. This should be based on the patient's symptoms and overall condition."
    )
    UPDRS_score: int = dspy.OutputField(
        desc="Unified Parkinson's Disease Rating Scale score, if applicable. This is a score used to quantify the severity of Parkinson's disease symptoms in the patient."
    )
    HDRS_score: int = dspy.OutputField(
        desc="Hamilton Depression Rating Scale score, if applicable. This is a score used to quantify the severity of depression symptoms in the patient."
    )
    true_disease: str = dspy.OutputField(
        desc="The true disease that the patient has, based on the symptoms and other findings in the history."
    )


def gen_note(vignette: str, complexity: int = 1, display_note=False):
    """
    Generate a medical note based on a vignette.
    """
    note_gen = dspy.Predict(medical_note)
    response = note_gen(
        role="World Expert Physician",
        one_liner=vignette,
        complexity=complexity,
        is_inpatient=True,
    )
    if display_note:
        print_note(response)

    return response


def print_note(response: medical_note):
    print("Generated Medical Note:")
    print("Chief Complaint:\n---------------")
    print(response.chief_complaint)
    print("Past Medical History:\n---------------")
    print(response.past_medical_history)
    print("Medications:\n---------------")
    print(response.medications)
    print("ROS:\n---------------")
    print(response.review_of_systems)
    print("Physical Exam:\n---------------")
    print(response.physical_exam)
    print("Labs:\n---------------")
    print(response.labs)
    print("Differential:\n---------------")
    print(response.differential_diagnosis)
    print("Management:\n---------------")
    print(response.management_plan)
    if hasattr(response, "UPDRS_score"):
        print("UPDRS Score:\n---------------")
        print(response.UPDRS_score)
    print("Estimated Severity:\n---------------")
    print(response.severity)
    return response


def parse_note(note: Union[str, PurePath] = None) -> str:
    if note is None:
        raise ValueError("Note cannot be None")

    # bring in the note based on whatever format it is
    preparse_note: str = None

    if not isinstance(note, str):
        match PurePath(note).parts[-1].lower():
            case ".txt":
                with open(note, "r") as f:
                    preparse_note = f.read()
            case ".md":
                with open(note, "r") as f:
                    preparse_note = f.read()
            case ".pdf":
                pass
            case ".json":
                pass
            case _:
                raise ValueError(f"Unsupported file format: {note.suffix}")
    else:
        preparse_note = note

    note_parser = dspy.Predict("medical_note -> chief_complaint")
    response = note_parser(medical_note=preparse_note)

    print(response.chief_complaint)

    clinical_infer = dspy.Predict("chief_complaint -> diagnosis : str")
    dx_response = clinical_infer(chief_complaint=response.chief_complaint)
    print(f"Diagnosis: {dx_response.diagnosis}")
