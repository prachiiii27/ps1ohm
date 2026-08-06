import xgboost as xgb
import numpy as np

class PhysicsInformedHeatModel:
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=1500, 
            learning_rate=0.01, 
            max_depth=10,
            subsample=0.75,
            colsample_bytree=0.8,
            min_child_weight=2,
            gamma=0.05,
            objective='reg:squarederror'
        )
    
    def custom_thermodynamic_loss(self, y_pred, dtrain):
        labels = dtrain.get_label()
        grad = (y_pred - labels)
        hess = np.ones_like(labels)
        return grad, hess

    def fit(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
