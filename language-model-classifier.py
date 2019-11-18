import os
import re
import pandas as pd
import math
import codecs
import sys

corpuspath = str(sys.argv[1]) # '/dropbox/19-20/473/project5/language-models'

#corpus data
lang = []
unigrams = []
unigrams_count = []

#language models, each index specific to a language
lang_set = [] #list of languages
full_chars = [] #characters in language unigrams  
end_chars = [] #list of strings with characters at  beginning/end of unigrams
strip_chars = [] #list of strings with characters not at the beginning/end

#reading corpus files in directory
for filename in os.listdir(corpuspath):

	lang_set.append(filename[:3])
	full_char_lst = []
	end_char_lst = []

	#reading file
	with open(os.path.join(corpuspath,filename),'r') as fp:
		for cnt, line in enumerate(fp):

			#getting unigrams
			lst = line.split()
			lang.append(filename[:3])
			unigrams.append(lst[0])
		
			#forming the set for each language
			end_char_lst.extend([lst[0][0],lst[0][-1]])
			full_char_lst.extend([char for char in lst[0]])
			unigrams_count.append(lst[1])

        full_char_set = ''.join(list(set(full_char_lst)))
        full_chars.append(full_char_set)
	
	end_char_set = ''.join(list(set(end_char_lst)))
	end_chars.append(end_char_set)
	
	strip_chars.append(''.join(set(list(full_char_set)).difference(set(list(end_char_set))))) 


# Calling DataFrame constructor after zipping column lists
df = pd.DataFrame(list(zip(lang, unigrams, unigrams_count)),
               columns =['lang', 'word', 'word_count'])

df['word_count'] = df['word_count'].astype(int)

#method to label text a language based on bayes theorem 
def label_text(filepath):

	#reading file in utf-8 format to check in dataframe
	f1 = open(filepath)
	lines = f1.readlines()
	f1.close()

	#reading file in latin-1 format
	latin_lines = []
	f2 =  codecs.open(filepath,'r','latin-1')
	for line in f2:
        	latin_lines.append(line)
	f2.close()

	#lines in file
	for idx in range(len(lines)):

		print(latin_lines[idx].encode('utf-8'))
		line = lines[idx]

		#list of relative score measures of language models
		scores = []
 
		#for each language in set
		for i in range(len(lang_set)):

			#for relative measure 
			sum_val = 0

			lang = lang_set[i]
			
			#spitting sentence into label, text 
			sentence = line
			words = sentence.split()
			label = words[0]
			text = ' '.join(words[1:])
	
			#clean the text by including only characters in the language model
			text_chars = [c for c in text if c in full_chars[i]+' \s']
			text = ''.join(text_chars)
	
			words = text.split()
			#trim unseen characters from beginning and ending of words for comparison  
			words = [word.strip(strip_chars[i]) for word in words]
		
			#for each cleaned word in text
			for word in words:
				if any(df.word == word):
					val = df[(df.word == word) & (df.lang == lang)]
					if not val.empty: #if word is seen in language model 
						sum_val = sum_val + math.log(val.iloc[0]['word_count']) #take log(count) since relative measure
					#else if unseen, assume count = 1
			scores.append(sum_val)
			print('{}\t{}'.format(lang,sum_val))
	
		#predict the language with maxumum score
		predict_index = scores.index(max(scores)) 
		predict_lang = lang_set[predict_index]
		
		#print the result
		print('Result\t{}'.format(predict_lang))


filepath =  str(sys.argv[2]) # '/dropbox/19-20/473/project5/train.txt'

label_text(filepath)


