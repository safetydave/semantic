import random
from scipy.stats import norm


def instantiate_and_solve(constructor, semantle):
    solver = constructor()
    target, steps = solver.solve(semantle)
    return steps
  

def run_trial(nullary_constructor, semantle, n=10, target_pool=None, cartesian=False, tick=10):
    obs = []
    targets = []
    for i in range(n):
        all_targets = [semantle.target]
        if target_pool is not None:
            all_targets = [random.choice(target_pool)] if not cartesian else target_pool
        for t in all_targets:
            semantle.target = t
            steps = instantiate_and_solve(nullary_constructor, semantle)
            obs.append(steps)
            targets.append(t)
        if tick is not None and i % tick == 0:
            print('.', end='')
    return obs, targets
  
  
def run_sweep(unary_constructor, values, semantle, n=10, target_pool=None, cartesian=False):
    results = []
    for v in values:
        trial = run_trial(lambda: unary_constructor(v), semantle, n, target_pool, cartesian)
        results.append(trial)
    return results
  
  
def sweep_norm(results):
    mu_std = [norm.fit(trials) for trials in results]
    return list(zip(*mu_std))
  
  
def compare(a, b, semantle, n=20):
    norm_a = norm.fit(run_trial(a, semantle, n))
    norm_b = norm.fit(run_trial(b, semantle, n))
    return norm_a, norm_b
  
  
def delta(test, base, semantle, n=20):
    comparison = compare(test, base, semantle, n)
    return comparison[1][0] - comparison[0][0]