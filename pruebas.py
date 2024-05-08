from pymoo.core.problem import Problem
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.util import plotting

problem = Problem(n_var=2, xl=0, xu=1, )

sampling = FloatRandomSampling()

X = sampling(problem, 10).get("X")
plotting.plot(X, no_fill=True)



