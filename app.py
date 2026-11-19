
import streamlit as st
from openai import OpenAI, AuthenticationError, RateLimitError, APIError

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="OpenAI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# 2. INITIALISE SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# 3. SIDEBAR CONFIGURATION
# --------------------------------------------------

st.sidebar.title("⚙️ Chatbot Settings")

st.sidebar.markdown("### OpenAI API Configuration")

api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key",
    type="password", # ensure the API key is not visible
    placeholder="sk-...", #example placeholder for the API key
    help="Your API key is used to authenticate requests to OpenAI." # informative help text for the user
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Select OpenAI Model")

models = [
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-mini"
]

selected_model = st.sidebar.selectbox(
    "Choose a model",
    models,
    index=1
)

st.sidebar.markdown("---")

# Clear conversation button

if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.sidebar.caption(
    "Your conversation is stored in the current Streamlit session."
)

# --------------------------------------------------
# 4. MAIN CHATBOT INTERFACE
# --------------------------------------------------

st.title("🤖 OpenAI Chatbot")

st.write(
    "Welcome! Enter your OpenAI API key in the sidebar "
    "to start chatting with an AI assistant."
)

st.caption(f"Currently selected model: {selected_model}")

# --------------------------------------------------
# 5. API KEY VALIDATION
# --------------------------------------------------

if not api_key.strip():

    st.warning(
        "🔑 Please enter your OpenAI API key in the sidebar "
        "before sending a message."
    )

    st.stop()

# Create OpenAI client after the user supplies a key

client = OpenAI(api_key=api_key.strip())

# --------------------------------------------------
# 6. DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# 7. CHAT INPUT
# --------------------------------------------------

user_prompt = st.chat_input(
    "Type your message here..."
)

if user_prompt:

    # Display and save user's message

    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # --------------------------------------------------
    # 8. SEND MESSAGE TO OPENAI
    # --------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.responses.create(
                    model=selected_model,
                    input=st.session_state.messages
                )

                assistant_response = response.output_text

                st.markdown(assistant_response)

                # Save assistant response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )

            except AuthenticationError:

                st.error(
                    "Invalid API key. Please check your "
                    "OpenAI API key in the sidebar."
                )

            except RateLimitError:

                st.error(
                    "API rate limit or quota exceeded. "
                    "Check your OpenAI account and billing."
                )

            except APIError as error:

                st.error(
                    f"OpenAI API error: {error}"
                )

            except Exception as error:

                st.error(
                    f"An unexpected error occurred: {error}"
                )