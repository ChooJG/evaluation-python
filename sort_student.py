def sort_names():
    print("학생 이름을 입력하세요. 종료하려면 '종료'를 입력하세요.")

    # 이름을 저장할 리스트
    names = []

    # 이름 입력 루프
    while True:
        name = input("학생 이름: ").strip()
        if name == '종료':
            break
        if name:  # 빈 문자열은 무시
            names.append(name)

    # 이름을 가나다순으로 정렬
    sorted_names = sorted(names)

    # 정렬된 이름 출력
    print("\n정렬된 학생 이름 목록:")
    for i, name in enumerate(sorted_names, start=1):
        print(f"{i}. {name}")


# 함수 실행
sort_names()
