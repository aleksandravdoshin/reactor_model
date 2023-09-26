import re
import numpy as np

def replace_substrings(s: str) -> str:
    def replacer(match):
        count_2 = match.group().count('2')
        return f"({count_2 * 2})"
    
    s = re.sub(r'(2_)+2', replacer, s)  # заменяем подстроки вида 2_2_2 на их сумму
    s = re.sub(r'2_', '(2)_', s)  # заменяем 2_ на (2)
    return s


def generate_combinations(N):
    # Генерация базовых комбинаций
    basic_combinations = [str(i) for i in range(2, N+1, 2)]
    
    results = basic_combinations.copy()

    # Рекурсивная функция для генерации комбинаций
    def generate_recursive(prefix):
        for basic in basic_combinations:
            combination = prefix + "_" + basic
            values = [int(val) for val in combination.split("_") if not val.startswith("(2)")]
            # Добавляем (2) к общему подсчету для каждого (2) в комбинации
            values_sum = sum(values) + 2 * combination.count("(2)")
            if values_sum <= N:
                results.append(combination)
                generate_recursive(combination)

    for basic in basic_combinations:
        generate_recursive(basic)
    results = list(filter(lambda x: not (x.endswith("_2") and len(x)>2), results))[1:]
    results = [s for s in results if not re.search(r'2_\d+$', s)]
    results = list(map(replace_substrings, results))
    return results


def grow_from_combination(combo):
    # Если комбинация начинается с "(2)"
    if combo.startswith("("):
        n = int(combo[1:].split(')')[0])
        prefix = combo[3:]

        if n == 2:
            return f"Cr{prefix.replace('_', '_C')[1:]} + C2 <-> Cr(C2){prefix.replace('_', '_C')}"
        
        return f"Cr(C{n-2}){prefix.replace('_', '_C')} + C2 <-> Cr(C{n}){prefix.replace('_', '_C')}"

    parts = combo.split("_")
    
    # Линейный рост
    if len(parts) == 1:
        return f"CrC{int(parts[0])-2} + C2 <-> CrC{parts[0]}"

    # Ветвистые структуры
    else:
        prefix = "_".join(parts[1:])
        # print(combo, '|',prefix)
        return f"CrC{prefix.replace('_', '_C')} + C{parts[0]} <-> CrC{combo.replace('_', '_C')}".replace('C(', '(C')

def alk_from_combination(combo):
    combo = combo.replace('(', '(C')
    if not combo.startswith("("):
        combo = 'C' + combo
    combo = combo.replace('_', '_C')
    return combo

def death_from_combination(combo):
    combo = alk_from_combination(combo)
    return f'Cr{combo} <-> {combo} + Cr'

def diff2pore(combo):
    alk = alk_from_combination(combo)
    return f'{alk} <-> {alk}_pore'

def diff_out(combo):
    alk = alk_from_combination(combo)
    return f'{alk}_pore -> {alk}_out'

def linear_out(N):
    linears = []
    for i in range(4, N+1, 2):
        linears.append(f'C{i} -> C{i}_out')
    return linears

def give_reaction_lists(N):
    combinations = generate_combinations(N)
    reactions = ['Cr + C2 <-> CrC2'] + [grow_from_combination(combo) for combo in combinations]
    death = [death_from_combination(combo) for combo in combinations]
    pore = [diff2pore(combo) for combo in combinations]
    out = [diff_out(combo) for combo in combinations] + linear_out(N)
    return reactions, death, pore, out