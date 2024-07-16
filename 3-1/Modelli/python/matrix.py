import re
endLoop = 0
matrix = []
inverses = []

while endLoop < 2:
    row = input()
    if row == "":
        endLoop += 1
        if endLoop == 1:
            inverses.append(matrix[3])
            inverses.append(-matrix[1])
            inverses.append(-matrix[2])
            inverses.append(matrix[0])
        matrix.clear()
        continue
    endLoop = 0
    tmp = re.split("\s", row)
    matrix.append(int(tmp[0]))
    matrix.append(int(tmp[1]))

i = 0
while i < len(inverses):
    if i%4 == 0:
        print("Case " + str(int(i/4) + 1))
    print(str(inverses[i]) + " " + str(inverses[i+1]))
    i += 2
