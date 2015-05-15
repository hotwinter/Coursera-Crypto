from collections import defaultdict
import string

def xor_str(a, b):
  length = min(len(a), len(b))
  s = ""
  for i in range(0, length, 2):
    s+=(chr(int(a[i:i+2],16) ^ int(b[i:i+2], 16)))
  return s

def find_spaces(ciphers, selected, limit):
  xors = []
  for i in range(len(ciphers)):
    if i != selected:
      xors.append(xor_str(ciphers[selected], ciphers[i]))
  d = defaultdict(list)
  for xor in xors:
    for i in range(len(xor)):
      if (xor[i] in string.letters):
        d[i].append(xor[i])
  return [xors, [i for i in d.keys() if len(d[i]) > limit or d[i].count("\x00") > 1]]
  
def guess_selected(xors, space_list, selected):
  message1 = ["_" for i in range(len(ciphers[selected]))]
  for xor in xors:
    for i in range(len(xor)):
      if i in space_list:
        message1[i]=" "
      else:
        if xor[i] in string.letters:
          if (message1[i] == "_"):
            message1[i]=chr(ord(xor[i]) ^ ord(" "))
  return message1
   
def guess(selected, limit, ciphers):
  res = find_spaces(ciphers, selected, limit)
  return guess_selected(res[0], res[1], selected)

def print_all(ciphers, guessk):
  for i in ciphers:
    guess_str = xor_str(guessk.encode("hex"), i)
    print guess_str
  print
  
with open("enc.txt", "rb") as f:
  ciphers = f.read().split("\r\n")
  assert( len(ciphers) == 10 )
with open("cipher.txt", "rb") as f:
  cipher = f.read().strip("\r\n")

lengths = [len(i) for i in ciphers]
print lengths

message1 = guess(0, 6, ciphers)

print message1
guess1 = "We can factor the number hz with quantum computers. We can also factor the number bT"
guessk = xor_str(ciphers[0], guess1.encode("hex"))
guess2 = xor_str(guessk.encode("hex"), ciphers[1])
print guess2
guess2 = "Euler would probably enjoy that now his theorem becomes a corner stone of crypto"
guessk = xor_str(ciphers[1], guess2.encode("hex"))
guess1 = xor_str(guessk.encode("hex"), ciphers[0])
print guess1
guess4 = xor_str(guessk.encode("hex"), ciphers[3])
print guess4
guess4 = "The ciphertext produced by a weak encryption algorithm looks as good as ciphertext produced by a strong encryption algorithm"
guessk = xor_str(ciphers[3], guess4.encode("hex"))
print_all(ciphers, guessk)
final = xor_str(guessk.encode("hex"), cipher)
print "\n" * 3
print "[+] Answer: " + final
print "\n" * 3
print_all(ciphers, guessk)
guess6 = "There are two types of cryptography - that which will keep secrets safe from your little sister, and that which will keep secrets from "
guessk = xor_str(ciphers[5], guess6.encode("hex"))
print_all(ciphers, guessk)
guess9 = "A (private-key)  encryption scheme states 3 algorithms, namely a procedure for generating keys, a procedure for encrypting, and a procedure for "
guessk = xor_str(ciphers[8], guess9.encode("hex"))
print lengths
print len(guessk) * 2
print_all(ciphers, guessk)
guess7 = "There are two types of cyptography: one that allows the Government to use brute force to break the code, and one that requires the Government to use brute force to break you"
guessk = xor_str(ciphers[6], guess7.encode("hex"))
print len(guessk) * 2
print_all(ciphers, guessk)
# All but cipher7 decrypted...Therefore can't proceed anymore