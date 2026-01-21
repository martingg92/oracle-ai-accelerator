"""
Footer Component - Mastellone/Serenísima Theme (Dark Mode)
Oracle AI Accelerator v2.0.4

Footer fijo con badges Serenísima y Oracle
"""

import streamlit as st


def get_footer():
    """Footer con tema Mastellone/Serenísima"""
    st.markdown(
        """
        <style>
            /* Footer fijo en la parte inferior */
            .mastellone-footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background: linear-gradient(90deg, #1E1E1E 0%, #2B2D31 100%);
                border-top: 2px solid #009639;
                color: #B0B0B0;
                font-size: 12px;
                padding: 10px 20px;
                z-index: 999;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }
            
            .footer-left {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .footer-center {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .footer-right {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .serenisima-badge {
                background: linear-gradient(135deg, #009639 0%, #006B2D 100%);
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: 700;
                color: white;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 2px 6px rgba(0, 150, 57, 0.3);
            }
            
            .oracle-badge {
                background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
                padding: 4px 10px;
                border-radius: 8px;
                font-weight: 700;
                color: white;
                font-size: 11px;
                box-shadow: 0 2px 6px rgba(255, 0, 0, 0.2);
            }
            
            .footer-link {
                color: #4CAF50 !important;
                text-decoration: none;
                transition: color 0.2s ease;
            }
            
            .footer-link:hover {
                color: #009639 !important;
            }
            
            .footer-separator {
                color: #404040;
                margin: 0 4px;
            }
            
            /* Espacio para el footer fijo */
            .main .block-container {
                padding-bottom: 60px !important;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .mastellone-footer {
                    flex-direction: column;
                    text-align: center;
                    padding: 12px 15px;
                }
                
                .footer-left, .footer-center, .footer-right {
                    justify-content: center;
                }
            }
        </style>
        
        <div class="mastellone-footer">
            <div class="footer-left">
                <span class="serenisima-badge">SERENÍSIMA</span>
                <span class="footer-separator">|</span>
                <span>© 2025 Mastellone Hnos. S.A.</span>
                <span class="footer-separator">|</span>
                <span>Asistente Virtual Serenísima</span>
            </div>
            
            <div class="footer-center">
                <span>Impulsado por</span>
                <span class="oracle-badge">ORACLE AI</span>
            </div>
            
            <div class="footer-right">
                <span>Desarrollado por</span>
                <a href="https://pe.linkedin.com/in/jganggini" target="_blank" class="footer-link">
                    Joel Ganggini
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_vector_db_status_banner(is_active: bool = True, custom_text: str = None):
    """
    Banner de estado de Vector Database
    
    Args:
        is_active: Si la base de datos vectorial está activa
        custom_text: Texto personalizado para mostrar
    """
    if is_active:
        status_color = "#009639"
        status_icon = "🟢"
        status_text = custom_text or "Vector Database Activa"
        subtitle = "Búsquedas semánticas habilitadas con documentos de Mastellone"
    else:
        status_color = "#FF6B6B"
        status_icon = "🔴"
        status_text = custom_text or "Vector Database Inactiva"
        subtitle = "Las búsquedas semánticas no están disponibles"
    
    st.markdown(f"""
    <div style="
        background: rgba(0, 150, 57, 0.08);
        border: 1px solid rgba(0, 150, 57, 0.25);
        border-left: 4px solid {status_color};
        border-radius: 10px;
        padding: 12px 16px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 12px;
    ">
        <span style="font-size: 1.25rem;">{status_icon}</span>
        <div>
            <span style="color: {status_color}; font-weight: 600;">{status_text}</span>
            <span style="color: #B0B0B0; margin-left: 8px;">|</span>
            <span style="color: #B0B0B0; margin-left: 8px; font-size: 0.9rem;">{subtitle}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def get_processing_indicator(show: bool = True):
    """
    Indicador de procesamiento
    """
    if show:
        st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 16px;
            background: rgba(0, 150, 57, 0.1);
            border-radius: 8px;
            margin: 0.5rem 0;
        ">
            <div style="
                width: 20px;
                height: 20px;
                border: 3px solid rgba(0, 150, 57, 0.3);
                border-top-color: #009639;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            "></div>
            <span style="color: #009639; font-weight: 500;">Procesando...</span>
        </div>
        
        <style>
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
        """, unsafe_allow_html=True)
