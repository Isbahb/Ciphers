import tkinter as tk

# -------ALPHABETS---------------------------------------------------------------------------
alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letter_index = dict(zip(alphabets, range(len(alphabets))))
index_letter = dict(zip(range(len(alphabets)), alphabets))


# -------SHIFT-CIPHER------------------------------------------------------------------------
def shift_encrypt(pt):
    et = ""
    key = int(input_key.get())
    pt = list(pt)
    for x in range(len(pt)):
        if " " in pt:
            pt.remove(" ")
    for i in pt:
        num = (letter_index[i] + key) % 26
        et += index_letter[num]
    return et


def shift_decrypt(et):
    pt = ""
    et = list(et)
    key = int(input_key.get())
    for x in range(len(et)):
        if " " in pt:
            et.remove(" ")
    for i in et:
        num = (letter_index[i] - key) % 26
        pt += index_letter[num]
    return pt


# -------VIGENERE-CIPHER---------------------------------------------------------------------
def v_encrypt(pt):
    et = ""
    pt = list(pt)
    key = input_key.get()
    key = key.upper()
    for x in range(len(pt)):
        if " " in pt:
            pt.remove(" ")
    msg = [pt[i:i + len(key)] for i in range(0, len(pt), len(key))]
    for part in msg:
        i = 0
        for x in part:
            num = (letter_index[x] + letter_index[key[i]]) % 26
            et += index_letter[num]
            i += 1
    return et


def v_decrypt(et):
    pt = ""
    et = list(et)
    key = input_key.get()
    key = key.upper()
    for x in range(len(et)):
        if " " in et:
            et.remove(" ")
    msg = [et[i:i + len(key)] for i in range(0, len(et), len(key))]
    for part in msg:
        i = 0
        for x in part:
            num = (letter_index[x] - letter_index[key[i]]) % 26
            pt += index_letter[num]
            i += 1
    return pt


# --------PLAYFAIR-CIPHER---------------------------------------------------------------------
def cube():
    sq = []
    key = input_key.get()
    for x in key.upper():
        if x not in sq:
            sq.append(x)
    for x in alphabets:
        if x not in sq:
            sq.append(x)
    matrix = []
    for e in range(5):
        matrix.append('')
    matrix[0] = sq[0:5]
    matrix[1] = sq[5:10]
    matrix[2] = sq[10:15]
    matrix[3] = sq[15:20]
    matrix[4] = sq[20:25]
    # print(matrix)
    return matrix


def pf_msg(pt):
    # pt = str(input_txt.get())
    # pt = pt.upper()
    msg = list(pt)
    for x in range(len(msg)):
        if " " in msg:
            msg.remove(" ")
    # If both letters are the same, add an "X" after the first letter.
    i = 0
    for e in range(int(len(msg) / 2)):
        if msg[i] == msg[i + 1]:
            msg.insert(i + 1, 'X')
        i = i + 2
    # If it is odd digit, add an "X" at the end
    if len(msg) % 2 == 1:
        msg.append("X")

    i = 0
    new = []
    for x in range(1, int(len(msg) / 2 + 1)):
        new.append(msg[i:i + 2])
        i = i + 2
    # print(new)
    return new


def get_position(sq, letter):
    x = y = 0
    for i in range(5):
        for j in range(5):
            if sq[i][j] == letter:
                x = i
                y = j
                break
    return x, y


