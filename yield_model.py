import pandas as pd 
data = pd.read_excel("Agri_data_Combine.xlsx")
# print(data.DESCR)

X = pd.DataFrame(data.data, columns=(data.feature_names))
y = pd.DataFrame(data.target, columns=['Target'])

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, test_size=0.3)


from sklearn.ensemble import RandomForestRegressor

def training_model():
    model = RandomForestRegressor(random_state=45,max_depth=16,n_estimators=200)
    trained_model = model.fit(X_train, y_train)
    return trained_model