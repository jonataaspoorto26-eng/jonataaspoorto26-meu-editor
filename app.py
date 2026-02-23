import streamlit as st
from PIL import Image, ImageOps, ImageEnhance

st.title("Meu Editor de Fotos Pro 📸")
st.write("Criei esse app pelo celular!")

arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    img = Image.open(arquivo).convert('RGB')
    st.image(img, caption="Original", use_container_width=True)

    st.sidebar.header("Filtros")
    filtro = st.sidebar.selectbox("Efeito", ["Nenhum", "Preto e Branco", "Inverter"])
    brilho = st.sidebar.slider("Brilho", 0.5, 2.0, 1.0)

    if filtro == "Preto e Branco":
        img = ImageOps.grayscale(img)
    elif filtro == "Inverter":
        img = ImageOps.invert(img)
    
    img = ImageEnhance.Brightness(img).enhance(brilho)
    st.image(img, caption="Resultado Final", use_container_width=True)
  
