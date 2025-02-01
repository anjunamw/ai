# backend/finetuner.py
import argparse
import datetime
import json
import os
import sys
import time

import torch
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)


def load_and_prepare_data(data_file):
    """Loads and prepares the data for fine-tuning."""
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def run_fine_tuning(data_file, output_dir, agent_id):
    """
    Fine-tunes a model based on the provided data file.
    """
    print(f"Starting fine-tuning for agent {agent_id}...")
    print(f"Data file: {data_file}")
    print(f"Output directory: {output_dir}")
    # Load and prepare the fine-tuning data
    raw_data = load_and_prepare_data(data_file)
    if not raw_data:
        print("No data loaded. Exiting.")
        return
    # Use the first entry in the dataset to determine the base model
    base_model = raw_data[0].get("base_model", "mistralai/Mistral-7B-v0.1")
    print(f"Using base model: {base_model}")
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        base_model, load_in_4bit=True, device_map="auto", trust_remote_code=True
    )
    # Tokenize the data
    tokenized_data = []
    for item in raw_data:
        messages = [
            {"role": "system", "content": item.get("system_prompt", "")},
            {"role": "user", "content": item.get("user_prompt", "")},
        ]

        # Format the messages in a way that the tokenizer understands
        formatted_messages = []
        for message in messages:
            if message["role"] == "system":
                formatted_messages.append(f"### System:\n{message['content']}")
            elif message["role"] == "user":
                formatted_messages.append(f"### User:\n{message['content']}")
            elif message["role"] == "assistant":
                formatted_messages.append(f"### Assistant:\n{message['content']}")

        # Add the EOS token to indicate the end of the conversation
        formatted_messages.append("</s>")

        # Join the formatted messages into a single string
        text = "\n".join(formatted_messages)

        # Tokenize the text
        tokenized_input = tokenizer(
            text, return_tensors="pt", padding=True, truncation=True
        )
        tokenized_data.append(tokenized_input)
    # Configure LoRA
    config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, config)
    # Define training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=1,  # Adjust as necessary
        gradient_accumulation_steps=4,  # Adjust as necessary
        learning_rate=2e-4,
        logging_steps=10,
        max_steps=500,
        remove_unused_columns=False,
    )

    # Create a dummy dataset
    class SimpleDataset(torch.utils.data.Dataset):
        def __init__(self, tokenized_data):
            self.input_ids = [item["input_ids"].squeeze() for item in tokenized_data]
            self.attention_mask = [
                item["attention_mask"].squeeze() for item in tokenized_data
            ]

        def __len__(self):
            return len(self.input_ids)

        def __getitem__(self, idx):
            return {
                "input_ids": self.input_ids[idx],
                "attention_mask": self.attention_mask[idx],
            }

    dataset = SimpleDataset(tokenized_data)
    # Create data collator
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )
    # Train the model
    trainer.train()
    # Save the model
    model.save_pretrained(output_dir)
    # Save the results
    results_file = os.path.join(output_dir, "fine_tuning_results.txt")
    with open(results_file, "w", encoding="utf-8") as f:
        f.write(f"Fine-tuning completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Agent ID: {agent_id}\n")
        f.write(f"Model saved to: {output_dir}\n")
    print(
        f"Fine-tuning completed for agent {agent_id}. Results written to {results_file}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run fine-tuning process.")
    parser.add_argument(
        "--data_file", type=str, required=True, help="Path to the data file."
    )
    parser.add_argument(
        "--output_dir", type=str, required=True, help="Path to the output directory."
    )
    parser.add_argument(
        "--agent_id",
        type=str,
        required=True,
        help="ID of the agent running fine-tuning.",
    )
    args = parser.parse_args()
    run_fine_tuning(args.data_file, args.output_dir, args.agent_id)
