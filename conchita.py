import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# Configuración de la página
st.set_page_config(page_title="Conchita Image Gen", page_icon="🎨")
st.title("🎨 Conchita Image Generator")

# Sidebar
with st.sidebar:
    api_key = st.text_input("", type="password")
    st.info("Powered by Nano Banana technology.")

# Interfaz Principal
if api_key:
    client = genai.Client(api_key=api_key)

    # Entradas del usuario
    description = st.text_area("What image do you want to generate?", 
                               placeholder="e.g., A futuristic city made of candy")

    style = st.radio(
        "Choose your style:",
        ["Photorealistic", "Cartoon", "Oil Painting", "Cyberpunk"],
        horizontal=True
    )

    if st.button("Generate with Conchita"):
        if description:
            # Combinar descripción con estilo
            full_prompt = f"Create an image of {description} in {style} style."

            with st.spinner("Conchita is painting your masterpiece..."):
                try:
                    # NOTA: En la imagen ponía 'gemini-2.5-flash-image'.
                    # He puesto 'imagen-3.0-generate-001' que es el estándar actual para imágenes.
                    # Si tienes acceso a la beta de Gemini 2.0, cambia el nombre aquí.
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-image", 
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=["IMAGE"]
                        )
                    )

                    # Procesar la respuesta para encontrar la imagen
                    for part in response.parts:
                        if part.inline_data:
                            # Convertir los bytes a imagen visible
                            image_bytes = part.inline_data.data
                            st.image(image_bytes, caption=f"Generated: {description}")
                            
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a description first.")
else:
    st.warning("Please enter your API Key in the sidebar to start.")
