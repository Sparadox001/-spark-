上传数据到hdfs

```scala
./bin/hdfs dfs -put /home/hadoop/data/game_of_thrones.csv
```



## （1）根据剧集主要内容统计任务出现词频

1、读取csv

```
 var data_df = spark.read.format("csv").option("header", "True").load("/user/hadoop/game_of_thrones")
```

2、 抽出主要剧集desc一列

```
val desc_df = data_df.select(data_df("desc"))
```

3、统计词频

```scala
var words = desc_df.flatMap(row=>row.getString(0).split(" ")).toDF() 
words.groupBy("value").count().orderBy($"count".desc) 
```

4、去停用词

```scala
val filteredWords = words.filter(!($"value".equalTo("the") || $"value".equalTo("The") ||
      $"value".equalTo("a") || $"value".equalTo("A") ||
      $"value".equalTo("an") || $"value".equalTo("An") ||
      $"value".equalTo("as") || $"value".equalTo("from") ||
      $"value".equalTo("is") || $"value".equalTo("are") ||
      $"value".equalTo("and") || $"value".equalTo("has") ||
      $"value".equalTo("with") || $"value".equalTo("to") ||
      $"value".equalTo("of") || $"value".equalTo("for") ||
      $"value".equalTo("at") || $"value".equalTo("in") ||
      $"value".equalTo("his") || $"value".equalTo("her")))

```

5、导出csv文件方便后续数据可视化处理

```scala
filteredWords.write.option("header", "true").csv("top_words")
```



## （2）对每一季的观看人数、IMDb评分还有参与评分的人数进行分析



1、从数据表中选取season、us_viewers、imdb_rating、total_votes这四列，并且定义好各列的数据类型

```scala
val season_df = data_df.select(data_df("season").cast("int"),
data_df("us_viewers").cast("int"),data_df("imdb_rating").cast("float")
      ,data_df("total_votes").cast("int"))
```

2、接下来我们按照season进行分组聚合，然后计算出其他三列的平均值：

```scala
// 按季节分组并计算其他三列的平均值
val season_avg_df = season_df.groupBy("season").agg(
    avg("us_viewers").alias("avg_us_viewers"),
    avg("imdb_rating").alias("avg_imdb_rating"),
    avg("total_votes").alias("avg_total_votes")
)
//按season升序
val season_avg_df_order = season_avg_df.orderBy($"season".asc
```

3、将结果保存为csv文件

```scala
season_avg_df_order.write.option("header", "true").csv("season_avgdata")
```

## （3）分析不同的导演和评分的关系

1、首先从数据表中选取directed_by、imdb_rating这两列，

```scala
val director_df = data_df.select(data_df("directed_by"), data_df("imdb_rating").cast("float"))
```

2、按照directed_by这一列进行聚合，计算评分的平均值，排序，

```scala
val director_avgdata = director_df.groupBy("directed_by").
      mean("imdb_rating").orderBy($"avg(imdb_rating)".desc).toDF()
```

3、导出不同的导演拍摄的剧集的平均得分

```scala
director_avgdata.write.option("header", "true").csv("director_avgdata")
```

4、对数据表中的directed_by这一列分组聚合后进行count()计数

```scala
val director_count = director_df.groupBy("directed_by").count().orderBy($"count".desc)
```

5、导出不同导演执教占比

```scala
director_count.write.option("header", "true").csv("director_countdata")
```



## （4） 分析不同作者和评分的关系

1、先选取written_by、imdb_rating这两列，之后根据written_by这列进行分组聚合，计算imdb_rating的平均，这样就得到了不同剧集的作者的平均得分。

```scala
val writer_df = data_df.select(data_df("written_by"),data_df("imdb_rating").cast("float"))
val writer_avgdata = writer_df.groupBy("written_by").mean("imdb_rating").orderBy($"avg(imdb_rating)".desc).toDF()

 writer_avgdata.write.option("header", "true").csv("file:///home/hadoop/data/writer_avgdata.csv")
```

2、不同作者占比

```scala
val writer_countdata = writer_df.groupBy("written_by").count().orderBy($"count".desc)

 writer_countdata.write.option("header", "true").csv("file:///home/hadoop/data/writer_countdata.csv")
```

## （5） 整部剧评分最高的剧集和评分最低的剧集

```scala
val first_video_msg = data_df.orderBy($"imdb_rating".desc).first()
println(first_video_msg)
val last_video_msg = data_df.orderBy("imdb_rating").first()
println(last_video_msg)
```


