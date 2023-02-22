import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import copy
import ast


class AnomalyDetection():

	#function for faltten N-D list to 1-D list
	def flatten(self, x):
		res = []
		for feature in x:
			if(isinstance(feature,int) or isinstance(feature, float)):
				res.append(feature)
			else:
				for dim in feature:
					res.append(dim)
		return res

	#generate feature dataframe, each dimension as one column
	def get_feature_df(self, df):
		feature = df['features']
		col_num = len(feature[0])
		col_name = [str(i) for i in range(col_num)]
		df1 = pd.DataFrame(df['features'].tolist(), columns=col_name)
		return df1

	def scaleNum(self, df, indices):
		df1 = self.get_feature_df(df)
		for i in indices:
			name = str(i)
			#get mean and std deviation
			mean = df1[name].mean()
			std = df1[name].std()
			#normalization
			df1[name] = (df1[name]-mean)/std
		#replace nan to 0 to avoid divide by 0
		df1.fillna(0, inplace=True)
		df1['features'] = df1.values.tolist()
		df = df.drop(columns = ['features'])
		scale = df1['features']
		df = df.merge(scale, left_index = True, right_index = True).reset_index()
		df = df.drop(columns = ['index'])
		return df

	def cat2Num(self, df, indices):
		df1 = self.get_feature_df(df)
		
		#self-implemented one-hot encoding
		for i in indices:
			name = str(i)
			#number of encoding digit is the number of different values 
			digit = df1[name].unique()
			encode_dict = {}
			encode = [0 for i in range(len(digit))]
			#for each different value, give it an ecoding with only one digit of 1
			for index, d in enumerate(digit):
				encode_dict[d] = copy.deepcopy(encode)
				encode_dict[d][index] = 1
			#use the encoding dictionary to perform one-hot encoding
			df1[name] = df1[name].map(lambda x: encode_dict[x])
		df1['features'] = df1.values.tolist()
		df1['features'] = df1['features'].apply(lambda x: self.flatten(x))

		#merge encoding to original dataframe
		df = df.drop(columns = ['features'])
		encode = df1['features']
		df = df.merge(encode, left_index = True, right_index = True)
		
		return df
				
	def detect(self, df, k, t):
		#sue sklearn tool kit to perform kmeans
		train_x = list(df['features'])
		kmeans = KMeans(n_clusters=k)
		labels = kmeans.fit_predict(train_x)
		df['label'] = labels

		#count each label's number
		new_df = df[['features', 'label']].groupby('label', as_index=False).count()
		new_df = new_df.rename(columns = {"features":"count"})
		df = df.merge(new_df, left_on = 'label', right_on = 'label')
		
		#calculate score
		min = df['count'].min()
		max = df['count'].max()
		divisor = max-min
		df['score'] = (max-df['count'])/divisor
		df = df.drop(df[df['score']<t].index)

		df = df[['id','features','score']]
		return df
	
if __name__ == "__main__":
	pd.set_option('display.max_colwidth', None)
	#notice that pandas would read features as json string
	df = pd.read_csv('logs-features-sample.csv',converters={'features': ast.literal_eval})

	ad = AnomalyDetection()
	df1 = ad.cat2Num(df, [0,1])
	print(df1)

	df2 = ad.scaleNum(df1, [6])
	print(df2)

	df3 = ad.detect(df2, 8, 0.97)
	print(df3)