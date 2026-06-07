import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

class Visualizer:
    def plot_mst_graph(self, graph_dict, positions, title, data_source, mst_edges, is_path=False, save_path=None):
        """Draw the geospatial graph highlighting the edges of the Minimum Spanning Tree (MST)"""
        G = nx.Graph()

        for node, edges in graph_dict.items():
            G.add_node(node)
            for neighbor, weight in edges:
                G.add_edge(node, neighbor, weight=weight)
        
        plt.figure(figsize=(10, 8))
        plt.style.use('default')

        nx.draw_networkx_edges(G, positions, edge_color='lightgray', alpha=0.3, node_size=10)
        nx.draw_networkx_nodes(G, positions, node_color='lightgray', node_size=10)
        if is_path:
            nx.draw_networkx_edges(G, positions, edgelist=mst_edges, edge_color='black', width=2, alpha=0.8, node_size=20)
            mst_nodes = list(set(node for edge in mst_edges for node in edge[:2]))
            nx.draw_networkx_nodes(G, positions, nodelist=mst_nodes, node_size=10, node_color="black")
            black_line = mlines.Line2D([], [], color='black', linewidth=2.5, label='Caminho rápido')
        else:
            nx.draw_networkx_edges(G, positions, edgelist=mst_edges, edge_color='black', width=2, alpha=0.8, node_size=20)
            nx.draw_networkx_nodes(G, positions, node_size=10, node_color="black")
            black_line = mlines.Line2D([], [], color='black', linewidth=2.5, label='Arestas MST')

        plt.title(title, fontsize=14)
        black_dot = mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=10, label='Municípios')
        gray_line = mlines.Line2D([], [], color='lightgray', linewidth=1.5, label='Malha Viária')
        plt.legend(handles=[black_dot, gray_line, black_line], loc='best', fontsize=9, framealpha=0.9)
        plt.figtext(0.5, 0.01, f"Fonte dos Dados: {data_source}", wrap=True, horizontalalignment='center', fontsize=9, style='italic')

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
    def plot_bst_tree(self, bst_nodes_list, title, data_source, save_path=None):
        """Draws a hierarchical visual representation of the Binary Tree for instances of 10 to 15 nodes"""
        G = nx.DiGraph()
    
        if not bst_nodes_list:
            return
        
        sorted_nodes = sorted(bst_nodes_list, key=lambda x: x[2])

        colors = []
        for i, node in enumerate(sorted_nodes):
            name_clean = node[1].split('-')[0].strip()
            risk = node[2]

            G.add_node(node[0], label=f"{name_clean}\nR: {risk:.2f}")
            if i > 0:
                parent_idx = (i - 1) // 2
                G.add_edge(sorted_nodes[parent_idx][0], node[0])
            
            if risk > 0.7:
                colors.append("#e63946")
            elif risk > 0.4:
                colors.append("#e9c46a")
            else:
                colors.append("#2a9d8f")
        
        pos = {}
        def set_pos(node_idx, x, y, dx):
            if node_idx < len(sorted_nodes):
                node_id = sorted_nodes[node_idx][0]
                pos[node_id] = (x, y)
                set_pos(2 * node_idx + 1, x - dx, y - 1, dx / 2)
                set_pos(2 * node_idx + 2, x + dx, y - 1, dx / 2)
                
        set_pos(0, 0, 0, 4)
        
        plt.figure(figsize=(10, 6))
        labels = nx.get_node_attributes(G, 'label')
        nx.draw(G, pos, labels=labels, with_labels=True, node_color=colors, node_size=2500, font_size=8, font_color="black", arrows=False, edge_color='gray')    
        
        y_values = [y for x, y in pos.values()]
        plt.ylim(min(y_values) - 1, max(y_values) + 0.5)

        plt.title(title, fontsize=14, fontweight='bold')
        legend_elements = [
            mpatches.Patch(color='#e63946', label='Risco Alto (> 0.70)'),
            mpatches.Patch(color='#e9c46a', label='Risco Médio (0.41 a 0.70)'),
            mpatches.Patch(color='#2a9d8f', label='Risco Baixo (<= 0.40)')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=9, title="Índice de Seca", framealpha=0.9)
        plt.figtext(0.5, 0.01, f"Fonte dos Dados: {data_source}", wrap=True, horizontalalignment='center', fontsize=9, style='italic')
        plt.subplots_adjust(bottom=0.3)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_time_performance(self, benchmark_results, title, data_source, save_path=None):
        """Plot the line graph: Time (Y) vs N (X)"""
        bf_data = benchmark_results.get('brute_force', [])
        gr_data = benchmark_results.get('greedy', [])
        
        n_bf = [item['N'] for item in bf_data]
        time_bf = [item['time_ms'] for item in bf_data]
        
        n_gr = [item['N'] for item in gr_data if item['N'] <= max(n_bf, default=12)]
        time_gr = [item['time_ms'] for item in gr_data if item['N'] in n_gr]
        
        plt.figure(figsize=(8, 5))
        plt.plot(n_bf, time_bf, marker='o', color='#ef4444', label='Força Bruta', linewidth=2)
        plt.plot(n_gr, time_gr, marker='s', color='#2563eb', label='Guloso (Dijkstra)', linewidth=2)
        plt.xlabel('Número de Municípios (N)', fontweight='bold')
        plt.ylabel('Tempo de Execução (ms)', fontweight='bold')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.legend(loc='upper left', framealpha=0.9)
        plt.figtext(0.5, -0.02, f"Fonte dos Dados: {data_source}", wrap=True, horizontalalignment='center', fontsize=9, style='italic')
        plt.tight_layout(rect=[0, 0.06, 1, 1])

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_memory_performance(self, benchmark_results, title, data_source, save_path=None):
        """Plot the line graph: memory (Y) vs N (X)"""
        bf_data = benchmark_results.get('brute_force', [])
        gr_data = benchmark_results.get('greedy', [])
        
        n_bf = [item['N'] for item in bf_data]
        mem_bf = [item['memory_mb'] for item in bf_data]

        n_gr = [item['N'] for item in gr_data if item['N'] <= max(n_bf, default=12)]
        mem_gr = [item['memory_mb'] for item in gr_data if item['N'] in n_gr]
        
        plt.figure(figsize=(8, 5))
        plt.plot(n_bf, mem_bf, marker='o', color='#b91c1c', label='Força Bruta (Pico RAM)', linewidth=2)
        plt.plot(n_gr, mem_gr, marker='s', color='#1d4ed8', label='Guloso (Pico RAM)', linewidth=2)
        plt.xlabel('Número de Municípios (N)', fontweight='bold')
        plt.ylabel('Uso de Memória (MB)', fontweight='bold')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(loc='upper left', framealpha=0.9)
        plt.figtext(0.5, -0.02, f"Fonte dos Dados: {data_source}", wrap=True, horizontalalignment='center', fontsize=9, style='italic')
        plt.tight_layout(rect=[0, 0.06, 1, 1])

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_optimality_gap(self, benchmark_results, title, data_source, save_path=None):
        """Plot the bar graph showing the percentage error (gap) of the Greedy One in relation to the optimum"""
        gr_data = [item for item in benchmark_results.get('greedy', []) if item.get('optimality_gap_percent') is not None]
        
        n_vals = [item['N'] for item in gr_data]
        gaps = [item['optimality_gap_percent'] for item in gr_data]
        
        plt.figure(figsize=(8, 5))
        plt.bar(n_vals, gaps, color='#d97706', edgecolor='black', alpha=0.85, label='Gap do Guloso vs Ótimo Global')
        for i, gap in enumerate(gaps):
            plt.text(n_vals[i], gap + 0.5, f"{gap}%", ha='center', fontsize=9, fontweight='bold')
        plt.xlabel('Número de Municípios (N)', fontweight='bold')
        plt.ylabel('Gap de Otimalidade (%)', fontweight='bold')
        plt.title(title, fontsize=14, fontweight='bold')
        plt.ylim(0, max(gaps + [5]) * 1.2)
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        plt.legend(loc='upper left', framealpha=0.9)
        plt.figtext(0.5, -0.02, f"Fonte dos Dados: {data_source}", wrap=True, horizontalalignment='center', fontsize=9, style='italic')
        plt.tight_layout(rect=[0, 0.06, 1, 1])

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()