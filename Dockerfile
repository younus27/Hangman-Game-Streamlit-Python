FROM python:3.7

WORKDIR /app

COPY . .

RUN pip install pyautogui
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["hangman.py"]