def rosenbrock(*args: float) -> float:
    result: float = 0
    for i in range(len(args) - 1):
        result += 100 * (args[i + 1] - args[i]**2)**2 + (1 - args[i])**2
    return result


def himmelblau(x: float, y: float) -> float:
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2
