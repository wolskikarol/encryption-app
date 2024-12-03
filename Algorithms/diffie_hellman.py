import random

def diffie_hellman(p, g):
    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    
    A = pow(g, a, p)
    B = pow(g, b, p)
    
    shared_secret_A = pow(B, a, p)
    shared_secret_B = pow(A, b, p)
    
    assert shared_secret_A == shared_secret_B, "Sekrety nie są zgodne!"
    
    print(f"Tajna liczba A: {a}")
    print(f"Tajna liczba B: {b}")
    print(f"Klucz publiczny A: {A}")
    print(f"Klucz publiczny B: {B}")
    print(f"Wspólny sekret: {shared_secret_A}")

p = 109438836907830768018697618956032988158573407045179287117661217393758413572949402503933439744580968654298922524526593226007186166653004202672752340837416107966716537121487726839106769510827258947158040839868966346207611672299366055805288866374891331256162207378857834229937657829357267658763792831856416764681
g = 2

diffie_hellman(p, g)
