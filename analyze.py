import numpy as np

ENCODING = {
    'Yes': 1,
    'No': -1,
    '': 0,
}

def prop_sort_key(prop):
  return ('', int(prop)) if prop.isdigit() else (prop, 0)

def endorsements_to_matrix(endorsements):
  orgs = sorted(set(k[0] for k in endorsements.keys()))
  props = sorted(set(k[1] for k in endorsements.keys()), key=prop_sort_key)
  m, n = len(orgs), len(props)
  data = np.zeros([m, n])
  for k, v in endorsements.items():
    org, prop = k
    i, j = orgs.index(org), props.index(prop)
    data[i, j] = ENCODING[v]
  return data, orgs, props
  
def pca(data):
  mu = np.mean(data, axis=0)
  x = data - mu[np.newaxis]
  cov = np.dot(x.T, x)
  vals, vecs = np.linalg.eig(cov)
  return vals, vecs
