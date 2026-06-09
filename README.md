# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
My system covers college student internship difficulty. It focuses on student-generated discussion posts about applying to internships, getting ghosted, dealing with rejection, worrying about grades, and trying to improve through resumes, projects, referrals, and networking.

This knowledge is valuable because official career center websites usually explain what students should do, but they do not always show what students actually experience. Student discussion posts are useful because they show real application struggles, repeated rejections, emotional stress, and practical advice from other students.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |Reddit - r/internships: “WHY IS AN INTERNSHIP SO HARD TO GET” |Reddit discussion thread |documents/raw/internship_hard_to_get_1.txt |
| 2 |Reddit - r/EngineeringStudents: “Why is it so much harder to get internships this year?” |Reddit discussion thread |documents/raw/harder_this_year_engineering_2.txt |
| 3 |Reddit - r/internships: “Sick of being unable to get an internship” |Reddit discussion thread |documents/raw/unable_to_get_internship_3.txt |
| 4 |Reddit - r/cscareerquestions: “Didn’t get an internship in college, am I screwed?” |Reddit discussion thread |documents/raw/no_internship_after_college_4.txt |
| 5 |Reddit - r/EngineeringStudents: “It shouldn’t be so hard to get an internship or entry level job” |Reddit discussion thread |documents/raw/internship_entry_level_too_hard_5.txt |
| 6 |Reddit - r/internships: “Have anybody have any luck getting an internship?” |Reddit discussion thread |documents/raw/fifty_applications_no_luck_6.txt |
| 7 |Reddit - r/cscareerquestions: “How hard is it to actually get an internship?” |Reddit discussion thread |documents/raw/how_hard_actually_get_internship_7.txt |
| 8 |Reddit - r/EngineeringStudents: “How screwed am I if I can’t get an engineering internship?” |Reddit discussion thread |documents/raw/engineering_no_internship_stress_8.txt |
| 9 |Reddit - r/EngineeringStudents: “Does anyone else feel ashamed they can’t get an internship?” |Reddit discussion thread |documents/raw/ghosted_hundreds_applications_9.txt |
| 10 |Reddit - r/internships: “I’ve watched hundreds of college students job hunt...” |Reddit discussion thread |documents/raw/warm_connections_advice_10.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
About 700 characters per chunk.
**Overlap:**
About 120 characters of overlap.
**Why these choices fit your documents:**
My documents are Reddit-style posts and comments, so each source contains short personal experiences and advice rather than long formal reports. I used paragraph-aware chunking because I wanted each chunk to preserve complete thoughts instead of cutting randomly every few hundred characters.

A 700-character chunk is small enough to keep each retrieved result focused on one topic, such as ghosting, GPA, applications, or networking. The 120-character overlap helps reduce the chance that useful context gets lost between two chunks.

Before chunking, the ingestion script cleaned extra blank lines, spacing issues, and text artifacts. I also removed planning-note style bullets and kept real source text so the RAG system would be grounded in actual documents.
**Final chunk count:**
30 chunks across 10 documents.
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 from sentence-transformers.
**Production tradeoff reflection:**
I used all-MiniLM-L6-v2 because it runs locally, is free, and works well enough for a small RAG project. It is also fast and easy to use with ChromaDB.

If I were deploying this system for real users, I would compare models based on accuracy, latency, cost, context length, and whether the model handles informal student language well. I would also consider multilingual support because real student communities may include mixed-language posts or slang. A larger hosted embedding model might retrieve more accurate results, but it would likely cost more and depend on an external API.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
My system prompt tells the LLM:

You are a grounded RAG assistant for a student internship difficulty guide.

Rules:
1. Answer using ONLY the provided context chunks.
2. Do not use outside knowledge.
3. If the context does not directly answer the question, say:
   "I don't have enough information from the documents to answer that."
4. Be honest about uncertainty.
5. Mention the source document names that support the answer.
6. Do not invent statistics, companies, numbers, or claims that are not in the context.

The model only receives the retrieved chunks as context. It does not receive the full dataset or any outside sources. This helps keep the answer tied to the documents that were retrieved.

