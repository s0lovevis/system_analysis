import pandas as pd
import json
import numpy as np

def membership_value(x, points):

    for i in range(len(points) - 1):
        (x1, y1), (x2, y2) = points[i], points[i + 1]
        if x1 <= x <= x2:
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return 0

def fuzzify(input_value, membership_functions):

    fuzzy_values = {}
    for mf in membership_functions:
        fuzzy_values[mf["id"]] = membership_value(input_value, mf["points"])
    return fuzzy_values

def apply_rules(fuzzy_temp, rules, output_memberships):

    rule_outputs = {}
    for condition, output in rules:
        rule_activation = fuzzy_temp.get(condition, 0)
        if output not in rule_outputs:
            rule_outputs[output] = []
        rule_outputs[output].append(rule_activation)

    fuzzy_output = {out: [] for out in output_memberships}
    for output, activations in rule_outputs.items():
        max_activation = max(activations)
        for point in output_memberships[output]["points"]:
            x, y = point
            fuzzy_output[output].append((x, min(y, max_activation)))
    return fuzzy_output

def defuzzify(fuzzy_output):

    numerator, denominator = 0, 0
    for output, points in fuzzy_output.items():
        for x, y in points:
            numerator += x * y
            denominator += y
    return numerator / denominator if denominator != 0 else 0

with open("функции-принадлежности-температуры.json", encoding="utf-8") as temp_file:
    temp_memberships = json.load(temp_file)["температура"]

with open("функции-принадлежности-управление.json", encoding="utf-8") as control_file:
    control_memberships = {
        mf["id"]: mf for mf in json.load(control_file)["температура"]
    }

rules = [
    ("холодно", "интенсивный"),
    ("комфортно", "умеренный"),
    ("жарко", "слабый")
]

def main():
    
    input_temperature = 25
    fuzzy_temp = fuzzify(input_temperature, temp_memberships)
    fuzzy_control = apply_rules(fuzzy_temp, rules, control_memberships)
    control_value = defuzzify(fuzzy_control)

    print(f"Оптимальное управление: {control_value}")

if __name__ == "__main__":
    main()