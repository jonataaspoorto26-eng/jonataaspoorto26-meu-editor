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

    # --- PROCESSAMENTO ---
    
    # 1. Exposição (usando Brilho como base)
    img = ImageEnhance.Brightness(img).enhance(exposicao)
    
    # 2. Contraste
    img = ImageEnhance.Contrast(img).enhance(contraste)
    
    # 3. Realces e Sombras (Simulação matemática)
    img_array = np.array(img).astype(float)
    if realces != 1.0:
        img_array[img_array > 128] *= realces
    if sombras != 1.0:
        img_array[img_array <= 128] *= sombras
        
    # 4. Brancos e Pretos
    img_array = img_array + brancos  # Ajusta os tons claros
    img_array = img_array + pretos   # Ajusta os tons escuros
    
    # Garante que as cores fiquem no limite de 0 a 255
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    img = Image.fromarray(img_array)

    # --- EXIBIÇÃO ---
    st.image(img, caption="Imagem Ajustada", use_container_width=True)
    
    # Botão de download atualizado com a imagem editada
    import io
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    st.download_button("Baixar Foto Editada", data=byte_im, file_name="foto_pro.jpg", mime="image/jpeg")
