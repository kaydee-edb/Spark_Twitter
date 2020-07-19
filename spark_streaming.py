import findspark
findspark.init('/home/kaydee/spark-2.4.6-bin-hadoop2.7')
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc
from collections import namedtuple

sc = SparkContext()

ssc = StreamingContext(sc,10)
sqlContext= SQLContext(sc)

socket_stream = ssc.socketTextStream("127.0.0.1", 9999)

lines = socket_stream.window(60)

# We will be counting the tags from the stream
fields = ("tag", "count")
Tweet = namedtuple('Tweet', fields)

# Read each line and split the words into a list by space 
# Filter the words to only ones which contain #tags by 
# converting each word into lower. Then we will reduce the 
# word tuple by each word and convert it into a dataframe
# This dataframe will be registered as temporary table tweets 

(lines.flatMap(lambda text: text.split(' '))
.filter(lambda word: word.lower().startswith("#"))
.map(lambda word: (word.lower(), 1))
.reduceByKey(lambda a, b: a + b)
.map(lambda rec: Tweet( rec[0], rec[1]))
.foreachRDD(lambda rdd: rdd.toDF().sort(desc("count"))
.limit(10).registerTempTable("tweets")))

# Start the streaming context

ssc.start()

# Lets plot the tweets
import time
import matplotlib.pyplot as plt
import seaborn as sns

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



