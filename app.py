import os
import streamlit as st
from huggingface_hub import InferenceClient

# ---------------------------
# System Prompt（文言文大師 × 古人風骨）
# ---------------------------
SYSTEM_PROMPT = """
汝為一古代文士，學識淵博，精通文言之書寫。
性情清峻而不失諷刺，文風可似：
- 史家之筆：如司馬遷，沈雄而冷諷
- 文人之趣：如蘇軾，灑脫含笑
- 諷諭之味：如韓愈，直指世情
- 詩人喻意：如辛棄疾，豪中見悲

汝所長者：
- 能以新聞之事化為古代史記、札記、議論、或文人筆談
- 善用典故、比興、寓言、古代修辭
- 語氣可含不平之慨，亦可藏微妙之諷
- 文辭典雅，不落俗套

我將給汝當代新聞，汝需將其轉寫成一篇古人之評議或古風短文。
請用繁體中文回答。
"""

# ---------------------------
# 範例新聞內容
# ---------------------------
EXAMPLE_TEXT = """館長（陳之漢）在板橋的蛋捲店今年10月2日開幕，不過先前館長捲入「大師兄」李慶元、小瑋（小偉）、吳明鑒三方的毀滅式爆料，相關音檔瘋傳，15日館長直播已透露要收回蛋捲店，如今民眾則目擊陸續有機台被撤出，對此經營方大師兄也向《三立新聞網》回應了。

「大師兄」李慶元今證實，蛋捲店的確已經歇業，目前與館長無雇傭關係存在。而先前大師兄曾在臉書為蛋捲店發文宣傳：「有關金元酥蛋捲配方製作研發，都是我本人李慶元（大師兄）親自操刀，沒有像外界所說是工廠拿貨或是貼牌」。

館長已收回蛋捲店。（圖／翻攝自YT @館長惡名昭彰）
館長已收回蛋捲店。（圖／翻攝自YT @館長惡名昭彰）

而先前館長在直播中也已經預告蛋捲店不做了，主要也是因蛋捲店捲入這一波爭議，所以他才決定收回不做，後續也已經在請律師處理，他強調自身都有股份。
"""

# ---------------------------
# Streamlit App
# ---------------------------

st.title("📜 文言文大師：古風新聞轉寫器")

# 初始化輸入框內容
if "news_text" not in st.session_state:
    st.session_state["news_text"] = ""

# 範例按鈕
if st.button("📌 放入範例新聞"):
    st.session_state["news_text"] = EXAMPLE_TEXT

# 單一輸入框
news_text = st.text_area("📰 新聞內容：", value=st.session_state["news_text"], height=260)

# 更新 session state
st.session_state["news_text"] = news_text

# HuggingFace  Client
client = InferenceClient(api_key=os.environ.get("HF_TOKEN"))

# 生成文言文
if st.button("✨ 產生文言文版本"):
    if not news_text.strip():
        st.warning("請先輸入新聞內容！")
    else:
        with st.spinner("生成中，請稍候..."):
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b:groq",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": news_text},
                ],
            )
            output = completion.choices[0].message["content"]

        st.subheader("📜 文言文改寫結果")
        st.text_area("輸出內容：", output, height=300)