import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt

data = pd.read_csv('spy.csv')

#split the data into training and testing data set
train_data = data.iloc[:int(.99*len(data)), :]
test_data = data.iloc[int(.99*len(data)):, :]

#Define the features and target varaible
features = ['Open' , 'Volume']
target = 'Close'

#Create and train the model
model = xgb.XGBRegressor()
model.fit(train_data[features], train_data[target])

#Make and show Predictions on the test data
predictions = model.predict(test_data[features])
print('Model Predictions:')
print(predictions)

#Show the Actual Values
print('Actual Values:')
print(test_data[target])

#Show the Models Accuracy
accuracy = model.score(test_data[features], test_data[target])
print('Accuracy:')
print(accuracy)

#Plot the predictions and the close price
plt.plot(data['Close'], label='Close Price')
plt.plot(test_data[target].index, predictions, label = 'Predictions')
plt.legend()
plt.show()
