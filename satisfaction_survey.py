import tkinter as tk
from tkinter import messagebox
import pandas as pd

# 문항 및 영역 정의
questions = {
    "AI 크리에이터 교육 (책, 영상 만들기)": [
        "교육에 즐겁게 참여하였고, 의미 있는 시간이었다.",
        "강사는 전문성과 열의를 가지고 교육하였다.",
        "흥미롭고 유익한 내용이었다.",
        "교육 시간(기간)이 적당했다."
    ],
    "LG U+ 특강": [
        "교육에 즐겁게 참여하였고, 의미 있는 시간이었다.",
        "흥미롭고 유익한 내용이었다.",
        "교육 시간(기간)이 적당했다."
    ]
}

# 주관식 문항 정의
subjective_questions = [
    "[1~4] AI 크리에이터 교육(책, 영상 만들기)에 대해 좋았던 점이나 아쉬웠던 점을 적어주세요.",
    "[5~7] LG U+ 특강에 대해 좋았던 점이나 아쉬웠던 점을 적어주세요.",
    "교육에 참여하면서 배우고 느낀 점을 적어주세요."
]

# DataFrame 초기화 (고유 열 이름)
columns = ["이름"] + [f"{section}: {q}" for section, question_list in questions.items() for q in question_list] + subjective_questions
data = pd.DataFrame(columns=columns)

def save_data():
    global data

    # 입력된 데이터를 가져오기
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("오류", "이름을 입력하세요.")
        return

    objective_responses = [entry.get() for entry in objective_entries]
    subjective_responses = [entry.get("1.0", tk.END).strip() for entry in subjective_entries]

    # 유효성 검사 (객관식)
    try:
        objective_responses = [int(response) for response in objective_responses]
        if any(response < 1 or response > 5 for response in objective_responses):
            raise ValueError("응답은 1에서 5 사이의 숫자여야 합니다.")
    except ValueError:
        messagebox.showerror("오류", "객관식 응답은 1에서 5 사이의 숫자여야 합니다.")
        return

    # DataFrame에 추가
    new_row = {"이름": name}
    for section, question_list in questions.items():
        for question, response in zip(question_list, objective_responses[:len(question_list)]):
            new_row[f"{section}: {question}"] = response
        objective_responses = objective_responses[len(question_list):]  # 이미 처리한 응답 제거

    for q, response in zip(subjective_questions, subjective_responses):
        new_row[q] = response

    # 중복된 열 확인
    if not set(new_row.keys()).issubset(data.columns):
        messagebox.showerror("오류", "열 이름이 데이터와 일치하지 않습니다.")
        return

    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    # 입력 필드 초기화
    name_entry.delete(0, tk.END)
    for entry in objective_entries:
        entry.delete(0, tk.END)
    for entry in subjective_entries:
        entry.delete("1.0", tk.END)

    messagebox.showinfo("성공", "데이터가 저장되었습니다!")

def export_data():
    if data.empty:
        messagebox.showerror("오류", "저장된 데이터가 없습니다.")
        return

    filename = "satisfaction_survey_with_name.csv"
    data.to_csv(filename, index=False, encoding='utf-8-sig')
    messagebox.showinfo("성공", f"데이터가 '{filename}' 파일로 저장되었습니다.")

def validate_and_focus(event):
    input_value = event.widget.get()
    if input_value.isdigit() and 1 <= int(input_value) <= 5:
        event.widget.tk_focusNext().focus()
    else:
        event.widget.delete(0, tk.END)
        messagebox.showerror("오류", "1에서 5 사이의 숫자를 입력하세요.")

# tkinter GUI 설정
root = tk.Tk()
root.title("만족도 조사 입력")

# Scrollable Frame 설정
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
objective_entries = []
subjective_entries = []

# 이름 입력 필드
tk.Label(scrollable_frame, text="이름:", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=5, sticky="w")
name_entry = tk.Entry(scrollable_frame, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# 객관식 문항 추가
row_index = 1
for i, (section, question_list) in enumerate(questions.items()):
    tk.Label(scrollable_frame, text=f"[{section}]", font=("Arial", 10, "bold")).grid(row=row_index, column=0, columnspan=2, pady=5, sticky="w")
    row_index += 1
    for question in question_list:
        tk.Label(scrollable_frame, text=question).grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(scrollable_frame, width=5)
        entry.grid(row=row_index, column=1, padx=5, pady=5)
        entry.bind("<KeyRelease>", validate_and_focus)  # 숫자 입력 후 바로 다음 칸으로 이동
        objective_entries.append(entry)
        row_index += 1

# 주관식 문항 추가
tk.Label(scrollable_frame, text="[주관식 문항]", font=("Arial", 10, "bold")).grid(row=row_index, column=0, columnspan=2, pady=5, sticky="w")
row_index += 1
for question in subjective_questions:
    tk.Label(scrollable_frame, text=question).grid(row=row_index, column=0, padx=5, pady=5, sticky="nw")
    text = tk.Text(scrollable_frame, width=40, height=3)
    text.grid(row=row_index, column=1, padx=5, pady=5, sticky="w")
    subjective_entries.append(text)
    row_index += 1

# 버튼
save_button = tk.Button(scrollable_frame, text="저장", command=save_data)
save_button.grid(row=row_index, column=0, pady=10)

export_button = tk.Button(scrollable_frame, text="CSV로 저장", command=export_data)
export_button.grid(row=row_index, column=1, pady=10)

# GUI 실행
root.mainloop()
