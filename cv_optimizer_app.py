import streamlit as st
import os
import sys
import subprocess
import chromadb
import ollama
from pypdf import PdfReader

def read_cv(file):
    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif file.name.endswith('.txt'):
        data = file.read()
        if isinstance(data, bytes):
            text = data.decode('utf-8', errors='replace')
        else:
            text = data
    else:
        st.error("Sadece PDF veya TXT dosyası yükleyin!")
        return ""
    return text

def extract_keywords(text):
    keywords = set()
    languages = ['python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'go', 'rust', 'php', 'swift', 'kotlin', 'typescript', 'scala', 'r']
    frameworks = ['django', 'flask', 'fastapi', 'react', 'vue', 'angular', 'express', 'spring', 'node.js', 'next.js', 'rails']
    databases = ['postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'oracle', 'sql server', 'dynamodb', 'elasticsearch']
    cloud = ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'ci/cd', 'gitlab']
    other = ['git', 'linux', 'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'tdd', 'machine learning', 'deep learning', 'celery', 'rabbitmq', 'kafka', 'spark']
    all_keywords = languages + frameworks + databases + cloud + other
    text_lower = text.lower()
    for keyword in all_keywords:
        if keyword in text_lower:
            keywords.add(keyword)
    return sorted(list(keywords))

def simple_text_splitter(text, chunk_size=500, chunk_overlap=50):
    # Basit bir metin bölücü, langchain'e gerek yok
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks

def create_cv_embeddings(cv_text, job_text):
    client = chromadb.Client()
    try:
        client.delete_collection("cv_job_matcher")
    except:
        pass
    collection = client.create_collection(name="cv_job_matcher", metadata={"description": "CV ve iş ilanı eşleştirme"})
    cv_chunks = simple_text_splitter(cv_text)
    job_chunks = simple_text_splitter(job_text)
    for i, chunk in enumerate(cv_chunks):
        collection.add(documents=[chunk], metadatas=[{"source": "cv", "chunk_id": i}], ids=[f"cv_{i}"])
    for i, chunk in enumerate(job_chunks):
        collection.add(documents=[chunk], metadatas=[{"source": "job", "chunk_id": i}], ids=[f"job_{i}"])
    return collection

def find_matching_sections(collection, query, n_results=5):
    results = collection.query(query_texts=[query], n_results=n_results, include=["documents", "metadatas", "distances"])
    return results

def compare_cv_job(cv_text, job_text):
    cv_keywords = set(extract_keywords(cv_text))
    job_keywords = set(extract_keywords(job_text))
    matched = cv_keywords & job_keywords
    missing = job_keywords - cv_keywords
    extra = cv_keywords - job_keywords
    match_percentage = (len(matched) / len(job_keywords) * 100) if job_keywords else 0
    return {
        'cv_keywords': cv_keywords,
        'job_keywords': job_keywords,
        'matched': matched,
        'missing': missing,
        'extra': extra,
        'match_percentage': match_percentage
    }

def ai_with_embeddings(cv_text, job_text):
    collection = create_cv_embeddings(cv_text, job_text)
    relevant_cv_parts = find_matching_sections(collection, job_text, n_results=3)
    cv_relevant = "\n\n".join([
        doc for doc, meta in zip(
            relevant_cv_parts['documents'][0],
            relevant_cv_parts['metadatas'][0]
        ) if meta['source'] == 'cv'
    ])
    prompt = f"""IMPORTANT: Respond ONLY in Turkish. No English words.\n\nSen bir Türk CV uzmanısın. Semantic analiz ile iş ilanına EN UYGUN CV bölümlerini buldum.\n\nİŞ İLANINDAKİ BAŞLICA GEREKSİNİMLER:\n{job_text[:1000]}\n\nCV'DEN İŞ İLANINA EN ALAKALI BÖLÜMLER:\n{cv_relevant[:1500]}\n\nTAM CV:\n{cv_text[:1000]}\n\nGÖREVİN (SADECE TÜRKÇE):\n1. Adayın hangi yönleri iş ilanıyla GÜÇLÜ ŞEKİLDE eşleşiyor? (3 madde)\n2. Hangi kritik beceriler EKSİK? (3 madde)\n3. CV'de hangi deneyimler ÖNE ÇIKARILMALI? (3 öneri)\n4. İş ilanına göre CV'ye MUTLAKA eklenecek 3 şey\n5. Genel değerlendirme (1-10 puan)\n\nCEVAP (TAMAMEN TÜRKÇE):"""
    try:
        response = ollama.generate(model='llama3.2', prompt=prompt)
        return response['response']
    except Exception as e:
        return f"AI Hatası: {e}"

def generate_cover_letter(cv_text, job_text, company_name=""):
    prompt = f"""IMPORTANT: You MUST write ONLY in Turkish language. Do NOT use any English words or phrases.\n\nSen profesyonel bir Türk kariyer danışmanısın. Aşağıdaki CV ve iş ilanına göre TAM TÜRKÇE bir ön yazı (cover letter) taslağı hazırla.\n\nCV ÖZETİ:\n{cv_text[:1500]}\n\nİŞ İLANI:\n{job_text[:1500]}\n\nŞİRKET ADI: {company_name if company_name else 'Şirket'}\n\nTALİMATLAR (SADECE TÜRKÇE):\n1. Profesyonel ama samimi bir dil kullan\n2. CV'deki deneyimleri iş ilanındaki gereksinimlerle eşleştir\n3. 3-4 paragraf yaz\n4. Kısa ve etkili olsun\n5. TAMAMEN TÜRKÇE YAZ - İNGİLİZCE KELİME KULLANMA\n6. 'Dear', 'Sincerely', 'Experience', 'Skills' gibi İngilizce kelimeler kullanma\n\nÖN YAZI TASLAĞI (TAM TÜRKÇE):"""
    try:
        response = ollama.generate(model='llama3.2', prompt=prompt)
        return response['response']
    except Exception as e:
        return f"AI Hatası: {e}"

st.title("CV Optimize Edici (ChromaDB + AI)")
st.write("Yapay zeka destekli CV analiz ve ön yazı oluşturucu. PDF veya TXT CV ve iş ilanı yükleyin.")

cv_file = st.file_uploader("CV Dosyası Yükle (PDF/TXT)", type=["pdf", "txt"], key="cv")
job_file = st.file_uploader("İş İlanı Yükle (PDF/TXT)", type=["pdf", "txt"], key="job")

if cv_file and job_file:
    cv_text = read_cv(cv_file)
    job_text = read_cv(job_file)
    st.subheader("Anahtar Kelime Analizi")
    result = compare_cv_job(cv_text, job_text)
    st.write(f"Eşleşme Oranı: {result['match_percentage']:.1f}%")
    st.write(f"Eşleşen: {', '.join(result['matched'])}")
    st.write(f"Eksik: {', '.join(result['missing'])}")
    st.write(f"Fazladan: {', '.join(result['extra'])}")
    st.subheader("ChromaDB + AI Analizi")
    if st.button("AI ile Derin Analiz Yap"):
        ai_result = ai_with_embeddings(cv_text, job_text)
        st.write(ai_result)
    st.subheader("Ön Yazı (Cover Letter) Oluştur")
    company = st.text_input("Şirket Adı (opsiyonel)")
    if st.button("Ön Yazı Oluştur"):
        cover = generate_cover_letter(cv_text, job_text, company)
        st.write(cover)
else:
    st.info("CV ve iş ilanı dosyalarını yükleyin.")

"""
Interpreter and pip listing removed by user request.
"""
