import dspy
from typing import Union
from pathlib import Path


class medical_note(dspy.Signature):
    role: str = dspy.InputField(desc="The role of the person writing the note.")
    one_liner: str = dspy.InputField()
    complexity: int = dspy.InputField(
        desc="The complexity of the case, on a scale from 1 to 10, where 1 is the least complex and 10 is the most complex. The more complex the case, the more the details of the note will deviate from the typical presentation for the given gold_updrs score."
    )
    gold_updrs: str = dspy.InputField(
        desc="The ground-truth UPDRS, either the full assessment or the score, for the patient. This will be used to assess downstream tools that ingest the synthetic notes."
    )
    chief_complaint: str = dspy.OutputField(
        desc="A concise summary of the patient's chief complaint. How long the symptoms have been present and the patient's age must be included."
    )
    past_medical_history: str = dspy.OutputField(
        desc="At least four paragraphs, each with at least three sentences, detailing the patient's past medical history. First paragraph should focus on the symptoms in the CC, and broaden to ask for symptoms typically associated. Second paragraph should focus on history of any/all illnesses. Third paragraph should focus on family history. Final paragraph should include occupation, socioeconomic factors, and any quirky components of the interaction with the patient."
    )
    medications: str = dspy.OutputField()
    review_of_systems: str = dspy.OutputField()
    physical_exam: str = dspy.OutputField(
        desc="A detailed physical exam of the patient, including any relevant findings from the review of systems. Break down by all systems, including neurological, cardiovascular, respiratory, gastrointestinal, musculoskeletal, and any other relevant systems. Each system should be described in detail, including any abnormalities or findings that may be relevant to the patient's condition."
    )
    labs: str = dspy.OutputField()
    differential_diagnosis: str = dspy.OutputField()
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


def gen_note(vignette: str, updrs_score: Union[str, int], complexity: int = 1):
    """
    Generate a medical note based on a vignette.
    """
    note_gen = dspy.Predict(medical_note)
    response = note_gen(
        role="World Expert Physician",
        one_liner=vignette,
        gold_updrs=updrs_score,
        complexity=complexity,
    )
    print_note(response)


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


def parse_note(note: Union[str, Path] = None) -> str:
    if note is None:
        raise ValueError("Note cannot be None")

    # bring in the note based on whatever format it is
    preparse_note: str = None

    if not isinstance(note, str):
        match note.split(".")[-1].lower():
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
