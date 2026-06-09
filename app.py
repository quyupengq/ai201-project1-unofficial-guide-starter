import gradio as gr

from src.query import ask


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""

    try:
        result = ask(question)

        answer = result["answer"]

        sources_text = ""
        for chunk in result["retrieved_chunks"]:
            sources_text += (
                f"- {chunk['source']} "
                f"(chunk {chunk['chunk_index']}, distance {round(chunk['distance'], 4)})\n"
            )

        return answer, sources_text

    except Exception as e:
        return f"Error: {e}", ""


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide to College Internship Difficulty")
    gr.Markdown(
        "Ask a question about student experiences with internships, applications, ghosting, rejection, grades, projects, and networking."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: Why do students say internships are hard to get?",
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved sources", lines=8)

    ask_button.click(
        fn=handle_query,
        inputs=question,
        outputs=[answer, sources],
    )

    question.submit(
        fn=handle_query,
        inputs=question,
        outputs=[answer, sources],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)