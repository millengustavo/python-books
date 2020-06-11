# Mastering Large Datasets with Python: Parallelize and Distribute Your Python Code

Authors: John T. Wolohan

[Available here](https://www.manning.com/books/mastering-large-datasets-with-python)

![cover](cover.png)

# Ch1. Introduction
Map and reduce style of programming:
- easily write parallel programs
- organize the code around two functions: `map` and `reduce`

> `MapReduce` = framework for parallel and distributed computing; `map` and `reduce` = style of programming that allows running the work in parallel with minimal rewriting and extend the work to distributed workflows

**Dask** -> another tool for managing large data without `map` and `reduce`

## Procedural programming
Program Workflow
1. Starts to run
2. issues an instruction
3. instruction is executed
4. repeat 2 and 3
5. finishes running

## Parallel programming
Program workflow
1. Starts to run
2. divides up the work into chunks of instructions and data
3. each chunk of work is executed independently
4. chunks of work are reassembled
5. finishes running

![map_reduce](map_reduce.png)

> The `map` and `reduce` style is applicable everywhere, but its specific strengths are in areas where you may need to scale

## The map function for transforming data
- `map`: function to transform sequences of data from one type to another
- Always retains the same number of objects in the output as were provided in the input
- performs one-to-one transformations -> is a great way to transform data so it is more suitable for use

> Declarative programming: focuses on explaining the logic of the code and not on specifying low-level details -> scaling is natural, the logic stays the same

## The reduce function for advanced transformations
- `reduce`: transform a sequence of data into a data structure of any shape or size
- MapReduce programming pattern relies on the `map` function to transform some data into another type of data and then uses the `reduce` function to combine that data
- performs one-to-any transformations -> is a great way to assemble data into a final result

## Distributed computing for speed and scale
Extension of parallel computing in which the computer resource we are dedicating to work on each chunk of a given task is its own machine

## Hadoop: A distributed framework for map and reduce
- Designed as an open source implementation of Google's original MapReduce framework
- Evolved into distributed computing software used widely by companies processing large amounts of data

## Spark for high-powered map, reduce, and more
- Something of a sucessor to the Apache Hadoop framework that does more of its work in memory instead of by writing to file
- Can run more than 100x faster than Hadoop

## AWS Elastic MapReduce (EMR) - Large datasets in the cloud
- Popular way to implement Hadoop and Spark
- tackle small problems with parallel programming as its cost effective
- tackle large problems with parallel programming because we can procure as many resources as we need

# Ch2. Accelerating large dataset work: Map and parallel computing