"""
Login Component - Mastellone/Serenísima Theme
Oracle AI Accelerator v2.0.4

Diseño: Tarjeta verde centrada con logo "S", badges y formulario
"""

import ast
import streamlit as st
from datetime import datetime

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


def load_login_css():
    """CSS específico para la página de login con diseño verde centrado"""
    st.markdown("""
    <style>
    /* ================================================================
       LOGIN PAGE - Mastellone/Serenísima Design
       Tarjeta verde centrada con gradiente
       ================================================================ */
    
    /* Ocultar elementos de Streamlit en login */
    .login-page header[data-testid="stHeader"],
    .login-page footer,
    .login-page #MainMenu {
        display: none !important;
    }
    
    /* Contenedor principal del login */
    .login-card {
        max-width: 420px;
        margin: 2rem auto;
        padding: 2.5rem 2rem;
        background: linear-gradient(160deg, #009639 0%, #007A2F 50%, #005A22 100%);
        border-radius: 24px;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.4),
            0 0 40px rgba(0, 150, 57, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    /* Efecto de brillo sutil */
    .login-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -50%;
        width: 200%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.03),
            transparent
        );
        pointer-events: none;
    }
    
    /* Logo circular con "S" */
    .login-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #4CAF50 0%, #81C784 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        box-shadow: 
            0 8px 24px rgba(0, 0, 0, 0.3),
            inset 0 2px 4px rgba(255, 255, 255, 0.3);
        position: relative;
    }
    
    .login-logo span {
        color: white;
        font-family: 'Segoe UI', 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Título principal */
    .login-title {
        color: white;
        font-family: 'Segoe UI', 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.75rem;
        line-height: 1.3;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Subtítulo */
    .login-subtitle {
        color: rgba(255, 255, 255, 0.85);
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    /* Contenedor de badges */
    .login-badges {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 1.75rem;
    }
    
    .login-badge {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 50px;
        padding: 0.4rem 0.85rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: white;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        transition: all 0.2s ease;
    }
    
    .login-badge:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-1px);
    }
    
    /* Labels del formulario */
    .login-label {
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
        text-align: left;
        display: block;
        margin-bottom: 0.4rem;
        margin-top: 0.75rem;
    }
    
    /* Estilos para inputs dentro del login */
    .login-card .stTextInput > div > div > input {
        background: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        color: #333 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    .login-card .stTextInput > div > div > input::placeholder {
        color: #999 !important;
    }
    
    .login-card .stTextInput > div > div > input:focus {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), 0 0 0 3px rgba(255, 255, 255, 0.4) !important;
        outline: none !important;
    }
    
    /* Select/Dropdown */
    .login-card .stSelectbox > div > div {
        background: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    .login-card .stSelectbox > div > div > div {
        color: #333 !important;
    }
    
    /* Botón de login */
    .login-card .stButton > button {
        width: 100%;
        background: white !important;
        color: #009639 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-top: 1.25rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        cursor: pointer;
    }
    
    .login-card .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3) !important;
    }
    
    .login-card .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Footer del login */
    .login-footer {
        margin-top: 1.75rem;
        padding-top: 1.25rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.8rem;
    }
    
    /* Mensaje de error */
    .login-card .stAlert {
        background: rgba(231, 76, 60, 0.2) !important;
        border: 1px solid rgba(231, 76, 60, 0.4) !important;
        border-radius: 10px !important;
        color: white !important;
        margin-top: 1rem;
    }
    
    /* Ocultar labels de Streamlit dentro del login */
    .login-card .stTextInput > label,
    .login-card .stSelectbox > label {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


def parse_modules(modules):
    """
    Parse modules from a JSON-like string or a comma-separated string.
    """
    try:
        return ast.literal_eval(modules)
    except (ValueError, SyntaxError):
        return [m.strip().strip('"') for m in modules.strip('[]').split(',')]


def get_menu(modules, user):
    """
    Build and display the sidebar menu based on the user's modules.
    """
    module_list = parse_modules(modules)
    
    with st.sidebar:
        # Header con versión
        st.markdown(f"""
        <div style="padding: 0.5rem 0;">
            <span style="color: #FF0000; font-weight: 700;">Oracle AI</span>
            <span style="color: white; font-weight: 600;">Accelerator</span>
            <span style="
                background: #3A3B46;
                color: #B0B0B0;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 0.7rem;
                margin-left: 0.5rem;
            ">v{global_version}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Logo Serenísima con diseño mejorado
        st.markdown("""
        <div style="
            background: white;
            border: 3px solid #009639;
            border-radius: 12px;
            padding: 12px;
            margin: 1rem 0;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 150, 57, 0.2);
        ">
            <div style="
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #009639 0%, #006B2D 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 8px;
            ">
                <span style="color: white; font-size: 2rem; font-weight: 700;">S</span>
            </div>
            <div style="color: #009639; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
                SERENÍSIMA
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Usuario actual
        st.markdown(f"""
        <div style="
            padding: 0.75rem;
            margin-bottom: 1rem;
        ">
            <span style="color: #B0B0B0; font-size: 0.85rem;">Hola,</span><br>
            <span style="color: #009639; font-weight: 600; font-size: 1rem;">{user}</span>
        </div>
        """, unsafe_allow_html=True)

        # Navegación principal
        st.page_link("app.py", label="Knowledge", icon="📚")
        
        if "Quiz" in st.session_state.get("modules", ""):
            st.page_link("pages/app_quiz.py", label="Quiz", icon="📝")

        # AI Demos Section
        ai_demos = [
            ("AI Speech Real-Time", "pages/app_speech.py", "🎤"),
            ("Select AI", "pages/app_chat_01.py", "🤖"),
            ("Select AI RAG", "pages/app_chat_02.py", "🔍"),
            ("Vector Database", "pages/app_chat_03.py", "💬")
        ]
        available_demos = [demo for demo in ai_demos if demo[0] in module_list]

        if available_demos:
            for label, page, icon in available_demos:
                display_label = "Chat Mastellone" if label == "Vector Database" else label
                st.page_link(page, label=display_label, icon=icon)
        
        # Settings Section
        st.markdown("""
        <div style="color: #009639; font-weight: 600; font-size: 0.8rem; margin-top: 1.5rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">
            CONFIGURACIÓN
        </div>
        """, unsafe_allow_html=True)
        
        if "Administrator" in module_list:
            st.page_link("pages/app_users.py", label="Users", icon="👥")
            st.page_link("pages/app_user_group.py", label="User Group", icon="👨‍👩‍👧‍👦")
        st.page_link("pages/app_profile.py", label="Perfil", icon="👤")
        
        # Reports Section
        if "Administrator" in module_list:
            st.markdown("""
            <div style="color: #009639; font-weight: 600; font-size: 0.8rem; margin-top: 1.5rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">
                REPORTES
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/app_quiz_report.py", label="Quiz Reports", icon="📊")

        # Espacio flexible
        st.markdown("<div style='flex-grow: 1; min-height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Powered by Oracle AI badge
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #FF0000, #CC0000);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.8rem;
            margin-top: 1rem;
        ">
            ⚡ Powered by ORACLE AI
        </div>
        """, unsafe_allow_html=True)
        
        # Sign out button
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar sesión", type="secondary", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.clear()
            st.rerun()


def render_login_form():
    """Renderiza el formulario de login con el nuevo diseño verde"""
    
    load_login_css()
    
    # Inicio del contenedor HTML
    st.markdown("""
    <div class="login-card">
        <div class="login-logo">
            <span>S</span>
        </div>
        <h1 class="login-title">Asistente Virtual<br>Serenísima</h1>
        <p class="login-subtitle">Powered by Oracle AI Accelerator v2.0.4</p>
        
        <div class="login-badges">
            <span class="login-badge">🤖 Agents</span>
            <span class="login-badge">📊 Vector DB</span>
            <span class="login-badge">✨ Generative AI</span>
            <span class="login-badge">🔍 RAG</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Formulario de Streamlit
    with st.form('form-login', clear_on_submit=False):
        st.markdown('<span class="login-label">Usuario</span>', unsafe_allow_html=True)
        username = st.text_input('Usuario', placeholder='Ingresa tu usuario', label_visibility='collapsed')
        
        st.markdown('<span class="login-label">Contraseña</span>', unsafe_allow_html=True)
        password = st.text_input('Contraseña', type='password', placeholder='Ingresa tu contraseña', label_visibility='collapsed')
        
        st.markdown('<span class="login-label">Idioma</span>', unsafe_allow_html=True)
        language = st.selectbox(
            "Idioma",
            options=["Español", "English", "Português"],
            label_visibility='collapsed'
        )
        
        # Mapeo de idiomas
        language_map = {
            "Español": "Spanish",
            "English": "English", 
            "Português": "Portuguese"
        }
        language_internal = language_map.get(language, "Spanish")
        
        language_message_map = {
            "Spanish": "No tengo esa información.",
            "Portuguese": "Não tenho essa informação.",
            "English": "I don't have that information."
        }
        language_message = language_message_map.get(language_internal, "No tengo esa información.")
        
        btn_login = st.form_submit_button('Ingresar', type='primary', use_container_width=True)
        
        if btn_login:
            if not username or not password:
                st.error("Por favor ingresa usuario y contraseña")
            else:
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
                            'language'           : language_internal,
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
                        st.error("Este usuario está desactivado.")
                else:
                    st.error("Usuario o contraseña incorrectos")
    
    # Footer del login
    st.markdown("""
        <div class="login-footer">
            Oracle AI Accelerator · v2.0.4 · Mastellone Hnos. S.A.
        </div>
    </div>
    """, unsafe_allow_html=True)


def get_login():
    """
    Handle the login process and render the appropriate menu.
    """
    # Cargar CSS personalizado
    load_mastellone_css()
    
    if all(k in st.session_state for k in ["username", "user", "user_id", "modules", "chat-history", "chat-save"]):
        get_menu(st.session_state["modules"], st.session_state["user"])
        return True
    else:
        # Mostrar formulario de login
        render_login_form()
        return False
