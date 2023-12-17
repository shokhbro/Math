import random
from calculus_db import MisolDB

def amallar_dasturi(soni):
    db_natijalar = MisolDB()

    ism = input("Ismingizni kiriting: ")
    oyinchi_id = db_natijalar.insert_oyinchi(ism)

    togri = 0
    notogri = 0

    for i in range(soni):
        n = random.randint(1, 50)
        m = random.randint(1, 50)

        amal = input("qaysi matematik amalni bajarmoqchisiz? [+,-,/,*]")

        if amal == '/':
            print(f"{n}/{m}=?")
            son = int(input("javob: "))
            if son == n / m:
                print("javob to'gri")
                togri += 1
            else:
                print("javob xato")
                notogri += 1

        if amal == "*":
            print(f"{n}*{m}=?")
            son = int(input("javob: "))
            if son == n * m:
                print("javob to'gri")
                togri += 1
            else:
                print("javob xato")
                notogri += 1

        if amal == "-":
            print(f"{n}-{m}=?")
            son = int(input("javob: "))
            if son == n - m:
                print("javob to'g'ri")
                togri += 1
            else:
                print("javob xato")
                notogri += 1

        if amal == "+":
            print(f"{n}+{m}=?")
            son = int(input("javob: "))
            if son == n + m:
                print("javob to'g'ri")
                togri += 1
            else:
                print("javob xato")
                notogri += 1

    print(f"To'g'ri javoblar: {togri} ta,\nNoto'g'ri javoblar: {notogri} ta")

    db_natijalar.insert_natija(oyinchi_id, togri, notogri)

    print("\nBarcha natijalar:")
    all_natijalar = db_natijalar.get_all_natijalar()
    k=1
    for natija in all_natijalar:
        print(f"{k}: {natija[0]}- {natija[1]} ta to'g'ri")
        k+=1

if __name__ == "__main__":
    soni = int(input("nechta masala ishlamoqchisiz: "))
    amallar_dasturi(soni)
