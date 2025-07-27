## Approach Explanation – Round 1B: Persona-Driven Document Intelligence

This solution aims to identify and rank the most relevant sections from a set of PDF documents based on a given persona and job-to-be-done. The approach is designed to work fully offline, on CPU-only systems, within the time and resource constraints specified in the Adobe India Hackathon 2025 – “Connecting the Dots”.

---

### 🔹 Inputs
The system accepts the following inputs from the `/input` directory:
- A set of 3 to 10 PDF files
- A plain-text file named `persona.txt` describing the user (e.g., _“PhD student in computational biology”_)
- A plain-text file named `job.txt` describing the user’s task (e.g., _“Prepare a literature review on graph neural networks”_)

---

### 🔹 Output
The system generates a JSON file `persona_output.json` in the `/output` directory. The output includes:
- Metadata (input documents, persona, job, and timestamp)
- Top 10 most relevant sections with document name, page number, and a relevance rank
- Refined summaries from each selected section in a structured format

---

### 🧠 Methodology

1. **PDF Parsing:**  
   Each PDF is parsed using the `PyMuPDF` library, which efficiently extracts structured text from each page. Text blocks are grouped as candidate sections based on layout and spacing.

2. **Query Construction:**  
   The `persona` and `job` text files are read and merged into a query sentence.  
   _Example:_ `"PhD student in computational biology needs to prepare a literature review on graph neural networks"`

3. **Vectorization and Relevance Ranking:**  
   All extracted section texts are vectorized using `TfidfVectorizer` from `scikit-learn`. The query is also vectorized and compared to all sections using cosine similarity. This provides a numerical relevance score for each section.

4. **Top-K Section Selection:**  
   The top 10 sections with the highest similarity scores are selected. Each section’s page number, title, and rank are recorded. A short refined text is also stored under the `subsections` key.

---

### ✅ Offline, Secure, and Fast

This solution is designed to meet the constraints of the hackathon:
- 📦 **Fully offline**: No internet access is required.
- 💾 **Lightweight**: Only PyMuPDF and scikit-learn are used.
- ⚙️ **CPU-only**: No GPU or large model dependencies.
- ⏱️ **Efficient**: Processes 3–5 PDFs within 60 seconds.
- 🔐 **Secure**: No external APIs or cloud services used.

---

### 🔄 Extensibility

The current system uses TF-IDF for relevance ranking, which is fast and offline. It can be further enhanced using sentence embeddings (e.g., MiniLM) if Docker space or time budgets allow in future rounds.

