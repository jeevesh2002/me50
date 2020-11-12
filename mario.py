n = int(input("get pyramid height"))
while (n<1 or n>8):
   print("please enter a height between 1 and 8")
   n = int(input("get pyramid height"))
for i in range(1, n+1):
    print(" " * (n-i), end="")
    print("#" * (i))
