import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import numpy as np

st.set_page_config(page_title="Editor Pro", layout="centered")
st.title("Meu Editor de Fotos Pro 📸")

arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    img = Image.open(arquivo).convert('RGB')
    
    # Criando colunas para os botões ficarem lado a lado
    col1, col2, col3 = st.columns(3)
    
    # Variáveis de controle na memória (Session State)
    if 'rotacao' not in st.session_state: st.session_state.rotacao = 0
    
    with col1:
        if st.button("Girar 90°"):
            st.session_state.rotacao += 90
            
    with col2:
        espelhar = st.checkbox("Espelhar")
        
    with col3:
        sepia = st.checkbox("Filtro Sépia")

    # Aplicando as transformações
    img = img.rotate(st.session_state.rotacao, expand=True)
    
    if espelhar:
        img = ImageOps.mirror(img)
        
    if sepia:
        # Lógica matemática para o efeito sépia
        img_array = np.array(img)
        filtro_sepia = np.array([[0.393, 0.769, 0.189], 
                                [0.349, 0.686, 0.168], 
                                [0.272, 0.534, 0.131]])
        img_array = img_array.dot(filtro_sepia.T)
        img_array /= img_array.max()
        img = Image.fromarray((img_array * 255).astype(np.uint8))

    # Barra lateral para ajustes finos
    st.sidebar.header("Ajustes de Luz")
    brilho = st.sidebar.slider("Brilho", 0.5, 2.0, 1.0)
    contraste = st.sidebar.slider("Contraste", 0.5, 2.0, 1.0)
    
    img = ImageEnhance.Brightness(img).enhance(brilho)
    img = ImageEnhance.Contrast(img).enhance(contraste)

    st.image(img, caption="Resultado Final", use_container_width=True)
    
    # Botão de Download
    st.download_button("Baixar Imagem", data=arquivo, file_name="editada.jpg")
