import xgboost as xgb
import numpy as np

class PhysicsInformedHeatModel:
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=800, 
            learning_rate=0.02, 
            max_depth=10,
            subsample=0.85,
            colsample_bytree=0.85,
            min_child_weight=3,
            gamma=0.1,
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
