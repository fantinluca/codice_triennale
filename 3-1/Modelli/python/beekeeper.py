maxVowelCouples = 0
curVowelCouples = 0
curFavWord = ""
favWords = []
vowels = ['a','e','i','o','u']
wordsNum = int(input())
while wordsNum != 0:
    curFavWord = ""
    maxVowelCouples = 0
    for i in range(wordsNum):
        curVowelCouples = 0
        word = input()
        for index in range(1, len(word)):
            if word[index] == word[index-1] and word[index-1] in vowels:
                curVowelCouples += 1
        if curVowelCouples > maxVowelCouples:
            maxVowelCouples = curVowelCouples
            curFavWord = word
    favWords.append(curFavWord)
    wordsNum = int(input())

for word in favWords:
    print(word)
