import streamlit as st
import os
import base64


def logo():
    logo_path = "img/agent_gallery.png"

    def get_image_base64(path):
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        return None

    img_b64 = get_image_base64(logo_path)

    if img_b64:
        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{img_b64}" class="logo-img">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<h1 style='text-align: center; color: #6a0dad;'>Agent Gallery</h1>",
            unsafe_allow_html=True,
        )
