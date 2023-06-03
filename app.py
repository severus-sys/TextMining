from flask import Flask, render_template, request
from helpers import summarize_text, extract_text_from_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summarize():
    text = request.form['text']
    file = request.files['file']
    
    if text:
        summary = summarize_text(text)
    elif file and (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        else:
            text = file.read().decode('utf-8')
        summary = summarize_text(text)
    else:
        return "Metin veya dosya girilmemiş."

    return render_template('summary.html', summary=summary)

if __name__ == '__main__':
    app.run()
