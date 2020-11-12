Height = int(input("get height"))

while (Height <1 or Height > 8):
   print("please enter a height between 1 and 8")
   Height = int(input("get height"))

for i in range(1, Height + 1):
    print(" " * (Height - i), end="")
    print("#" * (i))
