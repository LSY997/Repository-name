import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 应用配置
APP_TITLE = os.getenv('APP_TITLE', '乐新电子 - 电商绩效总控台')
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
DATA_FILE = os.getenv('DATA_FILE', 'performance_data.json')

# 用户账户配置
USERS = {
    "李绍远": {"password": "888888", "role": "director"},
    "庞宗建": {"password": "123456", "role": "operator"},
    "家华": {"password": "111111", "role": "operator"},
    "楚升": {"password": "222222", "role": "operator"},
    "杨华": {"password": "333333", "role": "operator"},
    "售前主管": {"password": "444444", "role": "supervisor"},
    "售后主管": {"password": "555555", "role": "supervisor"}
}

# 菜单配置
MENU_ITEMS = {
    "director": ["📊 全店绩效总览", "⚙️ 系统设置"],
    "supervisor": ["📝 数据录入", "📊 数据分析"],
    "operator": ["📝 数据录入", "📊 我的绩效"]
}
