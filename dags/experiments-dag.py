import sys
import os
from pathlib import Path

parent_path = str(Path(__file__).resolve().parents[1])
sys.path.append(parent_path)

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(parent_path, ".env"))

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator 
from airflow.sdk import DAG

from classical import setup_and_run_experiment, ExpTypes
from quantum_modified_version import run_quantum_modified
from quantum_default_version import run_quantum_default
from quantum_noisy import run_noisy_experiment, Backends

with DAG(
        "experiments",
        description="Run experiments",
        template_searchpath=parent_path,
    ) as dag:

    classical_1 = PythonOperator(task_id="default_random", python_callable=setup_and_run_experiment, op_args=[ExpTypes.DEFAULT_RANDOM])
    classical_2 = PythonOperator(task_id="default_random_seed", python_callable=setup_and_run_experiment, op_args=[ExpTypes.DEFAULT_RANDOM_SEED])
    classical_3 = PythonOperator(task_id="cpp", python_callable=setup_and_run_experiment, op_args=[ExpTypes.CPP])
    classical_4 = PythonOperator(task_id="cpp_set_seed", python_callable=setup_and_run_experiment, op_args=[ExpTypes.CPP_SET_SEED])

    setup_modified_aer = BashOperator(
            task_id="setup_modified_AER", 
            bash_command="setup-qiskit-aer.sh",
            cwd=parent_path)

    quantum_ideal_1 = PythonOperator(task_id="quantum_default", python_callable=run_quantum_default)
    quantum_ideal_2 = PythonOperator(task_id="quantum_modified", python_callable=run_quantum_modified)   

    quantum_noisy_fez = PythonOperator(task_id="quantum_noisy_fez", python_callable=run_noisy_experiment, op_args=[Backends.FEZ])
    quantum_noisy_torino = PythonOperator(task_id="quantum_noisy_torino", python_callable=run_noisy_experiment, op_args=[Backends.TORINO])

    run_notebook = BashOperator(
            task_id="run_notebook", 
            bash_command="jupyter nbconvert --execute analysis.ipynb --inplace",
            cwd=parent_path)

    run_dot_files = BashOperator(
            task_id="run_dot_scripts", 
            bash_command="dot-scripts.sh",
            cwd=parent_path)

    [classical_1, classical_2, classical_3, classical_4] >> setup_modified_aer
    setup_modified_aer >> [quantum_ideal_1, quantum_ideal_2]
    [quantum_ideal_1, quantum_ideal_2] >> quantum_noisy_fez
    [quantum_ideal_1, quantum_ideal_2] >> quantum_noisy_torino
    [quantum_noisy_fez, quantum_noisy_torino] >> run_notebook
    run_notebook >> run_dot_files

    
