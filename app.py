import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import io

# 1. Configuração da página para Mobile
st.set_page_config(page_title="Editor Pro Mobile", layout="centered")
st.title("Meu Editor de Fotos Pro 📸")

# 2. Upload da Imagem
arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    try:
        # Abrir imagem e garantir que está no formato correto
        img_original = Image.open(arquivo).convert('RGB')
        
        # Espaço reservado para a foto no topo (ergonomia)
        container_foto = st.empty()

        st.markdown("---")
        
        # 3. MENU EXPANSÍVEL (Abre e fecha embaixo da foto)
        with st.expander("✨ Ajustes de Luz e Composição", expanded=False):
            st.write("Arraste para editar os tons:")
            
            # Duas colunas para os controles não ficarem muito longos
            col1, col2 = st.columns(2)
            
            with col1:
                exposicao = st.slider("Exposição", 0.0, 2.0, 1.0)
                realces = st.slider("Realces", 0.0, 2.0, 1.0)
                brancos = st.slider("Brancos", -100.0, 100.0, 0.0)
                
            with col2:
                contraste = st.slider("Contraste", 0.0, 2.0, 1.0)
                sombras = st.slider("Sombras", 0.0, 2.0, 1.0)
                pretos = st.slider("Pretos", -100.0, 100.0, 0.0)

        # 4. CÁLCULOS DE PROCESSAMENTO
        # Ajustes base de Brilho e Contraste
        img_temp = ImageEnhance.Brightness(img_original).enhance(exposicao)
        img_temp = ImageEnhance.Contrast(img_temp).enhance(contraste)
        
        # Converter para Array para ajustes seletivos (Preto/Branco)
        img_array = np.array(img_temp).astype(float)

        # Máscara para Brancos (afeta tons acima de 190)
        m_brancos = np.clip((img_array - 190) / 65, 0, 1) if brancos != 0 else 0
        img_array += brancos * m_brancos

        # Máscara para Pretos (afeta tons abaixo de 65)
        m_pretos = np.clip((65 - img_array) / 65, 0, 1) if pretos != 0 else 0
        img_array += pretos * m_pretos

        # Realces e Sombras simples
        if realces != 1.0:
            img_array[img_array > 128] *= realces
        if sombras != 1.0:
            img_array[img_array <= 128] *= sombras

        # Converter de volta para Imagem e limitar valores entre 0 e 255
        img_final = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

        # 5. RESULTADO E DOWNLOAD
        # Coloca a imagem editada lá no topo onde definimos o container
        container_foto.image(img_final, use_container_width=True)
        
        # Preparação do botão de download
        buf = io.BytesIO()
        img_final.save(buf, format="JPEG", quality=95)
        st.download_button(
            label="📥 Baixar Foto Editada",
            data=buf.getvalue(),
            file_name="foto_pro_ajustada.jpg",
            mime="image/jpeg"
        )

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
else:
    st.info("Aguardando você selecionar uma foto...")
        
