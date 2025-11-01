import streamlit as st
from PIL import Image
import pandas as pd
import random

# -------------------------------------------
# Simulación de análisis de Hugging Face
# -------------------------------------------

def analizar_imagen_fake(image_path):
    """Simula resultados de un modelo de Hugging Face."""
    edades = ["0-10", "11-20", "21-30", "31-40", "41-50", "51+"]
    generos = ["masculino", "femenino", "indefinido"]
    objetos = ["person", "cat", "dog", "car", "tree"]

    resultado = {
        "hay_persona": random.choice([True, False]),
        "edad_estimada": random.choice(edades),
        "genero_estimado": random.choice(generos),
        "detecciones": [
            {"label": random.choice(objetos), "score": round(random.uniform(0.6, 0.99), 2)}
            for _ in range(random.randint(1, 4))
        ],
    }
    return resultado


# -------------------------------------------
# Configuración de la página
# -------------------------------------------

st.set_page_config(page_title="Visor de Imágenes AI", layout="wide")

st.title("🪐 Análisis de Imágenes con Hugging Face (Simulado)")
st.markdown("Sube una imagen y observa cómo se vería el análisis con el modelo.")

# -------------------------------------------
# Carga de imagen
# -------------------------------------------

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("📸 Sube una imagen", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen subida", use_column_width=True)

        # Simular análisis
        resultado = analizar_imagen_fake(uploaded_file.name)

        st.subheader("🔍 Resultados del análisis")
        st.write(f"**Hay persona:** {'✅ Sí' if resultado['hay_persona'] else '❌ No'}")
        st.write(f"**Edad estimada:** {resultado['edad_estimada']}")
        st.write(f"**Género estimado:** {resultado['genero_estimado']}")

        st.markdown("**Objetos detectados:**")
        st.json(resultado["detecciones"])

        # Guardar en sesión para mostrar en dashboard
        if "analisis" not in st.session_state:
            st.session_state["analisis"] = []
        st.session_state["analisis"].append({
            "nombre": uploaded_file.name,
            "edad": resultado["edad_estimada"],
            "género": resultado["genero_estimado"],
            "persona": "Sí" if resultado["hay_persona"] else "No"
        })

with col2:
    st.subheader("🧾 Dashboard de imágenes analizadas")

    if "analisis" in st.session_state and len(st.session_state["analisis"]) > 0:
        df = pd.DataFrame(st.session_state["analisis"])
        st.dataframe(df, use_container_width=True)

        # Gráficos simples
        st.markdown("### 📊 Distribución de género")
        genero_counts = df["género"].value_counts()
        st.bar_chart(genero_counts)

        st.markdown("### 👶 Distribución de edad")
        edad_counts = df["edad"].value_counts()
        st.bar_chart(edad_counts)
    else:
        st.info("Sube una imagen para comenzar a llenar el dashboard.")
