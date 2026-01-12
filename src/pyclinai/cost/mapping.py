import dspy


class cpt_costs(dspy.Signature):
    cpt_code: str = dspy.InputField(description="The CPT code to be mapped.")
    icd_codes: list[str] = dspy.InputField(
        description="List of ICD codes associated with the CPT code."
    )
    cost: float = dspy.OutputField(description="The cost associated with the CPT code.")


def map_cpt_to_cost(cpt_code: str, icd_codes: list[str]) -> cpt_costs:
    """
    Map a CPT code and associated ICD codes to a cost.

    Args:
        cpt_code (str): The CPT code to be mapped.
        icd_codes (list[str]): List of ICD codes associated with the CPT code.

    Returns:
        cpt_costs: An object containing the CPT code, associated ICD codes, and the mapped cost.
    """
    mapper = dspy.ChainOfThought(cpt_costs)
    response = mapper(cpt_code=cpt_code, icd_codes=icd_codes)

    return response
