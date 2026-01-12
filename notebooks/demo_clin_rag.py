import dspy


class medcopilot:
    def __init__(self):
        self.quick_lm = dspy.LM("/Llama-3.2-3B-Instruct", temperature=0.7)
        self.deep_lm = dspy.LM("openai/gpt-4o", temperature=0.7)

        self.DOCS = {}

    def instruct(self, prompt: str = None):
        if prompt is None:
            return None

        dspy.configure(lm=self.quick_lm)

    def load_data(self, data: str = None):
        if data is None:
            return None
        elif data == "demo":
            from dspy.datasets import DataLoader
            import random

            kwargs = dict(
                fields=("claim", "supporting_facts", "hpqa_id", "num_hops"),
                input_keys=("claim",),
            )
            hover = DataLoader().from_huggingface(
                dataset_name="hover-nlp/hover",
                split="train",
                trust_remote_code=True,
                **kwargs,
            )

            hpqa_ids = set()
            hover = [
                dspy.Example(
                    claim=x.claim,
                    titles=list(set([y["key"] for y in x.supporting_facts])),
                ).with_inputs("claim")
                for x in hover
                if x["num_hops"] == 3
                and x["hpqa_id"] not in hpqa_ids
                and not hpqa_ids.add(x["hpqa_id"])
            ]

            random.Random(0).shuffle(hover)
            trainset, devset, testset = hover[:100], hover[100:200], hover[650:]

    def search(self, query: str, k: int) -> list[str]:
        DOCS = self.DOCS
        results = dspy.ColBERTv2(url="")(query, k=k)
        results = [x["text"] for x in results]

        for result in results:
            title, text = result.split(" | ", 1)
            DOCS[title] = text
        return results
