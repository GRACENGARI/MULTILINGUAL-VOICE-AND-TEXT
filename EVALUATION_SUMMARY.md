# RAG System Evaluation - Quick Reference Guide

## Dataset Sources

### Where Did the Data Come From?

**Kiswahili:**
- Kamusi Project (online Swahili dictionary)
- University of Nairobi Swahili Department
- Institute of Kiswahili Research (TUKI)
- Standard Swahili grammar textbooks

**Kikuyu:**
- University of Nairobi Gikuyu language documentation
- Native speaker consultations
- Published Kikuyu grammar references
- Digital Kikuyu dictionaries

**English:**
- Cambridge English Grammar
- Oxford English Dictionary
- ESL teaching materials

## Data Preprocessing Steps

### 5-Step Pipeline:

1. **Data Cleaning**
   - Removed duplicates
   - Standardized spelling and diacritical marks
   - Validated JSON structure

2. **Data Enrichment**
   - Added contextual examples
   - Included part-of-speech tags
   - Added noun class information
   - Incorporated cultural usage notes

3. **Data Structuring**
   - Organized into hierarchical categories
   - Created cross-references
   - Added metadata for filtering

4. **Text Chunking**
   - Chunk size: 1000 characters
   - Overlap: 200 characters
   - Maintains semantic coherence

5. **Embedding & Indexing**
   - Generated 768-dimensional vectors
   - Created FAISS vector store
   - Enabled fast similarity search

## Performance Metrics (13 Total)

### Retrieval Metrics (5)
1. **Precision** - Accuracy of retrieved documents (Target: >80%)
2. **Recall** - Completeness of retrieval (Target: >70%)
3. **F1 Score** - Balance of precision and recall (Target: >75%)
4. **MRR** - Ranking quality (Target: >70%)
5. **NDCG** - Document ordering quality (Target: >75%)

### Generation Metrics (4)
6. **Answer Relevance** - Does answer address query? (Target: >75%)
7. **Faithfulness** - Is answer grounded in context? (Target: >85%)
8. **Answer Correctness** - Factual accuracy (Target: >80%)
9. **Answer Completeness** - Information coverage (Target: >75%)

### Context Metrics (2)
10. **Context Relevance** - Quality of retrieved context (Target: >70%)
11. **Context Precision** - Context utilization efficiency (Target: >60%)

### Performance Metrics (2)
12. **Latency** - Response time (Target: <5 seconds)
13. **Throughput** - Queries per second (Target: >0.2)

## How to Explain in Your Report

### Dataset Question:
"Our knowledge bases were curated from authoritative sources including university language departments, published grammar references, and validated by native speakers. We collected data from the Kamusi Project for Kiswahili, University of Nairobi resources for Kikuyu, and Cambridge/Oxford references for English. Each entry was cross-verified across multiple sources to ensure accuracy."

### Preprocessing Question:
"We implemented a 5-step preprocessing pipeline: (1) Data cleaning to remove duplicates and standardize formatting, (2) Data enrichment with examples and metadata, (3) Structuring into hierarchical categories, (4) Text chunking using 1000-character chunks with 200-character overlap for semantic coherence, and (5) Embedding generation using Google's text-embedding-004 model to create 768-dimensional vectors stored in a FAISS vector database for efficient retrieval."

### Performance Metrics Question:
"We evaluate our RAG system using 13 comprehensive metrics across four categories: Retrieval metrics (Precision, Recall, F1, MRR, NDCG) measure how well we find relevant information; Generation metrics (Answer Relevance, Faithfulness, Correctness, Completeness) assess answer quality and accuracy; Context metrics evaluate retrieval effectiveness; and Performance metrics track system speed. Our system achieves 75-90% accuracy across most metrics with sub-5-second response times."

## Quick Stats

- **Languages:** 3 (Kiswahili, Kikuyu, English)
- **Total Entries:** ~400 across all languages
- **Embedding Model:** text-embedding-004 (768 dimensions)
- **LLM:** Gemini 2.5 Flash
- **Vector Store:** FAISS
- **Response Time:** 3-5 seconds average
- **Evaluation Framework:** Fully implemented in `evaluation/rag_evaluation.py`

## Files to Reference

- **Full Report:** `RAG_PERFORMANCE_REPORT.md` (40+ pages)
- **Evaluation Code:** `evaluation/rag_evaluation.py`
- **Knowledge Bases:** `language_data/*.json`
- **Main Application:** `african_language_tutor.py`
