# Distributed Bayesian Optimization for Multi-Agent Systems

author: filipkl@kth.se

---

# Table of Contents
1. [Installation](#setup-instructions-for-debian-like-environments)
2. [Usage](#usage)
3. [Examples](#examples)
4. [Credits](#credits)

---
# Setup instructions for Debian-like environments

This package is developed for Python 3.7.

1. (Optional) Set up and activate a virtual environment
```bash
virtualenv -p python3 ~/.venvs/dboenv
source ~/.venvs/dboenv/bin/activate
```

2. (Optional) Set up alias for virtual environment
```bash
echo 'alias dboenv="source ~/.venvs/dboenv/bin/activate"' >> ~/.zshrc
source ~/.zshrc  
```

2. Install python dependencies and dbo
```bash
git clone git@github.com:FilipKlaesson/dbo.git && cd dbo
pip install -r requirements.txt
python setup.py install
```

---

# Usage

---

# Examples

Single-agent 1D example

```python
import sklearn.gaussian_process as gp
from src.bayesian_optimization import bayesian_optimization

# Domain
domain = np.array([[-10, 10]])
# Objective function
obj_fun = lambda x: (x[0]-0.5)*np.sin(x[0])

# Bayesian optimization object
BO = bayesian_optimization( obj = obj_fun,
                            domain = domain,
                            kernel = gp.kernels.RBF(),
                            acquisition_function = 'ei'
                          )

# Optimize
BO.optimize(n_iters = 20, n_pre_samples = 3)
for a in range(BO.n_workers):
    print("Predicted max {}: {}".format(a, BO.pre_max[a]))
```

Single-agent 1D regret analysis example

```python
import sklearn.gaussian_process.kernels as kernels
from src.bayesian_optimization import bayesian_optimization

# Domain
domain = np.array([[-10, 10]])
# Objective function
obj_fun = lambda x: (x[0]-0.5)*np.sin(x[0])

# Bayesian optimization object
BO = bayesian_optimization( obj = obj_fun,
                            domain = domain,
                            kernel = gp.kernels.RBF(),
                            acquisition_function = 'ei'
                          )

# Optimize
BO.optimize(n_iters = 20, n_runs = 10, n_pre_samples = 3)
```

Single-agent 2D example

```python
import sklearn.gaussian_process.kernels as kernels
from src.bayesian_optimization import bayesian_optimization
from src.benchmark_functions import *

# Benchmark function
fun = Bohachevsky_1()
domain = fun.domain
obj_fun = lambda x: -1*fun.function(x)

# Bayesian optimization object
BO = bayesian_optimization( obj = obj_fun,
                            domain = domain,
                            kernel = kernels.RBF(),
                            acquisition_function = 'ei',
                          )

# Optimize
BO.optimize(n_iters = 20, n_pre_samples = 3)
for a in range(BO.n_workers):
    print("Predicted max {}: {}".format(a, BO.pre_max[a]))
```


Multi-agent 2D example

```python
import sklearn.gaussian_process.kernels as kernels
from src.bayesian_optimization import bayesian_optimization
from src.benchmark_functions import *

# Benchmark function
fun = Bohachevsky_1()
domain = fun.domain
obj_fun = lambda x: -1*fun.function(x)

# Communication network
num_agents = 3
N = np.eye(3)
N[0,1] = N[1,0] = N[1,2] = N[2,1] = 1

# Bayesian optimization object
BO = bayesian_optimization( obj = obj_fun,
                            domain = domain,
                            n_workers = num_agents,
                            network = N,
                            kernel = kernels.RBF(),
                            acquisition_function = 'ei',
                            grid_density = 30
                          )

# Optimize
BO.optimize(n_iters = 20, n_pre_samples = 3)
for a in range(BO.n_workers):
    print("Predicted max {}: {}".format(a, BO.pre_max[a]))
```

---

# Credits

[Filip Klaesson](https://filipklaesson.github.io/)
[Na Li](https://nali.seas.harvard.edu/)
Runyu Zhang
[Petter Nilsson](https://pettni.github.io/#/)
