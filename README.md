## Quick Start
If you would like to get started using T-PHATE, check out our [guided example](https://github.com/KrishnaswamyLab/TPHATE/blob/main/tests/usage.ipynb).

If you have loaded a data matrix `data` in python (with samples on rows, features on columns, where you believe the samples are non-independent), you can run TPHATE as follows:

```
import tphate

tphate_op = tphate.TPHATE()
data_tphate = tphate_op.fit_transform(data)
```


## Temporal PHATE

Temporal PHATE (T-PHATE) is a python package for learning robust manifold representations of timeseries data with high temporal autocorrelation. TPHATE does so with a dual-kernel approach, estimating the first view as an affinity matrix based on PHATE manifold geometry, and the second view as summarizing the transitional probability between two timepoints based on the autocorrelation of the signal. For more information, see our [publication in Nature Computational Science](https://www.nature.com/articles/s43588-023-00419-0).

Busch, et al. **Multi-view manifold learning of human brain-state trajectories**. 2023. *Nature Computational Science.*


## Installation

`pip install tphate`
