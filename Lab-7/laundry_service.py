import math


def parse_order(text):
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    garment, kg = text.split(':')
    garment = garment.strip()
    if not garment:
        return None
    try:
        weight = float(kg.strip())
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(weight) or weight < 0:
        return None
    return garment.title(), weight


def weight_average(weights_csv):
    if not isinstance(weights_csv, str) or not weights_csv.strip():
        return None
    parts = weights_csv.split(',')
    try:
        values = [float(part.strip()) for part in parts]
    except (ValueError, OverflowError):
        return None
    if not values or any(not math.isfinite(n) or n < 0 for n in values):
        return None
    average = sum(values) / len(values)
    return average if math.isfinite(average) else None


def payable_charge(text):
    if not isinstance(text, str) or text.count('|') != 1:
        return None
    charge, discount = text.split('|')
    try:
        charge = float(charge.strip())
        discount = float(discount.strip())
    except (ValueError, OverflowError):
        return None
    if not all(math.isfinite(n) and n >= 0 for n in (charge, discount)):
        return None
    total = charge * 1.18 - discount
    return max(total, 0.0) if math.isfinite(total) else None


def main():
    print('==== Running parse_order ====')
    print('Garment and Weight:', parse_order(input('Enter garment:weight in kg (e.g. regular:6): ')))
    print('\n==== Running weight_average ====')
    print('Average Weight:', weight_average(input('Enter garment weights as CSV (e.g. 3,5,8): ')))
    print('\n==== Running payable_charge ====')
    print('Payable Charge:', payable_charge(input('Enter charge|discount (e.g. 300|40): ')))


if __name__ == '__main__':
    main()
