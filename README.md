# Temporal Video RAG: Multi-Modal Search Agent

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FD5200?style=for-the-badge&logo=chroma&logoColor=white)
![OpenAI Whisper](https://img.shields.io/badge/Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)

## Overview
Traditional RAG (Retrieval-Augmented Generation) systems are limited to static text. This project introduces a **Temporal RAG Architecture** capable of ingesting raw video files, performing on-the-fly translation, and allowing users to semantically search video content. 

Instead of just answering a question, the agent acts as a precise research assistant, providing the exact **Video ID and timestamp** where the answer is spoken.

## System Architecture

The system is divided into a robust ETL (Extract, Transform, Load) data pipeline and a Generative Inference engine.

### 1. Data Ingestion & ETL Pipeline
* **Extraction:** `FFmpeg` strips heavy `.mp4` visual data to lightweight `.mp3` audio, optimizing processing speed.
* **Transcription & Translation:** `OpenAI Whisper (large-v2)` transcribes audio while simultaneously translating Hindi speech to English, capturing precise `start` and `end` timestamps for every sentence.
* **Semantic Context Engineering:** A custom sliding-window algorithm dynamically merges 2-second Whisper segments into semantically rich **800-character chunks**, strictly preserving temporal boundaries.
* **Vectorization:** `Ollama (bge-m3)` generates high-dimensional embeddings optimized for retrieval.
* **Storage:** `ChromaDB` acts as the persistent vector store, injecting the precise timestamps and video metadata into the vector payload.

### 2. Inference & Generation
* **Retrieval:** User queries are embedded via `bge-m3` and run through a Cosine Similarity search to fetch the Top-K (k=4) most relevant video chunks.
* **Confidence Scoring:** Raw mathematical distance metrics are converted into human-readable confidence scores (High/Medium/Low) to mitigate AI hallucination.
* **Reasoning:** `Google Gemini ` synthesizes the retrieved context using strict prompt guardrails, forcing the LLM to output a concise answer backed by a strict citation format `(Video X, Ys - Zs)`.

## Engineering Highlights (Why this matters)
* **Temporal Metadata Preservation:** Unlike standard text chunking, this pipeline guarantees that no matter how sentences are merged, the exact video timestamp is mathematically tethered to the text embedding.
* **Asynchronous Multi-Lingual Support:** Capable of ingesting foreign-language audio (Hindi) and allowing users to query the database in English seamlessly.
* **Automated Evaluation:** Built a dedicated `evaluate.py` test suite tracking **Recall@4** to mathematically prove the accuracy of the retrieval layer against a ground-truth dataset.

## Getting Started

### Prerequisites
* Python 3.10+
* [Ollama](https://ollama.com/) installed and running locally.
* `bge-m3` model pulled via Ollama (`ollama pull bge-m3`).
* Google Gemini API Key.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/Somsubhra-Nandi/YOUR-REPO-NAME.git](https://github.com/Somsubhra-Nandi/YOUR-REPO-NAME.git)
   cd YOUR-REPO-NAME
