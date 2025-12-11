from basics import FunctionalBlock, Parameter, ParameterSet
from collections import deque
from numbers import Number


class RSTController(FunctionalBlock):
    def __init__(self, parameters: ParameterSet):
        super().__init__(parameters)
        self.error_history = deque(maxlen=10)  # История ошибок
        self.output_history = deque(maxlen=10)  # История выходов системы
        self.control_history = deque(maxlen=10)  # История управляющих воздействий

    def compute(self, tick_duration: Number = None) -> None:
        setpoint = self.parameters["Setpoint"].value
        process_variable = self.parameters["ProcessVariable"].value
        R = self.parameters["R"].value
        S = self.parameters["S"].value
        T = self.parameters["T"].value

        # Вычисление ошибки
        error = setpoint - process_variable
        self.error_history.appendleft(error)

        # Вычисление управляющего воздействия
        control_output = 0

        # R(z) * E(z)
        for i in range(len(R)):
            if i < len(self.error_history):
                control_output += R[i] * self.error_history[i]

        # -T(z) * Y(z)
        for i in range(len(T)):
            if i < len(self.output_history):
                control_output -= T[i] * self.output_history[i]

        # / S(z)
        for i in range(1, len(S)):
            if i < len(self.control_history):
                control_output -= S[i] * self.control_history[i]
        control_output /= S[0]

        # Сохранение результата
        self.control_history.appendleft(control_output)
        self.output_history.appendleft(process_variable)
        self.parameters["ControlOutput"].value = control_output


rst_controller_parameters = ParameterSet(
    Setpoint=Parameter("Setpoint", 0),  # Задание
    ProcessVariable=Parameter("ProcessVariable", 0),  # Текущее значение процесса
    R=Parameter("R", [1, 0.5]),  # Полином R(z)
    S=Parameter("S", [1, -0.3]),  # Полином S(z)
    T=Parameter("T", [0.1, 0.05]),  # Полином T(z)
    ControlOutput=Parameter("ControlOutput", 0, sensor=True)  # Управляющее воздействие
)