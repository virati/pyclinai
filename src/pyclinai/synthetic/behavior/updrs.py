import dspy


class PDState(dspy.Signature):
    UPDRS_score: str = dspy.InputField(
        description="The UPDRS score of the patient, which is a measure of the severity of Parkinson's disease symptoms. It is a number between 0 and 100, with higher scores indicating more severe symptoms."
    )
    past_medical_history: str = dspy.OutputField(
        desc="A summary of the patient's past medical history, including any relevant diagnoses, treatments, and medications. This should be based on the patient's symptoms and other findings in the history."
    )
    medications: str = dspy.OutputField(
        desc="A list of the patient's current medications, including the name, dosage, and frequency of each medication. This should be based on the patient's symptoms and other findings in the history."
    )
    review_of_systems: str = dspy.OutputField(
        desc="A review of the patient's symptoms and other findings in the history, organized by body system. This should include any relevant symptoms, signs, and findings that are consistent with the patient's condition."
    )
    physical_exam: str = dspy.OutputField(
        desc="A detailed physical examination of the patient, including any relevant findings from the review of systems and labs. This should include any relevant signs, symptoms, and findings that are consistent with the patient's condition."
    )
