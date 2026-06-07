import time
import tracemalloc

class PerformanceMonitor:
    def __init__(self):
        self.results = {
            "brute_force": [],
            "greedy": []
        }
    
    def measure_execution(self, algorithm_func, origin, destination, is_brute_force=False, *args, **kwargs):
        """Measures execution time, memory usage, and elementary operations of an algorithm"""
        tracemalloc.start()
        tracemalloc.clear_traces()
        start_time = time.perf_counter()

        result = algorithm_func(origin, destination, *args, **kwargs)

        end_time = time.perf_counter()
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time_ms = (end_time - start_time) * 1000
        peak_memory_mb = peak_memory / (1024 * 1024)

        if is_brute_force:
            ops_calls = result.get('recursive_calls', 0)
            ops_paths = result.get('evaluated_paths', 0)
            operations_metric = {"calls": ops_calls, "paths": ops_paths}
        else:
            operations_metric = {"nodes_evaluated": result.get('evaluated_nodes', 0)}

        return {
            "path": result.get("path"),
            "cost": result.get("cost"),
            "time_ms": execution_time_ms,
            "memory_mb": peak_memory_mb,
            "operations": operations_metric
        }

    def run_benchmarks(self, test_cases, bst_high_risk=None):
        """
        Runs benchmarks for both algorithms across different instance sizes (N)
        test_cases should be a list of dicts: [{'N': 5, 'origin': A, 'dest': B}, ...]
        """
        total_cases = len(test_cases)

        for i, case in enumerate(test_cases):
            n_size = case['N']
            orig = case['origin']
            dest = case['dest']
            brute_force_finder = case['fb_finder']
            greedy_finder = case['gr_finder']

            print(f"[{i+1}/{total_cases}] Testando instância N={n_size}... ", end="", flush=True)

            if n_size <= 12:
                bf_metrics = self.measure_execution(
                    brute_force_finder.find_best_path, orig, dest, is_brute_force=True
                )
                bf_metrics['N'] = n_size
                self.results['brute_force'].append(bf_metrics)
            else:
                bf_metrics = None

            gr_metrics = self.measure_execution(
                greedy_finder.find_best_path, orig, dest, is_brute_force=False, bst_high_risk=bst_high_risk
            )
            gr_metrics['N'] = n_size
            self.results['greedy'].append(gr_metrics)

            if bf_metrics is not None:
                cost_fb = bf_metrics['cost']
                cost_gr = gr_metrics['cost']

                if cost_fb > 0 and cost_fb != float('inf'):
                    gap = ((cost_gr - cost_fb) / cost_fb) * 100.0
                else:
                    print(f"\n[Aviso] Custo FB inválido (0 ou inf) em N={n_size}. Gap cravado em 0%.")
                    gap = 0.0
                
                gr_metrics['optimality_gap_percent'] = round(gap, 2)
            else:
                gr_metrics['optimality_gap_percent'] = None

            print(f"Concluído!")
        
        return self.results