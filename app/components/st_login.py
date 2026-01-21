"""
Login Component - Mastellone/Serenísima Theme
Oracle AI Accelerator v2.0.4

VERSIÓN FINAL - Corregida y funcional
"""

import ast
import json
import time
import random
from datetime import datetime
import streamlit as st

import services.database as database

global_version = "2.0.4"

# Initialize the service
db_user_service = database.UserService()
db_agent_service = database.AgentService()
db_quiz_service = database.QuizService()
db_file_service = database.FileService()


def load_mastellone_css():
    """Carga el tema CSS de Mastellone/Serenísima"""
    try:
        with open("styles/mastellone_theme.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    
    # CSS inline siempre aplicado
    st.markdown("""
    <style>
    /* Headers verdes */
    h1, h2 { color: #009639 !important; }
    
    /* Botones primarios verdes */
    .stButton button[kind="primary"],
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #009639, #006B2D) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
    }
    
    /* Sidebar navigation hover */
    [data-testid="stSidebar"] a:hover {
        background-color: rgba(0, 150, 57, 0.15) !important;
    }
    [data-testid="stSidebar"] a[aria-current="page"] {
        background-color: rgba(0, 150, 57, 0.2) !important;
        border-left: 4px solid #009639 !important;
    }
    
    /* Chat input verde */
    [data-testid="stChatInput"] {
        border: 2px solid #009639 !important;
        border-radius: 12px !important;
    }
    
    /* Info alerts verdes */
    .stAlert, .stInfo {
        background-color: rgba(0, 150, 57, 0.1) !important;
        border-left: 4px solid #009639 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def parse_modules(modules):
    """Parse modules from a JSON-like string or a comma-separated string."""
    try:
        return ast.literal_eval(modules)
    except (ValueError, SyntaxError):
        return [m.strip().strip('"') for m in modules.strip('[]').split(',')]


def get_menu(modules, user):
    """Build and display the sidebar menu based on the user's modules."""
    module_list = parse_modules(modules)
    
    with st.sidebar:
        # Header usando imagen GIF original
        st.image("images/st_pages.gif")
        st.markdown(f"## :red[Oracle AI] Accelerator :gray-badge[:material/smart_toy: {global_version}]")
        
        # Logo Serenísima - usando imagen si existe, sino HTML
        try:
            st.image("images/logo_SE.png", use_container_width=True)
        except:
            st.markdown("""
            <div style="background: white; border: 3px solid #009639; border-radius: 12px; padding: 15px; margin: 1rem 0; text-align: center;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #009639, #006B2D); border-radius: 10px; display: flex; align-items: center; justify-content: center; margin: 0 auto 8px;">
                    <span style="color: white; font-size: 1.75rem; font-weight: 700;">S</span>
                </div>
                <div style="color: #009639; font-weight: 700; font-size: 0.8rem;">SERENÍSIMA</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Usuario
        st.write(f"Hola, **:green[{user}]**")

        # Navegación principal
        st.page_link("app.py", label="Knowledge", icon=":material/book_ribbon:")
        
        if "Quiz" in st.session_state.get("modules", ""):
            st.page_link("pages/app_quiz.py", label="Quiz", icon=":material/quiz:")

        # AI Demos
        ai_demos = [
            ("AI Speech Real-Time", "pages/app_speech.py", ":material/mic:"),
            ("Select AI", "pages/app_chat_01.py", ":material/smart_toy:"),
            ("Select AI RAG", "pages/app_chat_02.py", ":material/plagiarism:"),
            ("Vector Database", "pages/app_chat_03.py", ":material/network_intelligence:")
        ]
        
        for label, page, icon in ai_demos:
            if label in module_list:
                display_label = "Chat Mastellone" if label == "Vector Database" else label
                st.page_link(page, label=display_label, icon=icon)
        
        # Settings Section
        st.subheader("Configuración")
        if "Administrator" in module_list:
            st.page_link("pages/app_users.py", label="Users", icon=":material/settings_account_box:")
            st.page_link("pages/app_user_group.py", label="User Group", icon=":material/group:")
        st.page_link("pages/app_profile.py", label="Perfil", icon=":material/manage_accounts:")
        
        # Reports Section
        if "Administrator" in module_list:
            st.subheader("Reportes")
            st.page_link("pages/app_quiz_report.py", label="Quiz Reports", icon=":material/analytics:")

        # Options section (del código original)
        st.subheader("Options")
        
        if st.session_state["page"] == "app_chat_01.py":
            with st.container(border=True, key="options_select_ai_container"):
                user_id = st.session_state["user_id"]
                df_agents = db_agent_service.get_all_agents_cache(user_id, force_update=True)
                df_agents = df_agents[df_agents["AGENT_TYPE"] == "Analytics"]

                action_options = ["narrate", "showsql", "explainsql", "runsql", "chat"]
                st.selectbox(
                    "Select AI Action",
                    options=action_options,
                    index=action_options.index(st.session_state.get("select_ai_action", "narrate"))
                    if st.session_state.get("select_ai_action", "narrate") in action_options
                    else 0,
                    key="select_ai_action"
                )
                
                st.checkbox("Analytics Agent", False, key="analytics_agent")
                st.session_state["sql_explain_agent"] = False

                analytics_enabled = st.session_state.get("analytics_agent", False)
                if analytics_enabled and not df_agents.empty:
                    st.selectbox(
                        "Select an Agent",
                        options=df_agents["AGENT_ID"],
                        format_func=lambda agent_id: f"{agent_id}: {df_agents.loc[df_agents['AGENT_ID'] == agent_id, 'AGENT_NAME'].values[0]}",
                        index=0,
                        key="selected_agent_id"
                    )
                elif not analytics_enabled:
                    st.session_state["selected_agent_id"] = st.session_state.get("selected_agent_id")

                col1, col2, = st.columns(2)

                with col1:
                    if st.button(key="clear", help="Clear Chat", label="", icon=":material/delete:", disabled=(not st.session_state["chat-select-ai"]), width="stretch"):
                        st.session_state["chat-select-ai"] = []
                        st.rerun()

                with col2:
                    st.download_button(
                        key="Save",
                        label="",
                        help="Save Chat",
                        icon=":material/download:",
                        data=json.dumps([
                            {k: v for k, v in msg.items() if k not in ("analytics_df", "analytics")}
                            for msg in st.session_state["chat-select-ai"]
                        ], indent=4, ensure_ascii=False),
                        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        disabled=(not st.session_state["chat-select-ai"]), 
                        width="stretch"
                    )
        
        if st.session_state["page"] == "app_chat_02.py":
            with st.container(border=True, key="options_select_ai_rag_container"):
                user_id = st.session_state["user_id"]
                df_agents = db_agent_service.get_all_agents_cache(user_id, force_update=False)
                df_agents = df_agents[df_agents["AGENT_TYPE"] == "Analytics"]
                
                action_options = ["narrate", "showsql", "explainsql", "runsql", "chat"]
                st.selectbox(
                    "Select AI Action",
                    options=action_options,
                    index=action_options.index(st.session_state.get("select_ai_rag_action", "narrate"))
                    if st.session_state.get("select_ai_rag_action", "narrate") in action_options
                    else 0,
                    key="select_ai_rag_action"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(
                        key="clear_rag", 
                        help="Clear Chat", 
                        label="", 
                        icon=":material/delete:",
                        disabled=(not st.session_state["chat-select-ai-rag"]),
                        width="stretch"
                    ):
                        st.session_state["chat-select-ai-rag"] = []
                        st.rerun()
                
                with col2:
                    st.download_button(
                        key="Save_rag",
                        label="",
                        help="Save Chat",
                        icon=":material/download:",
                        data=json.dumps([
                            {k: v for k, v in msg.items() if k not in ("analytics_df", "analytics")}
                            for msg in st.session_state["chat-select-ai-rag"]
                        ], indent=4, ensure_ascii=False),
                        file_name=f"chat_history_rag_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        disabled=(not st.session_state["chat-select-ai-rag"]),
                        width="stretch"
                    )
        
        if st.session_state["page"] == "app_chat_03.py":
            with st.container(border=True, key="options_vector_container"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(
                        key="clear_vector",
                        help="Clear Chat",
                        label="",
                        icon=":material/delete:",
                        disabled=(not st.session_state.get("chat-objects", [])),
                        width="stretch"
                    ):
                        from langchain_community.chat_message_histories import StreamlitChatMessageHistory
                        chat_ux_history = StreamlitChatMessageHistory(key="ux-history")
                        chat_ux_history.clear()
                        st.session_state["chat-tokens"] = 0
                        st.session_state["chat-save"] = []
                        st.session_state["chat_session_id"] = ""
                        st.session_state["chat-history"] = []
                        st.rerun()
                
                with col2:
                    st.download_button(
                        key="Save_vector",
                        label="",
                        help="Save Chat",
                        icon=":material/download:",
                        data=json.dumps(st.session_state.get("chat-save", []), indent=4),
                        file_name=f"chat_vector_{datetime.now().strftime('%H%M%S%f')}.json",
                        mime="text/plain",
                        disabled=(not st.session_state.get("chat-objects", [])),
                        width="stretch"
                    )

        if st.session_state["page"] == "app_quiz.py":
            with st.container(border=True, key="options_quiz_container"):
                user_id = st.session_state.get("user_id")
                df_files = db_file_service.get_all_files(user_id) if user_id else None
                df_quiz_files = df_files[df_files["MODULE_ID"] == 8] if df_files is not None and not df_files.empty else None
                
                if df_quiz_files is None or df_quiz_files.empty:
                    st.info("No quizzes available.", icon=":material/info:")
                else:
                    quiz_running = st.session_state.get("quiz_started", False) and not st.session_state.get("quiz_finished", False)
                    quiz_finished = st.session_state.get("quiz_finished", False)
                    
                    if not quiz_running and not quiz_finished:
                        selected_file_id = st.selectbox(
                            "Select Quiz",
                            options=df_quiz_files["FILE_ID"].tolist(),
                            format_func=lambda fid: f"{df_quiz_files.loc[df_quiz_files['FILE_ID'] == fid, 'FILE_DESCRIPTION'].values[0]}",
                            key="quiz_selected_file_id"
                        )
                        df_all_questions_sidebar = db_quiz_service.get_quiz_questions(selected_file_id)
                        st.caption(f"Total questions: **{len(df_all_questions_sidebar)}**")
                    
                    elif quiz_running:
                        st.markdown("**Evaluation in Progress**")
                        st.caption(f"{st.session_state.get('quiz_evaluation_name', '')}")
                        
                        if st.session_state.get("quiz_start_time"):
                            elapsed = int(time.time() - st.session_state["quiz_start_time"])
                            st.metric("Elapsed Time", f"{elapsed // 60}:{elapsed % 60:02d}")
                        
                        if st.button("Leave Quiz", type="secondary", icon=":material/cancel:", width="stretch"):
                            if st.session_state.get("quiz_confirm_abandon", False):
                                st.session_state["quiz_started"] = False
                                st.session_state["quiz_finished"] = False
                                st.session_state["quiz_confirm_abandon"] = False
                                st.rerun()
                            else:
                                st.session_state["quiz_confirm_abandon"] = True
                                st.warning("Click again to confirm")
                    
                    elif quiz_finished:
                        answers = st.session_state.get("quiz_answers", {})
                        if answers:
                            correct = sum(1 for ans in answers.values() if ans["is_correct"] == 1)
                            total = len(answers)
                            st.metric("Score", f"{(correct/total)*100:.1f}%")
                        
                        if st.button("Take Quiz", type="primary", icon=":material/refresh:", width="stretch"):
                            for key in list(st.session_state.keys()):
                                if key.startswith("quiz_") or key.startswith("saved_option_"):
                                    del st.session_state[key]
                            st.rerun()

        if st.session_state["page"] == "app_speech.py":
            with st.container(border=True, key="options_speech_container"):
                user_id = st.session_state["user_id"]
                df_agents = db_agent_service.get_all_agents_cache(user_id, force_update=False)
                df_agents = df_agents[df_agents["AGENT_TYPE"] == "Voice"]
                
                if not df_agents.empty:
                    use_select_ai = st.session_state.get("speech_use_select_ai", False)
                    st.selectbox(
                        "Select an Agent",
                        options=df_agents["AGENT_ID"],
                        format_func=lambda agent_id: f"{agent_id}: {df_agents.loc[df_agents['AGENT_ID'] == agent_id, 'AGENT_NAME'].values[0]}",
                        key="speech_agent_id",
                        disabled=use_select_ai
                    )
                
                language_options = ["Spanish", "Portuguese", "English"]
                current_language = st.session_state.get("language", "Spanish")
                default_index = language_options.index(current_language) if current_language in language_options else 0
                
                st.selectbox("Language", options=language_options, index=default_index, key="speech_language")
                st.checkbox("Select AI", value=st.session_state.get("speech_use_select_ai", False), key="speech_use_select_ai")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(key="clear_speech", help="Clear Conversation", label="", icon=":material/delete:", disabled=(not st.session_state.get("speech_conversation", [])), width="stretch"):
                        st.session_state["speech_conversation"] = []
                        st.session_state["speech_current_partial"] = ""
                        st.session_state["speech_processing_llm"] = False
                        st.rerun()
                
                with col2:
                    if st.session_state.get("speech_conversation", []):
                        st.download_button(
                            key="save_speech",
                            label="",
                            help="Save Conversation",
                            icon=":material/download:",
                            data=json.dumps(st.session_state["speech_conversation"], indent=4, ensure_ascii=False),
                            file_name=f"voice_chat_{datetime.now().strftime('%H%M%S%f')}.json",
                            mime="application/json",
                            width="stretch"
                        )
                    else:
                        st.button(key="save_speech_disabled", label="", help="Save Conversation", icon=":material/download:", disabled=True, width="stretch")

        # Sign out button
        if st.button(":material/exit_to_app: Cerrar sesión", type="secondary"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.clear()
            st.rerun()


def get_login():
    """Handle the login process and render the appropriate menu."""
    load_mastellone_css()
    
    if all(k in st.session_state for k in ["username", "user", "user_id", "modules", "chat-history", "chat-save"]):
        get_menu(st.session_state["modules"], st.session_state["user"])
        return True
    else:
        # Login Form - Estilo original mejorado
        with st.form('form-login'):
            st.markdown(f"## :red[Oracle AI] Accelerator :gray-badge[:material/smart_toy: {global_version}]")

            col1, col2 = st.columns(2)
            with col1:
                st.image("images/st_login.gif")
                st.markdown(
                    ":gray-badge[:material/smart_toy: Agents] "
                    ":gray-badge[:material/database: Autonomous 26ai] "
                    ":gray-badge[:material/database_search: Select AI] "
                    ":gray-badge[:material/plagiarism: Select AI RAG] "
                    ":gray-badge[:material/psychology: Generative AI] "
                    ":gray-badge[:material/privacy_tip: PII Detection] "
                    ":gray-badge[:material/flowchart: Agent Builder] "
                    ":gray-badge[:material/mic: AI Speech STT/TTS RealTime] "
                    ":gray-badge[:material/description: Document Understanding] "
                )
            with col2:                
                username = st.text_input('Usuario')
                password = st.text_input('Contraseña', type='password')
                language = st.selectbox("Idioma", options=("Spanish", "Portuguese", "English"))
                
                language_message = None
                match language:
                    case "Spanish":
                        language_message = "No tengo esa información."
                    case "Portuguese":
                        language_message = "Não tenho essa informação."
                    case "English":
                        language_message = "I don't have that information."

                btn_login = st.form_submit_button('Ingresar', type='primary')

            if btn_login:
                df = db_user_service.get_access(username, password)

                if df is not None and not df.empty:
                    user_state = df['USER_STATE'].iloc[0]

                    if user_state == 1:
                        st.session_state.update({
                            'page'               : "app.py",
                            'user_id'            : int(df['USER_ID'].iloc[0]),
                            'user_group_id'      : int(df['USER_GROUP_ID'].iloc[0]),
                            'modules'            : df['MODULE_NAMES'].iloc[0],
                            'username'           : df['USER_USERNAME'].iloc[0],
                            'user'               : f"{df['USER_NAME'].iloc[0]}, {df['USER_LAST_NAME'].iloc[0]}",
                            'language'           : language,
                            'language-message'   : language_message,
                            'chat-select-ai'     : [],
                            'chat-select-ai-rag' : [],
                            'chat-docs'          : [],
                            'chat-save'          : [],
                            'chat-modules'       : [],
                            'chat-objects'       : [],
                            'chat-agent'         : 0,
                            'chat-history'       : [],
                            'ai-agent'           : None
                        })
                        st.switch_page("app.py")
                    else:
                        st.error("Este usuario está desactivado.", icon=":material/gpp_maybe:")
                else:
                    st.error("Usuario o contraseña incorrectos", icon=":material/gpp_maybe:")
        
        return False
