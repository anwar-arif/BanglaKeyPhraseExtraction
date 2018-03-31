import math
import Helper

fin = open('in.txt' , 'r' , encoding='utf-8')
dari_coma = open('dari-coma.txt' , 'r' , encoding='utf-8')
fstp = open('stopwords.txt' , 'r' , encoding='utf-8')
fout = open('out.txt' , 'w' , encoding='utf-8')

DariComa = []
WordList = []
Sentence = []
StopWords = []
Ngrams = []

Dari = "।"
Coma = ","

for word in dari_coma.read().split() :
    DariComa.append(word)
for word in fstp.read().split() :
    word = word.lstrip()
    word = word.rstrip()
    StopWords.append(word)

dari_coma.close()
fstp.close()

# Seperating each sentences
Sentence = Helper.SeperateSentence(fin)

# for i in range(len(Sentence)) :
#     print("{}\n".format(Sentence[i]))

# Now Ngram Code begins
# this will store ngrams in the list named Ngrams

Ngrams = Helper.MakeNgrams(7 , Sentence , StopWords , fout )

# ------------------------------------------------------------
# Ready noun , verb , adj list
fnoun = open('G:/semester/semester 3-2/project 300/POS_Separator/noun.txt' , 'r' , encoding='utf-8')
fverb = open('G:/semester/semester 3-2/project 300/POS_Separator/verb.txt' , 'r' , encoding='utf-8')
fadj = open('G:/semester/semester 3-2/project 300/POS_Separator/adjective.txt' , 'r' , encoding='utf-8')

NounList = []
VerbList = []
AdjList = []

for word in fnoun.read().split() :
    NounList.append(word)
for word in fverb.read().split() :
    VerbList.append(word)
for word in fadj.read().split() :
    AdjList.append(word)

# ------------------------------------
# deleting invalid Ngrams
# Store valid Ngrams to FinalNgrams
# Removing the Ngrams whose first word is not noun/adj and does not contain a verb at last
# Removing the Ngrams which start/end with a stopword

FinalNgrams = []
FinalNgrams = Helper.ValidNgrams( NounList , AdjList , VerbList , StopWords , Ngrams )

# for i in range(len(FinalNgrams)) :
    # print("-->{}\n".format(FinalNgrams[i]))

# print("Total {}\n".format(len(FinalNgrams)))

fngrams = open('FinalNgrams.txt' , 'w' , encoding='utf-8')
for word in FinalNgrams :
    fngrams.write("{}\n".format(word))

# ----------IMPORTANT--------
# ----------IMPORTANT--------
# ----------IMPORTANT--------
# ------comment the following code , Run , then run Java code for stemming then commment out and run to get final result
#
# ---------------------------------------------------
# Assign score to Ngrams according to their frequency
# in stemmed Ngrams
#
# Calculating First occurence
FirstOccur = []
FirstOccur = Helper.CalculateFirstOccurence( FinalNgrams , Sentence )

# Mapping stemmed Ngrams to real Ngrams

fstmd = open('StemmedNgrams.txt' , 'r' , encoding='utf-8')
StemmedNgrams = []
StemmedNgrams = Helper.GetStemmedNgrams( fstmd )
fstmd.close()

# store PhraseFrequency
PhraseFreq = []
for word in StemmedNgrams :
    PhraseFreq.append(StemmedNgrams.count(word))

# Soore SubPhraseFreq
SubPhraseFreq = []
for word in StemmedNgrams :
    cnt = 0
    for w in StemmedNgrams :
        if w.find(word) != -1 :
            cnt = cnt + 1
    SubPhraseFreq.append(cnt)

# Finding Maximum phrase length
MaxPhraseLen = 0
ans = ""
for word in StemmedNgrams :
    if len(word)>MaxPhraseLen :
        MaxPhraseLen = max( MaxPhraseLen , len(word))
        ans = word

# Calculating scores for each Ngrams
Scores = []
for i in range(len(FinalNgrams)) :
    SP = (1.0/math.sqrt(FirstOccur[i]))
    PF = PhraseFreq[i]
    PL = len(StemmedNgrams[i])
    M = MaxPhraseLen
    E = ( 1.0 + PL*PL ) / ( M*M )
    LC = SubPhraseFreq[i]
    SF = math.sqrt( ( math.pow( (1.0 + PF*PF ) , E ) + LC ) )
    score = SP + SF
    Scores.append( score )

MaxScore = 0
for i in range(len(Scores)) :
    if MaxScore < Scores[i] :
        MaxScore = Scores[i]

for i in range(len(Scores)) :
    Scores[i] = Scores[i] / MaxScore


fextr = open('ExtractedKeyPhrase.txt' , 'w' , encoding='utf-8')
for i in range(len(FinalNgrams)) :
    fextr.write("{}   {}\n".format(FinalNgrams[i] , Scores[i]))

# Sort the result according to score
from collections import namedtuple
from operator import attrgetter

myType = namedtuple("myType", "KeyPhrase , score")
ResultArray = []
TempArray = []
for i in range(len(FinalNgrams)) :
    sample = myType(KeyPhrase=FinalNgrams[i] , score=Scores[i])
    TempArray.append(sample)
ResultArray = sorted(TempArray, key = attrgetter("score") , reverse=True)


for i in range(len(ResultArray)) :
    fextr.write("{}   {}\n".format( ResultArray[i].KeyPhrase , ResultArray[i].score ) )

threshold = Helper.GetThreshold(ResultArray)

# Store the selected FinalKeyPhrase
f = open('FinalKeyPhrase.txt' , 'w' , encoding='utf-8')
threshold = 0.0
temp = []
for i in range(len(ResultArray)) :
    if ResultArray[i].score >= threshold :
        # f.write("{}\n".format(ResultArray[i].KeyPhrase))
        temp.append(ResultArray[i].KeyPhrase)

for i in range( min(len(temp) , 10)):
    f.write("{}\n".format(temp[i]))

match = 0
fexpected = open('ExpectedKeyPhrase.txt' , 'r' , encoding='utf-8')
ExpectedPhrase = []
for Phrase in fexpected.readlines():
    Phrase.strip()
    ExpectedPhrase.append(Phrase)

for i in range(len(ExpectedPhrase)) :
    for j in range(len(temp)) :
        if temp[j] in ExpectedPhrase[i] :
            match = match + 1
            break

accuracy = ( match / len(temp) )

print("Noun = {} Verb = {} Adj = {}\n".format(len(NounList) , len(VerbList) , len(AdjList)))
