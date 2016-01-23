# -*- coding: utf-8 -*- <----necessary for our special beyonce font

# Jessica Cherayil and Sheree Liu
# Final Project: Beyoncé Lyrics Quiz
# Phase 3

from Tkinter import *
import random

difficultyLevel = ''

class StartPage(Tk):
    def __init__(self): #create variables necessary for startpage
        Tk.__init__(self)
        self.b_app = None
        self.title('Beyoncé Game Startup Window')
        self.configure(bg='black')
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        '''creates image of beyonce's album cover, as well as three different 
        difficulty level buttons'''
        pic = PhotoImage(file='albumcover.gif') #displays beyoncé's album cover on the top of the startpage
        self.startImage = Label(self, image=pic,borderwidth=0)
        self.startImage.pic = pic
        self.startImage.grid(row=0,columnspan=3)
        #gives user option to take easy quiz, medium quiz, or hard quiz
        easyButton = Button(self,text = 'Start an EASY game', command = self.onEasyButtonClick)
        easyButton.grid(row=1,column=0, sticky = N+E+W+S)
        mediumButton =Button(self,text = 'Start a MEDIUM game', command = self.onMediumButtonClick)
        mediumButton.grid(row=1,column=1, sticky = N+E+W+S)
        hardButton =Button(self,text = 'Start a HARD game', command = self.onHardButtonClick)
        hardButton.grid(row=1,column=2, sticky = N+E+W+S)
        
    def onEasyButtonClick(self):
        '''opens easy quiz when the easy level option is chosen'''
        global difficultyLevel
        difficultyLevel = 'Easy'
        if self.b_app!=None: self.b_app.destroy() #destroy existing lyrics game
        self.b_app = BeyonceLyricsApp() #opens new window with trivia game
        self.b_app.mainloop()
        
    def onMediumButtonClick(self):
        '''opens medium quiz when the medium level option is chosen'''
        global difficultyLevel
        difficultyLevel = 'Medium'
        if self.b_app!=None: self.b_app.destroy() #destroy existing lyrics game
        self.b_app = BeyonceLyricsApp() #opens new window with trivia game
        self.b_app.mainloop()
    
    def onHardButtonClick(self):
        '''opens hard quiz when the hard level option is chosen'''
        global difficultyLevel
        difficultyLevel = 'Hard'
        if self.b_app!=None: self.b_app.destroy() #destroy existing lyrics game
        self.b_app = BeyonceLyricsApp() #opens new window with trivia game
        self.b_app.mainloop()


class QandA:
    def __init__(self, filename): 
        lines = open(filename).readlines()
        self.QandA_list = []     # A list of question/answer tuples read in from file
        for line in lines:  # Populate list of questions/answers with data from file
            splitLine = line.strip().split(';')  # Assumes semicolon-delimited file
            self.QandA_list.append((splitLine[0], splitLine[1])) #adds lyrics and song title to QandA_list

    def get_random_QandA_number(self):
        '''Every question/answer has a number associated with it, i.e., the index
        it occurs in the list. Return the number associated with a randomly
        chosen question/answer.'''
        return random.randint(0, len(self.QandA_list)-1)

    def getQuestion(self, number):
        '''Returns the question associated with the given number.'''
        return self.QandA_list[number][1] #returns lyrics for question

    def getAnswer(self, number):
        '''Returns the answer associated with the given number.'''
        return self.QandA_list[number][0] #returns song name for answer
               
