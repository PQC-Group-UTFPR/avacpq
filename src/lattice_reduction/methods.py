from abc import ABC, abstractmethod
import json
from dash import html

class LatticeBasedMethod(ABC):

    @abstractmethod
    def initialize(self, dimension=2):
        """Initializes the method with the necessary parameters."""
        pass

    @staticmethod
    def get_method_by_name(cls, name, dimension=2):
        """Factory method to obtain the algorithm instance by name."""
        if name == 'Redução de Gauss':
            return None # Implement Gauss Reduction when needed
        elif name == 'LLL':
            return None  # Implement LLL when needed
        elif name == 'BKZ':
            return None  # Implement BKZ when needed
        else:
            return None
    def get_max_steps(self):
        """Returns the maximum number of steps for the algorithm."""
        # Finds the highest 'end' value across all phases
        return max(end for _, (_, end) in self.step_phases.items())
    
    @property
    @abstractmethod
    def step_phases(self):
        """
        Returns a dictionary with the phases and their step limits.
        Ex: {'processReduction': (0, 3), 'plotVectors': (4, 6)}
        """
        pass
    def get_phase_for_step(self, step):
        """Determines which phase a specific step is in."""
        for phase_name, (start, end) in self.step_phases.items():
            if start <= step <= end:
                return phase_name, step - start
        return "unknown", 0