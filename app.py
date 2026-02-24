import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import numpy as np
import io

# Configuração da página
st.set_page_config(page_title="Editor Ultra Pro", layout="wide")
st.title("Meu Editor de Fotos Pro 📸")

arquivo = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if arquivo is not None:
    try:
        img_original = Image.open(arquivo).convert('RGB')
        col_principal, col_ferramentas = st.columns([3, 1.2])

        # --- LADO DIREITO: FERRAMENTAS ORGANIZADAS ---
        with col_ferramentas:
            st.subheader("🛠️ Painel de Edição")
            
            with st.expander("📁 [Editar]", expanded=True):
                
                # --- SUBPASTA: LUZ ---
                with st.expander("↳ Luz", expanded=False):
                    exposicao = st.slider("Exposição", 0.0, 2.0, 1.0)
                    contraste = st.slider("Contraste", 0.0, 2.0, 1.0)
                    realces = st.slider("Realces", 0.0, 2.0, 1.0)
                    sombras = st.slider("Sombras", 0.0, 2.0, 1.0)
                    brancos = st.slider("Brancos", -100.0, 100.0, 0.0)
                    pretos = st.slider("Pretos", -100.0, 100.0, 0.0)

                # --- SUBPASTA: COR ---
                with st.expander("↳ Cor", expanded=False):
                    temp = st.slider("Temperatura", -50, 50, 0)
                    matiz_geral = st.slider("Matiz", -50, 50, 0)
                    vibracao = st.slider("Vibração", 0.0, 2.0, 1.0)
                    saturacao = st.slider("Saturação", 0.0, 2.0, 1.0)
                    
                    # Mistura de Cores Individual
                    with st.expander("🎨 Mistura de Cores"):
                        cor_ref = st.selectbox("Cor para editar:", ["Vermelho", "Laranja", "Amarelo", "Ciano", "Azul", "Roxo", "Magenta"])
                        st.slider(f"Matiz {cor_ref}", -100, 100, 0, key=f"m_{cor_ref}")
                        st.slider(f"Saturação {cor_ref}", -100, 100, 0, key=f"s_{cor_ref}")
                        st.slider(f"Luminância {cor_ref}", -100, 100, 0, key=f"l_{cor_ref}")
                        st.button("Concluído", use_container_width=True)

                # --- SUBPASTA: DESFOQUE ---
                with st.expander("↳ Desfoque", expanded=False):
                    desf_fundo = st.slider("Desfocar Fundo", 0, 20, 0)
                    desf_frente = st.slider("Desfocar Frente", 0, 20, 0)

                # --- SUBPASTA: EFEITOS ---
                with st.expander("↳ Efeitos", expanded=False):
                    textura = st.slider("Textura", 0.0, 2.0, 1.0)
                    claridade = st.slider("Claridade", 0.0, 2.0, 1.0)
                    desembacar = st.slider("Desembaçar", 0.0, 2.0, 1.0)
                    vinheta = st.slider("Vinheta", 0, 100, 0)
                    granulado = st.slider("Granulado", 0, 100, 0)

                # --- SUBPASTA: DETALHE ---
                with st.expander("↳ Detalhe", expanded=False):
                    nitidez = st.slider("Nitidez (Intensidade)", 0.0, 5.0, 1.0)
                    raio_n = st.slider("Raio", 0.1, 5.0, 1.0)
                    ruido = st.slider("Redução de Ruído", 0, 10, 0)
                
                # --- SUBPASTA: ÓTICA ---
                with st.expander("↳ Ótica", expanded=False):
                    rem_desvio = st.checkbox("Remover Desvio Cromático")

        # --- PROCESSAMENTO (RESUMO DA LÓGICA) ---
        # Luz
        img_e = ImageEnhance.Brightness(img_original).enhance(exposicao)
        img_e = ImageEnhance.Contrast(img_e).enhance(contraste)
        
        # Detalhe (Nitidez)
        if nitidez != 1.0:
            img_e = img_e.filter(ImageFilter.UnsharpMask(radius=raio_n, percent=int(nitidez*100)))

        # Saturação e Vibração
        img_e = ImageEnhance.Color(img_e).enhance(saturacao * vibracao)

        # Efeito Vinheta Simples
        if vinheta > 0:
            img_e = ImageOps.colorize(ImageOps.grayscale(img_e), "black", "white", mid="gray") # Simulação

        # --- EXIBIÇÃO ---
        with col_principal:
            st.image(img_e, use_container_width=True, caption="Edição em Tempo Real")
            
            # Botão de Download
            buf = io.BytesIO()
            img_e.save(buf, format="JPEG")
            st.download_button("📥 Salvar Resultado", data=buf.getvalue(), file_name="foto_pro.jpg", use_container_width=True)

    except Exception as e:
        st.error(f"Erro no processamento: {e}")
        
