import os
import time
import shutil
import pathlib
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askdirectory



def start_screen():

	all_widgets = root.grid_slaves()
	for widget in all_widgets:
		widget.destroy()

	label_text = """
Для того, чтобы начать, следует
выбрать директорию.
Нажмите "Продолжить".
"""
	label = Label(root, width=70, font=('Ubuntu', 15), text=label_text)
	btn_continue = Button(root, width=35, font=('Ubuntu', 15), text='Продолжить', command=directory_screen)
	label.grid(row=0, columnspan=2, sticky='ws')
	btn_continue.grid(row=1, columnspan=2, sticky='ew')


def directory_screen():
	global filename

	all_widgets = root.grid_slaves()
	for widget in all_widgets:
		widget.destroy()

	filename = filedialog.askopenfilename(title="Select a directory", filetypes = [("All Files",".*")])

	label = Label(root, width=70, font=('Ubuntu', 15), text=pathlib.Path(filename).resolve().parent)
	btn_continue = Button(root, width=35, font=('Ubuntu', 15), text='Продолжить', command=pattern_screen)
	btn_back = Button(root, width=35, font=('Ubuntu', 15), text='Назад', command=start_screen)
	
	label.grid(row=0, columnspan=2, sticky='ws')
	btn_continue.grid(row=1, columnspan=2, sticky='ew')
	btn_back.grid(row=2, columnspan=2, sticky='ew')

	filename = pathlib.Path(filename).resolve().parent


def pattern_screen():
	global enter_folder

	all_widgets = root.grid_slaves()
	for widget in all_widgets:
		widget.destroy()

	text = 'Введите какой-то текст, а мы за вас переименуем и пронумеруем файлы:'
	
	label_dir = Label(root, width=70, font=('Ubuntu', 15), text=text)
	enter_folder = Entry(root, width=70, font=('Ubuntu', 15))
	back_btn = Button(root, width=30, font=('Ubuntu', 15), text='Назад', command=directory_screen)
	startsort_btn = Button(root, width=30, font=('Ubuntu', 15), text='Далее', command=renaming_screen)

	label_dir.grid(row=0, columnspan=2, sticky='ew')
	enter_folder.grid(row=1, columnspan=2, sticky='ew')
	back_btn.grid(row=2, columnspan=2, sticky='ew')
	startsort_btn.grid(row=3, columnspan=2, sticky='ew')
	

def renaming_screen():
	global checked_list, pat

	pat = enter_folder.get()

	all_widgets = root.grid_slaves()
	for widget in all_widgets:
		widget.destroy()

	text = 'Список файлов в данной директории:'
	
	label_listing = Label(root, width=50, font=('Ubuntu', 15), text=text)
	label_listing.grid(row=0, columnspan=3)

	checked_list = []
	row = 0
	for i in [i for i in os.listdir(filename) if len(i.split('.')) > 1 and i.split('.')[0] != 'Renamer']:
		row += 1
		checked = IntVar()
		checked.set(0)


		lst_modified = str(time.ctime(os.stat(i)[-1]))

		# Упаковка checkbutton'ов
		label_file = Label(root, width=30, font=('Ubuntu', 15), text=i)
		label_time = Label(root, width=30, font=('Ubuntu', 15), text=lst_modified)
		check = Checkbutton(root, width=10, font=('Ubuntu', 15), variable=checked, relief='ridge')
		label_file.grid(row=row, column=0)
		label_time.grid(row=row, column=1)
		check.grid(row=row, column=2)

		checked_list.append([i, checked])

	clear_btn = Button(root, width=55, font=('Ubuntu', 15), text='Очистить', command=clear_checks)
	choose_btn = Button(root, width=55, font=('Ubuntu', 15), text='Выбрать все', command=select_checks)
	back = Button(root, width=15, font=('Ubuntu', 15), text='Назад', command=pattern_screen)
	cont = Button(root, width=15, font=('Ubuntu', 15), text='Переименовать!', command=func_x)

	clear_btn.grid(row=row+1, column=0, sticky='ew')
	choose_btn.grid(row=row+1, column=1, sticky='we')
	back.grid(row=row+2, columnspan=3, sticky='ew')
	cont.grid(row=row+3, columnspan=3, sticky='ew')


def func_x():
	# Проверка наличия хотя бы одной галочки
	zero_list = [i[1] for i in checked_list if i[1].get() == 0]

	if len(checked_list) == len(zero_list):
		messagebox.showinfo('Внимание!', 'Нужно выбрать хотя бы один файл')
	else:
		folder_question = messagebox.askyesno('Вопрос', 'Переименовать файлы?')
		if folder_question == True:
			# Очищаем окно

			all_widgets = root.grid_slaves()
			for widget in all_widgets:
				widget.destroy()

			number = 0
			for i in checked_list:
				if i[1].get() == 1:
					number += 1
					x = str(pat) + '_' + str(number) + '.' + str(i[0].split('.')[1])
					old_file = os.path.join(filename, i[0])
					new_file = os.path.join(filename, x)
					shutil.move(old_file, new_file)

			label = Label(root, text='Готово')
			label.grid(row=0, columnspan=2, sticky='ew')


def quit():
	root.destroy()


# Очистка checkbutton'ов
def clear_checks():
	for i in checked_list:
		i[1].set(0)
	root.update_idletasks() 


# Выбор всех checkbutton'ов
def select_checks():
	for i in checked_list:
		i[1].set(1)
	root.update_idletasks()


# Логика программы
def main():
	global root

	root = Tk()
	root.title('Renamer')

	start_screen()
	
	root.mainloop()


if __name__ == '__main__':
	main()
