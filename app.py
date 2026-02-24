import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import io

# Configuração da página
st.set_page_config(page_title="Editor Pro v3", layout="centered")
st.title("Meu Editor de Fotos Pro 📸")

arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    # Abrir a imagem de forma segura
    try:
        img_original = Image.open(arquivo).convert('RGB')
        
        # --- BARRA LATERAL ---
        st.sidebar.header("✨ Composição da Luz")
        exposicao = st.sidebar.slider("Exposição", 0.0, 2.0, 1.0)
        contraste = st.sidebar.slider("Contraste", 0.0, 2.0, 1.0)
        realces = st.sidebar.slider("Realces", 0.0, 2.0, 1.0)
        sombras = st.sidebar.slider("Sombras", 0.0, 2.0, 1.0)
        brancos = st.sidebar.slider("Brancos", -100.0, 100.0, 0.0)
        pretos = st.sidebar.slider("Pretos", -100.0, 100.0, 0.0)

        # --- PROCESSAMENTO ---
        # 1. Aplicar Exposição e Contraste primeiro
        img_edit = ImageEnhance.Brightness(img_original).enhance(exposicao)
        img_edit = ImageEnhance.Contrast(img_edit).enhance(contraste)
        
        # Converter para Array para manipulação precisa de pixels
        img_array = np.array(img_edit).astype(float)

        # 2. Máscaras para Brancos e Pretos (Lógica Seletiva)
        # Brancos: Afeta apenas pixels acima de 200 de luminosidade
        mask_brancos = np.clip((img_array - 200) / 55, 0, 1) if brancos != 0 else 0
        img_array += brancos * mask_brancos

        # Pretos: Afeta apenas pixels abaixo de 60 de luminosidade
        mask_pretos = np.clip((60 - img_array) / 60, 0, 1) if pretos != 0 else 0
        img_array += pretos * mask_pretos

        # 3. Realces e Sombras
        if realces != 1.0:
            img_array[img_array > 128] *= realces
        if sombras != 1.0:
            img_array[img_array <= 128] *= sombras

        # Voltar para o formato de imagem
        img_final = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

        # --- EXIBIÇÃO ---
        st.image(img_final, caption="Resultado com Ajustes Seletivos", use_container_width=True)
        
        # Botão de Download
        buf = io.BytesIO()
        img_final.save(buf, format="JPEG")
        st.download_button("📥 Baixar Foto Editada", data=buf.getvalue(), file_name="foto_editada.jpg", mime="image/jpeg")

    except Exception as e:
        st.error(f"Ops, deu erro ao processar a imagem: {e}")
else:
    st.info("Aguardando você subir uma foto...")
        
