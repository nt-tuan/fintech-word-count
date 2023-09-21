import pandas as pd
import statsmodels.api as sm
# Đọc dữ liệu từ tệp CSV
data = pd.read_csv('./data/data_for_sample_model.csv')
data = data[data['BankName'] == "CTG"] 

# Xác định biến độc lập (features) và biến phụ thuộc (target)
X = data[['Year', 'SIZE', 'CAR', 'LDR', 'ROE', 'Fintech']]
y = data['Risk']

# Thêm cột hằng số (intercept) vào mô hình
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())
