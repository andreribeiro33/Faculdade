import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# Funções para o banco de dados
def conectar():
    conn = sqlite3.connect('imobiliaria.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS imoveis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT NOT NULL,
                        telefone TEXT NOT NULL,
                        endereco TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def inserir(nome, cpf, telefone, endereco):
    conn = sqlite3.connect('imobiliaria.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO imoveis (nome, cpf, telefone, endereco) VALUES (?, ?, ?, ?)', (nome, cpf, telefone, endereco))
    conn.commit()
    conn.close()
    listar()

def listar():
    conn = sqlite3.connect('imobiliaria.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM imoveis')
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close()

def atualizar(id, nome, cpf, telefone, endereco):
    conn = sqlite3.connect('imobiliaria.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE imoveis SET nome=?, cpf=?, telefone=?, endereco=? WHERE id=?', (nome, cpf, telefone, endereco, id))
    conn.commit()
    conn.close()
    listar()

def deletar(id):
    conn = sqlite3.connect('imobiliaria.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM imoveis WHERE id=?', (id,))
    conn.commit()
    conn.close()
    listar()

def selecionar(event):
    item = tree.selection()[0]
    valores = tree.item(item, 'values')
    entry_nome.delete(0, END)
    entry_nome.insert(END, valores[1])
    entry_cpf.delete(0, END)
    entry_cpf.insert(END, valores[2])
    entry_telefone.delete(0, END)
    entry_telefone.insert(END, valores[3])
    entry_endereco.delete(0, END)
    entry_endereco.insert(END, valores[4])
    entry_id.config(state='normal')
    entry_id.delete(0, END)
    entry_id.insert(END, valores[0])
    entry_id.config(state='disabled')

# Interface gráfica
root = Tk()
root.title('Cadastro de Imóveis')
root.geometry('1000x600')


frame = Frame(root)
frame.pack(pady=20)

tree = ttk.Treeview(frame, columns=('ID', 'Nome', 'CPF', 'Telefone', 'Endereço'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('CPF', text='CPF')
tree.heading('Telefone', text='Telefone')
tree.heading('Endereço', text='Endereço')
tree.pack()

tree.bind('<ButtonRelease-1>', selecionar)

frame_form = Frame(root)
frame_form.pack(pady=20)

Label(frame_form, text='ID').grid(row=0, column=0)
entry_id = Entry(frame_form, state='disabled')
entry_id.grid(row=0, column=1)

Label(frame_form, text='Nome').grid(row=1, column=0)
entry_nome = Entry(frame_form)
entry_nome.grid(row=1, column=1)

Label(frame_form, text='CPF').grid(row=2, column=0)
entry_cpf = Entry(frame_form)
entry_cpf.grid(row=2, column=1)

Label(frame_form, text='Telefone').grid(row=3, column=0)
entry_telefone = Entry(frame_form)
entry_telefone.grid(row=3, column=1)

Label(frame_form, text='Endereço').grid(row=4, column=0)
entry_endereco = Entry(frame_form)
entry_endereco.grid(row=4, column=1)

frame_buttons = Frame(root)
frame_buttons.pack(pady=20)

Button(frame_buttons, text='Inserir', command=lambda: inserir(entry_nome.get(), entry_cpf.get(), entry_telefone.get(), entry_endereco.get())).grid(row=0, column=0, padx=5)
Button(frame_buttons, text='Atualizar', command=lambda: atualizar(entry_id.get(), entry_nome.get(), entry_cpf.get(), entry_telefone.get(), entry_endereco.get())).grid(row=0, column=1, padx=5)
Button(frame_buttons, text='Deletar', command=lambda: deletar(entry_id.get())).grid(row=0, column=2, padx=5)

conectar()
listar()

root.mainloop()
