import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

st.set_page_config(page_title="Editor Pro v3", layout="centered")
st.title("Meu Editor de Fotos Pro 📸")

arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    img = Image.open(arquivo).convert('RGB')
    
    # --- BARRA LATERAL DE COMPOSIÇÃO DE LUZ ---
    st.sidebar.header("✨ Composição da Luz")
    
    # Criando as barras medidoras (Sliders)
    exposicao = st.sidebar.slider("Exposição", 0.0, 2.0, 1.0)
    contraste = st.sidebar.slider("Contraste", 0.0, 2.0, 1.0)
    realces = st.sidebar.slider("Realces (Highlights)", 0.0, 2.0, 1.0)
    sombras = st.sidebar.slider("Sombras", 0.0, 2.0, 1.0)
    brancos = st.sidebar.slider("Brancos", -50, 50, 0)
    pretos = st.sidebar.slider("Pretos", -50, 50, 0)

    # --- PROCESSAMENTO AVANÇADO ---
    img_array = np.array(img).astype(float)
    
    # 1. Exposição e Contraste (Bibliotecas padrão são ótimas para isso)
    img = ImageEnhance.Brightness(img).enhance(exposicao)
    img = ImageEnhance.Contrast(img).enhance(contraste)
    img_array = np.array(img).astype(float)

    # 2. Lógica de Máscaras para Brancos e Pretos
    # Criamos uma máscara que identifica onde a imagem é clara (>180) ou escura (<70)
    mascara_brancos = (img_array > 180).astype(float)
    mascara_pretos = (img_array < 70).astype(float)

    # Aplicamos o ajuste apenas onde a máscara permite
    # O valor é suavizado para não criar manchas estranhas
    img_array += (brancos * mascara_brancos)
    img_array += (pretos * mascara_pretos)

    # 3. Realces e Sombras (Ajuste fino)
    if realces != 1.0:
        img_array[img_array > 128] *= realces
    if sombras != 1.0:
        img_array[img_array <= 128] *= sombras

    # Garante que as cores fiquem no limite de 0 a 255
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_array)
    
