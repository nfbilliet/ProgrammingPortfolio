# GQCML

The Ghent Quantum Chemistry Machine Learning (GQCML) library is a python library that is built with the intetion of applying deep learning techniques on model Hamiltonians such as 

- Hückel model
- Hubbard model

The library uses [Pytorch](https://pytorch.org/) and [Pytorch Geometric](https://github.com/rusty1s/pytorch_geometric). For more information regarding the research and its results please check the [outline repository](https://github.com/GQCG-res/ML_research) that is associated with this repository

## Setting up your environment on the CC HPC

[Compute Canada](https://docs.computecanada.ca/wiki/Getting_started) offers many [GPUs](https://docs.computecanada.ca/wiki/Using_GPUs_with_Slurm) on which you can run [jobs](https://docs.computecanada.ca/wiki/Running_jobs). This infrastructure requires that you create and use [virtual environments](https://docs.computecanada.ca/wiki/Python) for which we have provided convenient [build scripts](docs/README.md).

## Installation

[Pre-download](https://docs.computecanada.ca/wiki/Python#Pre-downloading_packages) the package on a **login node** as compute nodes do not have access to the internet (in this case we will download a given `devops/cc-update` branch)

```bash
export GIT_SSH_COMMAND="ssh -i ~/.ssh/id_rsa"
pip download --no-deps git+ssh://git@github.com/GQCG/gqcml.git@devops/cc-update#egg=gqcml
```

On a **compute node**, install the package inside your [virtual environment that contains all requirements](docs/README.md) 

```bash
pip install gqcml-0.0.1.zip
```

## Running examples



## How to cite

If you wish to cite GQCML in your own research please include the following reference

```
  @misc{gqcml,
    author        = "Niels Billiet",
    institution   = "Ghent University",
    title         = "GQCML: A pytorch ML framework for model Hamiltonians",
    url           = "https://github.com/GQCG/gqcml"}
```
