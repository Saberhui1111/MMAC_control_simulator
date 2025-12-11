import logging
from numbers import Number
from basics import FunctionalBlock, FunctionalBlockBank


class Supervisor:

    def __init__(self, logger: logging.Logger,
                 name: str = "",
                 controller_bank: FunctionalBlockBank = None,
                 estimator_bank: FunctionalBlockBank = None,
                 *args,
                 **kwargs):

        self.logger = logger

        if name == "":
            self.logger.warning(f"Не задано имя супервизора")
        self.name = name

        self.logger.info(f"Инициализация супервизора {name}")
        self.logger.debug(f"Банк контроллеров: {controller_bank}")
        self.logger.debug(f"Банк эстиматоров: {estimator_bank}")

        if controller_bank is None:
            self.logger.warning(f"Не задан банк контроллеров для супервизора {self.name}, создаётся пустой банк.")
            self.controller_bank = FunctionalBlockBank(logger, model_set=[], name="Default Controller Bank")
        else:
            self.controller_bank = controller_bank

        if estimator_bank is None:
            self.logger.warning(f"Не задан банк эстиматоров для супервизора {self.name}, создаётся пустой банк.")
            self.estimator_bank = FunctionalBlockBank(logger, model_set=[], name="Default Estimator Bank")
        else:
            self.estimator_bank = estimator_bank

        self.last_switch: Number = None  # TODO: Точно ли супервайзеру нужно это знать?
        self.current_controller: str = None
        self.current_estimator: str = None

    def choose_controller(self) -> None:
        raise NotImplementedError

    def chose_estimator(self) -> None:
        raise NotImplementedError

    def compute_estimators(self,
                           tick_duration: Number | dict[str, Number],
                           names: list[str] | None = None,
                           time_for_not_specified: Number = None) -> None:
        self.estimator_bank.compute(tick_duration, names, time_for_not_specified)

    def compute_controllers(self,
                            tick_duration: Number | dict[str, Number],
                            names: list[str] | None = None,
                            time_for_not_specified: Number = None) -> None:
        self.controller_bank.compute(tick_duration, names, time_for_not_specified)