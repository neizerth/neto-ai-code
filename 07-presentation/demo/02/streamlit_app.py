import streamlit as st

from pathlib import Path
import sys


# Позволяем импортировать общий модуль из demo/01
sys.path.append(str(Path(__file__).resolve().parents[1] / "01"))
from llm import handle_student_question  # noqa: E402


st.set_page_config(page_title="Ответ студенту — демо", layout="centered")
st.title("Ответ студенту (демо)")

st.write("Прототип: проверяем гипотезу, что LLM ускорит ответы на типовые вопросы.")

tone = st.selectbox("Тон ответа", ["Нейтрально", "Дружелюбно"])
text = st.text_area(
    "Вопрос студента",
    placeholder="Например: «Не понимаю, чем 4xx отличается от 5xx. Объясни простыми словами.»",
    height=180,
)

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

col1, col2 = st.columns([1, 1])
with col1:
    generate = st.button("Сгенерировать ответ", type="primary")
with col2:
    clear = st.button("Очистить")

if clear:
    st.session_state.last_result = ""
    st.rerun()

if generate:
    with st.spinner("Генерируем ответ..."):
        result = handle_student_question(text, tone)
    if result.ok:
        st.session_state.last_result = result.message
    else:
        st.error(result.message)

st.subheader("Результат")
st.write(st.session_state.last_result or "Пока пусто.")

