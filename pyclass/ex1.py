#Write a program to enter the marks of student in three subjects.
#Then calculate the total and average and display the grade obtained by the student.
#If the student scores an aggregate greater than 75% then grade is distinction.
#if the aggregate is 60>= and <75 then grade is first division,
#if the aggregate is 50>= and <60, then grade is second division else considered to be failed.
S1 = int(input("enter marks of subject1 out of 100"))
S2 = int(input("enter marks of subject2 out of 100"))
S3 = int(input("emter marks of subject3 out of 100"))
avg = (S1+S2+S3)/3
print(avg)
if avg >= 75:
    print("grade is distinction")
elif avg<75 and avg>=60:
    print("grade is first division")
elif avg>=50 and avg<60:
    print("grade is second division")
else:
    print("fail")