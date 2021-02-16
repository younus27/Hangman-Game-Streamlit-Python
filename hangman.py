# Import libraries
import streamlit as st
import random
import time
import pyautogui

alphabets = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
			 "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
vowels    = ["A","E","I","O","U"]



def create_buttons():

	"""
	Create Buttons for alphabets that are not attempted yet.
	params : none
	return : none
	"""

	# Create a dictionary to accomodate place holders for alphabets
	dict_ = {}

	
	# First row consisiting of alphabets A-M
	row1 = st.beta_columns(13)

	with open("./temp/attempted.txt","r") as attempted:
		attempted_words = list(set(attempted.read().split(",")))

	# If alphabet already attemted -> empty placeholder
	# Else place actual button
	for i in range(13):
		if alphabets[i] in attempted_words:
			dict_[alphabets[i]]=row1[i].empty()
		else:
			dict_[alphabets[i]]=row1[i].empty()
			if dict_[alphabets[i]].button(alphabets[i]):
				next_word(alphabets[i])
				dict_[alphabets[i]].empty()


	# First row consisiting of alphabets A-M
	row2 = st.beta_columns(13)
	
	for i in range(13,26):
		if alphabets[i] in attempted_words:
			dict_[alphabets[i]]=row2[i-13].empty()
		else:
			dict_[alphabets[i]]=row2[i-13].empty()
			if dict_[alphabets[i]].button(alphabets[i]):
				next_word(alphabets[i])
				dict_[alphabets[i]].empty()


def next_word(guessed_word):

	"""
	Store attempted alphabet to ./temp/attempted.txt
	params : guessed_word - str
	return : none
	"""

	with open("./temp/attempted.txt","a") as attempted:
		attempted.write(guessed_word)
		attempted.write(",")
		check_guess(guessed_word)
	pyautogui.hotkey('f5')

def check_guess(guessed_word):

	"""
	Check if attempted alphabet is correct or not

	IF guessed_word, reduce total number of blank space
	update ./temp/blank.txt [used to store blank words eg. _ A _ _ _    _ O _ _ E _]

	ELSE, Decrease the number of Lives 
	update the ./temp/score.txt [used to store no of blanks and lives left ]

	params : guessed_word - str
	return : none
	
	"""

	if guessed_word in vowels:
		return
	with open("./temp/movie_name.txt","r") as movie_name:
		movie = movie_name.read()
	with open("./temp/blank.txt","r") as blank:
		s = blank.read()
	with open("./temp/score.txt","r") as score_pointer:
		score =  score_pointer.read()
	blank_spaces,lives = [int(x) for x in score.split()]

	blank_str = ""
	count = 0
	for i in range(len(movie)):
		if movie[i]== guessed_word:
			blank_str+= movie[i]
			count+=1
		else:
			blank_str+= s[i]
	if blank_str == s:
		lives-=1
	else:
		blank_spaces -= count
		with open("./temp/blank.txt","w") as blank:
			blank.write(blank_str)
	with open("./temp/score.txt","w") as score_pointer:
		s = str(blank_spaces)+" "+str(lives)
		score_pointer.write(s)	


def main():

	st.title("Hangman")

	#Check if ./temp/movie_name.txt is empty 
	with open("./temp/movie_name.txt","r") as movie_name:
		movie =  movie_name.read()

	if movie == "":		

		# If ./temp/movie_name.txt is empty, get movie from user 
		placeholder = st.empty()
		movie_input = placeholder.text_input('Enter a Movie')
		movie = movie_input.upper()
		
		with open("./temp/movie_name.txt","w") as movie_name:
			movie_name.write(movie)



		#Generate blanks for given movie and store in ./temp/blank.txt
		s = ""
		blank_spaces = 0 #set a counter for number of blank spaces
		for i in range(len(movie)):
			if movie[i]==" ":
				s+=" "
				continue
			if movie[i] in vowels:
				s+= movie[i]
				continue
			else:
				s+="_"
				blank_spaces+=1

		with open("./temp/blank.txt","w") as blank:
			blank.write(s)



		#Initialize ./temp/score.txt
		#Set number of blank spaces as blank_spaces
		#Set number of lives to 7
		with open("./temp/score.txt","w") as score_pointer:
			s = str(blank_spaces) + " " + "7"
			score_pointer.write(s)


		startButton = st.empty()
		if startButton.button('Start'):
			
			placeholder.empty()
			startButton.empty() 
			placeholder.info("GOOD LUCK!")
			time.sleep(2)
			placeholder.empty()

			#Refresh the page to start the game
			pyautogui.hotkey('f5')


	# If ./temp/movie_name.txt is NOT empty 
	else:

		# Check ./temp/score.txt File
		with open("./temp/score.txt","r") as score_pointer:
			score =  score_pointer.read()
		blank_spaces,lives = [int(x) for x in score.split()]

		# If no blank_spaces are left - You WON !
		if  blank_spaces == 0:
			st.success("Hurray!!! you guessed the movie")
			st.info(movie)

		# If no lives are left - GAME OVER ... 
		elif lives == 0:
			st.warning("Better luck next Time")
			st.info("Movie was:\t"+movie)



		# If the game is still On
		else:
			# Display the Lives Left
			if lives > 3:
				color = "green"
			else:
				color = "red"
			css = "<h4 style='text-align: right; color: "+color+";'>Lives Left: "+str(lives)+"</h4>"
			st.markdown(css, unsafe_allow_html=True)


			# Display the Blank Guessed Word so far
			with open("./temp/blank.txt","r") as blank:
				s = blank.read()

			movie_row = st.beta_columns(max(len(movie),20))
			for i in range(len(s)):
				movie_row[i].write(s[i])

			# Create Remaining buttons
			create_buttons()

		# Reset the game
		if st.button('Play Again'):
			with open("./temp/attempted.txt", 'w+') as attempted:
				attempted.truncate(0)  
			with open("./temp/movie_name.txt", 'w+') as movie_name:
				movie_name.truncate(0) 
			with open("./temp/blank.txt", 'w+') as blank:
				blank.truncate(0)
			with open("./temp/score.txt", 'w+') as score_pointer:
				score_pointer.truncate(0)
			pyautogui.hotkey('f5')



if __name__ == "__main__":
	main()