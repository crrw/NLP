from collections import Counter
import math

# Questions:
def questions():
    # Q1 How many word types are there in the training corpus? Please include the padding symbols and the unknown token
    trainList = open('replaced.txt', 'r', encoding = 'utf8').read().split()
    traincnt = Counter(trainList)
    print("Question 1:")
    print(len(traincnt))
    print()

    # Q2 How many word tokens are there in the training corpus?
    trainList = open('replaced.txt', 'r', encoding = 'utf8').read().split()
    print("Question 2:")
    print(len(trainList))
    print()

    # Q3  What percentage of word tokens and word types in the test corpus did not occur in training?
    trainList = open('trainpadded.txt', 'r', encoding = 'utf8').read().split()
    testList = open('final.txt', 'r', encoding = 'utf8').read().split()
    pre_unk_list = open('testpadded.txt', 'r', encoding = 'utf8').read().split()
    pre_unk_cnt = Counter(pre_unk_list)

    traincnt = Counter(trainList)
    testcnt = Counter(testList)

    print("Question 3:")
    print("word tokens: ", str(testcnt['<unk>']/len(testList)*100) + "%")
    print("word types: ", str((testcnt['<unk>']-1)/len(pre_unk_cnt)*100) + "%")
    print()

def training_questions():
    finalList = open('final.txt', 'r', encoding = 'utf8').read().split()
    trainList = open('replaced.txt', 'r', encoding = 'utf8').read().split()
    testList = open('testpadded.txt', 'r', encoding = 'utf8').read().split()
    finalcnt = Counter(finalList)
    traincnt = Counter(trainList)
    testcnt = Counter(testList)

    train_ls = []
    for i in range(0, len(trainList)-1):
        train_ls.append((trainList[i], trainList[i+1]))

    # dict for tuples of bigrams
    train_map = {}
    for i in train_ls:
        if i in train_map:
            train_map[i] += 1
        else:
            train_map[i] = 1


    test_ls = []
    for i in range(0, len(testList)-1):
        test_ls.append((testList[i], testList[i+1]))
    
    test_map = {}
    for i in test_ls:
        if i in test_map:
            test_map[i] += 1
        else:
            test_map[i] = 1
    
    cnt = 0
    tcnt = 0
    for i in test_map:
        if i not in train_map:
            cnt += 1
            tcnt += test_map[i]

    print("Question 4:")
    print("Percent of word tokens and word types in test corpus that did not occur in training: ", str(cnt/len(test_ls)*100) + "%")
    print("Percent of word tokens that do no appear in training bigrams: ", str((tcnt/len(test_ls))*100) + "%") # TODO
    print()

    print("Question 5:")
    message = "I look forward to hearing your reply ."
    message = "<s> " + message.lower() + " </s>"
    inp = message.split()

    ls = ["<unk>" if traincnt[i] == 0 else i for i in inp]

    ung = 0
    uni_tot = 0
    for i in inp:
        ung = math.log2(traincnt[i]/sum(traincnt.values()))
        uni_tot += ung
        if i != '<s>' and i != '</s>':
            print("[" + i + "]", str(":"), ung)
    print("unigram total: ", uni_tot)

    print()

# ----------------------------------------------------------------------------------------------------------------------------------
    message = "I look forward to hearing your reply ."
    message = '<s> ' + message.lower() + ' </s>'
    inp = message.split()
    inp = ["<unk>" if traincnt[i] == 0 else i for i in inp]

    bigram_ls  = list(zip(inp, inp[1:]))

    bigram_tot = 0
    for i in bigram_ls:
        if(i not in train_map):
            bigram_tot = 'undefined'
            print("log prob of:" + "["+ i[0] + " " + i[1] + "] : undefined")
        else:
            if bigram_tot != 'undefined':
                bigram_tot += math.log2(train_map[i]/traincnt[i[0]])
            print("log prob of bigram:" + "[" + i[0] + " " + i[1] + "] : " + str(math.log2(train_map[i]/traincnt[i[0]])))
    
    print("sum of all bigram probability: ", bigram_tot)
        
    print()
    
    addone_tot = 0
    addone_ls = zip(inp, inp[1:])

    for i in addone_ls:
        if i not in train_map:
            curr = math.log2((1)/(traincnt[i[0]]+len(traincnt)))
            addone_tot += curr
        else:
            curr = math.log2((train_map[i] + 1)/(traincnt[i[0]]+len(traincnt)))
            addone_tot += curr

        print("add one log prob: [" + i[0] + " " + i[1] + "] : "+ str(curr))
    
    print("sum of all add one log probability: ", addone_tot)
    print()

    print("Question 6:")
    unilog = 0
    addonelog = 0

    if unilog != 'undefined':
        unilog = uni_tot/len(inp)
    else:
        unilog = 'undefined'

    addonelog = addone_tot/len(inp)
    
    print("unigram perplexity: ", math.pow(2, -1 * unilog))
    print("bigram perplexity: undefined")
    print("add one log perplexity: ", math.pow(2, -1 * addonelog))

    print()
    print("Question 7:")
    uniprob = 0

    for i in finalList:
        uniprob += math.log2(finalcnt[i]/len(finalList))

    unians = 0
    unians = uniprob/len(finalList)

    print("preplexity of test under unigram: ", math.pow(2, -1*unians))
    print("preplexity of test under bigram: undefined")

    addoneprob = 0
    addonels = list(zip(finalList, finalList[:1]))
    for i in addonels:
        if i not in train_map:
            addoneprob += math.log2(1/(traincnt[i[0]] + len(traincnt)))
        else:
            addoneprob += math.log2(((train_map[i] + 1)/(traincnt[i[0]] + len(traincnt))))

    addoneans = addoneprob / len(traincnt)
    addoneans = math.pow(2, abs(addoneans))
    print("preplexity of test under add-one bigram:", addoneans)
    # print("add one preplexity: 1127.3038079500982")

questions()
training_questions()