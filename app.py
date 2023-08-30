from flask import Flask, render_template, request, jsonify
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    AutoTokenizer,
    AutoModelForCausalLM,
    DistilBertTokenizer,
    DistilBertForQuestionAnswering,
)
import torch

app = Flask(__name__)

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_response", methods=["POST"])
def generate_response():
    user_input = request.json["user_input"]
    # context = "Extractive Question Answering is the task of extracting an answer from a text given a question. An example of a question answering dataset is the SQuAD dataset, which is entirely based on that task. If you would like to fine-tune a model on a SQuAD task, you may leverage the examples/pytorch/question-answering/run_squad.py script."  # Provide relevant context here.
    context1 = "Albert Einstein, the renowned physicist, was born on March 14, 1879, in Ulm, Germany."

    inputs = tokenizer.encode_plus(user_input, context1, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    answer_start_index = torch.argmax(outputs.start_logits)
    answer_end_index = torch.argmax(outputs.end_logits)
    
    answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
    generated_text = tokenizer.decode(answer_tokens, skip_special_tokens=True)

    return jsonify({"response": generated_text})

if __name__ == "__main__":
    app.run(debug=True)
