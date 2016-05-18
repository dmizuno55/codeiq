import sys

def convert_digit_array(num, base):
    digit_array = []

    next_num = num // base
    digit_array.append(num % base)

    while next_num >= base:
        digit_array.append(next_num % base)
        next_num = next_num // base

    digit_array.append(next_num)

    digit_array.reverse()

    return digit_array

def is_narcissistic(digit_array, base):
    size = len(digit_array)

    powered_value = sum([pow(num, size) for num in digit_array])

    decimal_value = sum([pow(base, size - 1 - i) * n for (i, n) in enumerate(digit_array)])

    #print(digit_array, powered_value, decimal_value)
    return powered_value == decimal_value

def print_narcissistic_num(base):
    num = int('10', base)

    count = 0
    while count < base:
        digit_array = convert_digit_array(num, base)
        if is_narcissistic(digit_array, base):
            print(''.join([str(n) for n in digit_array]))
            count = count + 1

        num = num + 1

try:
    while True:
        base = int(input())
        print_narcissistic_num(base)
except EOFError:
    pass
