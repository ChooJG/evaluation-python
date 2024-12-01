import tkinter as tk
from tkinter import messagebox
import pandas as pd

# 문항 및 영역 정의
questions = {
    "AI 기초 지식": [
        "AI의 기본 개념을 다른 사람에게 설명할 수 있다.",
        "생성형 AI의 원리를 다른 사람에게 설명할 수 있다."
    ],
    "AI 활용 능력": [
        "AI를 활용해 이미지나 영상을 생성할 수 있다.",
        "AI에게 원하는 답을 이끌어내기 위해 적절한 질문을 할 수 있다."
    ],
    "AI 윤리": [
        "AI 윤리적 문제에 대해 사례를 들어 설명할 수 있다.",
        "AI 윤리적 문제에 대한 해결책을 제시할 수 있다."
    ],
    "AI 친숙도": [
        "AI를 사용하는 것이 익숙하다.",
        "AI를 활용해 정보를 탐색할 수 있다."
    ],
    "AI 관심도": [
        "AI에 대한 공부 및 AI활용에 대한 관심이 있다.",
        "향후 AI를 활용해 창작물을 만들고 싶다."
    ],
    "AI 트랜드 이해": [
        "AI가 어떤 분야에서 활용되고 있는지 설명할 수 있다.",
        "우리 주변의 사회문제에 대한 AI기반 솔루션 (해결 방안)을 제시할 수 있다."
    ],
    "진로": [
        "본인의 꿈을 시각적으로 표현할 수 있다.",
        "본인의 진로를 계획 또는 탐색하고 있다."
    ],
    "LG유플러스": [
        "LG유플러스에 대한 호감도는 어느정도인가요?"
    ]
}

# DataFrame 초기화
columns = ['학생 이름'] + [f"{q} (사전)" for section in questions.values() for q in section] + \
          [f"{q} (사후)" for section in questions.values() for q in section]
data = pd.DataFrame(columns=columns)

def save_data():
    global data

    # 입력된 데이터를 가져오기
    student_name = name_entry.get()
    pre_scores = [pre_entries[i].get() for i in range(len(pre_entries))]
    post_scores = [post_entries[i].get() for i in range(len(post_entries))]

    # 유효성 검사
    if not student_name.strip():
        messagebox.showerror("오류", "학생 이름을 입력하세요.")
        return

    try:
        pre_scores = [int(score) for score in pre_scores]
        post_scores = [int(score) for score in post_scores]
        if any(score < 1 or score > 5 for score in pre_scores + post_scores):
            raise ValueError("점수는 1에서 5 사이여야 합니다.")
    except ValueError:
        messagebox.showerror("오류", "모든 점수는 1~5 사이의 정수여야 합니다.")
        return

    # DataFrame에 추가
    new_row = {'학생 이름': student_name}
    for i, question in enumerate([q for section in questions.values() for q in section]):
        new_row[f"{question} (사전)"] = pre_scores[i]
        new_row[f"{question} (사후)"] = post_scores[i]
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    # 입력 필드 초기화
    name_entry.delete(0, tk.END)
    for entry in pre_entries + post_entries:
        entry.delete(0, tk.END)

    messagebox.showinfo("성공", "데이터가 저장되었습니다!")

def export_data():
    if data.empty:
        messagebox.showerror("오류", "저장된 데이터가 없습니다.")
        return

    filename = "scores.csv"
    data.to_csv(filename, index=False, encoding='utf-8-sig')
    messagebox.showinfo("성공", f"데이터가 '{filename}' 파일로 저장되었습니다.")

def validate_and_focus(event):
    input_value = event.widget.get()
    if input_value.isdigit() and 1 <= int(input_value) <= 5:
        event.widget.tk_focusNext().focus()
    elif len(input_value) >= 1:  # 입력 길이가 1 이상일 때만 경고
        event.widget.delete(0, tk.END)
        messagebox.showerror("오류", "1에서 5 사이의 숫자를 입력하세요.")

# tkinter GUI 설정
root = tk.Tk()
root.title("사전/사후 평가 데이터 입력")

# Canvas와 Scrollbar 생성
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Scrollable Frame에 내용 추가
tk.Label(scrollable_frame, text="학생 이름").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(scrollable_frame, width=30)
name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# 문항별 사전 점수 입력
tk.Label(scrollable_frame, text="문항 번호").grid(row=1, column=0, padx=5, pady=5)
tk.Label(scrollable_frame, text="사전 점수").grid(row=1, column=1, padx=5, pady=5)
tk.Label(scrollable_frame, text="문항 내용").grid(row=1, column=2, padx=5, pady=5)
pre_entries = []

row_index = 2
for i, (section, questions_list) in enumerate(questions.items()):
    tk.Label(scrollable_frame, text=f"[{section}]").grid(row=row_index, column=0, padx=5, pady=5, sticky="w", columnspan=3)
    row_index += 1
    for j, question in enumerate(questions_list):
        tk.Label(scrollable_frame, text=f"{j + 1 + sum(len(q) for q in list(questions.values())[:i])}").grid(row=row_index, column=0, padx=5, pady=5)
        pre_entry = tk.Entry(scrollable_frame, width=5)
        pre_entry.grid(row=row_index, column=1, padx=5, pady=5)
        pre_entry.bind("<KeyRelease>", validate_and_focus)
        pre_entries.append(pre_entry)
        tk.Label(scrollable_frame, text=question).grid(row=row_index, column=2, padx=5, pady=5, sticky="w")
        row_index += 1

# 문항별 사후 점수 입력
tk.Label(scrollable_frame, text="사후 점수").grid(row=row_index, column=1, padx=5, pady=5)
row_index += 1
post_entries = []

for i, (section, questions_list) in enumerate(questions.items()):
    tk.Label(scrollable_frame, text=f"[{section}]").grid(row=row_index, column=0, padx=5, pady=5, sticky="w", columnspan=3)
    row_index += 1
    for j, question in enumerate(questions_list):
        tk.Label(scrollable_frame, text=f"{j + 1 + sum(len(q) for q in list(questions.values())[:i])}").grid(row=row_index, column=0, padx=5, pady=5)
        post_entry = tk.Entry(scrollable_frame, width=5)
        post_entry.grid(row=row_index, column=1, padx=5, pady=5)
        post_entry.bind("<KeyRelease>", validate_and_focus)
        post_entries.append(post_entry)
        tk.Label(scrollable_frame, text=question).grid(row=row_index, column=2, padx=5, pady=5, sticky="w")
        row_index += 1

# 버튼
save_button = tk.Button(scrollable_frame, text="저장", command=save_data)
save_button.grid(row=row_index, column=0, columnspan=1, pady=10)

export_button = tk.Button(scrollable_frame, text="CSV로 저장", command=export_data)
export_button.grid(row=row_index, column=1, columnspan=2, pady=10)

# GUI 실행
root.mainloop()
