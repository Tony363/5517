import numpy as np

def simple_pagerank(
    adjacency_matrix:np.ndarray, 
    epsilon:np.float64=1e-6, 
    max_iterations:int=100
)->np.ndarray:
    """
    Computes the simple PageRank using vectorized operations.
    
    Args:
        adjacency_matrix (np.ndarray): Square adjacency matrix where A[i][j] = 1 if there's a link from j to i.
        epsilon (float): Convergence threshold.
        max_iterations (int): Maximum number of iterations.
    
    Returns:
        np.ndarray: PageRank vector.
    """
    adjacency_matrix = adjacency_matrix 
    N = adjacency_matrix.shape[0]
    # Convert adjacency matrix to stochastic matrix
    out_degree = adjacency_matrix.sum(axis=0)
    # Handle dangling nodes by assigning equal probability to all nodes
    dangling = (out_degree == 0)
    out_degree[dangling] = N
    stochastic_matrix = adjacency_matrix / out_degree
    stochastic_matrix[:, dangling] = 1.0 / N  # Distribute dangling nodes uniformly
    # Initialize PageRank vector
    R = np.ones(N)

    for iteration in range(max_iterations):
        R_new = stochastic_matrix @ R 
        delta = np.linalg.norm(R_new - R, 1)
        print(f"Iteration {iteration + 1}: {R_new}")
        if delta < epsilon:
            break
        R = R_new
    return R

def modified_pagerank(
    adjacency_matrix: np.ndarray, 
    E:np.float64, 
    c1:np.float64=0.85, 
    epsilon:np.float64=1e-6, 
    max_iterations:int=100
)->np.ndarray:
    """
    Computes the modified PageRank using vectorized operations.
    
    Args:
        adjacency_matrix (np.ndarray): Square adjacency matrix where A[i][j] = 1 if there's a link from j to i.
        E (np.ndarray): External influence vector.
        c1 (float): Coefficient for the link-based PageRank component.
        epsilon (float): Convergence threshold.
        max_iterations (int): Maximum number of iterations.
    
    Returns:
        np.ndarray: Modified PageRank vector.
    """
    adjacency_matrix = adjacency_matrix 
    N = adjacency_matrix.shape[0]
    # Convert adjacency matrix to stochastic matrix
    out_degree = adjacency_matrix.sum(axis=0)
    # Handle dangling nodes by assigning equal probability to all nodes
    dangling = (out_degree == 0)
    out_degree[dangling] = N
    stochastic_matrix = adjacency_matrix / out_degree
    stochastic_matrix[:, dangling] = 1.0 / N  # Distribute dangling nodes uniformly
    # Initialize PageRank vector
    R_prime = np.ones(N)
    c1_factor = c1
    c2_factor = 1 - c1

    for iteration in range(max_iterations):
        # print(c1_factor * (stochastic_matrix @ R_prime))
        R_new = c1_factor * (stochastic_matrix @ R_prime) + c2_factor * E
        delta = np.linalg.norm(R_new - R_prime, 1)
        print(f"Iteration {iteration + 1}: {R_new}")
        if delta < epsilon:
            break
        R_prime = R_new

    return R_prime

# Example Usage
if __name__ == "__main__":
    
    pages = ['A', 'B', 'C']
    N = len(pages)
    adjacency_matrix = np.array([
        [0, 1, 1],  # A is linked by C
        [1, 0, 1],  # B is linked by A
        [1, 0, 0],  # C is linked by A and B
    ])

    print("Simple PageRank:")
    pagerank = simple_pagerank(adjacency_matrix)
    for page, rank in zip(pages, pagerank):
        print(f"PR({page}) = {rank:.6f}")
    
    # Define external influence vector E for modified PageRank
    E = np.array([1]*N)  # Uniform external influence

    print("\nModified PageRank:")
    modified_pagerank_values = modified_pagerank(adjacency_matrix, E,c1=0.8)
    for page, rank in zip(pages, modified_pagerank_values):
        print(f"PR’({page}) = {rank:.6f}")

