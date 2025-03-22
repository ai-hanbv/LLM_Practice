from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import huggingface_hub
import pandas as pd
from peft import get_peft_model, LoraConfig, TaskType
from datasets import Dataset

train_dataset = Dataset.from_json("./data/맞춤법오류_자유게시판.json")
datas = [data['data'] for data in train_dataset]

processing_data = []

for data in datas[0]:
    processing_data.append(data.get("annotation",{}))


dt = pd.DataFrame(processing_data)

question = dt["err_sentence"][:]
answer = dt["cor_sentence"][:]

train = pd.DataFrame({'question':question,'answer' : answer})


model_name = "meta-llama/Llama-3.2-3B-Instruct"

huggingface_hub.login("")
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-4b-pt")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token


lora_config = LoraConfig(
    r=8,  # rank
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],  # 모델마다 다를 수 있음
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)
dataset = Dataset.from_pandas(train[:5])

def tokenize(example):
    # 1. prompt + response 구조로 텍스트 생성
    full_text = f"<start_of_turn>user\n{example['question']}<end_of_turn>\n<start_of_turn>model\n{example['answer']}<end_of_turn>"

    # 2. 토크나이즈 (padding과 max_length 조심)
    tokens = tokenizer(
        full_text,
        padding="max_length",
        truncation=True,
        max_length=2048,  # 너무 크면 안 돼
    )

    # 3. 정답으로 사용될 라벨 생성
    tokens["labels"] = tokens["input_ids"][:]

    return tokens


tokenized_dataset = dataset.map(tokenize)

# 5. 훈련 설정
training_args = TrainingArguments(
    output_dir="./lora-llama",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    logging_steps=10,
    learning_rate=2e-4,
    fp16=True,
    save_total_limit=1,
)

# 6. Trainer 정의 및 학습
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)
trainer.train()

# 7. LoRA 어댑터만 저장
model.save_pretrained("./lora-llama")
"""
"data": [
{"metadata_info": "id": "grm2207060008746", "source": "자유게시판", "date": 20210929, "gender": "F", "age": 15},
    {"annotation": {"err_sentence": "오늘도 다너를 외우러 와따요", 
    "err_sentence_spell": "오늘도 다너를 외우러 와따요", 
    "cor_sentence": "오늘도 단어를 외우러 왔어요.",
    "cor_sentence_spell": "오늘도 단어를 외우러 왔어요.",
    "reg_date": 20220706,
    "errors": [{"err_idx": 0, "err_location": 1, "err_text": "다너를", "cor_text": "단어를", "err_details": ["유사 모양"], "edit_distance": 2}, {"err_idx": 1, "err_location": 3, "err_text": "와따요", "cor_text": "왔어요.", "err_details": ["문장부호", "유사 모양"], "edit_distance": 4}]}}, 
"""