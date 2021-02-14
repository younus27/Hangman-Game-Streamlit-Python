# Hangman-Game-Streamlit-Python

Hangman is a paper and pencil guessing game where one player thinks of a word, phrase or sentence
in this case a MOVIE name.. and the other tries to guess it by suggesting letters within a certain number of guesses

Here we are creating hangman with Streamlit python library used for building web applications.
https://www.streamlit.io/

Here the player needs to guess the words in 7 tries.
Vowels in the given word are arleady Displayed
for eg - movie > "HARRY POTTER"
    displayed> " _ A _ _ _    _ O _ _ E _ R "
All the Alphebets will be displayed, once the player clicks a particular letter, it disappears
if the gussed Letter is correct - "_" will be replaced by that letter
and if it is incorrect, the user looses a life and after & lives the game is lost and the movie name will be displayed
