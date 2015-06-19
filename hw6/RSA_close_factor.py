import gmpy2
import math
from gmpy2 import mpz, sqrt
N1 = mpz(179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581)

N2 = mpz(648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877)

N3 = mpz(720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929)

E = 65537

C = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

"""
n: Number to factor
val: Range to try A
a: exponent of p
b: exponent of q
"""

def factor(n, val, a, b):
  k = a * b
  temp = gmpy2.isqrt_rem(k * n)
  for i in xrange(val):
    A = temp[0] + i
    # doing ceil in a stupid way
    if temp[1] != 0:
      A += 1 
    x = gmpy2.isqrt(pow(A, 2) - k * n)
    p = A - x
    q = A + x
    if (p % a == 0):
      p = p / a 
      assert(q % b == 0)
      q = q / b
    else:
      assert(q % a == 0)
      assert(p % b == 0)
      q = q / a
      p = p / b

    # Check for validity
    if (gmpy2.is_prime(p) and gmpy2.is_prime(q) and p * q == n):
      return (p, q)
  return (-1, -1)

def decrypt(p, q, e, c):
  phi = (p - 1) * (q - 1)
  n = p * q
  d = gmpy2.invert(e, phi)
  m = hex(pow(c, d, n))[2:]
  if len(m) % 2 != 0:
    m = '0' + m
  return m

def pkcs1_decode(m):
  assert(m[:2] == '02')
  index = m.find('00')
  assert(index != -1)
  return m[index + 2:].decode("hex")
  

p1, q1 = factor(N1, 1, 1, 1)
assert(p1 != -1)
print "First Factor Taken Down !!!"
print "  " + str(p1)

p2, q2 = factor(N2, 2 ** 20, 1, 1)
assert(p2 != -1)
print "Second Factor Taken Down !!!"
print "  " + str(p2)

""" 
4 and 6 is used here instead of 3 and 2 is because
3p + 2q is an odd number, hence it's half is not an integer.
Instead we use 6p + 4q and 2 * (6N)^0.5 which when squared
is 24N, note that using twice the value does not break the
condition that distance of A and multiples of N is smaller than 1
"""

p3, q3 = factor(N3, 1, 4, 6)
print "Third Factor Taken Down !!!"
print "  " + str(p3)

m_hex = decrypt(p1, q1, E, C)
m = pkcs1_decode(m_hex)
print "Message is: "
print "  " + m

