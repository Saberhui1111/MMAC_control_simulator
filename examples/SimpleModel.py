from basics import FunctionalBlock, Parameter, ParameterSet
from numbers import Number
import logging


class SimpleModel(FunctionalBlock):
    def __init__(self, logger: logging.Logger, parameters: ParameterSet):
        super().__init__(logger, parameters)

    def compute(self, tick_duration: Number = None) -> None:
        control_input = self.parameters["ControlInput"].value
        current_state = self.parameters["State"].value

        new_state = current_state + control_input * tick_duration

        self.parameters["State"].value = new_state


simple_model_parameters = ParameterSet(
    ControlInput=Parameter("ControlInput", 0),
    State=Parameter("State", 0, sensor=True) 
)