import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# 페이지 설정 (반드시 코드 최상단에 위치)
st.set_page_config(
    page_title="Global LNG News Dashboard",
    page_icon="🚢",
    layout="wide"
)

# 뉴스 가져오는 함수 (Google News RSS 활용)
def get_google_news(query, lang='en'):
    # 검색어 인코딩 및 URL 생성
    encoded_query = query.replace(" ", "%20")
    
    # 언어 설정에 따른 URL 분기
    if lang == 'ko':
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(rss_url)
    
    news_items = []
    for entry in feed.entries[:10]:  # 최신 10개만 가져오기
        news_items.append({
            "Title": entry.title,
            "Link": entry.link,
            "Published": entry.published,
            "Source": entry.source.title if 'source' in entry else "Google News"
        })
    return news_items

# 뉴스 카드 디자인 함수
def display_news(news_list):
    if not news_list:
        st.warning("관련 뉴스를 찾을 수 없습니다.")
        return

    for item in news_list:
        # 날짜 포맷 정리 (옵션)
        try:
            date_obj = datetime.strptime(item['Published'], '%a, %d %b %Y %H:%M:%S %Z')
            date_str = date_obj.strftime('%Y-%m-%d %H:%M')
        except:
            date_str = item['Published']

        # 카드 형태의 UI 출력
        with st.container():
            st.markdown(f"""
            <div style="
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                margin-bottom: 10px;
                background-color: #f9f9f9;">
                <h4 style="margin-top:0;"><a href="{item['Link']}" target="_blank" style="text-decoration:none; color:#1f77b4;">{item['Title']}</a></h4>
                <div style="font-size: 12px; color: #555;">
                    <span>📰 <b>{item['Source']}</b></span> | 
                    <span>🕒 {date_str}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# 메인 앱 UI
def main():
    st.title("🚢 Global LNG Business News Tracker")
    st.markdown("오만, 세계 시장, 그리고 한국의 최신 LNG 사업 현황을 실시간으로 확인하세요.")
    st.divider()

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["🇴🇲 Oman LNG", "🌍 World LNG", "🇰🇷 Korea LNG"])

    with tab1:
        st.header("Oman LNG Business Updates")
        if st.button("🔄 오만 뉴스 새로고침", key='btn_oman'):
            st.rerun()
        # 검색어: Oman LNG, Oman Energy
        news_oman = get_google_news("Oman LNG project energy", lang='en')
        display_news(news_oman)

    with tab2:
        st.header("Global LNG Market Trends")
        if st.button("🔄 세계 뉴스 새로고침", key='btn_world'):
            st.rerun()
        # 검색어: Global LNG Market, LNG price
        news_world = get_google_news("Global LNG Market trends price", lang='en')
        display_news(news_world)

    with tab3:
        st.header("South Korea LNG Business")
        if st.button("🔄 한국 뉴스 새로고침", key='btn_korea'):
            st.rerun()
        # 검색어: 한국 LNG, 가스공사, 수급
        news_korea = get_google_news("한국 LNG 사업 수급 가스공사", lang='ko')
        display_news(news_korea)

    # 사이드바 정보
    with st.sidebar:
        st.subheader("About App")
        st.info("""
        이 대시보드는 Google News RSS를 기반으로 
        실시간 LNG 관련 뉴스를 수집합니다.
        
        **Target Regions:**
        - Oman (Middle East)
        - World (Global Market)
        - South Korea (Domestic)
        """)
        st.write("Developed with Streamlit")

if __name__ == "__main__":
    main()