import Pyro4

uri = input("Enter server URI: ")
calculator = Pyro4.Proxy(uri)
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
sum_result = calculator.add_numbers(a, b)
mul_result = calculator.multiply(a, b)
print("Addition result:", sum_result)
print("Multiplication result:", mul_result)
