# AVACPQ

Repository for the "Artifícios Visuais para Aprendizado de Criptografia Pós-Quântica" Project

## Requirements

- Docker environment

Alternatively, one can execute the Dash app by using `python3 main.py` after installing packages referred in `src/requirements.txt`. 


## Instructions

First, install docker. To build the docker image for this project download this repository, `cd avacpq` and then use `docker build -t avacpq .`

Execute with `docker run --network host -p 8050:8050 avacpq` (use `-d` if you want detached mode). It will create a Python/dash application accessible at port 8050.

Test it with [http://localhost:8050](http://localhost:8050).


## Overview of the source

- Root folder: Dockerfile, License, Readme, etc.
- `src/`: main folder for the application. Contains the dash-related application code.
    - `assets/`: web interface assets (CSS, favicon, logo).
    - `lattice-based/`: directory for the algorithms related to lattice-based cryptography
- `docs/`: auto-generated and additional documentation for the repository (TBD).

## Contribution Guidelines

See CONTRIBUTING file (TBD)

(Mainly, search for issues, assign one or more for you, create branch, commit, PR.)
