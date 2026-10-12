import streamlit as st
from PIL import Image
from openai import OpenAI
import base64

st.set_page_config(page_title="Торговый ассистент Сани", layout="wide")
st.title("📊 Торговый ассистент по чек-листам Александра")
st.markdown("Загружайте скриншот графика, и ИИ проверит его по вашим правилам (минимум 5 предпосылок).")

api_key = st.sidebar.text_input("Введите ваш OpenAI API Key:", type="password")

if api_key:
    client = OpenAI(api_key=api_key)
    uploaded_file = st.file_uploader("Загрузите скриншот с TradingView", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="График для анализа", use_column_width=True)
        note = st.text_input("Параметры сделки (монета, таймфрейм, уровень):", "Например: APTUSDT, 1H, уровень 0.90")
        
        if st.button("Проверить по чек-листу"):
            with st.spinner("Анализирую..."):
                image_path = "temp.png"
                image.save(image_path)
                
                with open(image_path, "rb") as f:
                    b64_img = base64.b64encode(f.read()).decode('utf-8')
                    
                prompt = "Ты строгий торговый ассистент. Проверь график по чек-листам пробоя/отбоя (нужно минимум 5 предпосылок). Определи модель ТВХ и дай вердикт."
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": f"{prompt} Контекст: {note}"},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                        ]}
                    ],
                    max_tokens=1000
                )
                st.success("Готово!")
                st.markdown(response.choices[0].message.content)
else:
    st.warning("Введите ваш ключ OpenAI API в поле слева.")
