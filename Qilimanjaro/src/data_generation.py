import numpy as np

def generate_3circles_data(n_samples):
    """Generate 3 circles pattern data

    Args:
        n_samples (int): Number of samples to generate

    Returns:
        data (tuple):
            X (np-array): x, y positions
            y (np-array): classes
    """
    centers = np.array([[-1, 1], [1, 0], [-.5, -.5]])
    radii = np.array([1, np.sqrt(6/np.pi - 1), 1/2]) 
    points=[]
    classes=[]
    dim = 2
    for i in range(n_samples):
        X = 2 * (np.random.rand(dim)) - 1
        y = 0
        for j, (c, r) in enumerate(zip(centers, radii)): 
            if np.linalg.norm(X - c) < r:
                y = j + 1 
                
        points.append(X)
        classes.append(y)

    data = np.array(points), np.array(classes)
    settings = centers, radii             
    
    return data, settings