import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import io

st.set_page_config(page_title="Editor Pro Mobile", layout="centered")
st.title("Meu Editor de Fotos Pro 📸")

arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    try:
        img_original = Image.open(arquivo).convert('RGB')
        
        # --- ÁREA DA FOTO (NO TOPO) ---
        # Criamos um espaço vazio para preencher depois com a imagem editada
        container_foto = st.empty()

        st.markdown("---")
        st.subheader("Configurações de Luz 🔧")
        
        # --- CONTROLES (NA PARTE DE BAIXO) ---
        # Usamos colunas para os sliders não ficarem gigantes
        col1, col2 = st.columns(2)
        
        with col1:
            exposicao = st.slider("Exposição", 0.0, 2.0, 1.0)
            realces = st.slider("Realces", 0.0, 2.0, 1.0)
            brancos = st.slider("Brancos", -100.0, 100.0, 0.0)
            
        with col2:
            contraste = st.slider("Contraste", 0.0, 2.0, 1.0)
            sombras = st.slider("Sombras", 0.0, 2.0, 1.0)
            pretos = st.slider("Pretos", -100.0, 100.0, 0.0)

        # --- PROCESSAMENTO ---
        img_edit = ImageEnhance.Brightness(img_original).enhance(exposicao)
        img_edit = ImageEnhance.Contrast(img_edit).enhance(contraste)
        
        img_array = np.array(img_edit).astype(float)

        # Lógica de Brancos e Pretos Seletivos
        mask_brancos = np.clip((img_array - 200) / 55, 0, 1) if brancos != 0 else 0
        img_array += brancos * mask_brancos

        mask_pretos = np.clip((60 - img_array) / 60, 0, 1) if pretos != 0 else 0
        img_array += pretos * mask_pretos

        if realces != 1.0:
            img_array[img_array > 128] *= realces
        if sombras != 1.0:
            img_array[img_array <= 128] *= sombras

        img_final = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

        # --- MOSTRAR A FOTO NO CONTAINER LÁ NO TOPO ---
        container_foto.image(img_final, use_container_width=True)
        
        # Botão de Download no final de tudo
        buf = io.BytesIO()
        img_final.save(buf, format="JPEG")
        st.download_button("📥 Baixar Foto Pronta", data=buf.getvalue(), file_name="foto_editada.jpg", mime="image/jpeg")

    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.info("Suba uma foto para começar a editar!")
