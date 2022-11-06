import numpy as np
import jieba
from wordcloud import wordcloud
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="centered")

# 文本
read_text_file_path = './bible.txt'
text_file = st.sidebar.file_uploader("请上传词云内容txt", type=["txt"])
encoding_list = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'big5hkscs', 'cp950', 'cp936', 'cp932', 'cp949', 'cp874', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig']
encoding = st.sidebar.selectbox("请选择文本编码格式", encoding_list)
# encoding = st.sidebar.text_input("请输入文本编码格式", value="utf-8")
# st.sidebar.markdown("默认编码格式为utf-8，支持的编码格式请参考：[支持的编码格式](https://docs.python.org/3/library/codecs.html#standard-encodings)")
if text_file is not None:
    text = pd.read_table(text_file, encoding=encoding)
else:
    text = pd.read_table(read_text_file_path, encoding=encoding)

# 颜色colormap
colormap = st.sidebar.text_input("请输入颜色主题", value="tab20c")
st.sidebar.markdown("默认编码格式为`tab20c`，[支持的颜色主题](https://matplotlib.org/stable/tutorials/colors/colormaps.html#sequential)")

# 轮廓图
outline_file = st.sidebar.file_uploader("自定义轮廓图", type=['png', 'jpg', 'jpeg'])
if outline_file is not None:
    read_outline_file_path = outline_file.name
    with open(read_outline_file_path, 'wb') as read_outline_file:
        read_outline_file.write(outline_file.getvalue())
        read_outline_file.close()
    outline_image = Image.open(read_outline_file_path)
    outline = np.array(outline_image)
else:
    outline = None

# 字体
read_font_file_path = './SourceHanSerifCN-Regular.otf'
font_file = st.sidebar.file_uploader("自定义字体", type=['otf', 'ttf'])
if font_file is not None:
    read_font_file_path = font_file.name
    with open(read_font_file_path, 'wb') as read_font_file:
        read_font_file.write(font_file.getvalue())
        read_font_file.close()


cut_text = jieba.cut(str(text).replace("columns", "").replace("row", ""))
wc = wordcloud.WordCloud(
    font_path=read_font_file_path,
    background_color='white',  # 背景颜色
    width=500,
    height=500,
    max_font_size=200,  # 字体大小
    min_font_size=1,
    mask=outline,
    max_words=10000,
    colormap=colormap,
    random_state=42,
    )
wc.generate(" ".join(cut_text))
wc.to_file('word_cloud.png')
col1, col2, col3 = st.columns([0.2, 1, 0.2])
with col1:
    st.empty()
with col2:
    st.image('word_cloud.png', use_column_width='auto', output_format="png")
with col3:
    st.empty()