import numpy as np
import sklearn.gaussian_process.kernels as kernels
from src.bayesian_optimization import bayesian_optimization
import safeopt
import GPy

# Set numpy random seed
np.random.seed(0)

# Domain
domain = np.array([[-10, 10]])

# Measurement noise
noise_var = 0.05 ** 2
# noise_var2 = 1e-5

# Bounds on the inputs variable
bounds = [(-10., 10.)]

# Define Kernel
kernel = GPy.kern.RBF(input_dim=len(bounds), variance=2., lengthscale=1.0, ARD=True)
kernel2 = kernel.copy()

# set of parameters
parameter_set = safeopt.linearly_spaced_combinations(bounds, 1000)

# Initial safe point
x0 = np.zeros((1, len(bounds)))

# Objective function
# obj_fun = lambda x: (x[0]-0.5)*np.sin(x[0])
obj_fun = safeopt.sample_gp_function(kernel, bounds, noise_var, 100)

# Communication network
N = np.eye(3)
N[0,1] = N[1,0] = N[1,2] = N[2,1] = 1

# Bayesian optimization object
BO = bayesian_optimization( objective = obj_fun,
                            domain = domain,
                            n_workers = 3,
                            network = N,
                            kernel = kernels.RBF(length_scale_bounds=(1, 1000.0)),
                            acquisition_function = 'ei',
                            policy = 'greedy',
                            fantasies = 0,
                            regularization = None,
                            regularization_strength = 0.01,
                            grid_density = 100 )

# Optimize
BO.optimize(n_iters = 10, n_runs = 1, n_pre_samples = 3, random_search = 1000, plot = True)
for a in range(BO.n_workers):
    print("Predicted max {}: {}".format(a, BO.pre_max[a]))
