
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="My Stock AI",
    page_icon="📈",
    layout="wide"
)

st.title("📈 My Stock AI")
st.caption("保有株管理アシスタント")

# データの初期化
if "stocks" not in st.session_state:
    st.session_state.stocks = pd.DataFrame(
        columns=[
            "銘柄コード",
            "銘柄名",
            "保有株数",
            "取得単価",
            "現在株価"
        ]
    )

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=[
            "取引日",
            "取引種類",
            "銘柄名",
            "株数",
            "単価"
        ]
    )

if "dividends" not in st.session_state:
    st.session_state.dividends = pd.DataFrame(
        columns=["銘柄名", "配当金"]
    )

# タブ
tab1, tab2, tab3, tab4 = st.tabs(
    ["資産状況", "保有株管理", "売買履歴", "配当管理"]
)

# --------------------
# 資産状況
# --------------------
with tab1:
    st.subheader("資産状況")

    stocks = st.session_state.stocks.copy()

    if not stocks.empty:
        stocks["評価額"] = (
            stocks["保有株数"] * stocks["現在株価"]
        )

        stocks["取得金額"] = (
            stocks["保有株数"] * stocks["取得単価"]
        )

        stocks["評価損益"] = (
            stocks["評価額"] - stocks["取得金額"]
        )

        total_value = stocks["評価額"].sum()
        total_cost = stocks["取得金額"].sum()
        total_profit = total_value - total_cost

        profit_rate = (
            total_profit / total_cost * 100
            if total_cost > 0 else 0
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "評価額",
            f"¥{total_value:,.0f}"
        )

        c2.metric(
            "取得金額",
            f"¥{total_cost:,.0f}"
        )

        c3.metric(
            "評価損益",
            f"¥{total_profit:,.0f}",
            f"{profit_rate:.2f}%"
        )

        st.subheader("保有銘柄")

        st.dataframe(
            stocks,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("銘柄別評価額")

        st.bar_chart(
            stocks.set_index("銘柄名")["評価額"]
        )

    else:
        st.info("保有株を登録してください。")

# --------------------
# 保有株管理
# --------------------
with tab2:
    st.subheader("保有株管理")

    st.write("保有株を追加してください。")

    with st.form("stock_form"):
        code = st.text_input("銘柄コード")
        name = st.text_input("銘柄名")

        shares = st.number_input(
            "保有株数",
            min_value=0.0,
            value=1.0
        )

        cost = st.number_input(
            "取得単価（円）",
            min_value=0.0,
            value=0.0
        )

        price = st.number_input(
            "現在株価（円）",
            min_value=0.0,
            value=0.0
        )

        submit = st.form_submit_button("登録")

        if submit:
            if code and name:
                new_stock = pd.DataFrame([{
                    "銘柄コード": code,
                    "銘柄名": name,
                    "保有株数": shares,
                    "取得単価": cost,
                    "現在株価": price
                }])

                st.session_state.stocks = pd.concat(
                    [
                        st.session_state.stocks,
                        new_stock
                    ],
                    ignore_index=True
                )

                st.success("登録しました。")
                st.rerun()

    st.divider()

    st.subheader("保有株の編集")

    edited = st.data_editor(
        st.session_state.stocks,
        num_rows="dynamic",
        use_container_width=True
    )

    if st.button("保有株を更新"):
        st.session_state.stocks = edited
        st.success("更新しました。")
        st.rerun()

# --------------------
# 売買履歴
# --------------------
with tab3:
    st.subheader("売買履歴")

    with st.form("history_form"):
        trade_date = st.date_input(
            "取引日",
            value=date.today()
        )

        trade_type = st.selectbox(
            "取引種類",
            ["購入", "売却"]
        )

        trade_name = st.text_input("銘柄名")

        trade_shares = st.number_input(
            "株数",
            min_value=0.0,
            value=1.0
        )

        trade_price = st.number_input(
            "取引単価",
            min_value=0.0,
            value=0.0
        )

        history_submit = st.form_submit_button(
            "履歴を追加"
        )

        if history_submit and trade_name:
            new_history = pd.DataFrame([{
                "取引日": str(trade_date),
                "取引種類": trade_type,
                "銘柄名": trade_name,
                "株数": trade_shares,
                "単価": trade_price
            }])

            st.session_state.history = pd.concat(
                [
                    st.session_state.history,
                    new_history
                ],
                ignore_index=True
            )

            st.success("履歴を追加しました。")
            st.rerun()

    st.dataframe(
        st.session_state.history,
        use_container_width=True,
        hide_index=True
    )

# --------------------
# 配当管理
# --------------------
with tab4:
    st.subheader("配当管理")

    with st.form("dividend_form"):
        dividend_name = st.text_input("銘柄名")

        dividend_amount = st.number_input(
            "受取配当金（円）",
            min_value=0.0,
            value=0.0
        )

        dividend_submit = st.form_submit_button(
            "配当を登録"
        )

        if dividend_submit and dividend_name:
            new_dividend = pd.DataFrame([{
                "銘柄名": dividend_name,
                "配当金": dividend_amount
            }])

            st.session_state.dividends = pd.concat(
                [
                    st.session_state.dividends,
                    new_dividend
                ],
                ignore_index=True
            )

            st.success("配当を登録しました。")
            st.rerun()

    st.dataframe(
        st.session_state.dividends,
        use_container_width=True,
        hide_index=True
    )

    total_dividend = (
        st.session_state.dividends["配当金"].sum()
    )

    st.metric(
        "配当金合計",
        f"¥{total_dividend:,.0f}"
    )

# --------------------
# CSV保存
# --------------------
st.sidebar.header("データ保存")

st.sidebar.download_button(
    "保有株を保存",
    st.session_state.stocks.to_csv(
        index=False
    ).encode("utf-8-sig"),
    "stocks.csv",
    "text/csv"
)

st.sidebar.download_button(
    "売買履歴を保存",
    st.session_state.history.to_csv(
        index=False
    ).encode("utf-8-sig"),
    "history.csv",
    "text/csv"
)

st.sidebar.download_button(
    "配当を保存",
    st.session_state.dividends.to_csv(
        index=False
    ).encode("utf-8-sig"),
    "dividends.csv",
    "text/csv"
)

st.sidebar.caption(
    "現在株価は手入力です。"
    "リアルタイム株価ではありません。"
)
