import pandas as pd
from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec

pd.set_option('display.max_columns', None)

def read_file():
    file_name = "cleaned_text.csv"
    df = pd.read_csv(file_name)
    df = df.drop("Unnamed: 0", axis=1)
    # Drop rows with any NaN in the selected columns only
    df = df.dropna(how='any', subset=['text'])
    df  = df.reset_index()
    df = df.drop(df.index[1])
    df = df.drop(df.index[12])
    df = df.drop(df.index[34])
    df = df.drop(df.index[154])
    df = df.drop(df.index[953]) # incredibly slow
    df = df.reset_index()
    return df

df = read_file()
print("read file... done")

my_text = []
for i in range(df.shape[0]):
    cur = df.loc[i,"text"]
    cur = cur.split()
    my_text.insert(i, cur)
print("compile corpora... done")

path = get_tmpfile("word2vec.model")
model = Word2Vec(my_text, size=100, window=5, min_count=1, workers=4)
model.train(my_text, total_examples=model.corpus_count, epochs=model.corpus_count)
model.save("word2vec.model")
print("train model... done")

print("======start adding vectors to dataset========")
for i in range(df.shape[0]):
    cur = df.loc[i,"text"]
    cur = cur.split()
    print("element " + str(i) + " of " + str(df.shape[0]))
    if len(cur) < 30:
        for j in range(len(cur)):
            for v in range(100):
                df.loc[i, j*100 + v + 8] = model.wv[str(cur[j])][v]
    else:
        print("not included -----------------------------------------------------------" + str(i))

print("adding vectors ... done")

result_file_name = "final.csv"
df.to_csv(result_file_name)
print("dataset has been saved to file")
