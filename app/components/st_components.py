"""
Components Helper - Mastellone/Serenísima Theme
Oracle AI Accelerator v2.0.4

Componentes auxiliares para la interfaz de chat y otras páginas
"""

import streamlit as st


def get_chat_header(title: str = "Chat Mastellone", subtitle: str = None, show_db_status: bool = True):
    """
    Renderiza el header del chat con status de vector database
    
    Args:
        title: Título principal
        subtitle: Subtítulo opcional
        show_db_status: Mostrar banner de estado de Vector DB
    """
    # Header principal
    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <h1 style="
            color: #009639;
            font-weight: 700;
            font-size: 1.75rem;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <span>💬</span> {title}
        </h1>
    """, unsafe_allow_html=True)
    
    if subtitle:
        st.markdown(f"""
        <p style="color: #B0B0B0; font-size: 0.95rem; margin-top: 4px;">
            {subtitle}
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Banner de Vector Database
    if show_db_status:
        st.markdown("""
        <div style="
            background: rgba(0, 150, 57, 0.08);
            border: 1px solid rgba(0, 150, 57, 0.2);
            border-left: 4px solid #009639;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <div style="
                width: 12px;
                height: 12px;
                background: #009639;
                border-radius: 50%;
                box-shadow: 0 0 8px rgba(0, 150, 57, 0.5);
                animation: pulse-glow 2s infinite;
            "></div>
            <span style="color: #009639; font-weight: 600;">Vector Database Activa</span>
            <span style="color: #606060;">|</span>
            <span style="color: #B0B0B0; font-size: 0.9rem;">
                Búsquedas semánticas habilitadas con documentos de Mastellone
            </span>
        </div>
        
        <style>
            @keyframes pulse-glow {
                0%, 100% { 
                    box-shadow: 0 0 4px rgba(0, 150, 57, 0.4);
                    opacity: 1;
                }
                50% { 
                    box-shadow: 0 0 12px rgba(0, 150, 57, 0.8);
                    opacity: 0.8;
                }
            }
        </style>
        """, unsafe_allow_html=True)


def get_source_citations(sources: list):
    """
    Renderiza las fuentes citadas de forma elegante
    
    Args:
        sources: Lista de nombres de archivos fuente
    """
    if not sources:
        return
    
    sources_html = "".join([
        f'<span class="source-citation">📄 {source}</span>'
        for source in sources
    ])
    
    st.markdown(f"""
    <style>
        .source-container {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 6px;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .source-label {{
            color: #808080;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .source-citation {{
            display: inline-flex;
            align-items: center;
            background: rgba(42, 42, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 0.8rem;
            color: #B0B0B0;
            transition: all 0.2s ease;
            cursor: default;
        }}
        
        .source-citation:hover {{
            border-color: #009639;
            color: #009639;
            background: rgba(0, 150, 57, 0.1);
        }}
    </style>
    
    <div class="source-container">
        <span class="source-label">📚 Fuente(s):</span>
        {sources_html}
    </div>
    """, unsafe_allow_html=True)


def get_token_metrics_inline(rate: str, tokens_current: int, tokens_total: int):
    """
    Renderiza métricas de tokens de forma inline
    """
    st.markdown(f"""
    <div style="
        display: flex;
        gap: 10px;
        margin-top: 10px;
    ">
        <span style="
            background: #009639;
            color: white;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        ">Rate: {rate}</span>
        <span style="
            background: #009639;
            color: white;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        ">Tokens: {tokens_current} to {tokens_total}</span>
    </div>
    """, unsafe_allow_html=True)


def get_empty_state(message: str, icon: str = "📭"):
    """
    Estado vacío con estilo consistente
    """
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(42, 42, 42, 0.5);
        border-radius: 12px;
        border: 1px dashed rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <p style="color: #808080; font-size: 1rem; margin: 0;">{message}</p>
    </div>
    """, unsafe_allow_html=True)


def get_success_message(message: str, icon: str = "✅"):
    """
    Mensaje de éxito con estilo Mastellone
    """
    st.markdown(f"""
    <div style="
        background: rgba(0, 150, 57, 0.1);
        border-left: 4px solid #009639;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 1.25rem;">{icon}</span>
        <span style="color: #4CAF50; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def get_error_message(message: str, icon: str = "❌"):
    """
    Mensaje de error con estilo consistente
    """
    st.markdown(f"""
    <div style="
        background: rgba(231, 76, 60, 0.1);
        border-left: 4px solid #E74C3C;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 1.25rem;">{icon}</span>
        <span style="color: #E74C3C; font-weight: 500;">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def get_processing(show: bool = True):
    """
    Indicador de procesamiento global (compatible con código existente)
    """
    if show:
        st.toast("Procesando...", icon="⏳")


def get_error(message: str):
    """
    Mostrar error (compatible con código existente)
    """
    st.error(message, icon="❌")


def get_success(message: str, icon: str = "✅"):
    """
    Mostrar éxito (compatible con código existente)
    """
    st.success(message, icon=icon)


def get_knowledge_header():
    """
    Header para la página de Knowledge
    """
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="
            color: #009639;
            font-weight: 700;
            font-size: 1.75rem;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        ">
            <span>📚</span> Base de Conocimiento Mastellone
        </h1>
        <p style="color: #B0B0B0; font-size: 0.95rem; margin-top: 6px;">
            Administra documentos para el Asistente Virtual Serenísima.
        </p>
    </div>
    
    <div style="
        background: rgba(0, 150, 57, 0.08);
        border: 1px solid rgba(0, 150, 57, 0.2);
        border-left: 4px solid #009639;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 1.1rem;">ℹ️</span>
        <span style="color: #009639; font-weight: 600;">Vector Database habilitada</span>
        <span style="color: #606060;">-</span>
        <span style="color: #B0B0B0; font-size: 0.9rem;">
            Los documentos se procesan automáticamente para búsquedas semánticas.
        </span>
    </div>
    """, unsafe_allow_html=True)
