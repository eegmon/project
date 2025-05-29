def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"원반 1을(를) {source}에서 {target}(으)로 이동")
        return
    hanoi(n - 1, source, auxiliary, target)
    print(f"원반 {n}을(를) {source}에서 {target}(으)로 이동")
    hanoi(n - 1, auxiliary, target, source)

if __name__ == "__main__":
    n = int(input("원반의 개수를 입력하세요: "))
    hanoi(n, 'A', 'C', 'B')