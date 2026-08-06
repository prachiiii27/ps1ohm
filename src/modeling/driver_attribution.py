import shap

def calculate_shap_values(model, X):
    explainer = shap.TreeExplainer(model.model)
    shap_values = explainer.shap_values(X)
    return shap_values
