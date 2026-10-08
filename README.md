# TripMind AI — AI Travel Intelligence Platform

Not just a chatbot — this project will evolve into an AI system that can reason,
retrieve information, call tools, maintain state, and produce structured travel plans.

## Project goal

Build a system where a user can ask:

> I'm planning a 5-day trip to Tokyo. Find interesting places, create an itinerary,
> estimate the budget, and explain why you selected each place.

The system will eventually combine an LLM or agent, memory, RAG, tools, APIs,
and structured output.


## Project structure

```
TripMind AI/
├── main.py                  # Entry point: extraction → hybrid search → rerank
├── ingest.py                # Load, chunk and index knowledge into Chroma
├── keyword_search.py        # BM25 keyword search with metadata filtering
├── hybrid_search.py         # Reciprocal Rank Fusion (RRF)
├── reranker.py              # Cross-encoder reranker (top 3)
├── schema/
│   └── MetaDataFiltering.py # Pydantic schema for LLM metadata extraction
├── knowledge/
│   └── Tokyo.txt            # Travel knowledge base (Tokyo)
├── db/                      # Persisted Chroma vector store (generated)
├── requirements.txt
└── .env.example
```

## Getting started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

Fill in the values:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### 3. Ingest the knowledge base

```bash
python ingest.py
```

This loads `knowledge/Tokyo.txt`, tags each chunk with metadata
(`city: Tokyo`, `category: place`), splits it into ~200-character chunks,
and stores them in the `places` Chroma collection under `./db`.

### 4. Run the application

```bash
python main.py
```

Example output for the query *"What temples can I visit in Tokyo?"*:

```
city='Tokyo' category='place'

---
Senso-ji is a historic Buddhist temple located in Asakusa.
It is one of Tokyo's most popular cultural attractions.

---
Ueno is known for its museums, parks and temples.
Banten Doji is one of the largest Buddhist temples in Tokyo,
with a huge bronze Kannon statue.

---
Tokyo is the capital city of Japan.
...
```

## How it works, step by step

1. **Metadata extraction** — the user's question is sent to the LLM with
   structured output (`MetaDataFiltering`), which extracts the filter fields
   (`city`, `category`) instead of answering the question.
2. **Hybrid retrieval** — 10 candidates are fetched from both the vector
   store (filtered by the extracted metadata) and the BM25 index.
3. **Fusion** — RRF merges the two rankings; documents that rank high in
   both searches move to the top.
4. **Reranking** — the cross-encoder scores each candidate against the
   original question and keeps the top 3.
5. **Answer** — the top 3 chunks are joined into `context` and passed to the
   LLM with a prompt that constrains it to answer using only that context.

## Roadmap

- [ ] Final answer generation (prompt + LLM chain) on top of the reranked context
- [ ] Tool calling: maps and place search, weather APIs, flight/travel APIs
- [ ] Memory: conversation state and user preferences
- [ ] Multi-city knowledge base and dynamic metadata categories
- [ ] Structured travel plan output: itinerary, budget and per-place explanations
