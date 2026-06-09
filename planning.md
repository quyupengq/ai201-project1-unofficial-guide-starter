# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is college student internship difficulty. This project focuses on student-generated posts and discussions about how hard it is to get internships, especially when students apply to many positions and receive few responses.

This knowledge is valuable because official career center pages usually explain what students should do, such as build a resume, apply early, and attend career fairs. However, official sources do not always show what students actually experience, such as ghosting, repeated rejection, lack of experience, stress, and confusion about whether grades, projects, referrals, or applications matter most.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Reddit - r/internships: “WHY IS AN INTERNSHIP SO HARD TO GET” |Student post about struggling to get an internship after many applications. Useful for general internship difficulty.|documents/raw/internship_hard_to_get_1.txt |
| 2 |Reddit - r/EngineeringStudents: “Why is it so much harder to get internships this year?”|Engineering students discussing why the internship market feels harder and more competitive. |documents/raw/harder_this_year_engineering_2.txt |
| 3 |Reddit - r/internships: “Sick of being unable to get an internship” |Student post about applying to many internships and mostly getting rejected or ghosted. |documents/raw/unable_to_get_internship_3.txt |
| 4 |Reddit - r/cscareerquestions: “Didn’t get an internship in college, am I screwed?” |Discussion about whether not having an internship hurts students after graduation. |documents/raw/no_internship_after_college_4.txt |
| 5 |Reddit - r/EngineeringStudents: “It shouldn’t be so hard to get an internship or entry level job” |Student discussion about applying to many internships and entry-level roles with very few interviews. |documents/raw/internship_entry_level_too_hard_5.txt |
| 6 |Reddit - r/internships: “Have anybody have any luck getting an internship?” |Student discussion about applying to many internships and still not finding one. |documents/raw/fifty_applications_no_luck_6.txt |
| 7 |Reddit - r/cscareerquestions: “How hard is it to actually get an internship?” |General student discussion about how difficult internships are to get. |documents/raw/how_hard_actually_get_internship_7.txt |
| 8 |Reddit - r/EngineeringStudents: “How screwed am I if I can’t get an engineering internship?” |Discussion about stress and fear around not getting an engineering internship. |documents/raw/engineering_no_internship_stress_8.txt |
| 9 |Reddit - r/EngineeringStudents: “Does anyone else feel ashamed they can’t get an internship?” |Student post about shame, rejection, ghosting, and comparing themselves to others. |documents/raw/ghosted_hundreds_applications_9.txt |
| 10 |Reddit - r/internships: “I’ve watched hundreds of college students job hunt...” |Advice-focused post about what helps students get offers faster, especially warm connections. |documents/raw/warm_connections_advice_10.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
Chunk size:
I will use paragraph-aware chunks with a target size of about 700 characters.
**Overlap:**
I will use about 150 characters of overlap between chunks.
**Reasoning:**
My documents are mostly Reddit-style posts and comments. They are not long official reports, so I do not want very large chunks that combine many unrelated opinions. I also do not want tiny chunks because a single sentence may not include enough context to explain what the student is talking about.

A 700 character chunk should usually contain one complete student experience, complaint, or advice point. This makes retrieval more useful for questions about rejection, ghosting, lack of experience, networking, grades, and stress. The 150-character overlap helps if an important idea gets split between two nearby paragraphs.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
I will use all-MiniLM-L6-v2 from sentence-transformers.
**Top-k:**
I will retrieve the top 5 chunks for each query.
**Production tradeoff reflection:**
I am using all-MiniLM-L6-v2 because it runs locally, is free, and is recommended for this type of beginner RAG project. It should be good enough for matching student questions to informal Reddit-style text.

If I were deploying this for real users and cost was not a constraint, I would compare embedding models based on retrieval accuracy, speed, context length, cost, and how well the model handles informal student language. I would also consider whether the model supports multilingual text, because real student communities may include posts written in different languages or mixed slang.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |Why do students say internships are hard to get? |Students say internships are hard because there is heavy competition, many applications receive no response, and students often lack prior experience or strong connections. |
| 2 |Do students report being ghosted after applying to internships? |Yes. Several students describe applying to many internships and either receiving no response or only generic rejection emails. |
| 3 |Does having good grades guarantee an internship? |No. Some students mention decent or strong grades but still struggle because employers also look for experience, projects, networking, and fit. |
| 4 |What advice do students give for improving internship chances? |Students recommend improving resumes, building projects or experience, applying broadly, using career centers or school events, and trying to make warm connections instead of only cold applying. |
| 5 |Are students worried that not getting an internship will hurt them after graduation? |Yes. Some students worry that not having an internship will make it harder to get a full-time job after college. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.Reddit documents can be noisy. Some comments may be jokes, arguments, off-topic replies, or personal rants. I need to clean the documents and only keep useful post/comment text that relates to internship difficulty.

2.Source attribution could break if I do not store metadata correctly. Every chunk needs to keep its source filename so the final answer can cite which document the information came from.

3.Chunks could be too small or too large. If chunks are too small, retrieval may return fragments without enough meaning. If chunks are too large, one chunk may contain too many topics and make the retrieved context less focused.

4.Some questions may not be answerable from the documents. In those cases, the system should say it does not have enough information instead of making up an answer.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
A[Raw Reddit discussion documents<br>10 .txt files] --> B[Document Ingestion<br>Python file loader] B --> C[Cleaning<br>Remove blank lines, extra spacing, and irrelevant text] C --> D[Chunking<br>Paragraph-aware chunks<br>700 characters with 150 character overlap] D --> E[Embeddings<br>sentence-transformers all-MiniLM-L6-v2] E --> F[Vector Store<br>ChromaDB] G[User Question] --> H[Retrieval<br>Top 5 similar chunks] F --> H H --> I[Grounded Generation<br>Groq llama-3.3-70b-versatile] I --> J[Answer with source citations]
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
I plan to use ChatGPT to help me create the ingestion and chunking script. I will give it my Domain, Documents, and Chunking Strategy sections. I expect it to produce Python code that loads .txt files from documents/raw, cleans the text, creates paragraph-aware chunks, and saves them to data/chunks.json with source metadata. I will verify the output by printing at least 5 chunks and checking that they are readable, complete, and connected to the correct source file.
**Milestone 4 — Embedding and retrieval:**
I plan to use ChatGPT to help me connect sentence-transformers and ChromaDB. I will give it my Retrieval Approach and Architecture sections. I expect it to produce code that loads data/chunks.json, embeds each chunk using all-MiniLM-L6-v2, stores the chunks in ChromaDB, and retrieves the top 5 chunks for a query. I will verify the output by testing at least 3 evaluation questions and checking whether the retrieved chunks are actually relevant.
**Milestone 5 — Generation and interface:**
I plan to use ChatGPT to help me write the grounded generation function and Gradio interface. I will give it my Architecture, Retrieval Approach, and Evaluation Plan sections. I expect it to produce code that sends only retrieved chunks to the Groq LLM and tells the model to answer using only the provided context. I will verify the output by asking questions from my evaluation plan and one out-of-scope question. If the documents do not contain enough information, the system should clearly say that instead of guessing.