"""
Footer Component - Mastellone/Serenísima Theme (Dark Mode)
Oracle AI Accelerator v2.0.4

Mantiene el fondo oscuro con gradiente verde Serenísima.
"""

import streamlit as st

def get_footer():
    """
    Displays a fixed footer at the bottom with Mastellone/Serenísima branding.
    Mantiene el esquema oscuro con acentos verdes.
    """
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
                text-align: center;
                font-size: 12px;
                padding: 10px 20px;
                z-index: 300;
                box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
            }
            
            .footer-left {
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 10px;
                color: #B0B0B0;
            }
            
            .footer-center {
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 11px;
            }
            
            .footer-right {
                display: flex;
                align-items: center;
                gap: 8px;
                color: #B0B0B0;
            }

            .footer a {
                text-decoration: none;
                color: #4CAF50;
                font-weight: 600;
                transition: color 0.3s ease;
            }
            
            .footer a:hover {
                color: #009639;
            }
            
            .serenisima-badge {
                background: linear-gradient(135deg, #009639, #006B2D);
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 10px;
                font-weight: 700;
                color: white;
                letter-spacing: 0.5px;
            }
            
            .oracle-badge {
                background: linear-gradient(135deg, #FF0000, #CC0000);
                padding: 4px 10px;
                border-radius: 10px;
                font-size: 9px;
                font-weight: 700;
                color: white;
                letter-spacing: 0.5px;
            }
            
            .divider {
                color: rgba(255, 255, 255, 0.3);
                margin: 0 8px;
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .footer {
                    flex-direction: column;
                    gap: 8px;
                    padding: 12px 10px;
                }
                
                .footer-left,
                .footer-center,
                .footer-right {
                    width: 100%;
                    justify-content: center;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Footer content
    st.markdown(
        """
        <div class='footer'>
            <div class='footer-left'>
                <span class='serenisima-badge'>SERENÍSIMA</span>
                <span class='divider'>|</span>
                <span>© 2025 Mastellone Hnos. S.A.</span>
            </div>
            
            <div class='footer-center'>
                <span>Powered by</span>
                <span class='oracle-badge'>ORACLE AI</span>
            </div>
            
            <div class='footer-right'>
                <span>Desarrollado por</span>
                <a href='https://pe.linkedin.com/in/jganggini' target='_blank'>Joel Ganggini</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
