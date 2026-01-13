import dspy


class DzState(dspy.Signature):
    disease: str = dspy.InputField(desc="The disease to generate a vignette for.")
    progression: float = dspy.InputField(
        desc="A number between 0 and 1 indicating how far along the disease has progressed. 0 means the disease is just starting, while 1 means the disease is at its most advanced stage."
    )
    perplexity: float = dspy.InputField(
        desc="A number between 0 and 1 indicating how typical the presentation is for the disease. 0 means the vignette should be very stereotypical, while 1 means the vignette should be a rare, Zebra presentation."
    )
    one_liner: str = dspy.OutputField(
        desc="A concise one-liner summary of the patient's presentation, including key symptoms, the Chief Complains, and brief relevant context."
    )
    clinical_scale: str = dspy.OutputField(
        desc="A clinical scale relevant to the disease, if applicable. This should include the name of the scale."
    )
    clinical_score: int = dspy.OutputField(
        desc="The score on the clinical scale, if applicable. This should be a number appropriate for the disease progression and specific scale used for the disease"
    )
