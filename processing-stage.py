import sys, os, re

class WordDict:

	def __init__(self, corpusDirPath):

		self.counts = dict()
		self.corpusDirPath = corpusDirPath
		self.fileContents = '' #string
		self.cleanContents = '' #string
	
	def getFiles(self):

		'''Getting Files .. '''

		self.fileContents = ''

        	for filename in os.listdir(self.corpusDirPath):
                	f=open(os.path.join(self.corpusDirPath,filename), "r")
                	text =f.read()
                	self.fileContents = self.fileContents + ' ' + text


	def cleanFiles(self):

		'''Cleaning File Contents ..'''

		words = []
	        for word in self.fileContents.split():
        	        if not re.match('\s*<.*>\s*',word): #ignore tag
                	        word = re.sub('[^a-zA-Z\']',' ',word)
				word = word.strip()
                        	words.append(word)

        	self.cleanContents = ' '.join(words)
        	self.cleanContents = re.sub('\s+',' ',self.cleanContents)
		

	def processDict(self):

		'''Creating Dictionary ..'''
      
        	for word in self.cleanContents.split():
                	word = word.lower()
                	word = re.sub('^\'+','',word)
                	word =  re.sub('\'+$','',word)
			word = word.strip()
                	if word: #not empty string
                        	self.counts[word] = self.counts.get(word, 0) + 1 
					#.get allows you to specify a default value if key not exists

        def printDict(self):

		'''Printing Dictionary ..'''

                #sort dictionary by value, reverse order
                for key, value in sorted(self.counts.items(), key=lambda p:p[1], reverse = True):
                        print('{}\t{}'.format(key, value))
                    


def main():
	
	#''' Accessing Folder'''
        dirpath = str(sys.argv[1]) #sys.argv[0] is the name of the python program, sys.arg[1] is the directory path

	#dirpath = '/corpora/LDC/LDC02T31/nyt/2000/'

	fileContents = ''

	solution = WordDict(dirpath)
	solution.getFiles()
	solution.cleanFiles()
	solution.processDict()
	solution.printDict()
 
if __name__ == '__main__':
	main()


