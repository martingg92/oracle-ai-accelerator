"""
Footer Component - Mastellone/Serenísima Theme (Dark Mode)
Oracle AI Accelerator v2.0.4

Mantiene el fondo oscuro con gradiente verde Serenísima.
"""

import streamlit as st

def get_footer():
    """Footer con tema Mastellone/Serenísima"""
    st.markdown(
        """
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background: linear-gradient(135deg, #2B2D31 0%, #1E1E1E 100%);
                border-top: 2px solid #009639;
                color: white;
                font-size: 11px;
                padding: 8px 15px;
                z-index: 300;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .serenisima-badge {
                background: linear-gradient(135deg, #009639, #006B2D);
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: 700;
                color: white;
            }
            
            .oracle-badge {
                background: linear-gradient(135deg, #FF0000, #CC0000);
                padding: 3px 8px;
                border-radius: 8px;
                font-weight: 700;
                color: white;
            }
            
            .footer a {
                color: #4CAF50;
                text-decoration: none;
            }
        </style>
        <div class='footer'>
            <div>
                <span class='serenisima-badge'>SERENÍSIMA</span>
                | © 2025 Mastellone Hnos. S.A.
            </div>
            <div>
                Powered by <span class='oracle-badge'>ORACLE AI</span>
            </div>
            <div>
                Desarrollado por <a href='https://pe.linkedin.com/in/jganggini' target='_blank'>Joel Ganggini</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
