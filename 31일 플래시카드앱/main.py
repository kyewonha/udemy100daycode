BACKGROUND_COLOR = "#B1DDC6"
Font_setting= ("Ariel", 40, 'italic')
Answer_font_Setting = ("Ariel", 60, 'bold')
current_card={}

import pandas as pd
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import random
import os

#take data and make flash card




try:
    learn_csv = pd.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data= pd.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn= learn_csv.to_dict(orient='records')


def next_card():
    global current_card
    global flip_timer #변수 설정이유: 카드를 계속 넘겨도 처음의 3초가 지나면 flipcard가 실행되서
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(word_label1, text='French', fill='black')
    canvas.itemconfig(word_label2, text= current_card['French'], fill='black')
    canvas.itemconfig(front_img, image= background_photo)
    flip_timer= window.after(3000, flip_card)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data= pd.DataFrame(to_learn)
    data.to_csv('./data/words_to_learn.csv', index=False)
    next_card()


def flip_card():
    canvas.itemconfig(word_label1, text="English", fill='white')
    canvas.itemconfig(word_label2, text= current_card['English'], fill='white')
    canvas.itemconfig(front_img, image= background_ch_photo)

#--ui---------
window =Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer= window.after(3000, flip_card)

canvas = Canvas(width=800, height= 540, highlightthickness=0, bg= BACKGROUND_COLOR)
canvas.pack()

background_ch = Image.open('./images/card_back.png')
background_ch_photo = ImageTk.PhotoImage(background_ch)
background = Image.open('./images/card_front.png')
background_photo = ImageTk.PhotoImage(background)
front_img= canvas.create_image(400,270,image= background_photo)
canvas.grid(column=0, row=0 ,columnspan=2)
word_label1=canvas.create_text(400, 150,text="" , font= Font_setting,anchor='center' )
word_label2=canvas.create_text(400, 263,text="" , font= Answer_font_Setting, anchor='center')

x_pic = Image.open('./images/wrong.png')
x_photo = ImageTk.PhotoImage(x_pic)
x_mark= Button(window, image= x_photo, highlightthickness=0, borderwidth=0, command=next_card)
x_mark.grid(row=1, column=0)

v_pic = Image.open('./images/right.png')
v_photo = ImageTk.PhotoImage(v_pic)
v_mark= Button(window, image= v_photo, highlightthickness=0, borderwidth=0, command=is_known)
v_mark.grid(row=1, column=1)

next_card()

window.mainloop()