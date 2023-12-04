# Docs

Documentation is generated using Sphinx and will be updated when changes are implemented on the develop branch. In addition to this documentation we also provide the virtual environment scripts utilized while operating on compute canada for different standard environments.

## Local

The documentation can be build locally, open a terminal window and navigate to the docs directory in the repository

```
make html
open index.html
```

Executing these commands in the docs directory will result in a webpage being opened offline

## Github

Alternatively you can always check the documentation online on the repository. To access the documentation via github navigate to the github pages and go to the latest deployment. Here you can click on the view deployment button which will redirect you to the documentation website.

## Compute Canada

We provide `virtualenv.sh` scripts that create a virtual environment based on the requirements in `graham_requirements.txt`. As Compute Canada periodically upgrades its [default environments](https://docs.computecanada.ca/wiki/Standard_software_environments), we provide support for the following default environments: 

   -[StdEnv/2016.4](stdenv-2016)
   -[StdEnv/2018.3](stdenv-2018)
   -[StdEnv/2020](stdenv-2020)


You can use such scripts as follows in e.g. [interactive jobs](https://docs.computecanada.ca/wiki/Running_jobs#Interactive_jobs)

```bash
source virtualenv.sh
```
