import streamlit as st
from utils import load_network
from pso_algorithm import pso_net
from visualization import (
    initialize_visualization,
    update_visualization,
    show_final_communities,
    create_visualization_placeholders
)
import pandas as pd
import time

def main():
    st.set_page_config(page_title="PSO-Net Community Detection", layout="wide")
    st.title("📊 Deteksi Komunitas dengan Particle Swarm Optimization Network (PSO-Net)")
    st.markdown(
        "Aplikasi ini menggunakan algoritma **PSO-Net** untuk menemukan komunitas dalam suatu jaringan. "
        "Silakan unggah file jaringan (dalam format `.tsv`) dan atur parameter yang dibutuhkan."
    )

    with st.sidebar:
        st.header("⚙️ Pengaturan")
        uploaded_file = st.file_uploader("Upload file TSV", type=["tsv"])
        num_particles = st.slider("Jumlah Partikel", 0, 500, 300)
        maxgen = st.slider("Maksimum Generasi", 0, 200, 100)
        run_button = st.button("🚀 Jalankan Algoritma PSO")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep="\t")
        st.sidebar.write("📄 **Pratinjau Data**", df.head())
        file_path = "temp_uploaded_file.tsv"
        df.to_csv(file_path, sep="\t", index=False)
        network, nodes = load_network(file_path, verbose=False)
        initialize_visualization(network)

        st.subheader("🔍 Proses Deteksi Komunitas")
        st.session_state.community_plot, st.session_state.modularity_plot, st.session_state.density_plot = create_visualization_placeholders()

        if run_button:
            
            with st.spinner("⏳ Menjalankan algoritma PSO..."):
                start_time = time.time()

                best_labels, best_modularity, q_scores = pso_net(
                    network,
                    num_particles=num_particles,
                    max_gen=maxgen,
                    update_callback=update_visualization
                )

                exec_time = time.time() - start_time
            show_final_communities(best_labels, network)
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"✅ Modularitas terbaik (Q): `{best_modularity:.4f}`")
            with col2:
                st.info(f"🕒 Waktu Eksekusi: `{exec_time:.2f} detik`")

if __name__ == "__main__":
    main()
