import pandas as pd
import streamlit as st
from datetime import datetime

inventory_data = {
    'Item': ['Fabric', 'Ready-made', 'Fabric', 'Ready-made'],
    'Type': ['Raw', 'Finished', 'Raw', 'Finished'],
    'Quantity': [100, 50, 150, 70],
    'Price per Unit': [20, 100, 20, 100],
    'Total Value': [2000, 5000, 3000, 7000]
}

inventory_df = pd.DataFrame(inventory_data)

invoices_data = {
    'Invoice ID': [1, 2, 3],
    'Date': [datetime(2025, 5, 1), datetime(2025, 5, 2), datetime(2025, 5, 3)],
    'Item Sold': ['Ready-made', 'Ready-made', 'Fabric'],
    'Quantity Sold': [2, 3, 10],
    'Total Sale': [300, 400, 200],
}

invoices_df = pd.DataFrame(invoices_data)

cash_data = {
    'Cash Register': ['Main Cash', 'Shipping Cash'],
    'Amount': [10000, 2000]
}

cash_df = pd.DataFrame(cash_data)

st.title('نظام إدارة الحسابات والمخزون والمبيعات')

st.header('المخزون')
st.dataframe(inventory_df)

st.header('الفواتير')
st.dataframe(invoices_df)

st.header('الخزائن')
st.dataframe(cash_df)

st.header('تقرير مبيعات')
report_type = st.selectbox('اختار نوع التقرير', ['يومي', 'أسبوعي', 'شهري'])

if report_type == 'يومي':
    selected_date = st.date_input('اختار التاريخ', datetime.today())
    daily_report = invoices_df[invoices_df['Date'] == pd.to_datetime(selected_date)]
    if daily_report.empty:
        st.write("لا توجد مبيعات لهذا اليوم.")
    else:
        st.write('تقرير المبيعات اليومي:', daily_report)
elif report_type == 'أسبوعي':
    start_date = st.date_input('اختار بداية الأسبوع', datetime.today() - pd.Timedelta(days=7))
    end_date = st.date_input('اختار نهاية الأسبوع', datetime.today())
    weekly_report = invoices_df[(invoices_df['Date'] >= pd.to_datetime(start_date)) & 
                                 (invoices_df['Date'] <= pd.to_datetime(end_date))]
    if weekly_report.empty:
        st.write("لا توجد مبيعات لهذا الأسبوع.")
    else:
        st.write('تقرير المبيعات الأسبوعي:', weekly_report)
else:
    start_date = st.date_input('اختار بداية الشهر', datetime.today().replace(day=1))
    end_date = st.date_input('اختار نهاية الشهر', datetime.today())
    monthly_report = invoices_df[(invoices_df['Date'] >= pd.to_datetime(start_date)) & 
                                 (invoices_df['Date'] <= pd.to_datetime(end_date))]
    if monthly_report.empty:
        st.write("لا توجد مبيعات لهذا الشهر.")
    else:
        st.write('تقرير المبيعات الشهري:', monthly_report)

st.header('إضافة عملية مالية')
cash_action = st.selectbox('اختار نوع العملية', ['إيداع', 'سحب'])

amount = st.number_input('المبلغ', min_value=0, step=100)

if st.button('تنفيذ العملية'):
    if cash_action == 'إيداع':
        cash_df.loc[cash_df['Cash Register'] == 'Main Cash', 'Amount'] += amount
        st.success(f'تم إضافة {amount} إلى الخزينة الرئيسية.')
    else:
        cash_df.loc[cash_df['Cash Register'] == 'Main Cash', 'Amount'] -= amount
        st.success(f'تم سحب {amount} من الخزينة الرئيسية.')

st.dataframe(cash_df)
