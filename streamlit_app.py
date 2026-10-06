import pandas as pd
import streamlit as st

st.set_page_config(page_title="Streamlit 요소 체험실", page_icon="📘", layout="wide")

st.title("Streamlit 요소 체험실")
st.markdown(
    "텍스트부터 차트까지, 웹 앱을 이루는 요소를 직접 눌러 보고 바꿔 보세요. "
    "각 요소의 설명과 작은 실습을 한곳에 모았습니다."
)
st.caption("화면의 입력을 바꾸면 앱이 다시 실행되며 결과가 바로 업데이트됩니다.")

overview = st.columns(3)
overview[0].metric("실습 주제", "3개")
overview[1].metric("직접 조작", "가능")
overview[2].metric("준비할 데이터", "없음")

input_tab, data_tab, layout_tab = st.tabs(
    ["1. 입력 위젯", "2. 표와 차트", "3. 배치와 피드백"]
)

with input_tab:
    st.header("입력 위젯")
    st.write("위젯은 사용자에게 값을 입력받거나 선택하게 하는 화면 요소입니다.")

    left, right = st.columns(2)
    with left:
        name = st.text_input("이름", value="민지", help="텍스트 한 줄을 입력합니다.")
        age = st.number_input("나이", min_value=1, max_value=120, value=20)
        topic = st.selectbox("먼저 알아볼 주제", ["텍스트", "데이터", "레이아웃"])
        mood = st.radio("오늘의 학습 기분", ["좋아요", "보통이에요", "조금 어려워요"], horizontal=True)

    with right:
        note = st.text_area("메모", placeholder="배우고 싶은 내용을 적어 보세요.")
        hours = st.slider("오늘 공부한 시간", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
        interests = st.multiselect(
            "관심 있는 위젯", ["버튼", "표", "차트", "폼", "파일 다운로드"], default=["버튼", "차트"]
        )
        show_summary = st.checkbox("입력한 내용으로 요약 보기", value=True)

    if st.button("입력값 확인", type="primary"):
        st.success(f"{name}님, '{topic}' 주제를 선택했어요. 나이는 {age}세, 기분은 {mood}입니다.")

    if show_summary:
        st.info(f"공부 시간: {hours:g}시간 · 관심 위젯: {', '.join(interests) if interests else '선택 없음'}")
        if note:
            st.write("메모:", note)

    st.progress(hours / 10, text=f"오늘의 공부 시간: {hours:g} / 10시간")

    with st.expander("텍스트 요소와 사용 예시 보기"):
        st.write("`st.title`은 큰 제목, `st.write`는 간단한 내용 표시, `st.caption`은 보조 설명에 사용합니다.")
        st.code('st.title("나의 첫 앱")\nst.write("화면에 내용을 표시합니다.")', language="python")

with data_tab:
    st.header("표와 차트")
    st.write("표에서 값을 직접 수정하거나 행을 추가해 보세요. 아래 차트가 같은 데이터를 사용합니다.")

    sample_data = pd.DataFrame(
        {
            "월": ["1월", "2월", "3월", "4월", "5월", "6월"],
            "방문자 수": [1200, 1450, 1380, 1760, 1930, 2150],
            "주문 수": [180, 220, 205, 270, 310, 355],
            "만족도": [4.1, 4.3, 4.2, 4.4, 4.6, 4.7],
        }
    )

    edited_data = st.data_editor(
        sample_data,
        hide_index=True,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "월": st.column_config.TextColumn("월", help="표시할 달 이름"),
            "방문자 수": st.column_config.NumberColumn("방문자 수", min_value=0, format="%d"),
            "주문 수": st.column_config.NumberColumn("주문 수", min_value=0, format="%d"),
            "만족도": st.column_config.NumberColumn("만족도", min_value=1.0, max_value=5.0, format="%.1f"),
        },
    )

    chart_metrics = st.multiselect(
        "차트에 표시할 항목", ["방문자 수", "주문 수", "만족도"], default=["방문자 수", "주문 수"]
    )
    if chart_metrics and not edited_data.empty:
        chart_left, chart_right = st.columns(2)
        with chart_left:
            st.subheader("선 그래프")
            st.line_chart(edited_data, x="월", y=chart_metrics, width="stretch")
        with chart_right:
            st.subheader("막대 그래프")
            st.bar_chart(edited_data, x="월", y=chart_metrics, width="stretch")
    else:
        st.warning("차트를 보려면 항목을 하나 이상 선택하고 표에 데이터를 남겨 두세요.")

    csv_data = edited_data.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "편집한 표를 CSV로 다운로드",
        data=csv_data,
        file_name="streamlit-실습-데이터.csv",
        mime="text/csv",
    )
    st.caption("`st.data_editor`는 수정할 수 있는 표, `st.line_chart`와 `st.bar_chart`는 기본 차트입니다.")

with layout_tab:
    st.header("배치와 피드백")
    st.write("열과 탭으로 내용을 나누고, 메시지와 폼으로 사용자의 행동에 반응할 수 있습니다.")

    metric_columns = st.columns(3)
    metric_columns[0].metric("완료한 실습", "2 / 3", "+1")
    metric_columns[1].metric("이번 주 학습", "4시간", "목표 5시간")
    metric_columns[2].metric("이해도", "좋아요", "상승")

    message_column, form_column = st.columns(2)
    with message_column:
        st.subheader("상태 메시지")
        st.success("성공: 작업이 완료됐어요.")
        st.info("안내: 이 상자는 참고할 정보를 보여 줍니다.")
        st.warning("주의: 중요한 내용을 눈에 띄게 알립니다.")
        st.error("오류: 문제가 생겼을 때 원인을 안내합니다.")

        with st.expander("레이아웃 요소"):
            st.write("이 내용은 펼치거나 접을 수 있는 영역 안에 있어요.")
            st.caption("`st.columns`는 나란한 배치, `st.expander`는 접이식 영역을 만듭니다.")

    with form_column:
        st.subheader("폼으로 학습 기록하기")
        st.write("폼 안의 값을 모아 제출 버튼을 눌렀을 때 한 번에 전달합니다.")
        with st.form("learning_form"):
            learned = st.text_input("오늘 배운 요소", placeholder="예: 슬라이더")
            understanding = st.select_slider(
                "이해도", options=["어려워요", "보통이에요", "쉬워요"], value="보통이에요"
            )
            submitted = st.form_submit_button("학습 기록 제출", type="primary")

        if submitted:
            if learned.strip():
                st.success(f"'{learned}' 기록 완료 · 이해도: {understanding}")
            else:
                st.warning("배운 요소를 입력한 뒤 제출해 주세요.")

    st.caption("`st.metric`은 핵심 수치, `st.form`은 여러 입력을 한 번에 제출할 때 유용합니다.")
