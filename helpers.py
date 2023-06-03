import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

#pdf or text file
import PyPDF2

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

# load the stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


# # Metni cümlelere ayırın
def summarize_text(text):
    sentences = sent_tokenize(text)

    # Cümleleri kelimelere ayırın
    words = [word_tokenize(sentence.lower()) for sentence in sentences]

    # Stop kelimelerini filtreleyin
    filtered_words = []
    for sentence in words:
        filtered_sentence = [word for word in sentence if word not in stop_words]
        filtered_words.append(filtered_sentence)

    # Kelime frekanslarını hesaplayın
    word_frequencies = FreqDist([word for sentence in filtered_words for word in sentence])

    # Kelime frekanslarına dayanarak cümle skorlarını hesaplayın
    sentence_scores = {}
    for i, sentence in enumerate(filtered_words):
        score = 0
        for word in sentence:
            score += word_frequencies[word]
        sentence_scores[i] = score

    # Cümleleri skorlarına göre sıralayın
    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)

    # Özet için en yüksek skora sahip ilk N cümleyi seçin
    N = 3  # Özetin cümle sayısı    
    summary_sentences = [sentences[index] for index, _ in sorted_sentences[:N]]

    # Özet
    return summary_sentences