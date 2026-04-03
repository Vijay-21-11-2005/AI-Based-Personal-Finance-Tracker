import numpy as np
from sklearn.linear_model import LinearRegression

class ExpensePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def predict_next_month(self, monthly_data):
        """
        monthly_data: list of total spending per month
        """
        if len(monthly_data) < 2:
            return sum(monthly_data) / len(monthly_data) if monthly_data else 0
        
        X = np.array(range(len(monthly_data))).reshape(-1, 1)
        y = np.array(monthly_data)
        
        self.model.fit(X, y)
        next_month_idx = len(monthly_data)
        prediction = self.model.predict([[next_month_idx]])
        return max(0, prediction[0])
