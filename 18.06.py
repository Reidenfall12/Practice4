#словарь
dct = {}
start, end = ord('a'), ord('z')+1
for i in range(start, end):
 dct[chr(i)] = i - start
#шифрует
def coder (word, key):
 result = ''
 for l,k in zip(word, key):
  sh = dct[k.lower()]
  n_l = 65 + (ord(l) - 65 + sh) % 26
  result += chr(n_l)
 return result
#расшифрововает
def decoder (word, key):
 result = ''
 for l,k in zip(word, key):
  sh = dct[k.lower()]
  n_l = 65 + (ord(l) - 65 - sh) % 26
  result += chr(n_l)
 return result
def adeq(word, key):
 size_word = len(word)
 while len(key) < size_word:
   key += key
 return key
print('Что будем делать?(ш - зашифровывать;р - расшифровывать)')
act = str(input())
word = input('Введите слово: ')
key = input('ключ: ')
nev_key = adeq(word, key)
if act == "ш":
 print ('Зашифрованное слово:', coder(word, nev_key))
else:
 print ('Расшифрованное слово:', decoder(word, nev_key))