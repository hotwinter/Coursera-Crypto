import urllib2
import multiprocessing as mp

TARGET = 'http://crypto-class.appspot.com/po?er='
LENGTH = 16
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
def strip_padding(s):
  length = ord(s[-1])
  return s[0:-length]
  
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            if e.code == 404:
                #print "Gotcha!"
                return True # good padding
            return False # bad padding

def decrypt_block(po, index, ciphers, output):
  fakeIV = list("\x00" * LENGTH)
  plaintext = list("X" * LENGTH)
  for i in range(LENGTH):
    for c in range (0,256):
      byte = chr(c ^ (i + 1) ^ ord(ciphers[index - 1].decode("hex")[LENGTH - i - 1]))
      fakeIV[LENGTH - i - 1] = byte
      if (po.query("".join(fakeIV).encode("hex") + ciphers[index])):        # Issue HTTP query with the given argument
        plaintext[LENGTH - i - 1] = chr(c)
        print "".join(i for i in plaintext)
        for j in range(i + 1):
          fakeIV[LENGTH - i - 1 + j] = chr(ord(fakeIV[LENGTH - i - 1 + j]) ^ (i + 1) ^ (i + 2))
        break
    if c == 255:
      print "WE FAILED"
      return
  print "Success!"
  output.put((index,"".join(i for i in plaintext)))
    
if __name__ == "__main__":
    po = PaddingOracle()
    cipher = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
    ciphers = [cipher[i:i+ LENGTH * 2] for i in range(0,len(cipher), LENGTH * 2)]
    print ciphers
    output = mp.Queue()
    processes = [mp.Process(target=decrypt_block, args=(po, i, ciphers, output)) for i in range(1,len(ciphers))]
    for p in processes:
      p.start()
    for p in processes:
      p.join()
    results = [output.get() for p in processes]
    results = [r[1] for r in sorted(results)]
    
    print strip_padding("".join(i for i in results))