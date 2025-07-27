# Persona-Driven Document Extractor (Round 1B)

## 📥 Input

Place these in `/input`:
- 3–10 PDF files
- `persona.txt` → e.g., "PhD student in computational biology"
- `job.txt` → e.g., "Prepare a literature review on graph neural networks"

## 🚀 Run

```bash
docker build --platform linux/amd64 -t persona_extractor:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none persona_extractor:latest
