"""
Footer Component - Mastellone/Serenísima Theme
Oracle AI Accelerator v2.0.4

VERSIÓN FINAL - Footer funcional
"""

import streamlit as st


def get_footer():
    """
    Footer con tema Mastellone/Serenísima
    Todo en un solo bloque de st.markdown para evitar problemas de renderizado
    """
    footer_html = """
    <style>
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
        
        .mastellone-footer .serenisima-badge {
            background: linear-gradient(135deg, #009639 0%, #006B2D 100%);
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 700;
            color: white;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .mastellone-footer .oracle-badge {
            background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
            padding: 4px 10px;
            border-radius: 8px;
            font-weight: 700;
            color: white;
            font-size: 11px;
        }
        
        .mastellone-footer a {
            color: #4CAF50 !important;
            text-decoration: none;
        }
        
        .mastellone-footer a:hover {
            color: #009639 !important;
        }
        
        .footer-section {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .footer-divider {
            color: #404040;
        }
        
        /* Espacio para el footer fijo */
        .main .block-container {
            padding-bottom: 60px !important;
        }
        
        @media (max-width: 768px) {
            .mastellone-footer {
                flex-direction: column;
                text-align: center;
                padding: 12px 15px;
            }
            .footer-section {
                justify-content: center;
            }
        }
    </style>
    
    <div class="mastellone-footer">
        <div class="footer-section">
            <span class="serenisima-badge">SERENÍSIMA</span>
            <span class="footer-divider">|</span>
            <span>© 2025 Mastellone Hnos. S.A.</span>
            <span class="footer-divider">|</span>
            <span>Asistente Virtual Serenísima</span>
        </div>
        <div class="footer-section">
            <span>Impulsado por</span>
            <span class="oracle-badge">ORACLE AI</span>
        </div>
        <div class="footer-section">
            <span>Desarrollado por</span>
            <a href="https://pe.linkedin.com/in/jganggini" target="_blank">Joel Ganggini</a>
        </div>
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)
