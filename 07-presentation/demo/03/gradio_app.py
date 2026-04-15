import gradio as gr

from pathlib import Path
import sys


# Позволяем импортировать общий модуль из demo/01
sys.path.append(str(Path(__file__).resolve().parents[1] / "01"))
from llm import handle_student_question  # noqa: E402


def handle(text: str, tone: str, last: str) -> tuple[str, str]:
    result = handle_student_question(text, tone)
    if result.ok:
        return result.message, result.message
    # Ошибка: показываем текст, но старый результат не затираем
    return result.message, last


with gr.Blocks(title="Ответ студенту — демо") as demo:
    gr.Markdown("## Ответ студенту (демо)\nПрототип: проверяем гипотезу, что LLM ускорит ответы на типовые вопросы.")

    text = gr.Textbox(lines=6, label="Вопрос студента")
    tone = gr.Dropdown(["Нейтрально", "Дружелюбно"], label="Тон ответа", value="Нейтрально")
    btn = gr.Button("Сгенерировать ответ")

    out = gr.Textbox(label="Результат", lines=10)
    last = gr.State("")

    btn.click(handle, inputs=[text, tone, last], outputs=[out, last])


if __name__ == "__main__":
    demo.launch()

