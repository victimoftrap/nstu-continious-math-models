from typing import List, Dict
from math import fabs


def get_deviations(fs: List[float], spline_fs: List[float]) -> List[float]:
    deviations = []
    for i in range(len(fs)):
        deviations.append(fabs(fs[i] - spline_fs[i]))
    return deviations


def get_recompute_dict(mean_deriv: float, grade: float, deviations: List[float]) -> Dict[int, float]:
    recompute_dict = dict()
    for i in range(len(deviations)):
        if deviations[i] > mean_deriv * grade:
            recompute_dict[i] = deviations[i] - mean_deriv
    return recompute_dict


def recompute_omega(recompute: Dict[int, float], a_omega: List[float], b_omega: List[float]):
    for key in recompute.keys():
        a_omega[key] += recompute[key]
        b_omega[key] += recompute[key]
