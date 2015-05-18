from Crypto.Cipher import AES

def xor_str(a, b):
  a = a.encode("hex")
  b = b.encode("hex")
  length = min(len(a), len(b))
  s = ""
  for i in range(0, length, 2):
    s+=(chr(int(a[i:i+2],16) ^ int(b[i:i+2], 16)))
  return s

def strip_padding(s):
  length = ord(s[-1])
  return s[0:-length]
  
def decrypt(IV, cipher_blocks, aes):
  message = []
  for i in range(len(cipher_blocks)-1, 0, -1):
    message.append(xor_str(aes.decrypt(cipher_blocks[i]), cipher_blocks[i - 1]))
  message.append(xor_str(aes.decrypt(cipher_blocks[0]), IV))
  return "".join(i for i in message[::-1])
    
def split_blocks(cipher, block_len):
  IV = cipher[:block_len]
  C = cipher[block_len:]
  cipher_blocks = []
  for j in range(0, len(C), block_len):
    this_block = C[j: j + block_len ]
    assert(len(this_block) == block_len)
    cipher_blocks.append(this_block)
  return IV,cipher_blocks
  
cipher1 = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
cipher2 = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
key = "140b41b22a29beb4061bda66b6747e14".decode("hex")
BLOCK = 16

ciphers = []
ciphers.append(cipher1.decode("hex"))
ciphers.append(cipher2.decode("hex"))
for cipher in ciphers:
  IV, cipher_blocks = split_blocks(cipher, BLOCK)
  aes = AES.new(key, AES.MODE_ECB)
  message = decrypt(IV, cipher_blocks, aes)
  message = strip_padding(message)
  print repr(message)