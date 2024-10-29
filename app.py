from flask import Flask, render_template, request
app = Flask(__name__)

def make_table(key):
    key = key.upper()
    alphabet = [chr(i) for i in range(65, 91)]
    alphabet += " "
    remaining = [ch for ch in alphabet if ch not in key]
    line1 = list(key) + remaining

    result = []
    for i in range(27):
        nextline = line1[i:] + line1[:i]
        result.append(nextline)

    return result

def encrypt(coded_table, message, key):
    message = message.upper()
    message = ''.join(char for char in message if (char.isalpha() or char == " "))
    key = key.upper()
    repeated_key = (key * (len(message) // len(key) + 1))[:len(message)]
    encrypted_text = []

    for msg_char, key_char in zip(message, repeated_key):
        row_index = coded_table[0].index(msg_char)
        col_index = coded_table[0].index(key_char)
        encrypted_char = coded_table[row_index][col_index]
        encrypted_text.append(encrypted_char)

    return ''.join(encrypted_text)

def decipher(coded_table, cipher_text, key):
    cipher_text = cipher_text.upper()
    key = key.upper()
    repeated_key = (key * (len(cipher_text) // len(key) + 1))[:len(cipher_text)]
    decipher_text = []

    for cipher_char, key_char in zip(cipher_text, repeated_key):
        row_index = coded_table[0].index(key_char)
        for i in range(27):
            if coded_table[row_index][i] == cipher_char:
                col_index = i
                break
        decipher_char = coded_table[0][col_index]
        decipher_text.append(decipher_char)

    return ''.join(decipher_text)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    action = None
    if request.method == 'POST':
        table_key = request.form['table_key']
        coded_table = make_table(table_key)
        cipher_key = request.form['cipher_key']
        message = request.form['message']
        action = request.form['action']

        if action == 'cipher':
            result = encrypt(coded_table, message, cipher_key)
        else:
            result = decipher(coded_table, message, cipher_key)

    return render_template('index.html', result=result, action=action)

if __name__ == "__main__":
    app.run(debug=True)
