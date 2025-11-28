import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="Global LNG News Dashboard",
    page_icon="🚢",
    layout="wide"
)

# ---------------------------------------------------------
# [수정됨] 뉴스 검색 함수 (시간 필터 기능 추가)
# period='30d' -> 최근 30일 기사만 검색
# ---------------------------------------------------------
def get_google_news(query, lang='en', period='30d'):
    # 검색어에 시간 제한 명령어를 추가 (예: "Oman LNG when:30d")
    # 이렇게 하면 구글이 강제로 해당 기간 내의 기사만 보내줍니다.
    timed_query = f"{query} when:{period}"
    encoded_query = timed_query.replace(" ", "%20")
    
    # URL 생성
    if lang == 'ko':
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    else:
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(rss_url)
    
    news_items = []
    # 최신순 정렬을 위해 가져온 리스트를 한 번 더 날짜순으로 정렬 (옵션)
    # 구글이 대략 맞춰주지만, 확실하게 하기 위함
    entries = feed.entries[:15] # 넉넉히 15개 가져옴
    
    for entry in entries:
        news_items.append({
            "Title": entry.title,
            "Link": entry.link,
            "Published": entry.published,
            "DateObj": datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now(),
            "Source": entry.source.title if 'source' in entry else "Google News"
        })
        
    # 날짜 기준 내림차순 정렬 (최신 기사가 맨 위로)
    news_items.sort(key=lambda x: x['DateObj'], reverse=True)
    
    return news_items

# 뉴스 카드 디자인 함수
def display_news(news_list):
    if not news_list:
        st.info("⚠️ 지정된 기간(최근) 내의 관련 뉴스가 없습니다.")
        return

    for item in news_list:
        # 날짜 포맷 깔끔하게 변경
        try:
            date_str = item['DateObj'].strftime('%Y-%m-%d %H:%M')
        except:
            date_str = str(item['Published'])

        # 카드 디자인
        with st.container():
            st.markdown(f"""
            <div style="
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #ddd;
                margin-bottom: 12px;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="font-size: 12px; color: #888; margin-bottom: 5px;">
                    {date_str} | <span style="color:#e63946; font-weight:bold;">{item['Source']}</span>
                </div>
                <h4 style="margin: 0 0 10px 0;">
                    <a href="{item['Link']}" target="_blank" style="text-decoration:none; color:#2c3e50; font-weight:600;">
                        {item['Title']}
                    </a>
                </h4>
            </div>
            """, unsafe_allow_html=True)

# 메인 앱 UI
def main():
    st.title("🚢 Real-time LNG News Tracker")
    st.markdown("현재 시점 기준 **최근 1~3개월** 이내의 최신 뉴스만 필터링하여 보여줍니다.")
    st.divider()

    # 기간 설정 사이드바 옵션 (사용자가 조절 가능하게)
    with st.sidebar:
        st.header("⚙️ 검색 설정")
        period_option = st.selectbox(
            "검색 기간 선택",
            ("최근 7일", "최근 30일", "최근 3개월", "기간 제한 없음"),
            index=1 # 기본값: 최근 30일
        )
        
        # 선택에 따른 코드 변환
        period_map = {
            "최근 7일": "7d",
            "최근 30일": "30d",
            "최근 3개월": "90d",
            "기간 제한 없음": "5y" # 사실상 전체
        }
        selected_period = period_map[period_option]
        
        st.info(f"현재 **{period_option}** 이내의 기사를 검색합니다.")

    tab1, tab2, tab3 = st.tabs(["🇴🇲 Oman LNG", "🌍 World LNG", "🇰🇷 Korea LNG"])

    with tab1:
        st.subheader(f"Oman Market Updates ({period_option})")
        if st.button("🔄 새로고침", key='btn1'): st.rerun()
        # 검색어: Oman LNG, Energy (범위를 약간 넓혀야 최신 기사가 잘 잡힘)
        news = get_google_news("Oman LNG energy gas project", 'en', period=selected_period)
        display_news(news)

    with tab2:
        st.subheader(f"Global Market Trends ({period_option})")
        if st.button("🔄 새로고침", key='btn2'): st.rerun()
        news = get_google_news("Global LNG price market trend", 'en', period=selected_period)
        display_news(news)

    with tab3:
        st.subheader(f"South Korea Updates ({period_option})")
        if st.button("🔄 새로고침", key='btn3'): st.rerun()
        # 한국어는 'when:30d'가 잘 안 먹힐 때가 있어 정렬 로직이 중요
        news = get_google_news("한국 LNG 가스공사 수급 도입", 'ko', period=selected_period)
        display_news(news)

if __name__ == "__main__":
    main()
