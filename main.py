import streamlit as st
import torch
from diffusers import StableDiffusionPipeline


# Параметры запуска страницы, в т.ч. полнооконное представление
st.set_page_config(layout="wide",
                   page_title="make_pic",
                   page_icon="🏠")


model_id = "runwayml/stable-diffusion-v1-5"
# Загрузка модели. Если cuda доступна, грузим под неё
# Если нет, грузим под cpu
if torch.cuda.is_available():
    st.write("on CUDA")
    pipe = StableDiffusionPipeline.from_pretrained(model_id,
                                                   torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

else:
    st.write("on CPU")
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe = pipe.to("cpu")


def image_gen(prompt):
    '''
    на вход подаём текстовое описание картинки
    на выходе получаем сгенерированное изображение
    '''
    return pipe(prompt).images[0]


# Заголовок страницы
st.write("# Приложение для создание картинок по текстовому описанию")

# Строка ввода текстового описания картинки
prompt = st.text_area("Ввод текстового описания картинки",
                      value="A reindeer next to the chum",
                      help="Введите текстовое описание картинки")

# Кнопка для запуска модели
btn = st.button("Создать картинку",
                help="Жмакай кнопку только после ввода строки")

# Если кнопка жмакнута, запускаем функцию генератора картинки
if btn:
    image = image_gen(prompt)
    # Выводим картинку на экран
    st.image(image,
             caption="Вот такая вот картинка")
