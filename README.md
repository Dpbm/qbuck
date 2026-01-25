# A Study of Fairness in Buckshot Roulette Using Classical and Quantum Simulations

In this repo, we store all the code, results and analysis from our study on random engines fairness.

Here, we simulated the Buckshot Roulette dynamics in both quantum and classical domains.

Our primary goal was to identify which version could lead to a better player payoff. But at the end, our results raised the fairness discussing, 
since we found some bias in the classical version.

## How to run?

All the code was done in `python` with a bit of `jupyter`, `bash` and `graphviz dot language`. 

To automate and make it all easier to maintain, we developed an `Apache Airflow` pipeline.

To run that, we recommend you using `uv` for managing your python environment and `make` to allow you build and setup things easily. Then, running:

```bash
make # to build our cpp random engine
make airflow-up # to start the airflow setup
```

you'll have an `Airflow` instance at `localhost:8080`.

![pipeline](./assets/pipeline.png)
