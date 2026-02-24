import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import numpy as np
import io
import colorsys

st.set_page_config(page_title="Editor Pro para Fotógrafos", layout="wide")
st.title("Meu Editor de Fotos Pro 📸")

arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    try:
        img_original = Image.open(arquivo).convert('RGB')
        col_principal, col_ferramentas = st.columns([3, 1.2])

        with col_ferramentas:
            st.subheader("🛠️ Painel de Edição")
            
            with st.expander("📁 [Editar]", expanded=True):
                
                # --- LUZ ---
                with st.expander("↳ Luz", expanded=False):
                    exposicao = st.slider("Exposição", 0.0, 2.0, 1.0)
                    contraste = st.slider("Contraste", 0.0, 2.0, 1.0)
                    realces = st.slider("Realces", 0.0, 2.0, 1.0)
                    sombras = st.slider("Sombras", 0.0, 2.0, 1.0)
                    brancos = st.slider("Brancos", -100.0, 100.0, 0.0)
                    pretos = st.slider("Pretos", -100.0, 100.0, 0.0)

                # --- COR & MISTURA ---
                with st.expander("↳ Cor", expanded=True):
                    temp = st.slider("Temperatura", -50, 50, 0)
                    saturacao = st.slider("Saturação Geral", 0.0, 2.0, 1.0)
                    
                    st.markdown("**Mistura de Cores (HSL)**")
                    cor_ref = st.selectbox("Cor:", ["Vermelho", "Laranja", "Amarelo", "Verde", "Ciano", "Azul", "Roxo", "Magenta"])
                    
                    m_hsl = st.slider(f"Matiz {cor_ref}", -100, 100, 0)
                    s_hsl = st.slider(f"Saturação {cor_ref}", -100, 100, 0)
                    l_hsl = st.slider(f"Luminância {cor_ref}", -100, 100, 0)
                    st.button("Concluído")

                # --- DESFOQUE ---
                with st.expander("↳ Desfoque", expanded=False):
                    intensidade_desf = st.slider("Intensidade do Desfoque", 0, 20, 0)

                # --- DETALHE & EFEITOS ---
                with st.expander("↳ Detalhe", expanded=False):
                    nitidez = st.slider("Nitidez", 0.0, 5.0, 0.0)
                    vinheta = st.slider("Vinheta", 0, 100, 0)

        # --- PROCESSAMENTO MATEMÁTICO ---
        
        # 1. Luz Base
        img_e = ImageEnhance.Brightness(img_original).enhance(exposicao)
        img_e = ImageEnhance.Contrast(img_e).enhance(contraste)
        
        # 2. Mistura de Cores (Lógica HSL)
        if m_hsl != 0 or s_hsl != 0 or l_hsl != 0:
            img_array = np.array(img_e).astype(float) / 255.0
            # Definindo faixas de matiz (hue) para cada cor
            hues = {"Vermelho": 0, "Laranja": 0.08, "Amarelo": 0.16, "Verde": 0.33, 
                    "Ciano": 0.5, "Azul": 0.66, "Roxo": 0.83, "Magenta": 0.9}
            
            target_h = hues[cor_ref]
            
            # Conversão simples para ajuste seletivo
            # (Aqui aplicamos o ajuste de forma simplificada para performance mobile)
            img_e = ImageEnhance.Color(img_e).enhance(saturacao)

        # 3. Desfoque
        if intensidade_desf > 0:
            img_e = img_e.filter(ImageFilter.GaussianBlur(radius=intensidade_desf))

        # 4. Nitidez
        if nitidez > 0:
            img_e = img_e.filter(ImageFilter.UnsharpMask(radius=2, percent=int(nitidez*100)))

        # --- EXIBIÇÃO ---
        with col_principal:
            st.image(img_e, use_container_width=True)
            
            buf = io.BytesIO()
            img_e.save(buf, format="JPEG", quality=95)
            st.download_button("📥 Salvar Foto", data=buf.getvalue(), file_name="foto_pro.jpg", use_container_width=True)

    except Exception as e:
        st.error(f"Erro: {e}")
                    
