# -*- coding: utf-8 -*-

# Imports
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string
import sys 
from nltk.corpus import wordnet as wn
 
# Reading stopwords from a text file including punctuations

stopwords = open('stop_words.txt', 'r').read().split()
stopwords.extend(string.punctuation)
stopwords.append('')
stopwords.remove("not")

#Inputs
user_sentence = sys.argv[1];
db_sentence = sys.argv[2];
z= sys.argv[3];
#z=z.replace(' ', '')
key=z.split(',');


#If a keyword is a stopword then remove it from stopword list
if(key):    
    key1=z.replace(' ',',')
    key2=key1.split(',')
    stopwords=[i for i in stopwords if i not in key2]

#Local Variables
flag=1
similarity_index=0
k=0
d=0
u=0

#Word list with apostrophe
contractions=["aren't","can't","couldn't","didn't","doesn't","don't","hadn't","hasn't","haven't","he'd","he'll","he's","I'd","I'll","I'm","I've","isn't","it's","let's","mustn't","shan't","she'd","she'll","she's","shouldn't","that's","there's","they'd","they'll","they're","they've","we'd","we're","we've","weren't","what'll","what're","what's","what've","where's","who'd","who'll","who're","who's","who've","won't","wouldn't","you'd","you'll","you're","you've"] 
original_words=["are not","can not","could not","did not","does not","do not","had not","has not","have not","he had","he will","he is","I had","I will","I am","I have","is not","it is","let us","must not","shall not","she would","she will","she is","should not","that is","there is","they would","they will","they are","they have","we would","we are","we have","were not","what will","what are","what is","what have","where is","who had","who will","who are","who is","who have","will not","would not","you would","you will","you are","you have"]


#Mapping function to map contractions to original word
def contraction_mapper(user_sentence):
    user_list=user_sentence.split(' ')
    for i in range(len(user_list)):
        if "'" in user_list[i]:
            for j in range(len(contractions)) :
                if contractions[j]==user_list[i]:
                    user_list[i]=original_words[j]       
    user_sentence=' '.join(user_list)
    return user_sentence         

#Parts of speech tagging
def pos_tagging(pos_tag):
    if pos_tag[1].startswith('J'):
        return (pos_tag[0], wn.ADJ)
    elif pos_tag[1].startswith('V'):
        return (pos_tag[0], wn.VERB)
    elif pos_tag[1].startswith('N'):
        return (pos_tag[0], wn.NOUN)
    elif pos_tag[1].startswith('R'):
        return (pos_tag[0], wn.ADV)
    else:
        return (pos_tag[0], wn.NOUN)

            
#Check similarity between 2 words 
def calc_similar(db_sentence,user_sentence):
    similar=[]
    s1=wn.synsets(db_sentence)
    s2=wn.synsets(user_sentence)
  
    for i in s1:
        for j in s2:
            if (i.path_similarity(j)):
                z=i.path_similarity(j)        
                z = "%.4f" % z
                similar.append(z)
    
    if(similar):
        max_similarity=max(similar)
        return max_similarity
    

del_db_sentence=[]
del_user_sentence=[]

#Removing Contractions
user_sentence=contraction_mapper(user_sentence)

# Create Tokenizer 
tokenizer = nltk.tokenize.punkt.PunktWordTokenizer()

#Tokenizatiopn
tokens_db_sentence = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(db_sentence) \
                    if token.lower().strip(string.punctuation) not in stopwords]
tokens_user_sentence = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(user_sentence) \
                    if token.lower().strip(string.punctuation) not in stopwords]

key_prac=key[:]
key_prac1=key[:]
if(key):
    x='/'    
    temp=[]    
    user_sentence=user_sentence.lower();    
    db_sentence=db_sentence.lower(); 
    for i in range(len(key_prac1)):
        key_prac1[i]=key_prac1[i].lower();   
        check=0
        
        if(x in key_prac1[i]):
            check=1
            temp=key_prac1[i].split('/')
        
        if(check==1):
            for j in range(len(temp)):
                if(temp[j] in user_sentence):
                    key_prac.remove(key_prac1[i]);
                    temp1 =  [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(temp[j])]
                    tokens_user_sentence=[p for p in tokens_user_sentence if p not in temp1]
                    for k in range(len(temp)):
                        if(temp[k] in db_sentence):
                            temp2 = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(temp[k])]
                            tokens_db_sentence=[p for p in tokens_db_sentence if p not in temp2]
                            break;
                    break;
        
        if(check==0):        
            if (key_prac1[i] in user_sentence):
                key_prac.remove(key_prac1[i]);
    if(key_prac):
        k=0
    else:
        k=0.5   
	
                        
                       

#Create Lemmatizer
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

#Lemmatization
pos_db_sentence = map(pos_tagging, nltk.pos_tag(tokenizer.tokenize(db_sentence)))

pos_user_sentence = map(pos_tagging, nltk.pos_tag(tokenizer.tokenize(user_sentence)))


lemmae_db_sentence = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_db_sentence \
                    if (pos == wn.NOUN or pos == wn.VERB or pos == wn.ADV or pos == wn.ADJ) and token.lower().strip(string.punctuation) not in stopwords]
                    
lemmae_user_sentence = [lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_user_sentence \
                    if (pos == wn.NOUN or pos == wn.VERB or pos == wn.ADV or pos == wn.ADJ) and token.lower().strip(string.punctuation) not in stopwords]
                    

#declaring lists->
exact=[]
partial=[]
exact_key_match=[]

#Checking frequency of not
for i in range(len(tokens_db_sentence)):
    if(tokens_db_sentence[i] == "not"):
        d=d+1

for i in range(len(tokens_user_sentence)):
    if(tokens_user_sentence[i] == "not"):
        u=u+1  

#If frequency of not does not match then exit
if(d != u):
    flag=0

#Finding exact match between 2 token lists
exact=list(set(tokens_db_sentence) & set(tokens_user_sentence))


#removing exact matches from the token lists
#For token list a--> 
tokens_db_sentence=[i for i in tokens_db_sentence if i not in exact]

#For token list b-->
tokens_user_sentence=[i for i in tokens_user_sentence if i not in exact]


#initializing lists to store values which need to be deleted after similarity 
del_db_sentence=[]
del_user_sentence=[]
#checking word pairs which are going to be compared by the similarity function

for i in range(len(tokens_db_sentence)):
    for j in range(len(tokens_user_sentence)):
        similar_index=calc_similar(tokens_db_sentence[i],tokens_user_sentence[j])
        if(similar_index):        
            if float(similar_index) >= 0.35:
                partial.append(tokens_user_sentence[j])
                del_db_sentence.append(tokens_db_sentence[i])
                del_user_sentence.append(tokens_user_sentence[j])                
##removing similar matches from the token lists
tokens_db_sentence=[i for i in tokens_db_sentence if i not in del_db_sentence]
tokens_user_sentence=[j for j in tokens_user_sentence if j not in del_user_sentence]


#Checking for not in remaining tokens
tokens_not= tokens_db_sentence + tokens_user_sentence
if(tokens_not):
    for i in range(len(tokens_not)):
        if tokens_not[i] == 'not':
            flag=0

#jaccard Similarity
if flag==1:  
    numerator= float(len(exact)+len(partial))
    denominator=float(numerator+(len(tokens_db_sentence)+len(tokens_user_sentence))/2)
    similarity_index=numerator/denominator
    if (key):
        similarity_index=k+(similarity_index/2)
print similarity_index

