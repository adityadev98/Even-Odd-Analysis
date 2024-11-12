def print_cfg(cfg):
    for node in cfg.nodes():
        print(f"Node {node}:")
        print(f"  Label: {cfg.nodes[node].get('label', 'N/A')}")
        if 'instruction' in cfg.nodes[node]:
            print(f"  Instruction: {cfg.nodes[node]['instruction']}")
        print(f"  Successors: {list(cfg.successors(node))}")
        print()

def print_analysis_results(results):
    for node, state in results.items():
        print(f"Node {node}:")
        for var, parity in state.items():
            print(f"  {var}: {parity}")
        print()