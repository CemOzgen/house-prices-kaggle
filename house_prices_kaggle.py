# -*- coding: utf-8 -*-
"""house-prices-kaggle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oBTTIVQPuUOjVxPi3ABY4i--pr-gCOWZ
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import seaborn as sns

train = pd.read_csv('train.csv')
train_sale_price = train['SalePrice']
train = train.drop('SalePrice', axis=1)
x_train = train.drop('Id', axis=1)
test = pd.read_csv('test.csv')
x_test = test.drop('Id', axis=1)

x_train20 = x_train[['LotArea','MiscVal','2ndFlrSF','BsmtFinSF1','PoolArea','BsmtFinSF2', 'MasVnrArea', 'BsmtUnfSF', 'LowQualFinSF','GrLivArea','TotalBsmtSF','3SsnPorch','ScreenPorch','WoodDeckSF','1stFlrSF','EnclosedPorch','GarageArea','GarageYrBlt','OpenPorchSF','MSSubClass']]
x_test20 = x_test[['LotArea','MiscVal','2ndFlrSF','BsmtFinSF1','PoolArea','BsmtFinSF2', 'MasVnrArea', 'BsmtUnfSF', 'LowQualFinSF','GrLivArea','TotalBsmtSF','3SsnPorch','ScreenPorch','WoodDeckSF','1stFlrSF','EnclosedPorch','GarageArea','GarageYrBlt','OpenPorchSF','MSSubClass']]

x_test20

x_train20 = x_train20.fillna(0)
x_test20 = x_test20.fillna(0)

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

best_features = SelectKBest(score_func=chi2, k=20)
fit = best_features.fit(x_train20,train_sale_price)
dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(x_train20.columns)
featureScores = pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns = ['Specs','Score']
print(featureScores.nlargest(20,'Score'))

x_train20 = pd.get_dummies(x_train20)
x_test20 = pd.get_dummies(x_test20)
x_test20

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self,epoch,logs={}):
    if (logs.get('accuracy')>0.90):
      print("\nReached %90 accuracy, so cancelling training!")
      self.model.stop_training = True

callbacks = myCallback()

from sklearn.preprocessing import StandardScaler
std = StandardScaler()
std.fit(pd.concat([x_train20,x_test20],axis=0))
x_train20 = scaler.transform(x_train20)
x_test20 = scaler.transform(x_test20)



model = tf.keras.Sequential([
                             tf.keras.layers.Dense(32, activation = 'relu'),
                             tf.keras.layers.Dense(1)                             
])

model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics= ['accuracy'])

model.fit(x_train20, train_sale_price,batch_size=128, epochs = 1000, callbacks = [callbacks])

losses = pd.DataFrame(model.history.history)
losses.plot()

test_sale_prices = model.predict(x_test20)

test_for_id = pd.read_csv('test.csv')

Id = test_for_id['Id'] 
Id

df = pd.DataFrame(test_sale_prices)

df['Id'] = Id

df = df[['Id', 0]]

df.columns = ['Id', 'SalePrice']

df

df.to_csv('submission3.csv', index = False)

