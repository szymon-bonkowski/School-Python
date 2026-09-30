from random import randint


def make_binary_file():
    with open("zad1.txt", "w") as file:
        for _ in range(1000):
            number = ""
            for _ in range(8):
                number += str(randint(0, 1))
            file.write(number + "\n")


def read_binary_file():
    numbers = []
    with open("zad1.txt", "r") as file:
        for line in file:
            numbers.append(int(line.strip(), 2))
    return numbers


def save_numbers(numbers, name):
    with open(name, "w") as file:
        for number in numbers:
            file.write(str(number) + "\n")


def sort_numbers(numbers):
    for end in range(len(numbers) - 1, 0, -1):
        for i in range(end):
            if numbers[i] > numbers[i + 1]:
                numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]


def factors(number):
    if number < 2:
        return [number]
    result = []
    divisor = 2
    while number > 1:
        while number % divisor == 0:
            result.append(divisor)
            number //= divisor
        divisor += 1
    return result


def make_factor_file(numbers):
    with open("zad4.txt", "w") as file:
        for number in numbers:
            file.write(str(number) + "-" + "-".join(str(x) for x in factors(number)) + "\n")


def make_other_files(numbers):
    with open("zad5.txt", "w") as file:
        with open("zad1.txt", "r") as source:
            for line in source:
                word = line.strip()
                if word == word[::-1]:
                    file.write(word + "\n")

    with open("zad6.txt", "w") as file:
        for number in numbers:
            file.write(f"{number} - {number:b}\n")

    with open("zad7.txt", "w") as file:
        for number in numbers:
            if number % 3 == 0 and number % 5 == 0:
                file.write(str(number) + "\n")

    with open("zad8.txt", "w") as file:
        for number in numbers:
            total = 0
            for digit in str(number):
                total += int(digit)
            file.write(f"{number} - {total}\n")

    with open("zad9.txt", "w") as file:
        i = len(numbers) - 1
        while i >= 0:
            file.write(str(numbers[i]) + "\n")
            i -= 1

    with open("zad10.txt", "w") as file:
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] + numbers[j] == 100:
                    file.write(f"{numbers[i]} - {numbers[j]}\n")


if __name__ == "__main__":
    make_binary_file()
    numbers = read_binary_file()
    save_numbers(numbers, "zad2.txt")
    sort_numbers(numbers)
    save_numbers(numbers, "zad3.txt")
    make_factor_file(numbers)
    make_other_files(numbers)
