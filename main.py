import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_sections_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            text = ""
            for line in block["lines"]:
                line_text = " ".join([span["text"] for span in line["spans"]]).strip()
                if len(line_text) > 4:
                    text += line_text + " "
            if text:
                sections.append({
                    "document": os.path.basename(pdf_path),
                    "page": page_num + 1,
                    "section_title": text.strip(),
                    "text": text.strip()
                })
    return sections

def rank_sections(sections, query):
    texts = [s["text"] for s in sections]
    vectorizer = TfidfVectorizer().fit([query] + texts)
    query_vec = vectorizer.transform([query])
    text_vecs = vectorizer.transform(texts)
    scores = cosine_similarity(query_vec, text_vecs).flatten()
    
    for i, score in enumerate(scores):
        sections[i]["score"] = score

    ranked = sorted(sections, key=lambda x: x["score"], reverse=True)
    return ranked[:10]

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    persona_file = os.path.join(input_dir, "persona.txt")
    job_file = os.path.join(input_dir, "job.txt")

    with open(persona_file) as pf, open(job_file) as jf:
        persona = pf.read().strip()
        job = jf.read().strip()

    query = f"{persona} needs to {job}"
    all_sections = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            sections = extract_sections_from_pdf(pdf_path)
            all_sections.extend(sections)

    top_sections = rank_sections(all_sections, query)
    timestamp = datetime.utcnow().isoformat() + "Z"

    output = {
        "metadata": {
            "documents": [f for f in os.listdir(input_dir) if f.endswith(".pdf")],
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": timestamp
        },
        "sections": [],
        "subsections": []
    }

    for rank, sec in enumerate(top_sections, 1):
        output["sections"].append({
            "document": sec["document"],
            "page": sec["page"],
            "section_title": sec["section_title"],
            "importance_rank": rank
        })
        output["subsections"].append({
            "document": sec["document"],
            "page": sec["page"],
            "refined_text": sec["text"]
        })

    with open(os.path.join(output_dir, "persona_output.json"), "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
