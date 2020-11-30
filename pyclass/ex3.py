#Write a program to enter a number and find the reverse of the number
#   for eg : 1234 is input output should be 4321

n = int(input("enter a number"))
j = 0

while(n > 0):
    a = n % 10
    j = j * 10 + a
    n = n // 10

print(j)