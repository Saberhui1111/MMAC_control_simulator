from basics import FunctionalBlock, Parameter, ParameterSet
from numbers import Number
import logging


class PIDController(FunctionalBlock):
    def __init__(self, logger: logging.Logger, parameters: ParameterSet, supervisor=None, name: str = ""):
        super().__init__(logger, parameters, name=name)
        self.supervisor = supervisor  # Добавляем атрибут supervisor
        self.previous_error = 0
        self.integral = 0

        if self.supervisor is None:
            self.logger.warning("Supervisor не был передан в PIDController.")

    def compute(self, tick_duration: Number = None) -> None:
        """
        Вычисляет управляющее воздействие на основе текущей ошибки.
        """
        setpoint = self.parameters["Setpoint"].value
        process_variable = self.parameters["ProcessVariable"].value
        kp = self.parameters["Kp"].value
        ki = self.parameters["Ki"].value
        kd = self.parameters["Kd"].value

        # Вычисление ошибки
        error = setpoint - process_variable

        # Пропорциональная составляющая
        proportional = kp * error

        # Интегральная составляющая
        self.integral += error * tick_duration
        integral = ki * self.integral

        # Дифференциальная составляющая
        derivative = kd * (error - self.previous_error) / tick_duration

        # Итоговое управляющее воздействие
        control_output = proportional + integral + derivative

        # Сохранение результата
        self.parameters["ControlOutput"].value = control_output

        # Обновление предыдущей ошибки
        self.previous_error = error

    def load_sensor_data(self, sensor_data: dict) -> None:
        """
        Загружает данные с сенсоров (например, состояние модели) в контроллер.
        """
        if "ProcessVariable" in sensor_data:
            self.parameters["ProcessVariable"].value = sensor_data["ProcessVariable"]

    def read_control_actions(self) -> dict:
        """
        Возвращает управляющее воздействие, рассчитанное контроллером.
        """
        return {"ControlInput": self.parameters["ControlOutput"].value}

    def get_state(self) -> dict:
        """
        Возвращает текущее состояние контроллера.
        """
        return {
            "Setpoint": self.parameters["Setpoint"].value,
            "ProcessVariable": self.parameters["ProcessVariable"].value,
            "ControlOutput": self.parameters["ControlOutput"].value,
            "Kp": self.parameters["Kp"].value,
            "Ki": self.parameters["Ki"].value,
            "Kd": self.parameters["Kd"].value,
            "Integral": self.integral,
            "PreviousError": self.previous_error
        }

    def set_supervisor(self, supervisor) -> None:
        """
        Устанавливает объект supervisor для контроллера.
        """
        self.supervisor = supervisor

    def get_supervisor(self):
        """
        Возвращает текущий объект supervisor.
        """
        return self.supervisor


# Определение параметров для PIDController
pid_controller_parameters = ParameterSet(
    Setpoint=Parameter("Setpoint", 100),  # Задание
    ProcessVariable=Parameter("ProcessVariable", 0),  # Текущее значение процесса
    Kp=Parameter("Kp", 1),  # Пропорциональный коэффициент
    Ki=Parameter("Ki", 0),  # Интегральный коэффициент
    Kd=Parameter("Kd", 0),  # Дифференциальный коэффициент
    ControlOutput=Parameter("ControlOutput", 0, sensor=True)  # Управляющее воздействие
)