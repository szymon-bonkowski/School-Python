from random import randint
from math import sqrt


def save_numbers():
    with open("numbers.txt", "w") as file:
        for _ in range(1000):
            file.write(f"{randint(1, 10)} {randint(1, 10)} {randint(1, 10)}\n")


def read_numbers():
    numbers = []
    with open("numbers.txt", "r") as file:
        for line in file:
            numbers.append([int(x) for x in line.split()])
    return numbers


def triangle(a, b, c):
    return a + b > c and a + c > b and b + c > a


def right(a, b, c):
    sides = sorted([a, b, c])
    return sides[0] ** 2 + sides[1] ** 2 == sides[2] ** 2


def area(a, b, c):
    half = (a + b + c) / 2
    return sqrt(half * (half - a) * (half - b) * (half - c))


def make_triangle_files(numbers):
    files = {
        "triangles.txt": [],
        "equilateral_triangles.txt": [],
        "right_triangles.txt": [],
        "isosceles_triangles.txt": []
    }
    biggest = 0
    biggest_sides = []

    for sides in numbers:
        a, b, c = sides
        text = f"{a} {b} {c}\n"
        if triangle(a, b, c):
            files["triangles.txt"].append(text)
            if a == b == c:
                files["equilateral_triangles.txt"].append(text)
            if right(a, b, c):
                files["right_triangles.txt"].append(text)
            if a == b or a == c or b == c:
                files["isosceles_triangles.txt"].append(text)
            current = area(a, b, c)
            if current > biggest:
                biggest = current
                biggest_sides = sides

    for name, lines in files.items():
        with open(name, "w") as file:
            file.writelines(lines)
    print("biggest triangle:", biggest_sides, biggest)


def temperatures():
    with open("zad1.txt", "w") as file:
        for _ in range(20):
            file.write(f"{randint(-30, -1)}\n")

    values = []
    with open("zad1.txt", "r") as file:
        for line in file:
            values.append(int(line))
    values.sort()
    print("three lowest temperatures:", values[:3])


def caesar(text, move):
    result = ""
    for char in text:
        if "a" <= char <= "z":
            result += chr((ord(char) - ord("a") + move) % 26 + ord("a"))
        elif "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") + move) % 26 + ord("A"))
        else:
            result += char
    return result


def text_tasks():
    text = "This is a short text for the cipher task.\n"
    with open("zad3.txt", "w") as file:
        file.write(text)
    with open("zad3.txt", "r") as file:
        encrypted = caesar(file.read(), 3)
    with open("zad3_encrypted.txt", "w") as file:
        file.write(encrypted)

    with open("zad4.txt", "w") as file:
        file.write(encrypted)
    with open("zad4.txt", "r") as file:
        decrypted = caesar(file.read(), -3)
    with open("zad4_decrypted.txt", "w") as file:
        file.write(decrypted)


def table_and_matrix():
    with open("zad5.txt", "w") as file:
        for a in range(1, 11):
            for b in range(1, 11):
                file.write(f"{a} x {b} = {a * b}\n")

    with open("zad6.txt", "w") as file:
        for row in range(10):
            for column in range(10):
                file.write(f"{1 if row == column else 0} ")
            file.write("\n")


if __name__ == "__main__":
    save_numbers()
    make_triangle_files(read_numbers())
    temperatures()
    text_tasks()
    table_and_matrix()
