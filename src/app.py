import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage 
from controller import RAGController

st.set_page_config(
    page_title='ChatRAG',
    page_icon=':robot:',
    layout='centered',
    initial_sidebar_state='expanded',
)

@st.cache_resource
def get_controller():
    return RAGController()

if __name__ == '__main__':
    controller = get_controller()

    # Initializing session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.markdown(
            'Made by Lelis.\n\n'
            '<a target="_blank" href="https://github.com/gblelis"><img alt="Github Button" src="https://img.shields.io/badge/Github-black?style=for-the-badge&logo=github&logoColor=white"></a>',
            unsafe_allow_html=True
        )
        st.divider()

        if st.button('Clear PDF memory (Reset)', icon='🗑️'):
            controller.clear_memory()
            st.session_state.messages = []
            st.rerun()

        uploaded_files = st.file_uploader(
            'Upload your documents',
            type=['pdf'],
            accept_multiple_files=True,
        )

        if uploaded_files:
            if st.button('Add PDFs to context'):
                st.info('This may take a while depending on the file size.', icon='ℹ️')
                with st.spinner('Indexing document(s)...'):
                    status_text, success = controller.ingest_pdfs(uploaded_files)
                    if success:
                        st.success(status_text)
                        st.session_state.messages = []
                    else:
                        st.error(status_text)

    st.title('ChatRAG: Talk with your documents.')

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input('Text your message...'):

        st.chat_message(
            name='User',
            avatar='user',
        ).markdown(prompt)

        st.session_state.messages.append({'role': 'user', 'content': prompt})

        langchain_history = []
        for msg in st.session_state.messages[:-1]:
            if msg['role'] == 'user':
                langchain_history.append(HumanMessage(content=msg['content']))
            else:
                langchain_history.append(AIMessage(content=msg['content']))

        
        with st.chat_message(name='LLM Model', avatar='assistant'):
            with st.spinner('Thinking...'):
                response = controller.get_answer(prompt, langchain_history)
            st.markdown(response)

        st.session_state.messages.append({'role': 'assistant', 'content': response})