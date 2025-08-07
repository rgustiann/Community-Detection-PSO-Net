import random
from collections import defaultdict, deque
import numpy as np
import time

def initialize_population(network, num_particles):
    population = []
    nodes = list(network.keys())
    for _ in range(num_particles):
        particle = {}
        for node in nodes:
            neighbors = list(network[node])
            if neighbors:
                particle[node] = random.choice(neighbors)
        population.append(particle)
    return population

def decode_particle(particle):
    communities = defaultdict(set)
    visited = set()
    for node in particle:
        if node in visited:
            continue
        queue = deque([node])
        visited.add(node)
        cid = len(communities) + 1
        while queue:
            current = queue.popleft()
            communities[cid].add(current)
            neighbor = particle[current]
            if neighbor not in visited and neighbor in particle:
                queue.append(neighbor)
                visited.add(neighbor)

    comm_map = {}
    large_communities = {}
    temp_map = {}

    for cid, nodes in communities.items():
        if len(nodes) >= 5:
            for n in nodes:
                comm_map[n] = cid
            large_communities[cid] = nodes
        else:
            for n in nodes:
                temp_map[n] = cid

    for node, small_cid in temp_map.items():
        neighbor = particle.get(node)
        if neighbor in comm_map:
            comm_map[node] = comm_map[neighbor]
        else:
            comm_map[node] = small_cid

    return comm_map

def calculate_modularity(network, labels):
    m = sum(len(neigh) for neigh in network.values()) / 2
    if m == 0:
        return 0

    communities = defaultdict(list)
    for node, comm in labels.items():
        communities[comm].append(node)

    Q = 0
    for nodes in communities.values():
        ls = 0
        ds = 0
        for i in nodes:
            neighbors = network[i]
            ds += len(neighbors)
            for j in neighbors:
                if j in nodes:
                    ls += 1
        ls /= 2
        Q += (ls / m) - ((ds / (2 * m)) ** 2)

    return Q

def crossover(parent1, parent2):
    keys = list(parent1.keys())
    i, j = sorted(random.sample(range(len(keys)), 2))
    child1, child2 = {}, {}
    for k in range(len(keys)):
        node = keys[k]
        if k < i or k >= j:
            child1[node] = parent1[node]
            child2[node] = parent2[node]
        else:
            child1[node] = parent2[node]
            child2[node] = parent1[node]
    return child1, child2

def mutate(particle, network):
    new_particle = particle.copy()
    node = random.choice(list(particle.keys()))
    neighbors = list(network[node])
    if neighbors:
        new_particle[node] = random.choice(neighbors)
    return new_particle

def pso_net(network, num_particles=30, max_gen=100, update_callback=None):
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

        if update_callback:
            decoded = decode_particle(globalbest)
            update_callback(decoded, q_scores, q_scores, network, gen + 1)

    end_time = time.time()
    print(f"\nExecution Time: {end_time - start_time:.4f} seconds")
    delta_q = q_scores[-1] - q_scores[0] if len(q_scores) > 1 else 0
    print(f"Modularity awal: {q_scores[0]:.4f}")
    print(f"Modularity akhir: {q_scores[-1]:.4f}")
    print(f"Δ Modularity (Q akhir - Q awal): {delta_q:.4f}")

    best_communities = decode_particle(globalbest)
    return best_communities, globalbest_fitness, q_scores
