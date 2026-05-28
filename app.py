import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime
from config import USERS, APP_TITLE, DATA_FILE, MENU_ITEMS

# --- 数据管理模块 ---
def load_data():
    """加载数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"operations": {}, "pre_sales": {}, "after_sales": {}}

def save_data(data):
    """保存数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 页面配置 ---
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS 美化 ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 " + APP_TITLE)

# --- 1. 登录与身份识别 ---
if "user_info" not in st.session_state:
    st.sidebar.header("🔐 身份验证")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://img.icons8.com/color/96/000000/login.png", width=80)
    
    with col2:
        st.subheader("欢迎登录")
    
    username = st.sidebar.text_input("👤 姓名")
    password = st.sidebar.text_input("🔑 6位数字密码", type="password")
    
    if st.sidebar.button("✅ 登录", use_container_width=True):
        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
            st.session_state["user_info"] = {"name": username, "role": role}
            st.rerun()
        else:
            st.sidebar.error("❌ 用户名或密码错误")
    
    st.info("💡 提示：请使用正确的用户名和密码登录系统")

else:
    user = st.session_state["user_info"]
    
    # 侧边栏用户信息
    st.sidebar.success(f"✅ 当前用户: {user['name']}")
    st.sidebar.info(f"角色: {get_role_name(user['role'])}")
    
    if st.sidebar.button("🚪 退出登录", use_container_width=True):
        del st.session_state["user_info"]
        st.rerun()
    
    st.sidebar.divider()
    
    # --- 2. 数据录入模块 (运营/主管) ---
    if user['role'] in ['operator', 'supervisor']:
        st.header("📝 数据录入")
        data = load_data()
        
        tab1, tab2, tab3 = st.tabs(["📊 运营数据", "☎️ 售前接待", "📦 售后跟踪"])
        
        with tab1:
            if user['role'] == 'operator':
                st.subheader(f"👤 {user['name']} - 今日运营数据")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    visitors = st.number_input("👥 访客数", min_value=0, value=0)
                with col2:
                    views = st.number_input("👀 浏览量", min_value=0, value=0)
                with col3:
                    sales = st.number_input("💰 销售额 (¥)", min_value=0.0, value=0.0, step=0.01)
                with col4:
                    orders = st.number_input("📦 订单数", min_value=0, value=0)
                
                ad_cost = st.number_input("💳 广告花费 (¥)", min_value=0.0, value=0.0, step=0.01)
                
                if st.button("✅ 提交运营数据", use_container_width=True):
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    if user['name'] not in data['operations']:
                        data['operations'][user['name']] = {}
                    
                    data['operations'][user['name']][date_str] = {
                        "visitors": int(visitors),
                        "views": int(views),
                        "sales": float(sales),
                        "orders": int(orders),
                        "ad_cost": float(ad_cost)
                    }
                    save_data(data)
                    st.success("✅ 运营数据已保存！")
                    
                    # 显示统计
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.metric("访客数", visitors)
                    with col2:
                        st.metric("浏览量", views)
                    with col3:
                        st.metric("销售额", f"¥{sales:.2f}")
                    with col4:
                        st.metric("订单数", orders)
                    with col5:
                        conversion_rate = (orders / visitors * 100) if visitors > 0 else 0
                        st.metric("转化率", f"{conversion_rate:.2f}%")

        with tab2:
            if user['name'] == "售前主管" or user['role'] == 'supervisor':
                st.subheader("☎️ 售前接待录入")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    reception = st.number_input("📞 今日接待量", min_value=0, value=0)
                with col2:
                    intention = st.number_input("🎯 意向客户数", min_value=0, value=0)
                with col3:
                    conversion = st.number_input("📈 咨询转化率 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
                
                if st.button("✅ 提交售前数据", use_container_width=True):
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    data['pre_sales'][date_str] = {
                        "reception": int(reception),
                        "intention": int(intention),
                        "conversion": float(conversion)
                    }
                    save_data(data)
                    st.success("✅ 售前数据已保存！")

        with tab3:
            if user['name'] == "售后主管" or user['role'] == 'supervisor':
                st.subheader("📦 售后跟踪录入")
                
                col1, col2 = st.columns(2)
                with col1:
                    returns = st.number_input("🔄 退货申请数", min_value=0, value=0)
                with col2:
                    disputes = st.number_input("⚠️ 纠纷单数", min_value=0, value=0)
                
                if st.button("✅ 提交售后数据", use_container_width=True):
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    data['after_sales'][date_str] = {
                        "returns": int(returns),
                        "disputes": int(disputes)
                    }
                    save_data(data)
                    st.success("✅ 售后数据已保存！")

    # --- 3. 总监总控台 ---
    elif user['role'] == 'director':
        st.header("📊 全店绩效总览")
        data = load_data()
        
        # 关键指标
        col1, col2, col3, col4 = st.columns(4)
        
        total_sales = 0
        total_orders = 0
        total_visitors = 0
        total_ad_cost = 0
        
        for name, records in data.get('operations', {}).items():
            for record in records.values():
                total_sales += record.get('sales', 0)
                total_orders += record.get('orders', 0)
                total_visitors += record.get('visitors', 0)
                total_ad_cost += record.get('ad_cost', 0)
        
        with col1:
            st.metric("💰 总销售额", f"¥{total_sales:.2f}")
        with col2:
            st.metric("📦 总订单数", total_orders)
        with col3:
            st.metric("👥 总访客数", total_visitors)
        with col4:
            roi = (total_sales - total_ad_cost) / total_ad_cost * 100 if total_ad_cost > 0 else 0
            st.metric("📈 ROI", f"{roi:.2f}%")
        
        st.divider()
        
        # 运营汇总分析
        st.subheader("💼 运营团队销售占比")
        ops_data = []
        for name, records in data.get('operations', {}).items():
            total_name_sales = sum(r.get('sales', 0) for r in records.values())
            ops_data.append({"姓名": name, "总销售额": total_name_sales})
        
        if ops_data:
            df_ops = pd.DataFrame(ops_data)
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(df_ops, values='总销售额', names='姓名', title='各运营销售贡献占比')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.subheader("📊 销售排行")
                df_ops_sorted = df_ops.sort_values('总销售额', ascending=False)
                st.dataframe(df_ops_sorted, hide_index=True, use_container_width=True)
        else:
            st.info("📭 暂无运营数据")

        # 售前/售后概览
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("☎️ 售���转化趋势")
            pre_data = data.get('pre_sales', {})
            if pre_data:
                df_pre = pd.DataFrame(pre_data).T.reset_index()
                df_pre.columns = ['日期', '接待量', '意向客户', '转化率']
                
                fig_line = px.line(df_pre, x='日期', y='转化率', markers=True, title='转化率趋势')
                st.plotly_chart(fig_line, use_container_width=True)
                
                st.dataframe(df_pre, hide_index=True, use_container_width=True)
            else:
                st.info("📭 暂无售前数据")
        
        with col2:
            st.subheader("⚠️ 售后风险预警")
            after_data = data.get('after_sales', {})
            if after_data:
                df_after = pd.DataFrame(after_data).T.reset_index()
                df_after.columns = ['日期', '退货数', '纠纷数']
                
                fig_bar = px.bar(df_after, x='日期', y=['退货数', '纠纷数'], barmode='group', title='售后指标对比')
                st.plotly_chart(fig_bar, use_container_width=True)
                
                st.dataframe(df_after, hide_index=True, use_container_width=True)
            else:
                st.info("📭 暂无售后数据")

def get_role_name(role):
    """获取角色名称"""
    role_names = {
        "director": "总监",
        "supervisor": "主管",
        "operator": "操作员"
    }
    return role_names.get(role, "未知")
