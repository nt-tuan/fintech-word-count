import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.gmm import GMM

# Tạo một DataFrame chứa dữ liệu
data = pd.read_csv('./data/data_for_sample_model.csv')
# data = data[data['BankName'] == "CTG"] 

# Xác định biến độc lập (features) và biến phụ thuộc (target)
X = data[['Year', 'SIZE', 'CAR', 'LDR', 'ROE', 'Fintech']]
Y = data['Risk']

# Thêm một cột hằng số (intercept) vào ma trận X
X = sm.add_constant(X)

# Định nghĩa lớp mô hình GMM
class MyGMM(GMM):
    def __init__(self, *args, **kwds):
        super(MyGMM, self).__init__(*args, **kwds)

    def momcond(self, params):
        # Định nghĩa các hàm mục tiêu (moment conditions) ở đây
        beta0, beta1, beta2, beta3, beta4, beta5, beta6 = params
        moments = Y - (beta0 + beta1*X['Year'] + beta2*X['SIZE'] + beta3*X['CAR'] + beta4*X['LDR'] + beta5*X['ROE'] + beta6*X['Fintech'])
        print(str(moments))
        return moments

# Khởi tạo mô hình GMM
model = MyGMM(endog=Y, exog=X, npars=7, instrument=None)

# Bắt đầu ước tính tham số
results = model.fit(start_params=np.zeros(7))

# In kết quả mô hình
print(results.summary())