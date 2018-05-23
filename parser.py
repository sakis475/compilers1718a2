from plex import *



class ParseError(Exception):
	""" A user defined exception class, to describe parse errors. """
	pass



class MyParser:
	""" A class encapsulating all parsing functionality
	for a particular grammar. """
	
	def create_scanner(self,fp):
		""" Creates a plex scanner for a particular grammar 
		to operate on file object fp. """

		# define some pattern constructs
		letter = Range("AZaz")
		digit  = Range("09")

		name  = letter + Rep(letter | digit)
		space = Rep1(Any(" \t\n"))

		notToken = Str("not")
		andToken = Str("and")
		orToken  = Str("or")
		equal 	 = Str("=")
		booleanValueTrue = NoCase(Str("true", "t", "1"))
		booleanValueFalse = NoCase(Str("false", "f", "0"))
		
		lexicon = Lexicon([
			(notToken, "foundNot"),
			(andToken, "foundAnd"),
			(orToken, "foundOr"),
			(equal, "equalSign"),
			(booleanValueTrue, "foundTrue"),
			(booleanValueFalse, "foundFalse"),
			(name, "Identifier"),
			(space, IGNORE)
		])


		# create and store the scanner object
		self.scanner = Scanner(lexicon,fp)
		
		# get initial lookahead
		self.la,self.val = self.next_token()


	def next_token(self):
		""" Returns tuple (next_token,matched-text). """
		
		return self.scanner.read()		

	
	def position(self):
		""" Utility function that returns position in text in case of errors.
		Here it simply returns the scanner position. """
		
		return self.scanner.position()
	

	def match(self,token):
		""" Consumes (matches with current lookahead) an expected token.
		Raises ParseError if anything else is found. Acquires new lookahead. """ 
		
		if self.la==token:
			self.la,self.val = self.next_token()
		else:
			raise ParseError("found {} instead of {}".format(self.la,token))
	
	
	def parse(self,fp):
		""" Creates scanner for input file object fp and calls the parse logic code. """
		
		# create the plex scanner for fp
		self.create_scanner(fp)
		
		# call parsing logic
		self.session()
	
			
	def session(self):
		""" Session  -> Facts Question | ( Session ) Session """
		if self.la == "Identifier":
			print("found identifier")
			self.match(self.la)
			self.equalSign()
		elif self.la == "print":
			print("found print keyword")
			self.match(self.la)
		
		else:
			raise ParseError("Expected identifier or print keyword")
	
	def identifier(self):
		if self.la == "Identifier":
			print("found Identifier")
			self.match(self.la)
			self.operation()
		elif self.la == "foundTrue" or self.la == "foundFalse":
			print("found boolean Value")
			self.match(self.la)
			self.operation()
		else:
			raise ParseError("Expected identifier or boolean value")

	def equalSign(self):
		if self.la == "equalSign":
			print("found Equal Sign")
			self.match(self.la)
			self.identifier()
		else:
			raise ParseError("Expected equal sign (=)")
	
	def operation(self):
		if self.la == "foundNot" or (self.la == "foundOr" or self.la == "foundAnd"):
			print("found operation")
			self.match(self.la)
			self.identifier()
		else:
			raise ParseError("Expected operation (not, and, or")
		
# the main part of prog

# create the parser object
parser = MyParser()

# open file for parsing
with open("test.txt","r") as fp:

	# parse file
	try:
		parser.parse(fp)
	except errors.PlexError:
		_,lineno,charno = parser.position()	
		print("Scanner Error: at line {} char {}".format(lineno,charno+1))
	except ParseError as perr:
		_,lineno,charno = parser.position()	
		print("Parser Error: {} at line {} char {}".format(perr,lineno,charno+1))

