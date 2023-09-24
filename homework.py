from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    INFO_MESSAGE = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')
    training_type: str
    duration: int
    distance: int
    speed: float
    calories: float

    def get_message(self) -> str:
        """Возвращение строки сообщения"""
        return self.INFO_MESSAGE.format(training_type=self.training_type,
                                        duration=self.duration,
                                        distance=self.distance,
                                        speed=self.speed,
                                        calories=self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_OF_HORS = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.M_OF_HORS)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_WALK_1 = 0.035
    COEF_WALK_2 = 0.029
    COEF_M_S = 0.278
    COEF_WALK_3 = 100

    def __init__(self, action, duration, weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return (self.COEF_WALK_1 * self.weight + ((self.get_mean_speed()
                * self.COEF_M_S) ** 2 / (self.height / self.COEF_WALK_3))
                * self.COEF_WALK_2 * self.weight) * (self.duration
                                                     * self.M_OF_HORS)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_SWIM_1 = 1.1
    COEF_SWIM_2 = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Получить среднюю скорость плавания."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEF_SWIM_1) * self.COEF_SWIM_2
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
