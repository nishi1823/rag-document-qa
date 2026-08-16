import streamlit as st

from src.document_loader import (
    extract_text_from_pdf,
    chunk_text
)

from src.embeddings import (
    create_embeddings,
    create_query_embedding
)

from src.vector_store import (
    create_vector_store,
    search_vector_store
)

from src.qa import generate_answer


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="AI Document Q&A",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------
# Title
# --------------------------------

st.title("🤖 AI Document Question Answering")

st.write(
    "Upload a PDF and ask questions about its content "
    "using Retrieval-Augmented Generation (RAG)."
)


# --------------------------------
# Session State
# --------------------------------

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None


# --------------------------------
# Sidebar
# --------------------------------

with st.sidebar:

    st.header("📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )

    top_k = st.slider(
        "Number of relevant chunks",
        min_value=1,
        max_value=5,
        value=3
    )


# --------------------------------
# Process PDF
# --------------------------------

if uploaded_file is not None:

    if (
        st.session_state.document_name
        != uploaded_file.name
    ):

        with st.spinner(
            "Processing document..."
        ):

            # Extract text

            text = extract_text_from_pdf(
                uploaded_file
            )

            if not text.strip():

                st.error(
                    "Could not extract text from "
                    "this PDF."
                )

                st.stop()


            # Create chunks

            chunks = chunk_text(
                text
            )


            # Create embeddings

            embeddings = create_embeddings(
                chunks
            )


            # Create FAISS index

            vector_store = create_vector_store(
                embeddings
            )


            # Save in session

            st.session_state.chunks = chunks

            st.session_state.vector_store = (
                vector_store
            )

            st.session_state.document_name = (
                uploaded_file.name
            )


        st.success(
            f"Document processed successfully!"
        )


# --------------------------------
# Document Information
# --------------------------------

if st.session_state.chunks:

    st.info(
        f"📄 Document: "
        f"{st.session_state.document_name}  |  "
        f"📦 Chunks: "
        f"{len(st.session_state.chunks)}"
    )


# --------------------------------
# Question Input
# --------------------------------

st.subheader(
    "💬 Ask a Question"
)


question = st.text_input(
    "Enter your question",
    placeholder=(
        "Example: What is the main topic "
        "of this document?"
    )
)


# --------------------------------
# Ask Button
# --------------------------------

if st.button(
    "🔍 Ask Question",
    type="primary",
    use_container_width=True
):

    if st.session_state.vector_store is None:

        st.warning(
            "Please upload a PDF first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching document..."
        ):

            # Create question embedding

            query_embedding = (
                create_query_embedding(
                    question
                )
            )


            # Search FAISS

            results = search_vector_store(
                st.session_state.vector_store,
                query_embedding,
                st.session_state.chunks,
                top_k=top_k
            )


            # Generate answer

            answer = generate_answer(
                question,
                results
            )


        # --------------------------------
        # Answer
        # --------------------------------

        st.subheader(
            "🤖 Answer"
        )

        st.write(
            answer
        )


        # --------------------------------
        # Retrieved Sources
        # --------------------------------

        st.subheader(
            "📚 Retrieved Sources"
        )

        for i, result in enumerate(
            results,
            start=1
        ):

            with st.expander(
                f"Source {i} — "
                f"Similarity: "
                f"{result['score']:.3f}"
            ):

                st.write(
                    result["text"]
                )


# --------------------------------
# Footer
# --------------------------------

st.divider()

st.caption(
    "AI Document Q&A • "
    "Sentence Transformers + FAISS + RAG"
)