def pf_encrypt(pt):
    message = pf_msg(pt)
    key_matrix = cube()
    cipher = []
    for e in message:
        p1, q1 = get_position(key_matrix, e[0])
        p2, q2 = get_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            cipher.append(key_matrix[p1][q1 + 1])
            cipher.append(key_matrix[p1][q2 + 1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1
            if p2 == 4:
                p2 = -1
            cipher.append(key_matrix[p1 + 1][q1])
            cipher.append(key_matrix[p2 + 1][q2])
        else:
            cipher.append(key_matrix[p1][q2])
            cipher.append(key_matrix[p2][q1])
    # print(cipher)
    ct = ''.join(map(str, cipher))
    return ct


def msg_to_pairs(et):
    i = 0
    new = []
    for x in range(int(len(et) / 2)):
        new.append(et[i:i + 2])
        i = i + 2
    return new


def pf_decrypt(et):
    et = msg_to_pairs(et)
    key_matrix = cube()
    pt = []
    for e in et:
        p1, q1 = get_position(key_matrix, e[0])
        p2, q2 = get_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            pt.append(key_matrix[p1][q1 - 1])
            pt.append(key_matrix[p1][q2 - 1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1
            if p2 == 4:
                p2 = -1
            pt.append(key_matrix[p1 - 1][q1])
            pt.append(key_matrix[p2 - 1][q2])
        else:
            pt.append(key_matrix[p1][q2])
            pt.append(key_matrix[p2][q1])

    for unused in range(len(pt)):
        if "X" in pt:
            pt.remove("X")

    output = ""
    for e in pt:
        output += e
    return output


# --------RAILFENCE-CIPHER-------------------------------------------------------------------
def rf_encrypt(pt):
    pt = list(pt)
    key = int(input_key.get())
    et = []
    for x in range(len(pt)):
        if " " in pt:
            pt.remove(" ")

    # initializing the rail to "\n"
    rail = [['\n' for i in range(len(pt))]
            for j in range(key)]
    # finding the direction
    dir_down = False
    row, col = 0, 0

    for i in range(len(pt)):
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
        rail[row][col] = pt[i]
        col += 1
        # find the next row
        if dir_down:
            row += 1
        else:
            row -= 1

    for i in range(key):
        for j in range(len(pt)):
            if rail[i][j] != '\n':
                et.append(rail[i][j])
    return "".join(et)


def rf_decrypt(et):
    pt = []
    et = list(et)
    key = int(input_key.get())
    for x in range(len(et)):
        if " " in et:
            et.remove(" ")
    rail = [['\n' for i in range(len(et))]
            for j in range(key)]

    dir_down = None
    row, col = 0, 0

    for i in range(len(et)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        # marking places to fill with text
        rail[row][col] = '*'
        col += 1

        if dir_down:
            row += 1
        else:
            row -= 1

    index = 0
    for i in range(key):
        for j in range(len(et)):
            if ((rail[i][j] == '*') and
                    (index < len(et))):
                rail[i][j] = et[index]
                index += 1

    row, col = 0, 0
    for i in range(len(et)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        if rail[row][col] != '*':
            pt.append(rail[row][col])
            col += 1

        if dir_down:
            row += 1
        else:
            row -= 1
    return "".join(pt)


# -------ENCRYPTION---------------------------------------------------------------------------
def encryption(event):
    pt = str(input_txt.get()).upper()
    et = ""
    if label_select.cget("text") == "SHIFT CIPHER":
        et = str(shift_encrypt(pt))
    if label_select.cget("text") == "VIGENERE CIPHER":
        et = str(v_encrypt(pt))
    if label_select.cget("text") == "PLAYFAIR CIPHER":
        et = str(pf_encrypt(pt))
    if label_select.cget("text") == "RAILFENCE CIPHER":
        et = str(rf_encrypt(pt))
    output_txt.delete(0, tk.END)
    output_txt.insert(0, et)


# -------DECRYPTION---------------------------------------------------------------------------
def decryption(event):
    et = str(input_txt.get()).upper()
    pt = ""
    if label_select.cget("text") == "SHIFT CIPHER":
        pt = str(shift_decrypt(et))
    if label_select.cget("text") == "VIGENERE CIPHER":
        pt = str(v_decrypt(et))
    if label_select.cget("text") == "PLAYFAIR CIPHER":
        pt = str(pf_decrypt(et))
    if label_select.cget("text") == "RAILFENCE CIPHER":
        pt = str(rf_decrypt(et))
    output_txt.delete(0, tk.END)
    output_txt.insert(0, pt)


def selection(event):
    option = algo.get()
    label_select.config(text=option.upper())


# -------GUI---------------------------------------------------------------------------------
n = 5
window = tk.Tk()
window.geometry("400x400")
window.title("Cipher Software")

label_heading = tk.Label(text="Encryption/Decryption Program")
label_heading.grid(row=1, column=1, padx=10, pady=10)

algo = tk.StringVar()
algo.set("Select algorithm")
menu = tk.OptionMenu(window, algo, "Shift Cipher", "Vigenere Cipher", "Playfair Cipher", "Railfence Cipher")
menu.grid(row=3, column=1)

label_select = tk.Label(window, font=("Times", 16), fg="darkblue")
label_select.grid(row=5, column=1)

button0 = tk.Button(window, text="Select", activebackground="grey")
button0.bind("<Button-1>", selection)
button0.grid(row=3, column=2)

label_key = tk.Label(window, text="Key: ")
label_key.grid(row=n + 1, column=0)

input_key = tk.Entry(window, bd=3)
input_key.grid(row=n + 1, column=1)

label_input = tk.Label(window, text="Text to Convert: ")
label_input.grid(row=n + 2, column=0)

input_txt = tk.Entry(window, bd=3)
input_txt.grid(row=n + 2, column=1)

button1 = tk.Button(window, text="Encrypt", activebackground="grey")
button1.bind("<Button-1>", encryption)
button1.grid(row=n + 3, column=0)

button2 = tk.Button(window, text="Decrypt", activebackground="grey")
button2.bind("<Button-1>", decryption)
button2.grid(row=n + 3, column=1)

label_output = tk.Label(window, text="Converted text: ")
label_output.grid(row=n + 4, column=0)

output_txt = tk.Entry(window, bd=3)
output_txt.grid(row=n + 4, column=1)

window.mainloop()
# -------------------------------------------------------------------
