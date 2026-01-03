from typing import List, Tuple, Optional
from abc import ABC, abstractmethod
from enum import Enum
import random
import os

from tqdm import trange 
import pandas as pd

from random_utility import RandomUtility

from constants import DEFAULT_RANDOM_FILE, DEFAULT_RANDOM_SEED_FILE, CPP_RANDOM_FILE, CPP_FILE, TOTAL_RUNS, TARGET_ASSETS_FOLDER

class Shell(Enum):
    BLANK=0
    LIVE=1

class Play(Enum):
    HIMSELF=0
    OPPONENT=1

class RandomEngine(ABC):
    @abstractmethod
    def set_seed(self, seed:int):
        pass

    @abstractmethod
    def get_random_value(self, values:Optional[List[float]]=None) -> int:
        pass

class ClassicalEngine(RandomEngine):
    def set_seed(self, seed:int):
        pass

    def get_random_value(self,values:Optional[List[float]]=None) -> int:
        if(values is None):
            return int(random.random() < 0.5)
        
        return random.choice(values)

class DefaultRandomEngineNoSeed(ClassicalEngine):
    pass

class DefaultRandomEngineWithSeed(ClassicalEngine):
    def set_seed(self, seed:int):
        random.seed(seed)

class CppEngine(RandomEngine):
    def __init__(self):
        self._random_util = RandomUtility()

    def set_seed(self, seed:int):
        pass
    
    def get_random_value(self,values:Optional[List[float]]=None) -> int:
        if(values is None):
            return self._random_util.get_random_value()

        t_values = len(values)
        prob = 1/t_values
        dist_probs = [prob]*t_values
        selected_i = self._random_util.get_random_value_by_array(dist_probs)

        return values[selected_i]

class CppRandomEngineNoSeed(CppEngine):
        def get_random_value(self,values:Optional[List[float]]=None) -> int:
                new_seed = RandomUtility().seed
                self._random_util.set_seed(new_seed)
                return super().get_random_value(values)

class CppRandomEngineWithSeed(CppEngine):
    def set_seed(self, seed:int):
        self._random_util.set_seed(seed)

class Player(ABC):

    def __init__(self, life:int, name:str, random_engine:RandomEngine):
        self._life = life
        self._points = 0
        self._name = name
        self._randomng = random_engine()

    @abstractmethod
    def play(self, bullets:List[Shell]) -> Play:
        """Think and then play"""
        pass

    def decrease_life(self):
        self._life -= 1

    def add_point(self):
        self._points += 1

    @property
    def randomng(self) -> RandomEngine:
        return self._randomng

    @property
    def name(self) -> str:
        return self._name

    @property
    def points(self) -> int:
        return self._points

    @property
    def life(self) -> int:
        return self._life

    @property
    def is_alive(self) -> bool:
        return self._life > 0

    def __str__(self):
        return self._name
    
    def __repr__(self):
        return self._name

class Game:
    def __init__(
        self,
        bullets: List[Shell],
        players: List[Player],
        random_engine: RandomEngine
    ):
        self._bullets = bullets
        self._players = players

        self._rounds = 0

        self._total_players = len(players)
        self._current_player_i = 0

        self._randomng = random_engine()

    def _get_next_player_i(self) -> int:
        return (self._current_player_i+1)%self._total_players

    def set_seed(self, seed:int):
        self._randomng.set_seed(seed)
        for player in self._players:
            player.randomng.set_seed(seed)

    @property
    def _opponent(self) -> Player:
        return self._players[self._get_next_player_i()]

    def _set_next_player(self):
        self._current_player_i = self._get_next_player_i()

    @property
    def _current_player(self) -> Player:
        return self._players[self._current_player_i]

    @property
    def _next_bullet(self) -> Shell:
        bullet = self._randomng.get_random_value(self._bullets)
        self._bullets.remove(bullet)
        return bullet

    @property
    def _has_live_shells(self) -> bool:
        return self._bullets.count(Shell.LIVE) > 0

    @property
    def _both_players_are_alive(self) -> bool:
        return all([player.is_alive for player in self._players]) 

    @property
    def _has_ended(self) -> bool:
        return not self._has_live_shells or not self._both_players_are_alive

    @property
    def _winner(self) -> Player:
        return max(self._players, key=lambda p: p.points)


    def run(self, debug:bool=True) -> Tuple[Player, int]:
        while not self._has_ended:
            player = self._current_player
            play = player.play(self._bullets)
            bullet = self._next_bullet
            self._rounds += 1

            if(play == Play.HIMSELF and bullet == Shell.BLANK):
                if(debug): print("Player shot himself and it was blank")
                continue
            elif(play == Play.HIMSELF and bullet == Shell.LIVE):
                if(debug):print("Player shot himself and it was live (-1)")
                player.decrease_life()
                self._opponent.add_point()
            elif(play == Play.OPPONENT and bullet == Shell.BLANK):
                if(debug):
                    print("Player shot his opponent and it was blank")
                    print("Next player")
                self._set_next_player()
            elif(play == Play.OPPONENT and bullet == Shell.LIVE):
                if(debug):
                    print("Player shot his opponent and it was Live (+1)")
                    print("Next player")
                self._opponent.decrease_life()
                self._set_next_player()
            
        
        if(debug): print("End game!")

        return self._winner, self._rounds




