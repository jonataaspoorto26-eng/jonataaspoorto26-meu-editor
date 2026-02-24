import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import io

# 1. Configuração da página (Wide mode para usar melhor a tela)
st.set_page_config(page_title="Editor Pro Desktop", layout="wide")
st.title("Meu Editor de Fotos Pro 📸")

arquivo = st.file_uploader("Escolha uma imagem para começar...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    try:
        img_original = Image.open(arquivo).convert('RGB')
        
        # 2. CRIANDO AS COLUNAS (Lado Esquerdo: Foto | Lado Direito: Ferramentas)
        # O [3, 1] significa que a coluna da foto é 3x maior que a de ferramentas
        col_principal, col_ferramentas = st.columns([3, 1])

        # --- LADO DIREITO (FERRAMENTAS) ---
        with col_ferramentas:
            st.subheader("🛠️ Ajustes")
            
            # Usando o Expander para manter organizado mesmo na lateral
            with st.expander("✨ Composição de Luz", expanded=True):
                exposicao = st.slider("Exposição", 0.0, 2.0, 1.0)
                contraste = st.slider("Contraste", 0.0, 2.0, 1.0)
                realces = st.slider("Realces", 0.0, 2.0, 1.0)
                sombras = st.slider("Sombras", 0.0, 2.0, 1.0)
                brancos = st.slider("Brancos", -100.0, 100.0, 0.0)
                pretos = st.slider("Pretos", -100.0, 100.0, 0.0)

            # Botão de Download logo abaixo das ferramentas
            buf = io.BytesIO()
            # O processamento precisa acontecer antes de salvar, então vamos definir o img_final primeiro
            
        # --- PROCESSAMENTO (Atrás das cortinas) ---
        img_temp = ImageEnhance.Brightness(img_original).enhance(exposicao)
        img_temp = ImageEnhance.Contrast(img_temp).enhance(contraste)
        img_array = np.array(img_temp).astype(float)

        mask_brancos = np.clip((img_array - 190) / 65, 0, 1) if brancos != 0 else 0
        img_array += brancos * mask_brancos
        mask_pretos = np.clip((65 - img_array) / 65, 0, 1) if pretos != 0 else 0
        img_array += pretos * mask_pretos

        if realces != 1.0:
            img_array[img_array > 128] *= realces
        if sombras != 1.0:
            img_array[img_array <= 128] *= sombras

        img_final = Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

        # --- LADO ESQUERDO (EXIBIÇÃO) ---
        with col_principal:
            st.image(img_final, use_container_width=True)

        # Atualizando o botão de download com a imagem final processada
        with col_ferramentas:
            img_final.save(buf, format="JPEG", quality=95)
            st.download_button(
                label="📥 Baixar Foto",
                data=buf.getvalue(),
                file_name="foto_editada.jpg",
                mime="image/jpeg",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.info("Aguardando imagem...")
        
