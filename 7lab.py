import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from itertools import combinations

# Данные претендентов
candidates = ['A','B','C','D','E','F']
salary    = dict(zip(candidates, [40,50,60,70,80,90]))
skill     = dict(zip(candidates, [80,80,80,80,80,100]))

# Генерация всех вариантов
def generate_variants(cands):
    return [
        (mids, juns)
        for mids in combinations(cands, 2)
        for juns in combinations([c for c in cands if c not in mids], 2)]

# Фильтрация по бюджету и минимальному навыку, отбор оптимальных
def filter_and_select(variants, budget, min_skill):
    valid = []
    for mids, juns in variants:
        tot_sal = sum(salary[x] for x in mids + juns)
        tot_sk  = sum(skill[x] for x in mids + juns)
        if tot_sal <= budget and tot_sk >= min_skill:
            valid.append((mids, juns, tot_sal, tot_sk))
    if not valid:
        return [], 0
    max_skill = max(item[3] for item in valid)
    best = [item for item in valid if item[3] == max_skill]
    return best, max_skill

# Обработчик нажатия кнопки
def show_results():
    try:
        budget    = int(entry_budget.get())
        min_skill = int(entry_min_skill.get())
    except ValueError:
        messagebox.showwarning("Ошибка", "Введите целые числа в оба поля")
        return

    variants = generate_variants(candidates)
    best, max_skill = filter_and_select(variants, budget, min_skill)

    text_output.config(state='normal')
    text_output.delete(1.0, 'end')
    if not best:
        text_output.insert('end', "Нет вариантов под заданные параметры.\n")
    else:
        text_output.insert('end', f"Найдено {len(best)} оптимальных вариантов с навыком = {max_skill}\n\n")
        for mids, juns, tot_sal, tot_sk in best:
            text_output.insert('end', f"Mids={mids}, Juniors={juns}, Salary={tot_sal}, Skill={tot_sk}\n")
        # Лучший по минимальной зарплате
        best_one = min(best, key=lambda x: x[2])
        m, j, sal, sk = best_one
        text_output.insert('end', f"\nЛучший вариант (минимальная зарплата):\n")
        text_output.insert('end', f"Mids={m}, Juniors={j}, Salary={sal}, Skill={sk}\n")
    text_output.config(state='disabled')

# Главное окно
root = tk.Tk()
root.title("Подбор сотрудников")
root.configure(bg='lightblue')
frame = ttk.Frame(root, padding=10)
frame.pack(fill='x')

# Поля ввода
ttk.Label(frame, text="Бюджет:").grid(row=0, column=0, sticky='w')
entry_budget = ttk.Entry(frame)
entry_budget.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(frame, text="Минимальный навык:").grid(row=1, column=0, sticky='w')
entry_min_skill = ttk.Entry(frame)
entry_min_skill.grid(row=1, column=1, padx=5, pady=2)
entry_min_skill.insert(0, "0")

# Кнопка запуска расчёта
btn = ttk.Button(frame, text="Рассчитать", command=show_results)
btn.grid(row=2, column=0, columnspan=2, pady=5)

# Область вывода с прокруткой
text_output = ScrolledText(root, width=60, height=15, state='disabled')
text_output.pack(fill='both', expand=True, padx=10, pady=5)

root.mainloop()
