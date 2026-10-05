import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="AI Fake News Detection Assistant",
    page_icon="📰"
)

st.title("📰 AI Fake News Detection Assistant")
st.write("Check whether a news article appears fake or real.")

option = st.radio(
    "Choose input type:",
    ["News URL", "Paste Article"]
)

article = ""

# ---------------- URL INPUT ----------------
if option == "News URL":

    url = st.text_input("Enter News Article URL")

    if st.button("Check News"):

        if not url:
            st.warning("Please enter a URL.")

        else:
            try:
                response = requests.get(
                    url,
                    timeout=10,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

                soup = BeautifulSoup(response.text, "html.parser")

                title = soup.title.string if soup.title else "No title found"

                paragraphs = soup.find_all("p")

                article = " ".join(
                    p.get_text() for p in paragraphs
                )

                st.subheader("📰 Article Title")
                st.write(title)

                st.subheader("Article Content")
                st.write(article[:3000])

            except Exception as e:
                st.error(f"Unable to read the article: {e}")


# ---------------- ARTICLE INPUT ----------------
else:

    article = st.text_area(
        "Paste your news article here:",
        height=300
    )

    if st.button("Check Article"):

        if not article:
            st.warning("Please paste an article.")

        elif len(article) < 100:
            st.warning("Article is too short.")

        else:

            # Words commonly found in suspicious/fake news
            fake_words = [
                "shocking",
                "breaking",
                "miracle",
                "secret",
                "guaranteed",
                "100%",
                "scientists claim",
                "reportedly",
                "no evidence",
                "unbelievable",
                "you won't believe",
                "cure",
                "overnight"
            ]

            text = article.lower()

            score = 0

            for word in fake_words:
                if word in text:
                    score += 1

            # ---------------- RESULT ----------------

            st.subheader("🔍 Fake News Detection Result")

            if score >= 2:

                st.error("🔴 FAKE NEWS / SUSPICIOUS")

                confidence = min(60 + score * 8, 95)

                st.metric(
                    "Confidence",
                    f"{confidence}%"
                )

                st.write(
                    "⚠️ This article contains several suspicious "
                    "words or claims commonly associated with "
                    "unverified news."
                )

                st.write("### 🚩 Suspicious indicators")

                for word in fake_words:
                    if word in text:
                        st.write(f"• {word}")

            else:

                st.success("🟢 LIKELY REAL NEWS")

                st.metric(
                    "Confidence",
                    "70%"
                )

                st.write(
                    "The article does not contain many obvious "
                    "suspicious indicators."
                )

            st.info(
                "⚠️ This is a basic AI-style demonstration. "
                "It does not guarantee that an article is actually "
                "true or false. Always verify important news using "
                "reliable sources."
            )