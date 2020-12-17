from typing import List, Dict
from math import fabs


def get_deviations(fs: List[float], spline_fs: List[float]) -> List[float]:
    """Получить список отклонений значений сплайна от значений заданного набора.

    Args:
        fs (List[float]): список значений функции
        spline_fs (List[float]): список значений сплайна

    Returns:
        Список отклонений.
    """
    deviations = []
    for i in range(len(fs)):
        deviations.append(fabs(fs[i] - spline_fs[i]))
    return deviations


def get_recompute_dict(mean_deviation: float, grade: float, deviations: List[float]) -> Dict[int, float]:
    """Получить словарь коэффициентов, на которые будут меняться веса omega.
    Ключ словаря (int) - индекс, которому соответсвует точка x в массиве xs, значение функции в fs и значение сплайна.
    Значение (float) - коэффициент, на который изменится omega.

    Args:
        mean_deviation (float): среднее отклонение
        grade (float): значение, контроллирующее, насколько отклонение будет больше среднего
        deviations (List[float]): отклонения для каждой точки

    Returns:
        Словарь изменения omega.
    """
    recompute_dict = dict()
    for i in range(len(deviations)):
        if deviations[i] > mean_deviation * grade:
            recompute_dict[i] = deviations[i] - mean_deviation
    return recompute_dict


def recompute_omega(recompute: Dict[int, float], omega: List[float]):
    """Пересчитать omega.

    Args:
        recompute (Dict[int, float]): словарь, по которому будут пересчитываться omega
        omega (List[float]): веса, регулирующие близость сплайна в точке x

    Returns:
        none
    """
    for key in recompute.keys():
        omega[key] += recompute[key]
