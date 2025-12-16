from typing import List, Tuple, Callable, TypedDict, Dict, Any
import os

from tqdm import trange
import pandas as pd
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, qasm3
from qiskit.circuit.library import XGate, IGate, RYGate, HGate 
from qiskit import generate_preset_pass_manager
from qiskit.circuit.classical import expr

from constants import TOTAL_RUNS, TARGET_ASSETS_FOLDER

def player1(total_bullets:int, amount_of_live_shells:int):
    prob_of_live_shell = amount_of_live_shells/total_bullets
    op = IGate().to_mutable()
    if(prob_of_live_shell >= 0.5):
        op = XGate().to_mutable()
    op.label = "P1"
    return op

def player2(total_bullets:int, amount_of_live_shells:int):
    op = XGate().to_mutable()
    op.label = "P2"
    return op

def player3(total_bullets:int, amount_of_live_shells:int):
    op = HGate().to_mutable()
    op.label = "P3"
    return op

def player4(total_bullets:int, amount_of_live_shells:int):
    op = IGate().to_mutable()
    op.label = "P4"
    return op

def dealer(total_bullets:int, amount_of_live_shells:int):
    op = HGate().to_mutable()
    op.label = "D"
    return op

def gun(total_bullets:int, amount_of_live_shells:int):
    theta = 2*np.arcsin(np.sqrt(amount_of_live_shells/total_bullets))
    op = RYGate(theta).to_mutable()
    op.label = "GUN"
    return op


# a type to define all the function calls we do inside the circuit
class BuckshotRouletteCalls(TypedDict):
    player_first_play: QuantumCircuit

    player_if_himself_1: QuantumCircuit
    
    player_if_player_2: QuantumCircuit
    dealer_if_player_2: QuantumCircuit

    dealer_if_shot_1: QuantumCircuit

    player_if_dealer_2:QuantumCircuit
    dealer_if_dealer_2:QuantumCircuit


def player_play(player:Callable, total_bullets_player:int, live_shells_player:int, name:str) -> QuantumCircuit:
    inner_qc = QuantumCircuit(3, name=name)
    inner_qc.append(player(total_bullets_player, live_shells_player), [0])
    inner_qc.append(gun(total_bullets_player, live_shells_player).control(1, ctrl_state='0'), [0,1])
    inner_qc.append(gun(total_bullets_player, live_shells_player).control(1), [0,2])
    return inner_qc

def dealer_play(dealer:Callable, total_bullets_dealer:int, live_shells_dealer:int, name:str) -> QuantumCircuit:
    inner_qc = QuantumCircuit(3, name=name)
    inner_qc.append(dealer(total_bullets_dealer, live_shells_dealer), [0])
    inner_qc.append(gun(total_bullets_dealer, live_shells_dealer).control(1, ctrl_state='0'), [0,1])
    inner_qc.append(gun(total_bullets_dealer, live_shells_dealer).control(1), [0,2])
    return inner_qc

def buckshot_roulette(calls:BuckshotRouletteCalls, gun:Callable, total_bullets:int=3, live_shells:int=1):
    assert total_bullets > 0, "INVALID NUMBER OF BULLETS" 
    assert live_shells <= total_bullets and live_shells >= 0, "INVALID NUMBER OF LIVE SHELLS"
   
    player_life  = QuantumRegister(3, name="p") 
    dealer_life  = QuantumRegister(3, name="d")

    game = QuantumRegister(3, name="game")

    player_life_out = ClassicalRegister(3, name="po")
    dealer_life_out = ClassicalRegister(3, name="do")
    choice = ClassicalRegister(3, name="b")
    
    qc = QuantumCircuit(game, player_life, dealer_life, choice, player_life_out, dealer_life_out)

    def get_shot(index:int) -> expr.Expr:
        return expr.bit_and( expr.bit_not(player_life_out[index]), expr.bit_not(dealer_life_out[index]) )


    #qc.append(player_play(total_bullets, live_shells, name="Player Bullet 1"), [game[0], player_life[0], dealer_life[0]])
    qc.append(calls["player_first_play"], [game[0], player_life[0], dealer_life[0]])

    qc.measure(game[0], choice[0])
    qc.measure(player_life[0], player_life_out[0])
    qc.measure(dealer_life[0], dealer_life_out[0])

    qc.barrier()

    shot_first = get_shot(0)
    first_player = expr.bit_and(shot_first, expr.bit_not(choice[0]))
    first_dealer = expr.bit_and(shot_first, choice[0])

    with qc.if_test(first_player):
        #qc.append(player_play(total_bullets-1, live_shells, name="Player Bullet 2"), [game[1], player_life[1], dealer_life[1]])
        qc.append(calls["player_if_himself_1"], [game[1], player_life[1], dealer_life[1]])
        qc.measure(game[1], choice[1])
        qc.measure(player_life[1], player_life_out[1])
        qc.measure(dealer_life[1], dealer_life_out[1])

        shot_second = get_shot(1)
        second_player = expr.bit_and(shot_second, expr.bit_not(choice[1]))
        second_dealer = expr.bit_and(shot_second, choice[1])

        with qc.if_test(second_player):
            #qc.append(player_play(total_bullets-2, live_shells, name="Player Bullet 3"), [game[2], player_life[2], dealer_life[2]])
            qc.append(calls["player_if_player_2"], [game[2], player_life[2], dealer_life[2]])
            qc.measure(game[2], choice[2])
            qc.measure(player_life[2], player_life_out[2])
            qc.measure(dealer_life[2], dealer_life_out[2])
        with qc.if_test(second_dealer):
            #qc.append(dealer_play(total_bullets-2, live_shells, name="Player Bullet 3"), [game[2], dealer_life[2], player_life[2]])
            qc.append(calls["dealer_if_player_2"], [game[2], dealer_life[2], player_life[2]])
            qc.measure(game[2], choice[2])
            qc.measure(player_life[2], player_life_out[2])
            qc.measure(dealer_life[2], dealer_life_out[2])


    
    with qc.if_test(first_dealer):
        #qc.append(dealer_play(total_bullets-1, live_shells, name="Dealer Bullet 2"), [game[1], dealer_life[1], player_life[1]])
        qc.append(calls["dealer_if_shot_1"], [game[1], dealer_life[1], player_life[1]])
        qc.measure(game[1], choice[1])
        qc.measure(player_life[1], player_life_out[1])
        qc.measure(dealer_life[1], dealer_life_out[1])


        shot_second = get_shot(1)
        second_dealer = expr.bit_and(shot_second, expr.bit_not(choice[1]))
        second_player = expr.bit_and(shot_second, choice[1])

        with qc.if_test(second_player):
            #qc.append(player_play(total_bullets-2, live_shells, name="Player Bullet 3"), [game[2], player_life[2], dealer_life[2]])
            qc.append(calls["player_if_dealer_2"], [game[2], player_life[2], dealer_life[2]])
            qc.measure(game[2], choice[2])
            qc.measure(player_life[2], player_life_out[2])
            qc.measure(dealer_life[2], dealer_life_out[2])
        with qc.if_test(second_dealer):
            #qc.append(dealer_play(total_bullets-2, live_shells, name="Player Bullet 3"), [game[2], dealer_life[2], player_life[2]])
            qc.append(calls["dealer_if_dealer_2"], [game[2], dealer_life[2], player_life[2]])
            qc.measure(game[2], choice[2])
            qc.measure(player_life[2], player_life_out[2])
            qc.measure(dealer_life[2], dealer_life_out[2])

    return qc

