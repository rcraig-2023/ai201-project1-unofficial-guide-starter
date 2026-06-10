# The Unofficial Guide — Project 1

## Domain
This system covers unofficial student knowledge, opinions, and reviews about campus dining at Cornell University. This information is highly valuable because official university websites only provide menus, prices, and hours, whereas students actually need to know realistic wait times, comparative food quality across different dining halls, and the best strategies for maximizing their meal plans on a budget.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Dining Hall Rankings & Timing | Reddit | https://www.reddit.com/r/Cornell/comments/124z4ai/dining_hall_rankings_time/ |
| 2 | Toni Morrison Dining Hall | Yelp | https://www.yelp.com/biz/toni-morrison-dining-hall-ithaca |
| 3 | Okenshields Reviews | Yelp | https://www.yelp.com/biz/okenshields-ithaca |
| 4 | South Campus Meal Plan Options | Reddit | https://www.reddit.com/r/Cornell/comments/1sn7r66/south_campus_meal_plan_city_bucks_college_town/ |
| 5 | Cheap Central Campus Food | Reddit | https://www.reddit.com/r/Cornell/comments/1n0bh9z/cheap_central_campus_food/ |
| 6 | Taking Food Out of Dining Halls | Reddit | https://www.reddit.com/r/Cornell/comments/1m9m70c/taking_food_out_of_dining_halls/ |
| 7 | Dining Hall Hours | Reddit | https://www.reddit.com/r/Cornell/comments/1dtjq04/dining_hall_hours/ |
| 8 | Homage to Okenshields | The Cornell Daily Sun | https://www.cornellsun.com/article/2026/03/a-foodie-s-homage-to-okenshields-why-it-deserves-more-love |
| 9 | Vegan/Vegetarian Dining | Reddit | https://www.reddit.com/r/Cornell/comments/1f18lfs/vegansvegetarians_what_are_you_doing_about_the/ |
| 10 | The Terrace Restaurant | Yelp | https://www.yelp.com/biz/the-terrace-restaurant-ithaca |

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 80 characters

**Why these choices fit your documents:** Because the corpus is predominantly made up of informal text (Reddit comments, Yelp reviews), the structural boundaries are highly irregular. A 400-character size ensures that concise student opinions are not diluted by unrelated surrounding text. An 80-character overlap ensures that context isn't severed mid-sentence when a student transitions between topics. Before chunking, the text was preprocessed using regular expressions to strip out markdown links, URLs, and excessive whitespace. Ad copy was also manually scrubbed.

**Final chunk count:** 147 chunks.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`.

**Production tradeoff reflection:** If deploying this system for real users where cost was not a constraint, I would weigh switching to an enterprise model like OpenAI's `text-embedding-3-small`. This would allow for a much larger context window and better baseline accuracy for localized campus slang. However, this would introduce persistent API costs, network latency, and a dependency on external services compared to the current free, local, and incredibly fast `MiniLM` model.

---

## Grounded Generation

**System prompt grounding instruction:** 
"You are an assistant for answering student questions about Cornell campus dining. You must answer the user's question using ONLY the provided context below. If the answer cannot be found in the context, explicitly say 'I don't have enough information on that.' Do NOT use your general knowledge. Always cite your sources in your response by referencing the Document name (e.g., 'According to source_2.txt...')." Furthermore, the LLM temperature was set to 0.1 to eliminate creative hallucinations.

**How source attribution is surfaced in the response:** 
The UI application dynamically loops through the retrieved chunks, extracts the unique `source` metadata from each dictionary, and visually appends them as a bulleted list in a dedicated "Retrieved From" sidebar column in the Gradio web interface.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the general consensus on the quality of Toni Morrison Dining Hall? | Highly rated for variety/quality, crowded at peak hours. | Positive consensus, 3.8/5 rating, far better than older halls, highly recommended. | Relevant | Partially accurate (missed the crowdedness aspect) |
| 2 | Is it permissible or common practice to sneak food out of dining halls? | Officially against policy, but students debate logistics of taking small items. | Common practice but not permitted. A "noble tradition" of hiding items like pizza in cups. | Relevant | Accurate |
| 3 | Why do some students defend Okenshields despite its reputation? | Nostalgic value, central campus proximity, and dependable staples. | Defended for its convenience, wide selection, predictability, and comforting soups. | Relevant | Partially accurate |
| 4 | What are some recommendations for finding cheap food options on Central Campus? | Specific hidden cafes, à la carte spots, prioritizing retail over dining halls. | Retrieved chunks about Aldi/Wegmans. LLM stated it did not have enough info for Central Campus specific hacks. | Off-target | Inaccurate |
| 5 | Does the system know about the meal options at operational hours past midnight? | No, focus is on regular hours. (Control question). | Noted 7-Eleven is 24/7, but explicitly stated it lacks info on dining halls past midnight. | Relevant | Accurate |

---

## Failure Case Analysis

**Question that failed:** What are some recommendations for finding cheap food options on Central Campus?

**What the system returned:** The system retrieved chunks mentioning off-campus grocery stores (Aldi, Wegmans) and general meal prep, but missed the chunks specifically detailing Central Campus hacks. Consequently, the LLM accurately adhered to its grounding constraints and stated: "I don't have enough information on specific cheap food options on Central Campus from the provided context."

**Root cause (tied to a specific pipeline stage):** This was a **retrieval failure** during the embedding semantic search stage. The phrase "cheap food options" heavily matched with chunks discussing extreme budget eating (like grocery shopping at Aldi) rather than chunks that contained the exact keyword "Central Campus". Because semantic search focuses on overall meaning rather than strict keyword matching, the geographical constraint of the query was overpowered by the budgetary constraint.

**What you would change to fix it:** I would implement a Hybrid Search approach (combining semantic search with a BM25 keyword search). This would ensure that exact keywords like "Central Campus" carry heavy weight during retrieval, forcing the system to pull chunks that are both semantically related to budget eating AND explicitly located in the right area.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the spec beforehand forced me to deliberately choose my chunk size (400 characters) based on the actual formatting of Reddit reviews, rather than blindly guessing during coding. It gave me a clear benchmark to test my `ingest.py` script against to ensure the data was dense enough for semantic search.

**One way your implementation diverged from the spec, and why:** My original spec anticipated that noisy forum boilerplate (like markdown links and URLs) would be a challenge for the embeddings. To solve this, I diverged slightly by adding a dedicated regex cleaning function inside my ingestion script to completely strip out URLs and Wayfair ad copy before the chunking stage even occurred.

---

## AI Usage

**Instance 1**
- *What I gave the AI:* I provided Gemini with my raw `Documents` table and my specified `Chunking Strategy` (400 size, 80 overlap) from my `planning.md` file.
- *What it produced:* It produced a fully functional Python script (`ingest.py`) that utilized regex to strip out links and a custom chunking loop to divide the text and attach metadata.
- *What I changed or overrode:* I had to manually intervene and scrub the raw `.txt` files when the script chunked ads that were in Reddit threads.

**Instance 2**
- *What I gave the AI:* I asked Gemini for help debugging a Git authentication error (`fatal: Authentication failed`) when trying to push my first milestone commit from my Mac terminal.
- *What it produced:* It explained that GitHub deprecated password authentication and provided a step-by-step guide to generating a Personal Access Token (PAT) and injecting it into the terminal.
- *What I changed or overrode:* I directly followed the instructions to adjust my remote URL to bypass the Mac Keychain, which successfully allowed me to push the remaining milestones to my repository.
