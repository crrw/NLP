from collections import Counter

# add padding symbols <s>, </s>
def pad(name):
    newFileName = name[:-4] + "padded.txt"
    with open(name, 'r', encoding='utf8') as train, open(newFileName, 'w+', encoding='utf8') as pad:
        for line in train:
            pad.write(" <s> " + line.rstrip("\n").lower() + " </s> ")


# if freq of a word is < 1, replaced with unk 
def replace(train):
    trainList = open(train, 'r', encoding = 'utf8').read().split()
    traincnt = Counter(trainList)

    with open('trainpadded.txt', 'r', encoding = 'utf8') as train, open('replaced.txt', 'w+', encoding = 'utf8') as replaced:
        for line in train.readlines():
            for word in line.split():
                if(traincnt[word] == 1):
                    # print(word)
                    replaced.write(" <unk> ")
                else:
                    replaced.write(word + ' ')

    remove('replaced.txt', traincnt) 

# use counter in remove unseen words in the training set
def remove(name, hm):
    testList = open('testpadded.txt', 'r', encoding = 'utf8').read().split()
    with open('final.txt', 'w+', encoding = 'utf8') as f:
        for i in testList:
            if i not in hm:
                f.write("<unk> ")
            else:
                f.write(i + " ")

    finalList = open('final.txt', 'r', encoding = 'utf8').read().split()
    c = Counter(finalList)
    print(c["<unk>"])
    print(len(c))

pad("train.txt")
pad("test.txt")
replace("trainpadded.txt")