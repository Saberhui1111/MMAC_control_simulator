import logging
from basics.SimulationEngine import SimulationEngine
from basics.Supervisor import Supervisor
from basics.FunctionalBlockBank import FunctionalBlockBank
from basics.Historizer import Historizer
from examples.PIDController import PIDController, pid_controller_parameters
from examples.SimpleModel import SimpleModel, simple_model_parameters

# Создание логгера
logger = logging.getLogger("Simulation")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Создание пустого набора моделей для controller_bank
model_set = []

# Создание FunctionalBlockBank с пустым набором моделей
controller_bank = FunctionalBlockBank(logger=logger, model_set=model_set, name="Controller Bank")

# Создание supervisor
supervisor = Supervisor(logger=logger, controller_bank=controller_bank, name="Main Supervisor")

# Создание контроллера с supervisor
pid_controller = PIDController(logger=logger, parameters=pid_controller_parameters, supervisor=supervisor, name="PID Controller")

# Создание модели управляемой системы
simple_model = SimpleModel(logger=logger, parameters=simple_model_parameters)

# Создание системы сбора данных
historizer = Historizer()

# Создание SimulationEngine
engine = SimulationEngine(
    name="PID Simulation",
    model=simple_model,
    control_system=pid_controller,
    historizer=historizer,  # Передаём объект системы сбора данных
    tick_duration=0.1,
    logger=logger
)

# Запуск симуляции на 10 секунд
engine.run(simulation_time=10)