How source attribution is surfaced in the response:
Each retrieved chunk includes its source filename and chunk index. The generated answer mentions the source filenames, and the Gradio interface also displays the retrieved source files, chunk indexes, and distance scores. This lets the user see which documents were used to answer the question.
**How source attribution is surfaced in the response:**
Each retrieved chunk includes its source filename and chunk index. The generated answer mentions the source filenames, and the Gradio interface also displays the retrieved source files, chunk indexes, and distance scores. This lets the user see which documents were used to answer the question.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |Why do students say internships are hard to get? |Students say internships are hard because there is heavy competition, many applications receive no response, and students often lack prior experience or strong connections. |The system said internships are hard because students submit many applications, receive few responses, and face high competition. It cited sources about 100+ applications, thousands of applications, and competitive internship types. |Relevant |Accurate |
| 2 |Do students report being ghosted after applying to internships? |Yes. Several students describe applying to many internships and either receiving no response or only generic rejection emails. |The system said yes and cited examples of students being ghosted after hundreds of applications or receiving rejection emails after applying to many internships. |Relevant |Accurate |
| 3 |Does having good grades guarantee an internship?|No. Some students mention decent or strong grades but still struggle because employers also look for experience, projects, networking, and fit. |The system said good grades do not guarantee an internship. It cited a student with a 3.4 GPA and Dean’s/President’s list recognition who still struggled to get interviews. |Relevant |Accurate |
| 4 |What advice do students give for improving internship chances? |Students recommend improving resumes, building projects or experience, applying broadly, using career centers or school events, and trying to make warm connections instead of only cold applying. |The system recommended applying early, improving resumes, building projects, gaining experience, looking at smaller companies, and using warm introductions. |Partially relevant |Partially accurate |
| 5 |Are students worried that not getting an internship will hurt them after graduation? |Yes. Some students worry that not having an internship will make it harder to get a full-time job after college. |The system retrieved documents about students worrying that no internship would hurt their post-graduation job search and future career options. |Relevant |Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
What exact company hires the most students?
**What the system returned:**
The system said it did not have enough information from the documents to answer that. It explained that the retrieved chunks discussed internship difficulty, applications, and job-search strategies, but did not contain data about which company hires the most students.
**Root cause (tied to a specific pipeline stage):**
This was an out-of-scope question for the dataset. The retrieval stage could only retrieve chunks from documents about internship difficulty and student experiences. Since none of the documents contained exact company hiring statistics, the generation stage did not have enough evidence to answer.
**What you would change to fix it:**
To answer this type of question, I would need to add new documents that contain company-specific hiring information, such as career center reports, internship placement data, or company recruiting statistics. I could also add metadata filters or a separate source category for company hiring data. Without those documents, the correct behavior is refusing to answer instead of making up a company name.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning document helped me stay focused before writing code. It made me choose the domain, sources, chunking strategy, retrieval approach, and evaluation questions first. Because I already knew what the system was supposed to answer, it was easier to test whether retrieval and generation were working correctly.
**One way your implementation diverged from the spec, and why:**
My original plan expected more chunks, but the final system created 30 chunks across 10 documents. I removed low-quality text and planning-note style bullets from the raw documents, which made the dataset cleaner but smaller. I decided to continue because retrieval testing still returned relevant chunks for the main evaluation questions.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I gave ChatGPT my project domain, the assignment requirements, and my chunking strategy.
- *What it produced:*
It helped produce starter code for src/ingest.py, including loading .txt files, cleaning text, creating chunks, and saving them to data/chunks.json.
- *What I changed or overrode:*
I adjusted the source documents after testing because some early chunks contained planning-note style bullet lists instead of real source text. I removed those notes and reran ingestion so the chunks were based on actual documents.
**Instance 2**

- *What I gave the AI:*
I gave ChatGPT my retrieval approach using all-MiniLM-L6-v2, ChromaDB, and top-k retrieval.
- *What it produced:*
It helped produce code for building the ChromaDB vector index and testing retrieval with my evaluation questions.
- *What I changed or overrode:*
I inspected the retrieval results manually and decided whether the chunks were relevant. When the system returned weak results, I cleaned the source files and rebuilt the index.