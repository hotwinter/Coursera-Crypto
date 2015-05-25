import hashlib
FILENAME = "problem.mp4"
BLOCKSIZE = 1024
with open(FILENAME, "rb") as f:
  s = f.read()
s = [s[i:i+BLOCKSIZE] for i in range(0,len(s), BLOCKSIZE)]
s = s[::-1]
hash = ""
for i in s:
  m = hashlib.sha256()
  m.update(i + hash)
  hash = m.digest()
print hash.encode("hex")
