import streamlit as st
import random
import time
import pyautogui

import os
os.environ['DISPLAY'] = ':0'

alphabets = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
			 "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
vowels = ["A","E","I","O","U"]



def create_buttons():
	row1 = st.beta_columns(13)
	row2 = st.beta_columns(13)
	dict_ = {}

	with open("attempted.txt","r") as attempted:
		attempted_words = list(set(attempted.read().split(",")))

	for i in range(13):
		if alphabets[i] in attempted_words:
			dict_[alphabets[i]]=row1[i].empty()
		else:
			dict_[alphabets[i]]=row1[i].empty()
			if dict_[alphabets[i]].button(alphabets[i]):
				next_word(alphabets[i])
				dict_[alphabets[i]].empty()
	for i in range(13,26):
		if alphabets[i] in attempted_words:
			dict_[alphabets[i]]=row2[i-13].empty()
		else:
			dict_[alphabets[i]]=row2[i-13].empty()
			if dict_[alphabets[i]].button(alphabets[i]):
				next_word(alphabets[i])
				dict_[alphabets[i]].empty()

def next_word(guessed_word):		
	with open("attempted.txt","a") as attempted:
		attempted.write(guessed_word)
		attempted.write(",")
		check_guess(guessed_word)
	pyautogui.hotkey('f5')

def check_guess(guessed_word):
	if guessed_word in vowels:
		return
	with open("movie_name.txt","r") as movie_name:
		movie = movie_name.read()
	with open("blank.txt","r") as blank:
		s = blank.read()
	with open("score.txt","r") as score_pointer:
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
		with open("blank.txt","w") as blank:
			blank.write(blank_str)
	with open("score.txt","w") as score_pointer:
		s = str(blank_spaces)+" "+str(lives)
		score_pointer.write(s)	


def main():
	st.title("Hangman")

	with open("movie_name.txt","r") as movie_name:
		movie =  movie_name.read()

	if movie == "":		
		placeholder = st.empty()
		movie_input = placeholder.text_input('Enter a Movie')
		movie = movie_input.upper()
		
		with open("movie_name.txt","w") as movie_name:
			movie_name.write(movie)
		s = ""
		blank_spaces = 0
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

		with open("blank.txt","w") as blank:
			blank.write(s)

		with open("score.txt","w") as score_pointer:
			s = str(blank_spaces) + " " + "7"
			score_pointer.write(s)


		startButton = st.empty()
		if startButton.button('Start'):
			
			placeholder.empty()
			startButton.empty() 
			placeholder.info("GOOD LUCK!")
			time.sleep(2)
			placeholder.empty()



			movie_row = st.beta_columns(max(len(movie),20))
			for i in range(len(s)):
				movie_row[i].write(s[i])


			create_buttons()
			if st.button('Play Again'):
				with open("attempted.txt", 'w+') as attempted:
					attempted.truncate(0)  
				with open("movie_name.txt", 'w+') as movie_name:
					movie_name.truncate(0)
				with open("blank.txt", 'w+') as blank:
					blank.truncate(0)
				pyautogui.hotkey('f5')

			pyautogui.hotkey('f5')
	else:

		with open("score.txt","r") as score_pointer:
			score =  score_pointer.read()
		blank_spaces,lives = [int(x) for x in score.split()]

		if  blank_spaces == 0:
			st.success("Hurray!!! you guessed the movie")
			st.info(movie)

			if st.button('Play Again'):
				with open("attempted.txt", 'w+') as attempted:
					attempted.truncate(0)  
				with open("movie_name.txt", 'w+') as movie_name:
					movie_name.truncate(0) 
				with open("blank.txt", 'w+') as blank:
					blank.truncate(0)
				with open("score.txt", 'w+') as score_pointer:
					score_pointer.truncate(0)
				pyautogui.hotkey('f5')


		elif lives == 0:
			st.warning("Better luck next Time")
			st.info("Movie was:\t"+movie)

			if st.button('Play Again'):
				with open("attempted.txt", 'w+') as attempted:
					attempted.truncate(0)  
				with open("movie_name.txt", 'w+') as movie_name:
					movie_name.truncate(0) 
				with open("blank.txt", 'w+') as blank:
					blank.truncate(0)
				with open("score.txt", 'w+') as score_pointer:
					score_pointer.truncate(0)
				pyautogui.hotkey('f5')



		else:
			if lives > 3:
				color = "green"
			else:
				color = "red"
			css = "<h4 style='text-align: right; color: "+color+";'>Lives Left: "+str(lives)+"</h4>"
			st.markdown(css, unsafe_allow_html=True)

			with open("blank.txt","r") as blank:
				s = blank.read()
			movie_row = st.beta_columns(max(len(movie),20))
			for i in range(len(s)):
				movie_row[i].write(s[i])


			create_buttons()
			if st.button('Play Again'):
				with open("attempted.txt", 'w+') as attempted:
					attempted.truncate(0)  
				with open("movie_name.txt", 'w+') as movie_name:
					movie_name.truncate(0) 
				with open("blank.txt", 'w+') as blank:
					blank.truncate(0)
				with open("score.txt", 'w+') as score_pointer:
					score_pointer.truncate(0)
				pyautogui.hotkey('f5')



if __name__ == "__main__":
	main()