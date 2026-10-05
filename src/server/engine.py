import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class InferenceEngine:
    def __init__(self):
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"

        model_name = "Qwen/Qwen2.5-0.5B-Instruct"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side='left')
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        self.model.to(self.device)
        self.model.eval()

    # generates response to single prompt with max max_tokens
    def generate(self, prompt: str, max_tokens: int) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
            )

        input_length = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_length:]

        return self.tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # generates batch of responses to prompts. assumes equal max_tokens.
    def generate_batch(self, prompts: list, max_tokens: int) -> list:
        inputs = self.tokenizer(prompts, return_tensors="pt", padding=True)
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens
            )

        results = []

        for i in range(len(prompts)):
            input_length = inputs["attention_mask"][i].sum().item()
            generated_tokens = outputs[i][input_length:]
            
            results.append(self.tokenizer.decode(generated_tokens, skip_special_tokens=True))

        return results
