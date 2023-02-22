# similarity_join.py
import re
import pandas as pd

class SimilarityJoin:
	def __init__(self, data_file1, data_file2):
		self.df1 = pd.read_csv(data_file1)
		self.df2 = pd.read_csv(data_file2)
		
	def concat_row(self, x):
		l = x.to_numpy().astype(str)
		return ' '.join(l)

	def tokenize(self, col_value):
		tokens = re.split(r'\W+', col_value)
		return [token.lower().strip() for token in tokens if(token!='')]

	def jaccard(self,x):
		return len(set(x['joinKey1']) & set(x['joinKey2']))/len(set(x['joinKey1']) | set(x['joinKey2']))

	def preprocess_df(self, df, cols):          
		df['concat_col'] = df[cols].apply(self.concat_row, axis=1)
		df['joinKey'] = df['concat_col'].apply(self.tokenize)
		return df.drop('concat_col',axis = 1)
			
	def filtering(self, df1, df2):
		df1['j'] = df1['joinKey']
		df2['j'] = df2['joinKey']
		df1 = df1.explode('j')
		df2 = df2.explode('j')
		res = pd.merge(df1, df2, on='j', suffixes=('1', '2'))
		res = res[['id1', 'joinKey1', 'id2', 'joinKey2']]
		res = res.drop_duplicates(subset=['id1','id2'])
		return res

	def verification(self, cand_df, threshold):
		cand_df['jaccard'] = cand_df.apply(self.jaccard, axis=1)
		cand_df = cand_df[cand_df['jaccard']>=threshold]
		return cand_df
		
	def evaluate(self, result, ground_truth):
		R = len(result)
		T = len([x for x in result if x in ground_truth])
		A = len(ground_truth)
		precision = T/R
		recall = T/A 
		fmeasure = (2 *precision*recall) / (precision+recall)
		return (precision, recall, fmeasure)
		
	def jaccard_join(self, cols1, cols2, threshold):
		new_df1 = self.preprocess_df(self.df1, cols1)
		new_df2 = self.preprocess_df(self.df2, cols2)
		print ("Before filtering: %d pairs in total" %(self.df1.shape[0] *self.df2.shape[0])) 
		
		cand_df = self.filtering(new_df1, new_df2)
		print ("After Filtering: %d pairs left" %(cand_df.shape[0]))
		
		result_df = self.verification(cand_df, threshold)
		print ("After Verification: %d similar pairs" %(result_df.shape[0]))
		
		return result_df
	
		

if __name__ == "__main__":
	er = SimilarityJoin("Amazon_sample.csv", "Google_sample.csv")
	amazon_cols = ["title", "manufacturer"]
	google_cols = ["name", "manufacturer"]
	result_df = er.jaccard_join(amazon_cols, google_cols, 0.5)

	result = result_df[['id1', 'id2']].values.tolist()
	ground_truth = pd.read_csv("Amazon_Google_perfectMapping_sample.csv").values.tolist()
	print ("(precision, recall, fmeasure) = ", er.evaluate(result, ground_truth))