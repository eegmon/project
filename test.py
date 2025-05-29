def arithmetic_caesar(plain, start, diff):
    cipher = ""
    for idx, ch in enumerate(plain):
        key = start + idx * diff
        if ch.isalpha():
            if ch.islower():
                cipher += chr((ord(ch) - ord('a') + key) % 26 + ord('a'))
            elif ch.isupper():
                cipher += chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
        else:
            cipher += ch
    return cipher

def fibonacci_sequence(n):
    fibs = [1, 1]
    for i in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

def fibonacci_caesar(plain):
    cipher = ""
    fibs = fibonacci_sequence(len(plain))
    for idx, ch in enumerate(plain):
        key = fibs[idx]
        if ch.isalpha():
            if ch.islower():
                cipher += chr((ord(ch) - ord('a') + key) % 26 + ord('a'))
            elif ch.isupper():
                cipher += chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
        else:
            cipher += ch
    return cipher

def de_arithmetic_caesar(cipher, start, diff):
    plain = ""
    for idx, ch in enumerate(cipher):
        key = start + idx * diff
        if ch.isalpha():
            if ch.islower():
                plain += chr((ord(ch) - ord('a') - key) % 26 + ord('a'))
            elif ch.isupper():
                plain += chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
        else:
            plain += ch
    return plain

def de_fibonacci_caesar(cipher):
    plain = ""
    fibs = fibonacci_sequence(len(cipher))
    for idx, ch in enumerate(cipher):
        key = fibs[idx]
        if ch.isalpha():
            if ch.islower():
                plain += chr((ord(ch) - ord('a') - key) % 26 + ord('a'))
            elif ch.isupper():
                plain += chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
        else:
            plain += ch
    return plain


while True:
    key = input("사용기능 (1: 산술 Caesar, 2: 피보나치 Caesar, 3: 종료): ")
    if key == '1':
        plain = input("평문 입력: ")
        start = int(input("a1 입력: "))
        diff = int(input("공차 입력: "))
        cipher = arithmetic_caesar(plain, start, diff)
        print(f"암호문: {cipher}")
        de_cipher = de_arithmetic_caesar(cipher, start, diff)
        print(f"복호문: {de_cipher}")
    elif key == '2':
        plain = input("평문 입력: ")
        cipher = fibonacci_caesar(plain)
        print(f"암호문: {cipher}")
        de_cipher = de_fibonacci_caesar(cipher)
        print(f"복호문: {de_cipher}")
    elif key == '3':
        break
    else:
        print("잘못된 선택입니다. 다시 시도하세요.")