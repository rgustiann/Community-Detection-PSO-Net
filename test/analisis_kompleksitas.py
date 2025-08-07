from collections import defaultdict
from itertools import product
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import sys
import os
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pso_algorithm import calculate_modularity, crossover, decode_particle, initialize_population, mutate, pso_net
# ===== FUNGSI TAMBAHAN UNTUK ANALISIS KOMPLEKSITAS =====

def create_test_network(n_nodes, connection_prob=0.1):
    network = defaultdict(set)
    
    # Create random connections
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if random.random() < connection_prob:
                network[i].add(j)
                network[j].add(i)
    
    # Ensure all nodes have at least one connection
    for i in range(n_nodes):
        if not network[i]:
            # Connect to a random node
            j = random.choice([x for x in range(n_nodes) if x != i])
            network[i].add(j)
            network[j].add(i)
    
    return network

def get_network_stats(network):
    """Get number of nodes and edges in the network"""
    n_nodes = len(network)
    n_edges = sum(len(neighbors) for neighbors in network.values()) // 2
    return n_nodes, n_edges

def pso_net_timed(network, num_particles=30, max_gen=100):
    start_time = time.time()

    population = initialize_population(network, num_particles) 
    clusterings = [decode_particle(p) for p in population]
    fitness = [calculate_modularity(network, c) for c in clusterings]

    personalbest = population.copy()
    personalbest_fitness = fitness.copy()

    gbest_idx = np.argmax(fitness)
    globalbest = personalbest[gbest_idx].copy()
    globalbest_fitness = personalbest_fitness[gbest_idx]

    q_scores = []

    for gen in range(max_gen):
        for i in range(num_particles):
            child1, child2 = crossover(population[i], personalbest[i])
            mod1 = calculate_modularity(network, decode_particle(child1))
            mod2 = calculate_modularity(network, decode_particle(child2))
            temp_particle = child1 if mod1 > mod2 else child2

            child1, child2 = crossover(temp_particle, globalbest)
            mod1 = calculate_modularity(network, decode_particle(child1))
            mod2 = calculate_modularity(network, decode_particle(child2))
            temp_particle = child1 if mod1 > mod2 else child2

            temp_particle = mutate(temp_particle, network)

            decoded = decode_particle(temp_particle)
            modularity = calculate_modularity(network, decoded)
            population[i] = temp_particle
            fitness[i] = modularity

            if modularity > personalbest_fitness[i]:
                personalbest[i] = temp_particle
                personalbest_fitness[i] = modularity

        best_idx = np.argmax(personalbest_fitness)
        if personalbest_fitness[best_idx] > globalbest_fitness:
            globalbest = personalbest[best_idx]
            globalbest_fitness = personalbest_fitness[best_idx]

        current_modularity = calculate_modularity(network, decode_particle(globalbest))
        q_scores.append(current_modularity)

    end_time = time.time()
    execution_time = end_time - start_time
    
    best_communities = decode_particle(globalbest)
    return best_communities, globalbest_fitness, q_scores, execution_time

def run_complexity_analysis():
    node_sizes = [100, 150, 200, 250, 300, 350, 400, 450, 500]
    execution_times = []
    network_stats = []
    
    # Fixed parameters (G and P constant)
    num_particles = 15  # P
    max_gen = 25       # G
    connection_prob = 0.15
    
    print("=" * 70)
    print("ANALISIS KOMPLEKSITAS WAKTU PSO COMMUNITY DETECTION")
    print("=" * 70)
    print(f"Parameter tetap: P (particles) = {num_particles}, G (generations) = {max_gen}")
    print(f"Kompleksitas teoritis: O(G × P × (n + m))")
    print(f"Dengan G dan P konstan, kompleksitas = O(n + m)")
    print(f"Connection probability = {connection_prob}")
    print("-" * 70)
    
    for n in node_sizes:
        print(f"Testing network dengan {n} nodes...")
        
        # Create test network
        network = create_test_network(n, connection_prob=connection_prob)
        n_nodes, n_edges = get_network_stats(network)
        network_stats.append((n_nodes, n_edges))
        
        print(f"  Network: {n_nodes} nodes, {n_edges} edges")
        
        # Run algorithm multiple times and take average
        times = []
        for run in range(3):  # Run 3 times for averaging
            print(f"  Run {run + 1}/3...", end=" ")
            _, _, _, exec_time = pso_net_timed(
                network, 
                num_particles=num_particles, 
                max_gen=max_gen
            )
            times.append(exec_time)
            print(f"{exec_time:.4f}s")
        
        avg_time = np.mean(times)
        std_time = np.std(times)
        execution_times.append(avg_time)
        print(f"  Average: {avg_time:.4f}s (±{std_time:.4f}s)")
        print()
    
    return node_sizes, execution_times, network_stats, max_gen, num_particles

