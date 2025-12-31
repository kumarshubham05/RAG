import streamlit as st

# -----------------------------------
# Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Infra Assistant",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Infra Assistant")
st.caption("Internal DevOps Knowledge Base")

# -----------------------------------
# Load backend (cached)
# -----------------------------------
@st.cache_resource(show_spinner="Loading AI models and infrastructure documents...")
def load_backend():
    from rag_core import build_qa_chain
    return build_qa_chain()

qa_chain = load_backend()

# -----------------------------------
# Session state (chat history)
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------
# Display chat history
# -----------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------------
# User input
# -----------------------------------
user_input = st.chat_input("Ask about infrastructure, deployments, incidents...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        with st.spinner("Searching internal docs..."):
            response = qa_chain.invoke({"query": user_input})

            # Guardrail: no sources → no answer
            if not response["source_documents"]:
                answer = "I don't have information about that."
            else:
                answer = response["result"]

            st.markdown(answer)

            # Show sources
            if response["source_documents"]:
                with st.expander("📄 Sources"):
                    for doc in response["source_documents"]:
                        source = doc.metadata.get("source", "unknown")
                        st.markdown(f"- {source}")

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
