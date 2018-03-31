
# Takes file as input returns a list
# This function removes ( | , ! - ) etc and seperate each sentences
def SeperateSentence(fin) :
    Sentence = []
    first = ""
    str = ""
    cnt = 0
    taken = 0
    Dari = "।"
    Coma = ","
    FirstWord = 1
    for word in fin.read().split():
        if FirstWord == 1:
            tmp = ""
            for i in range(1, len(word)):
                tmp += word[i]
            word = tmp
            FirstWord = 0
        word = word.lstrip()
        word = word.rstrip(' ')
        word = word.rstrip(',')
        word = word.rstrip('!')
        word = word.rstrip('-')
        if taken == 0:
            first = word
            taken = 1
        if word == Coma:
            continue
        if word == " – ":
            continue
        if word == "–" :
            continue
        if word.__contains__(Dari) :
            str += " "
            word = word.rstrip('।')
            str += word
            str.rstrip('।')
            Sentence.append(str)
            cnt = 0
            str = ""
            continue
        if word[(len(word) - 1)] == '।':
            word = word.rstrip('।')
        if cnt > 0:
            str += " "
        str += word
        cnt = cnt + 1
        # print("-->{}\n".format(word))

    if str.__len__() > 0:
        Sentence.append(str)
    fin.close()
    return Sentence


# This function takes MaxGram(int) Sentence(list) StopWords(list) and output file
# It makes Ngrams from each sentence
def MakeNgrams( MaxGram , Sentence , StopWords , fout ) :
    Ngrams = []
    for sen in Sentence:
        words = sen.split()
        for g in range(3, MaxGram):
            for i in range(0, len(words)):
                cnt = 0
                okay = 1
                str = ""
                for j in range(i, len(words)):
                    word = words[j]
                    if cnt > 0:
                        str += " "
                    str += word
                    # if word in StopWords:
                    #     okay = 0
                    #     break
                    cnt = cnt + 1
                    if cnt == g:
                        break
                if okay == 1 and cnt == g:
                    fout.write("{}\n".format(str))
                    Ngrams.append(str)

    return Ngrams


# This function returns valid Ngrams
def ValidNgrams(NounList , AdjList , VerbList , StopWords , Ngrams) :
    FinalNgrams = []
    for i in range(len(Ngrams)):
        tmp = Ngrams[i]
        words = tmp.split()
        first = words[0]
        last = words[len(words) - 1]
        okay = 1
        noun = 0
        adj = 0
        verb = 0
        stp = 0
        for j in range(len(NounList)):
            if NounList[j].find(first) != -1:
                noun = 1
                break
        for j in range(len(AdjList)):
            if AdjList[j].find(first) != -1:
                adj = 1
                break
        for j in range(len(VerbList)):
            if VerbList[j].find(first) != -1:
                verb = 1
                break
        for j in range(len(VerbList)):
            if VerbList[j].find(last) != -1:
                verb = 1
                break
        for j in range(len(StopWords)):
            if StopWords[j].find(first) != -1:
                stp = 1
                break
            if StopWords[j].find(last) != -1:
                stp = 1
                break
        if noun == 0 and adj == 0 :
            okay = 0
        if verb == 1 :
            okay = 0
        if stp==1 :
            okay = 0
        if okay == 1:
            FinalNgrams.append(Ngrams[i])

    return FinalNgrams


# This function returns a list with first occurence in sentence for each Ngrams
def CalculateFirstOccurence(FinalNgrams , Sentence ) :
    FirstOccur = []
    for i in range(len(FinalNgrams)):
        for j in range(len(Sentence)):
            if Sentence[j].find(FinalNgrams[i]) != -1:
                FirstOccur.append(j + 1)
                break
    return FirstOccur


def GetStemmedNgrams(fstmd) :
    StemmedNgrams = []
    str = ""
    cnt = 0
    for word in fstmd.read().split():
        # print(word)
        if word == "#":
            StemmedNgrams.append(str)
            str = ""
            cnt = 0
            continue
        if cnt > 0:
            str += " "
        str += word
        cnt = cnt + 1

    return StemmedNgrams

def GetThreshold( ResultArray ) :
    fexpected = open('ExpectedKeyPhrase.txt' , 'r' , encoding='utf-8')
    ExpectedPhrase = []
    threshold = 0
    mx = 0
    temp = []
    for Phrase in fexpected.readlines():
        Phrase.strip()
        ExpectedPhrase.append( Phrase )
        # print("Expected->{}\n".format(Phrase))
    sz = len(ExpectedPhrase)
    i = 0.0
    for ii in range(0 , 100000) :
        tot = 0
        match = 0
        for j in range(len(ResultArray)) :
            if ResultArray[j].score > i :
                temp.append( ResultArray[j].KeyPhrase )
                tot = tot + 1
                # if ExpectedPhrase.__contains__(ResultArray[j].KeyPhrase) :
                if ResultArray[j].KeyPhrase in str(ExpectedPhrase) :
                    match = match + 1
        # for j in range(len(ExpectedPhrase)) :
        #     if temp.__contains__(ExpectedPhrase[j]) :
        #         match = match + 1

        accuracy = 0
        if tot > 0 :
            accuracy = ( match / tot )
        if accuracy > mx :
            mx = accuracy
            threshold = i
        i = i + 0.005
        if i >= 1.0 :
            break

    # if mx > 1.00 :
    #     mx = 1.00
    # print("{} {}\n".format(mx , threshold))
    return threshold