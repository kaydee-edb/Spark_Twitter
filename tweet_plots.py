import time
import matplotlib.pyplot as plt
import seaborn as sns

def tweet_plots(sqlContext):
    count = 0

    while count < 10:
        time.sleep(3)
        top_10_tweets = sqlContext.sql('select tag, count from tweets')
        top_10_df = top_10_tweets.toPandas()
        display.clear_output(wait=True)
        sns.plt.figure(figsize = (10, 8))
        sns.barplot( x="count", y="tag", data = top_10_df)
        sns.plt.show()
        count = count + 1

        
