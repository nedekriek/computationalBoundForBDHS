# computationalBoundForBDHS

Before running code, you must install the computational_bound_for_bdhs package, using: `pip install .`

## Docker

We've added a Dockerfile to the repo. This will allow us to avoid issues with changing dependencies, and ensure that setting up the code on any other machine is dead simple (clone the repo, run `make docker-pull`).

The intention is that all experiments should be run within a Docker container. Don't worry, very little changes in how we operate the code - in fact, it's a bit easier now. The only major change is that we no longer run `python main.py` to start experiments (as this would not run them within a docker container). Now we run `make experiment`.
