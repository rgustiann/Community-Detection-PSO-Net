import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import io
import itertools
import os

# 🔹 Buat folder hasil jika belum ada
RESULT_DIR = "hasil"
os.makedirs(RESULT_DIR, exist_ok=True)

def initialize_visualization(network):
    st.subheader("Visualisasi Awal Jaringan")
    col1, col2, col3 = st.columns([1, 3, 1])

    G = nx.Graph()
    for node, neighbors in network.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', 
            ax=ax, font_size=3, node_size=200)

    with col2:
        st.pyplot(fig)
        plt.close(fig)

        st.markdown(f"""
        **ℹ️ Informasi Jaringan Awal**
        - Jumlah Node: **{G.number_of_nodes()}**
        - Jumlah Edge: **{G.number_of_edges()}**
        """)

def create_visualization_placeholders():
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        community_plot = st.empty()
    with col3:
        modularity_plot = st.empty()
        density_plot = st.empty()
    return community_plot, modularity_plot, density_plot

def update_visualization(labels, modularity_scores, q_scores, network, gen):
    if 'community_plot' not in st.session_state:
        st.session_state.community_plot, st.session_state.modularity_plot, st.session_state.density_plot = create_visualization_placeholders()

    with st.session_state.community_plot:
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        G = nx.Graph(network)

        unique_communities = list(set(labels.values()))
        colors = plt.cm.get_cmap("tab10", len(unique_communities))
        community_colors = {community: colors(i) for i, community in enumerate(unique_communities)}
        node_colors = [community_colors[labels[node]] for node in G.nodes()]
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, ax=ax1, node_color=node_colors, with_labels=False, node_size=80, edge_color="gray")

        handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8)
            for color in community_colors.values()
        ]
        legend_labels = [f"Komunitas {i+1}" for i in range(len(unique_communities))]
        ax1.legend(handles, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=6, frameon=False)

        fig1.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    with st.session_state.modularity_plot:
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.plot(range(len(q_scores)), q_scores, linestyle="-", color="b")
        ax2.set_xlabel("Generasi")
        ax2.set_ylabel("Modularitas Q")
        if q_scores:
            last_idx = len(q_scores) - 1
            ax2.text(last_idx, q_scores[-1], f"{q_scores[-1]:.4f}", fontsize=10, color="black",
                     ha="right", va="bottom", fontweight="bold")
        st.pyplot(fig2)
        
        # ✅ Simpan grafik modularitas ke file
        fig2.savefig(os.path.join(RESULT_DIR, f"modularitas_iterasi_{gen}.png"), bbox_inches='tight')
        plt.close(fig2)

    with st.session_state.density_plot:
        last_modularity = q_scores[-1] if q_scores else 0
        st.markdown(f"""
        **📢 Keterangan**
        - **Iterasi**: {gen} , **Modularitas (Q)**: {last_modularity:.4f}
        """)

def show_final_communities(final_labels, network):
    st.subheader("🎯 Hasil Akhir Deteksi Komunitas")

    col1, col2, col3 = st.columns([1, 3, 1])
    G = nx.Graph(network)

    unique_communities = list(set(final_labels.values()))
    colors = plt.cm.Set1(np.linspace(0, 1, len(unique_communities)))
    community_colors = {community: colors[i] for i, community in enumerate(unique_communities)}
    node_colors = [community_colors[final_labels[node]] for node in G.nodes()]
    
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
    pos_initial = nx.spring_layout(G, seed=42)
    pos = nx.kamada_kawai_layout(G, pos=pos_initial)

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray',
            node_size=200, font_size=5, ax=ax)

    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10)
               for color in community_colors.values()]
    labels = [f"Komunitas {i+1}" for i in range(len(unique_communities))]
    ax.legend(handles, labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=6, frameon=False)
    fig.tight_layout()

    with col2:
        st.pyplot(fig)
        
        # ✅ Simpan hasil akhir ke file
        fig.savefig(os.path.join(RESULT_DIR, "komunitas_akhir.png"), bbox_inches='tight')
        plt.close(fig)

    st.subheader("🔍 Visualisasi Setiap Komunitas")
    communities = {}
    for node, community in final_labels.items():
        communities.setdefault(community, []).append(node)

    cols = st.columns(3)
    col_cycle = itertools.cycle(cols)

    for i, (community, nodes) in enumerate(communities.items(), start=1):
        subgraph = G.subgraph(nodes)
        if subgraph.number_of_nodes() == 0:
            continue
        pos_sub = nx.spring_layout(subgraph, seed=42, k=0.8) if subgraph.number_of_edges() > 0 else nx.circular_layout(subgraph)

        fig_c, ax_c = plt.subplots(figsize=(4.5, 3.5), dpi=150)
        nx.draw(subgraph, pos_sub, with_labels=True,
                node_color=[community_colors[community]] * len(subgraph.nodes()),
                edge_color="gray", ax=ax_c, node_size=300, font_size=6)
        ax_c.set_title(f"Komunitas {i} - {len(nodes)} Node", fontsize=10)

        with next(col_cycle):
            st.pyplot(fig_c)
        
        # ✅ Simpan per komunitas ke file
        fig_c.savefig(os.path.join(RESULT_DIR, f"komunitas_{i}.png"), bbox_inches='tight')
        plt.close(fig_c)

    st.subheader("📋 Preview Komunitas dalam Bentuk Tabel")

    max_length = max(len(nodes) for nodes in communities.values())
    table_data = {f"Komunitas {i+1}": nodes + [""] * (max_length - len(nodes)) 
                  for i, nodes in enumerate(communities.values())}
    df_table = pd.DataFrame(table_data)

    df_community_rows = pd.DataFrame(
        [[", ".join(map(str, nodes))] for nodes in communities.values()],
        columns=["Komunitas"]
    )

    st.dataframe(df_table)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_table.to_excel(writer, sheet_name="Tabel Komunitas", index=False)
        df_community_rows.to_excel(writer, sheet_name="Komunitas per Baris", index=False)
    output.seek(0)


    st.download_button(
        label="📥 Download Hasil (Excel)",
        data=output,
        file_name="hasil_komunitas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