class Human1(Player):
    def play(self, bullets:List[Shell]) -> Play:
        total_live = bullets.count(Shell.LIVE)
        prob_of_live_shell = total_live/len(bullets)

        if(prob_of_live_shell >= 0.5):
            return Play.OPPONENT
        return Play.HIMSELF

class Human2(Player):
    def play(self, bullets:List[Shell]) -> Play:
        return Play.OPPONENT

class Human3(Player):
    def play(self, bullets:List[Shell]) -> Play:
        if(self._randomng.get_random_value()):
            return Play.OPPONENT
        return Play.HIMSELF

class Human4(Player):
    def play(self, bullets:List[Shell]) -> Play:
        return Play.HIMSELF

class Dealer(Player):
    def play(self, bullets:List[Shell]) -> Play:
        if(self._randomng.get_random_value()):
            return Play.OPPONENT
        return Play.HIMSELF

def execute_experiment(df:pd.DataFrame, file:str, engine:RandomEngine):
    for evaluation_i in trange(TOTAL_RUNS, desc=file):
        random_util = RandomUtility()
        seed = random_util.seed
        rows = []

        for strategy_i, player in enumerate((Human1, Human2, Human3, Human4)):
            
            # pseudo shots
            for run in range(TOTAL_RUNS):
                game = Game(
                    [Shell.BLANK, Shell.BLANK, Shell.LIVE], 
                    [player(2, "player", engine), Dealer(2, "dealer", engine)], 
                    engine)
                game.set_seed(seed)
                winner,rounds = game.run(debug=False)
                rows.append({"eval_i":evaluation_i+1, "winner":winner.name, "shot":run+1, "strategy":strategy_i+1, "rounds":rounds})
        
        tmp_df = pd.DataFrame(rows)

        df = pd.concat([df,tmp_df],ignore_index=True)
    df.to_csv(os.path.join(TARGET_ASSETS_FOLDER, file),index=False)

def get_df() -> pd.DataFrame:
    return pd.DataFrame(columns=("eval_i", "shot", "winner", "strategy", "rounds"))

class ExpTypes(Enum):
    DEFAULT_RANDOM=0
    DEFAULT_RANDOM_SEED=1
    CPP=2
    CPP_SET_SEED=3

experiments = {
        ExpTypes.DEFAULT_RANDOM:(DEFAULT_RANDOM_FILE, DefaultRandomEngineNoSeed),
        ExpTypes.DEFAULT_RANDOM_SEED:(DEFAULT_RANDOM_SEED_FILE, DefaultRandomEngineWithSeed),
        ExpTypes.CPP:(CPP_FILE, CppRandomEngineNoSeed),
        ExpTypes.CPP_SET_SEED:(CPP_RANDOM_FILE,CppRandomEngineWithSeed)
}

def setup_and_run_experiment(exp_type:ExpTypes):
    df = get_df()
    file,engine = experiments[exp_type]
    execute_experiment(df,file,engine)
    print(f"Finished for {exp_type.name}:{file}!")