def plot_complexity_comparison(node_sizes, execution_times, network_stats, G=25, P=15):
    # Extract nodes and edges
    nodes = [stats[0] for stats in network_stats]
    edges = [stats[1] for stats in network_stats]
    n_plus_m = [n + m for n, m in network_stats]
    
    # Fit theoretical O(I×P×(n+m)) curve to actual data
    def gp_n_plus_m_func(n_plus_m_val, k):
        return k * G * P * n_plus_m_val
    
    # Also fit simple O(n+m) for comparison
    def n_plus_m_func(n_plus_m_val, k):
        return k * n_plus_m_val
    
    # Fit O(n²) for comparison (old complexity assumption)
    def n_squared_func(n, k):
        return k * (n**2)
    
    # Fit all curves to actual data
    popt_gp_nm, _ = curve_fit(gp_n_plus_m_func, n_plus_m, execution_times)
    popt_nm, _ = curve_fit(n_plus_m_func, n_plus_m, execution_times)
    popt_n2, _ = curve_fit(n_squared_func, nodes, execution_times)
    
    k_gp_nm = popt_gp_nm[0]
    k_nm = popt_nm[0]
    k_n2 = popt_n2[0]
    
    theoretical_times_gp_nm = [gp_n_plus_m_func(nm, k_gp_nm) for nm in n_plus_m]
    theoretical_times_nm = [n_plus_m_func(nm, k_nm) for nm in n_plus_m]
    theoretical_times_n2 = [n_squared_func(n, k_n2) for n in nodes]
    
    # Create the plot
    plt.figure(figsize=(15, 10))
    
    # Plot actual times
    plt.plot(nodes, execution_times, 'bo-', label='Waktu Eksekusi Aktual', 
             linewidth=3, markersize=10, markerfacecolor='lightblue', markeredgecolor='blue')
    
    # Plot theoretical O(I×P×(n+m))
    plt.plot(nodes, theoretical_times_gp_nm, 'r--', label=f'Teoritis O(I×P×(N+E))', 
             linewidth=3, alpha=0.8)

    
    plt.xlabel('Jumlah Node (n)', fontsize=14)
    plt.ylabel('Waktu Eksekusi (detik)', fontsize=14)
    plt.title('Analisis Kompleksitas Waktu PSO Community Detection\nO(G × P × (n + m))', fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Calculate R² for all fits
    ss_res_gp_nm = np.sum((np.array(execution_times) - np.array(theoretical_times_gp_nm)) ** 2)
    ss_res_nm = np.sum((np.array(execution_times) - np.array(theoretical_times_nm)) ** 2)
    ss_res_n2 = np.sum((np.array(execution_times) - np.array(theoretical_times_n2)) ** 2)
    ss_tot = np.sum((np.array(execution_times) - np.mean(execution_times)) ** 2)
    
    r_squared_gp_nm = 1 - (ss_res_gp_nm / ss_tot)
    r_squared_nm = 1 - (ss_res_nm / ss_tot)
    r_squared_n2 = 1 - (ss_res_n2 / ss_tot)
    
    print("=" * 80)
    print("HASIL ANALISIS KOMPLEKSITAS:")
    print("=" * 80)
    print(f"R² (goodness of fit terhadap O(I×P×(n+m))): {r_squared_gp_nm:.6f}")
    print(f"R² (goodness of fit terhadap O(n+m)):        {r_squared_nm:.6f}")
    print(f"R² (goodness of fit terhadap O(n²)):         {r_squared_n2:.6f}")
    print()
    print(f"Koefisien O(I×P×(n+m)): {k_gp_nm:.8f}")
    print(f"Koefisien O(n+m):       {k_nm:.6f}")
    print(f"Koefisien O(n²):        {k_n2:.6f}")
    print()
    print(f"Persamaan O(I×P×(n+m)): waktu ≈ {k_gp_nm:.8f} × {G} × {P} × (n+m)")
    print(f"Persamaan O(n+m):       waktu ≈ {k_nm:.6f} × (n+m)")
    print(f"Persamaan O(n²):        waktu ≈ {k_n2:.6f} × n²")
    print()
    
    # Find the best model
    models = {
        'O(I×P×(n+m))': r_squared_gp_nm,
        'O(n+m)': r_squared_nm,
        'O(n²)': r_squared_n2
    }
    
    best_model = max(models, key=models.get)
    best_r2 = models[best_model]
    
    print(f"MODEL TERBAIK: {best_model} dengan R² = {best_r2:.6f}")
    
    if best_model == 'O(I×P×(n+m))':
        print("✓ Konfirmasi: Kompleksitas sebenarnya adalah O(I×P×(n+m))")
        if best_r2 > 0.95:
            print("  🎯 Fit sangat baik! Teori kompleksitas terbukti akurat")
        elif best_r2 > 0.85:
            print("  ✓ Fit baik. Algoritma mendekati scaling O(I×P×(n+m))")
        else:
            print("  ⚠ Fit cukup. Ada faktor lain yang mempengaruhi")
    elif best_model == 'O(n+m)':
        print("✓ Dengan G dan P konstan, kompleksitas efektif menjadi O(n+m)")
        print("  Ini konsisten dengan analisis teoritis")
    else:
        print("⚠ Kompleksitas lebih mendekati O(n²)")
        print("  Mungkin karena dense network atau overhead implementasi")
    
    print("=" * 80)
    
    # Print detailed timing table
    print("\nTABEL DETAIL WAKTU EKSEKUSI:")
    print("-" * 90)
    print(f"{'Nodes':<8} {'Edges':<8} {'n+m':<8} {'Aktual (s)':<12} {'O(I×P×(n+m))':<15} {'O(n+m)':<12} {'O(n²)':<12}")
    print("-" * 90)
    for i, (n, m) in enumerate(network_stats):
        nm = n + m
        print(f"{n:<8} {m:<8} {nm:<8} {execution_times[i]:<12.4f} {theoretical_times_gp_nm[i]:<15.4f} {theoretical_times_nm[i]:<12.4f} {theoretical_times_n2[i]:<12.4f}")
    print("-" * 90)

# Run the analysis
if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Run complexity analysis
    node_sizes, execution_times, network_stats, max_gen, num_particles = run_complexity_analysis()
    
    # Plot the results
    plot_complexity_comparison(node_sizes, execution_times, network_stats, max_gen, num_particles)