class BeyonceLyricsApp(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        if difficultyLevel == 'Easy':
            self.QA = QandA('Easy.txt') #gets lyrics from easy text file
        elif difficultyLevel == 'Medium':
            self.QA = QandA('Medium.txt') #gets lyrics from medium text file
        elif difficultyLevel == 'Hard':
            self.QA = QandA('Hard.txt') #gets lyrics from hard text file
        self.title('Beyoncé Lyrics Game')
        self.configure(bg='black') #makes entire background of GUI black
        self.grid()
        self.totalNumberOfQuestions = 10  # Total number of lyrics
        self.numberOfAnswers = 4          # Number of song options
        self.currentQuestionNumber = 1    # Current question number (increments after each question)
        self.numberAnsweredCorrectly = 0  # Number of questions answered correctly
        self.alreadyUsedIndices = [] #list of indices of questions that have already been asked
        self.indexOfCurrentQuestion = self.QA.get_random_QandA_number()  # Number/index of current question
        self.alreadyUsedIndices.append(self.indexOfCurrentQuestion) #add to list to ensure that there arent any repeat questions
        self.createWidgets()
        

    def createWidgets(self):
        '''creates title of game, image of beyonce, question labels, answer labels,
        radiobuttons, status label, submit button, and quit button'''

        # Image and Title
        rand = random.randint(1,14)
        pic = PhotoImage(file='bey' + str(rand) + '.gif') #chooses random picture of beyonce from our folder
        self.imageLabel = Label(self, image=pic,borderwidth=0)
        self.imageLabel.pic = pic
        self.imageLabel.grid(row=0,column=1)
        titleLabel = Label(self, text='BEYONCÉ\nTrivia', bg='black',fg='pink', font='Steelfish 72')
        titleLabel.grid(row=0,column=0,sticky=N+E+W+S)

        # Question
        self.question = StringVar()
        questionLabel = Label(self, bg='black',fg='pink',font='Steelfish 24',textvariable=self.question)
        questionLabel.grid(rowspan=self.numberOfAnswers,column=0,sticky=E+W)
        self.setQuestion()  # Set text of question

        # Answers
        self.answerIndex = IntVar()  # Index of selected radiobutton
        self.answerTexts = []  # List of StringVars, one for each radiobutton. Each list element allows getting/setting the text of a radiobutton.
        for i in range(0, self.numberOfAnswers):
            self.answerTexts.append(StringVar())
        for i in range(0, self.numberOfAnswers):  # Create radiobuttons
            rb = Radiobutton(self,bg='pink',font='Steelfish 20',textvariable=self.answerTexts[i], variable=self.answerIndex, value=i)
            rb.grid(row=1+i, column=1, sticky=W)
        self.setAnswers()  # Set text of radiobuttons

        # Status Label
        self.results = StringVar()
        self.resultsLabel = Label(self,bg='black', fg='pink', font='Steelfish 24 italic', textvariable=self.results)
        self.resultsLabel.grid(row=1+self.numberOfAnswers,column=0)

        # Submit Button
        self.submitButton = Button(self, text='Submit', command=self.onSubmitButtonClick)
        self.submitButton.grid(row=2+self.numberOfAnswers,column=1)

        # Quit Button        
        quitButton = Button(self, text='Quit', command=self.onQuitButtonClick)
        quitButton.grid(row=2+self.numberOfAnswers,column=0,sticky=W)

    def setQuestion(self):
        '''displays current question number and total number of questions, displays 
        question 'what song is this lyric from?', and displays random lyric'''
        self.question.set('Question ' + str(self.currentQuestionNumber) + ' out of ' + str(self.totalNumberOfQuestions) + '.\n' + 'What song is this lyric from?' +'\n' +self.QA.getQuestion(self.indexOfCurrentQuestion))

    def setAnswers(self):
        '''Populates the answer radiobuttons in a random order 
        with the correct answer as well as random answers.'''
        self.answers = []  # List of possible answers.
        self.answers.append(self.QA.getAnswer(self.indexOfCurrentQuestion))  # Add correct answer to list
        while len(self.answers) != self.numberOfAnswers:  # Add random answers to list. Ensure each random answer is not already in list, i.e., no duplicates.
            index = self.QA.get_random_QandA_number()  # Get random number/index
            if self.QA.getAnswer(index) not in self.answers:  # Ensure random answer is not already in answer list
                self.answers.append(self.QA.getAnswer(index))  # Add random answer to list     
        random.shuffle(self.answers)  # Randomly shuffle answer list
        for i in range(0, len(self.answers)):  # Populate text of radiobuttons
            self.answerTexts[i].set(self.answers[i])
        
        
    def onSubmitButtonClick(self):
        '''when the submit button is clicked and the game is not yet over, checks
        if answer selected matches correct answer and updates results label
        accordingly. Changes to 'next' button'''
        if self.currentQuestionNumber <= 10: #if you havent answered all ten questions
            for i in range(0,self.numberOfAnswers): #range (0,4)
                if self.answerIndex.get() == i: #get the text at the selected radio button
                    if self.answers[i]==self.QA.getAnswer(self.indexOfCurrentQuestion): # if the answer is correct
                        self.results.set('Correct!') #updates results label to display that the user was correct
                        self.numberAnsweredCorrectly +=1 
                    else: #if the answer is wrong, updates results label with correct answer 
                        self.results.set('Incorrect: the correct answer is ' + self.QA.getAnswer(self.indexOfCurrentQuestion))
                    self.currentQuestionNumber += 1 #increase question number
                    self.submitButton.configure(text='Next',command=self.onNextButtonClick) #change to Next button
            
    def onNextButtonClick(self): #when it says next...
        '''when the next button is clicked and the game is not yet over, generates 
        a new random lyric and populates radiobuttons with a new set of possible
        answers'''
        if self.currentQuestionNumber==11: #if it's the last question
            self.results.set('Game over: you answered ' + str(self.numberAnsweredCorrectly) + ' out of 10 correctly.') #return # correct answers
            self.submitButton.configure(text='Next',state='disabled') #user can't continue after this point
        else : #if it isnt the last question    
            self.indexOfCurrentQuestion = self.QA.get_random_QandA_number() #generate a new question to be asked
            while self.indexOfCurrentQuestion in self.alreadyUsedIndices: #if it has already been asked...
                self.indexOfCurrentQuestion = self.QA.get_random_QandA_number() #generate a new question so there are no repeats
            self.alreadyUsedIndices.append(self.indexOfCurrentQuestion) #add to list once it has been asked
            self.setQuestion() #updates question number and gets new random lyric
            self.setAnswers() #gets new set of randomly chosen answer options
            self.results.set('') #erase the results from the last question 
            self.submitButton.configure(text='Submit',command=self.onSubmitButtonClick) #change back to Submit button
            rand2 = random.randint(1,14)
            beypic = PhotoImage(file='bey' + str(rand2) + '.gif') #changes current pic of beyonce to another randomly chosen pic of beyonce
            self.imageLabel.configure(image=beypic)
            self.imageLabel.image=beypic
            
    def onQuitButtonClick(self):
        '''when quit button is selected, exits the window'''
        self.destroy()

app = StartPage()
app.mainloop()
