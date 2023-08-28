from flask import Flask, render_template, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    user_input = request.json['user_input']

    model_name = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer(user_input, return_tensors="pt").input_ids
    model = AutoModelForCausalLM.from_pretrained(model_name)
    outputs = model.generate(inputs, max_new_tokens=100, do_sample=True, top_k=50, top_p=0.95)
    generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    return jsonify({'response': generated_text})

if __name__ == '__main__':
    app.run(debug=True)
    