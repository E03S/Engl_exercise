import spacy 
import random 
import pandas as pd
from nltk.tokenize import sent_tokenize,word_tokenize
import lemminflect 

nltk.download('punkt')

class EngExer:
    
    def __init__(self):
        self.__text = ''
        self.__nlp = spacy.load('en_core_web_sm')
        self.__dataframe = pd.DataFrame(columns = ['raw','type','task','options','answer'])
        self.__sent = []
        self.__position = 0
        
        
    def load_path(self, file_path):
        with open(file_path) as file:
            self.__text = file.read()
        self.__sent = sent_tokenize(self.__text)

    def load_text(self, text):
        self.__sent = sent_tokenize(text)
        
    def verb_replace(self, hard = False):
        doc = self.__nlp(self.__sent[self.__position])
        words = []
        pos = []
        options = []
        correct = []
        raw = []
        for w in doc:
            words.append(w.text)
            pos.append(w.pos_)
        if not 'VERB' in pos:
            #print(self.__position)
            self.__position+=1
            return None
        for i in range(len(pos)):
            if pos[i] == 'VERB':
                temp = []
                correct.append(words[i])
                temp.append(words[i])
                w = list( lemminflect.getAllInflections(lemminflect.getLemma(words[i], upos='VERB')[0], upos = "VERB").values() ) 
                for i in range(len(w)):
                    if w[i][0] not in temp:
                        temp.append(w[i][0])
                options.append(temp[:3])
                raw.append('___')
            else:
                raw.append(words[i])
        if hard == True:
            options = None
        dict = {'raw':[raw],'type':'verb selection', 'task':'Выберете правильную форму глагола','options':[options],'answer': [correct]}
        self.__position+=1
        return pd.DataFrame(dict) 
        
    def sent_dissection(self):
    #scale = {'A1': [1,6],'A2': [3, 9],}
        while True:
            line = self.__sent[self.__position]
            words = word_tokenize(line)
            words_rec = []
            for i in range(len(words)):
                if i == 0 and not (words[0].isalpha())  :
                    words_rec = [words[0]+words[1]]
                    continue
                if words[i].isalpha():
                    words_rec.append(words[i])
                else:
                    words_rec[-1] = words_rec[-1]+ words[i]
            random.shuffle(words_rec)
            if len(words) >1: #add dif
                dict = {'raw':line,'type':'sentence recombination', 'task':'Постройте предложение','options':[words_rec],'answer': [line.split()]}
                self.__position+=1
                return pd.DataFrame(dict)

    def mlt_sentences(self):
        sent_true = self.__sent[self.__position:(self.__position+5)]
        sent_rand = self.__sent[self.__position:(self.__position+5)]
        random.shuffle(sent_rand)
        #print(sent_rand)
        #print(sent_true)
        dict = {'raw': None,'type': 'Multiple sentence recombination', 'task': 'Выстройте предложения в правильном порядке','options': [sent_rand],'answer': [sent_true]}
        #print(dict)
        self.__position+=1
        return pd.DataFrame(dict)
        
    def conj_rem(self):
        doc = self.__nlp(self.__sent[self.__position])
        words = []
        pos = []
        raw = [self.__sent[self.__position-1]]
        correct = []
        for w in doc:
            words.append(w.text)
            pos.append(w.pos_)
        if not ('CONJ' in pos) and not ('CCONJ' in pos) and  not ('SCONJ' in pos):
            #print(self.__position)
            self.__position+=1
            return None
        #correct = self.__sent[self.__position]
        for i in range(len(words)):
            if pos[i] in ['CONJ','CCONJ','SCONJ']:
                raw.append('___')
                correct.append(words[i])
            else:
                raw.append(words[i])
        #print(self.__position)
        dict = {'raw':[raw],'type':'Conjunction writing', 'task':'Напишите правильное соединение','options':None,'answer': [correct]}
        self.__position+=1
        return pd.DataFrame(dict)

    def det_rem(self):
        doc = self.__nlp(self.__sent[self.__position])
        words = []
        pos = []
        raw = []
        correct = []
        for w in doc:
            words.append(w.text)
            pos.append(w.pos_)
        if not 'DET' in pos:
            #print(self.__position)
            self.__position+=1
            return None
        #correct = self.__sent[self.__position]
        for i in range(len(words)):
            if pos[i] == 'DET':
                raw.append('___')
                correct.append(words[i])
            else:
                raw.append(words[i])
        dict = {'raw':[raw],'type':'Det writing', 'task':'Напишите правильный артикль','options':None,'answer': [correct]}
        #print(self.__position)
        self.__position+=1
        return pd.DataFrame(dict)

    def set_params(self, verb_r,sent_d, mlt_sent, det_rem,conj_r):
        count = verb_r+sent_d+mlt_sent*5+conj_r
        self.__position = random.randint(0,int( (len(self.__sent)-count)/2 ) )
        df_final =pd.DataFrame()

        for i in range(verb_r): 
            while True:
                w = self.verb_replace()
                if type(w) == type(pd.DataFrame()):
                    df_final = pd.concat([df_final,w])
                    break
        for i in range(sent_d):
            df_final = pd.concat([df_final,self.sent_dissection()])
        for i in range(mlt_sent):
            df_final = pd.concat([df_final,self.mlt_sentences()])
        temp = self.__position
        for i in range(det_rem): 
            while True:
                w = self.det_rem()
                if type(w) == type(pd.DataFrame()):
                    df_final = pd.concat([df_final,w])
                    break
        self.__position = temp
        temp = self.__position
        for i in range(conj_r): 
            while True:
                w = self.conj_rem()
                if type(w) == type(pd.DataFrame()):
                    df_final = pd.concat([df_final,w])
                    break
        self.__position = temp
        
        return df_final
        
''' def noun_syn(self):
        doc = nlp(self.__sent[self.__position])
        words = []
        pos = []
        options = []
        correct = []
            for w in doc:
            words.append(w.text)
            pos.append(w.pos_)
        for i in range(len(pos)):
            if pos[i] == 'NOUN':
                temp = []
                correct.append(words[i])
                temp.append(words[i])
                w = list( lemminflect.getAllInflections(lemminflect.getLemma(words[i], upos='VERB')[0], upos = "VERB").values() ) 
                for i in range(len(w)):
                    if w[i][0] not in temp:
                        temp.append(w[i][0])
                options.append(temp)
        if hard == True:
            options = None
        dict = {'raw':line,'type':'verb selection', 'task':'Выберете правильную форму глагола','options':options,'answer': correct}
        self.__position+=1
        return pd.DataFrame(dict) 
    '''    

    



        
