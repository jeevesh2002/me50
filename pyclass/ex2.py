#Write  a program  using while loop to enter a number and find the sum of the digits.
#    for eg ::  if 123 is given as input then the output should be 1+2+3 = 6
n = int(input("enter a number"))
s = 0
for i in str(n):
    s = s+int(i)

print(s)