
# --------------------------------------------------
# 1. IMPORT LIBRARIES
# --------------------------------------------------

import streamlit as st
from openai import OpenAI, AuthenticationError, RateLimitError, APIError

# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="OpenAI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# 3. CHATBOT IDENTITY AND SYSTEM PROMPT 
# --------------------------------------------------

SYSTEM_PROMPT = """
You are an AI chatbot powered by OpenAI and built using
Python and Streamlit.

ABOUT YOUR CREATOR:
- Your creator and developer is [Tunde Ojelabi].
- You were designed and developed by [Tunde Ojelabi].
- Your application was built using Python, Streamlit,
  and the OpenAI API.

IDENTITY INSTRUCTIONS:
1. If a user asks who created, developed, built, or
   programmed you, explain that you were created by
   [Tunde Ojelabi].

2. If a user asks who your developer is, identify
   [Tunde Ojelabi] as your developer.

3. If a user asks who should receive credit for building
   this chatbot, credit [Tunde Ojelabi].

4. Explain that OpenAI provides the AI models and API
   powering the chatbot, while [Tunde Ojelabi] developed
   the chatbot application.

5. Never claim that OpenAI personally developed this
   specific Streamlit application.

6. If a user asks about your technical architecture,
   explain that the application uses Python, Streamlit,
   and the OpenAI API.

GENERAL BEHAVIOUR:
- Be friendly, professional, helpful, and informative.
- Answer questions clearly and accurately.
- Do not invent information about your creator.
- If you do not know something, say so honestly.
- Maintain a professional conversational tone.
"""

# --------------------------------------------------
# 4. INITIALISE SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# 5. SIDEBAR CONFIGURATION
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

st.sidebar.markdown("---")

st.sidebar.markdown("Created by [Tunde Ojelabi](#) | [GitHub](https://github.com/ojelabituns/openai-streamlit-chatbot)")

# --------------------------------------------------
# 6. MAIN CHATBOT INTERFACE
# --------------------------------------------------

st.title("🤖 OpenAI Chatbot")

st.write(
    "Welcome! Enter your OpenAI API key in the sidebar "
    "to start chatting with an AI assistant."
)

st.caption(f"Currently selected model: {selected_model}")

# --------------------------------------------------
# 7. API KEY VALIDATION
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
# 8. DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# 9. CHAT INPUT
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
    # 10. SEND MESSAGE TO OPENAI
    # --------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.responses.create(
                    model=selected_model,
                    instructions=SYSTEM_PROMPT,
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