Meas = Dict[str,int]

def who_won(measurements:Meas) -> List[Dict[str,int]]:
    results = []

    for bit_string, total in measurements.items():
        dealer_string = bit_string[:3][::-1]
        player_string = bit_string[3:6][::-1]
        #print("dealer=%s, player=%s"%(dealer_string, player_string))

        if('1' in dealer_string):
            results.append({"winner":"player", "total":total, "rounds":dealer_string.index('1')+1})

        elif('1' in player_string):
            results.append({"winner":"dealer", "total":total, "rounds":player_string.index('1')+1})



    return results

def run_quantum_version(df:pd.DataFrame, file:str, methods:Tuple[Any, Any]):
    total_bullets = 3
    live_shells = 1
    sim,sampler = methods
    pm = generate_preset_pass_manager(backend=sim, optimization_level=2)
    for evaluation_i in trange(TOTAL_RUNS):

        for strategy_i, player in enumerate((player1, player2, player3, player4)):

            calls = {
                "player_first_play": player_play(player, total_bullets, live_shells, name="Player Bullet 1"),
                "player_if_himself_1": player_play(player, total_bullets-1, live_shells, name="Player Bullet 2"),
                "player_if_player_2": player_play(player, total_bullets-2, live_shells, name="Player Bullet 3"),
                "dealer_if_player_2": dealer_play(dealer, total_bullets-2, live_shells, name="Player Bullet 3"),
                "dealer_if_shot_1": dealer_play(dealer, total_bullets-1, live_shells, name="Dealer Bullet 2"),
                "player_if_dealer_2": player_play(player, total_bullets-2, live_shells, name="Player Bullet 3"),
                "dealer_if_dealer_2": dealer_play(dealer, total_bullets-2, live_shells, name="Player Bullet 3")
            }

            qc = buckshot_roulette(calls, gun, total_bullets, live_shells)
            isa_qc = pm.run(qc)

            result = sampler.run([isa_qc], shots=TOTAL_RUNS).result()[0]

            measurements = dict(result.join_data().get_counts())

            results = [ {**result, "eval_i":evaluation_i+1, "strategy":strategy_i+1} for result in who_won(measurements) ]
            
            tmp_df = pd.DataFrame(results)
            df = pd.concat([df, tmp_df], ignore_index=True)

    df.to_csv(os.path.join(TARGET_ASSETS_FOLDER, file),index=False)


def get_circuit_image():
    total_bullets = 3
    live_shells = 1

    calls = {
        "player_first_play": player_play(player1, total_bullets, live_shells, name="Player Bullet 1"),
        "player_if_himself_1": player_play(player1, total_bullets-1, live_shells, name="Player Bullet 2"),
        "player_if_player_2": player_play(player1, total_bullets-2, live_shells, name="Player Bullet 3"),
        "dealer_if_player_2": dealer_play(dealer, total_bullets-2, live_shells, name="Player Bullet 3"),
        "dealer_if_shot_1": dealer_play(dealer, total_bullets-1, live_shells, name="Dealer Bullet 2"),
        "player_if_dealer_2": player_play(player1, total_bullets-2, live_shells, name="Player Bullet 3"),
        "dealer_if_dealer_2": dealer_play(dealer, total_bullets-2, live_shells, name="Player Bullet 3")
    }

    qc = buckshot_roulette(calls, gun, total_bullets, live_shells)
    qc.draw('mpl', style="clifford", filename=os.path.join(TARGET_ASSETS_FOLDER, "quantum-buckshot-roulette-circuit.png"))
