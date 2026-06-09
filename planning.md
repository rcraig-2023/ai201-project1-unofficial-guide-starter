# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This system covers unofficial student knowledge, opinions, and reviews about campus dining at Cornell University. This information is highly valuable because official university websites only provide menus, prices, and hours, whereas students actually need to know realistic wait times, comparative food quality across different dining halls, and the best strategies for maximizing their meal plans.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit Thread | Dining Hall Rankings & Timing analysis | https://www.reddit.com/r/Cornell/comments/124z4ai/dining_hall_rankings_time/ |
| 2 | Yelp Page | Toni Morrison Dining Hall customer reviews | https://www.yelp.com/biz/toni-morrison-dining-hall-ithaca |
| 3 | Yelp Page | Okenshields historical reviews and student opinions | https://www.yelp.com/biz/okenshields-ithaca |
| 4 | Reddit Thread | South Campus meal options, City Bucks vs. Collegetown | https://www.reddit.com/r/Cornell/comments/1sn7r66/south_campus_meal_plan_city_bucks_college_town/ |
| 5 | Reddit Thread | Advice on finding cheap food on Central Campus | https://www.reddit.com/r/Cornell/comments/1n0bh9z/cheap_central_campus_food/ |
| 6 | Reddit Thread | Logistics and ethics of sneaking food out of dining halls | https://www.reddit.com/r/Cornell/comments/1m9m70c/taking_food_out_of_dining_halls/ |
| 7 | Reddit Thread | Realities and student frustrations over operational hours | https://www.reddit.com/r/Cornell/comments/1dtjq04/dining_hall_hours/ |
| 8 | The Cornell Daily Sun | Unofficial student op-ed defending Okenshields' reputation | https://www.cornellsun.com/article/2026/03/a-foodie-s-homage-to-okenshields-why-it-deserves-more-love |
| 9 | Reddit Thread | Vegan/Vegetarian community feedback on dining plan options | https://www.reddit.com/r/Cornell/comments/1f18lfs/vegansvegetarians_what_are_you_doing_about_the/ |
| 10 | Yelp Page | The Terrace Restaurant campus cafe crowd reviews | https://www.yelp.com/biz/the-terrace-restaurant-ithaca |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 400 characters

**Overlap:** 80 characters

**Reasoning:** Because the dataset features messy text collections (Reddit comment chains, Yelp reviews, and a short student news article), the structural boundaries vary significantly. Review-style text and individual comments are packed with concise opinions; larger chunks would dilute specific nuances. An 80-character overlap prevents critical context from being broken mid-sentence when a student shifts topics from food options to layout dynamics.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Top-k:** 4 chunks

**Production tradeoff reflection:** If deploying this for a large volume of actual production users without financial guardrails, we would prioritize switching to an enterprise API embedding model (like OpenAI `text-embedding-3-small`). This would grant us larger input token context lengths and better baseline semantic accuracy on specialized vocabulary, though at the expense of introducing persistent API dependency, recurring costs, and network latency over our current lightweight, local solution.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the general consensus on the quality of Toni Morrison Dining Hall? | It is highly rated by students for variety and quality, though peak hours can be quite crowded. |
| 2 | Is it permissible or common practice for students to sneak food out of Cornell dining halls? | Officially it is against policy, but students heavily debate the logistics and general ethics of taking small items out in containers. |
| 3 | Why do some students defend Okenshields despite its reputation? | It offers immense nostalgic value, exceptional central campus proximity, and dependable staple items like the stir-fry. |
| 4 | What are some recommendations for finding cheap food options on Central Campus? | Students suggest specific hidden cafes, ordering à la carte items, or prioritizing retail spots over swiping into traditional dining halls. |
| 5 | Does the system know about the meal options at operational hours past midnight? | No, the source documents focus on regular hours and standard schedules, not midnight alternatives. (Out-of-scope control question). |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Noisy Forum Boilerplate:** Reddit comment threads feature bot automation language, hyperlinked text formatting, and deleted text tags that risk muddying the downstream embedding generation.
2. **Sarcasm and Campus Dialect:** High usage of heavy sarcasm and localized slang phrases ("Okies", "West campus lines", "swipes") might challenge baseline context alignment if similarities aren't tight.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```mermaid
graph TD
    A[Document Ingestion: Local Text Files] --> B[Chunking Strategy: Recursive Character Splitting]
    B --> C[Embedding Stage: sentence-transformers/all-MiniLM-L6-v2]
    C --> D[Vector Database: ChromaDB Local Store]
    E[User Query Box] --> F[Semantic Search Retrieval: Top-4 Matches]
    D --> F
    F --> G[Grounded Context Generation: Groq Llama-3.3-70b-versatile]
    G --> H[Final Web App UI: Gradio Layout with Source Citations]

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** 
I will provide my Documents and Chunking Strategy sections to Gemini. I expect it to write a clean ingest.py processing script using regular expressions to clean out forum boilerplate (like web links) and slice raw texts into 400-character blocks with an 80-character overlap. I will verify it by printing out exactly 5 generated blocks to check readability.

**Milestone 4 — Embedding and retrieval:** 
I will feed my Retrieval Approach section and the architecture flow to the AI tool to write an embedding script leveraging sentence-transformers and local ChromaDB logic. I will test the output by running 3 validation queries directly through my terminal to verify that the returned chunks are relevant.

**Milestone 5 — Generation and interface:**
I will prompt the AI with the project’s strict grounding requirements alongside the sample Gradio layout instructions. I want it to code an app wrapper where the prompt constraints strictly prohibit model hallucinations and ensure the source dictionary maps clean metadata labels to the interface.