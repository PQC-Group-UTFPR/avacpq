from abc import ABC, abstractmethod
import json
from dash import html

class BaseAlgorithm(ABC):
    """Base class for algorithms in the application."""
    
    @abstractmethod
    def initialize(self, dimension=2):
        """Initializes the algorithm with the necessary parameters."""
        pass
    
    @abstractmethod
    def process_step(self, step, data):
        """Processes a specific step of the algorithm and returns visualization."""
        pass
    
    @property
    @abstractmethod
    def step_phases(self):
        """
        Returns a dictionary with the phases and their step limits.
        Ex: {'keygen': (0, 3), 'encrypt': (4, 6), 'decrypt': (7, 10)}
        """
        pass
    
    def get_phase_for_step(self, step):
        """Determines which phase a specific step is in."""
        for phase_name, (start, end) in self.step_phases.items():
            if start <= step <= end:
                return phase_name, step
        return "unknown", 0
    
    @classmethod
    def get_algorithm_by_name(cls, name, dimension=2):
        """Factory method to obtain the algorithm instance by name."""
        if name == 'GGH':
            from lattice_based.ggh.ggh import GGH
            return GGH(dimension)
        elif name == 'LWE':
            return None  # Implement LWE when needed
        elif name == 'Alkaline':
            return None  # Implement Alkaline when needed
        else:
            return None
    def get_max_steps(self):
        """Returns the maximum number of steps for the algorithm."""
        # Finds the highest 'end' value across all phases
        return max(end for _, (_, end) in self.step_phases.items())
    