try:
    import pyperclip  # copies text to clipboard
except ImportError:
    pass

# sumbols to encrypt
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

print('CAESAR CIPHER')
print('The Caesar cupher encrypts letters by shifting them over by a')
print('key number. For example, key of 2 means the letter A is')
print('encrypted into C, B -> D, etc.')
print()

# Enter if encrypting or decrypting
while True:
    print('Do you want to (e)ncrypt or (d)ecrypt?')
    response = input('> ').lower()
    if response.startswith('e'):
        mode = 'encrypt'
        break
    elif response.startswith('d'):
        mode = 'decrypt'
        break
    print('Please enter the letter e or d.')

# User enter key
while True:
    maxKey = len(SYMBOLS) - 1
    print(f'Please enter the key (0 - {maxKey})')
    response = input('> ').upper()
    if not response.isdecimal():
        continue
    if 0 <= int(response) < len(SYMBOLS):
        key = int(response)
        break

# Enter message to en/decrypy
print(f'Enter message to {mode}.')
message = input('> ')

message = message.upper()

translated = ''

# deal with wrap-around
for symbol in message:
    if symbol in SYMBOLS:
        num = SYMBOLS.find(symbol)
        if mode == 'encrypt':
            num = num + key
        elif mode == 'decrypt':
            num = num - key
        if num >= len(SYMBOLS):
            num = num - len(SYMBOLS)
        elif num < 0:
            num = num + len(SYMBOLS)

        translated = translated + SYMBOLS[num]
    else:
        translated = translated + symbol

print(translated)

try:
    pyperclip.copy(translated)
    printf(' Full {mode}ed text copied to clipboard.')
except:
    pass
