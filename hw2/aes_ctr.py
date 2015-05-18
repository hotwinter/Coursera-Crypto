from Crypto.Cipher import AES

def xor_str(a, b):
  a = a.encode("hex")
  b = b.encode("hex")
  length = min(len(a), len(b))
  s = ""
  for i in range(0, length, 2):
    s+=(chr(int(a[i:i+2],16) ^ int(b[i:i+2], 16)))
  return s
  
def decrypt(IV, cipher_blocks, aes, block_len):
  message = []
  for i in range(len(cipher_blocks)):
    counter = hex(int(IV.encode("hex"),16) + i)[2:-1]
    counter = ((len(counter) % 2) * '0' + counter).decode("hex")
    assert(len(counter) == block_len)
    s = xor_str(aes.encrypt(counter), cipher_blocks[i])
    message.append(s)
  return "".join(i for i in message)
  
def split_blocks(cipher, block_len):
  IV = cipher[:block_len]
  C = cipher[block_len:]
  cipher_blocks = []
  for j in range(0, len(C), block_len):
    this_block = C[j: j + block_len]
    cipher_blocks.append(this_block)
  return IV,cipher_blocks
  
cipher1 = "69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329"
cipher2 = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
key = "36f18357be4dbd77f050515c73fcf9f2".decode("hex")
BLOCK = 16

ciphers = []
ciphers.append(cipher1.decode("hex"))
ciphers.append(cipher2.decode("hex"))
for cipher in ciphers:
  IV, cipher_blocks = split_blocks(cipher, BLOCK)
  aes = AES.new(key, AES.MODE_ECB)
  message = decrypt(IV, cipher_blocks, aes, BLOCK)
  print repr(message)