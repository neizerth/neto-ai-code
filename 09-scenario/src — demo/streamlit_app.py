import streamlit as st

from services.shopping_service import build_shopping_list


st.set_page_config(page_title="Список покупок", layout="centered")
st.title("Список покупок")

dish = st.text_area("Что приготовить", placeholder="Например: борщ", height=140)
people = st.selectbox("На сколько человек", ["1", "2", "4", "6"], index=1)
output_format = st.selectbox("Формат", ["Список продуктов", "Список + шаги"], index=0)

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

col1, col2 = st.columns([1, 1])
with col1:
    generate = st.button("Сгенерировать", type="primary")
with col2:
    clear = st.button("Очистить")

if clear:
    st.session_state.last_result = ""
    st.rerun()

if generate:
    with st.spinner("Думаю..."):
        result = build_shopping_list(dish, people, output_format)
    if result.ok:
        st.session_state.last_result = result.message
    else:
        st.error(result.message)

st.subheader("Результат")
st.write(st.session_state.last_result or "Пока пусто.")

