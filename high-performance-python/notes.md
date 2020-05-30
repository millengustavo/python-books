# High performance Python: Practical Performant Programming for Humans

Authors: Micha Gorelick, Ian Ozsvald

![cover](cover.jpg)

> "Every programmer can benefit from understanding how to build performant systems (...) When something becomes ten times cheaper in time or compute costs, suddenly the set of applications you can address is wider than you imagined"

Supplemental material for the book (code examples, exercises, etc.) is available for download at https://github.com/mynameisfiber/high_performance_python_2e.

# Ch1. Understanding Performant Python

## Why use Python?
- highly expressive and easy to learn
- `scikit-learn` wraps LIBLINEAR and LIBSVM (written in C)
- `numpy` includes BLAS and other C and Fortran libraries
- python code that properly utilizes these modules can be as fast as comparable C code
- "batteries included"
- enable fast prototyping of an idea

## How to be a highly performant programmer
Overall team velocity is far more important than speedups and complicated solutions. Several factors are key to this:
- Good structure
- Documentation
- Debuggability
- Shared standards

# Ch2. Profiling to Find Bottlenecks

Profiling let you make the most pragmatic decisions for the least overall effort: Code run "fast enough" and "lean enough"

> "If you avoid profiling and jump to optmization, you'll quite likely do more work in the long run. Always be driven by the results of profiling"

*"Embarrassingly parallel problem"*: no data is shared between points

`timeit` module temporarily disables the garbage collector

## cProfile module
Built-in profiling tool in the standard library

- `profile`: original and slower pure Python profiler
- `cProfile`: same interface as `profile` and is written in `C` for a lower overhead

1. Generate a *hypothesis* about the speed of parts of your code
2. Measure how wrong you are
3. Improve your intuition about certain coding styles

### Visualizing cProfile output with Snakeviz
`snakeviz`: visualizer that draws the output of `cProfile` as a diagram -> larger boxes are areas of code that take longer to run

## Using line_profiler for line-by-line measurements
`line_profilier`: strongest tool for identifying the cause of CPU-bound problems in Python code: profile individual functions on a line-by-line basis

Be aware of the complexity of **Python's dynamic machinery**

The order of evaluation for Python statements is both **left to right and opportunistic**: put the cheapest test on the left side of the equation

## Using memory_profiler to diagnose memory usage
`memory_profiler` measures memory usage on a line-by-line basis:
- Could we use less RAM by rewriting this function to work more efficiently?
- Could we use more RAM and save CPU cycles by caching?

**Tips**
- Memory profiling make your code run 10-100x slower
- Install `psutil` to `memory_profiler` run faster
- Use `memory_profiler` occasionally and `line_profiler` more frequently
- `--pdb-mmem=XXX` flag: `pdb` debugger is activate after the process exceeds XXX MB -> drop you in directly at the point in your code where too many allocations are occurring

## Introspecting an existing process with PySpy
`py-spy`: sampling profiler, don't require any code changes -> it introspects an already-running Python process and reports in the console with a *top-like* display

# Ch3. Lists and Tuples
- **Lists**: dynamic arrays; mutable and allow for resizing
- **Tuples**: static arrays; immutable and the data within them cannot be changed aftey they have been created
- Tuples are cached by the Python runtime which means that we don't need to talk to the kernel to reserve memory every time we want to use one

Python lists have a built-in sorting algorithm that uses Tim sort -> O(n) in the best case and O(nlogn) in the worst case

Once sorted, we can find our desired element using a binary search -> average case of complexity of O(logn)

Dictionary lookup takes only O(1), but:
- converting the data to a dictionary takes O(n)
- no repeating keys may be undesirable

`bisect` module: provide alternative functions, heavily optimized

> "**Pick the right data structure and stick with it!** Although there may be more efficient data structures for particular operations, the cost of converting to those data structures may negate any efficiency boost"

- Tuples are for describing multiple properties of one unchanging thing
- List can be used to store collections of data about completely disparate objects
- Both can take mixed types

> "Generic code will be much slower than code specifically designed to solve a particular problem"

- Tuple (immutable): lightweight data structure
- List (mutable): extra memory needed to store them and extra computations needed when using them

# Ch4. Dictionaries and Sets
Ideal data structures to use when your data has no intrinsic order (except for insertion order), but does have a unique object that can be used to reference it
- *key*: reference object
- *value*: data

Sets do not actually contain values: is a collection of unique keys -> useful for doing set operations

**hashable** type: implements `__hash__` and either `__eq__` or `__cmp__`

## Complexity and speed
- O(1) lookups based on the arbitrary index
- O(1) insertion time
- Larger footprint in memory
- Actual speed depends on the hashing function

## How do dictionaries and sets work?
Use *hash tables* to achieve O(1) lookups and insertions -> clever usage of a hash function to turn an arbitrary key (i.e., a string or object) into an index for a list

> *load factor*: how well distributed the data is throughout the hash table -> related to the entropy of the hash function

Hash functions must return integers

- Numerical types (`int` and `float`): hash is based on the bit value of the number they represent
- Tuples and strings: hash value based on their contents
- Lists: do not support hashing because their values can change

> A custom-selected hash function should be careful to evenly distribute hash values in order to avoid collisions (will degrade the performance of a hash table) -> constantly "probe" the other values -> worst case O(n) = searching through a list

**Entropy**: "how well distributed my hash function is" -> max entropy = *ideal* hash function = minimal number of collisions

# Ch5. Iterators and Generators

## Python `for` loop deconstructed
```python
# The Python loop
for i in object:
    do_work(i)

# Is equivalent to
object_iterator = iter(object)
while True:
    try:
        i = next(object_iterator)
    except StopIteration:
        break
    else:
        do_work(i)
```

- Changing to generators instead of precomputed arrays may require algorithmic changes (sometimes not so easy to understand)

> "Many of Python’s built-in functions that operate on sequences are generators themselves. `range` returns a generator of values as opposed to the actual list of numbers within the specified range. Similarly, `map`, `zip`, `filter`, `reversed`, and `enumerate` all perform the calculation as needed and don’t store the full result"

- Generators have less memory impact than list comprehension
- Generators are really a way of organizing your code and having smarter loops

## Lazy generator evaluation
*Single pass* or *online* algorithms: at any point in our calculation with a generator, we have only the current value and cannot reference any other items in the sequence

`itertools` from the standard library provides useful functions to make generators easier to use:
- `islice`: slicing a potentially infinite generator
- `chain`: chain together multiple generators
- `takewhile`: adds a condition that will end a generator
- `cycle`: makes a finite generator infinite by constantly repeating it

# Ch6. Matrix and Vector Computation
> Understanding the motivation behind your code and the intricacies of the algorithm will give you deeper insight about possible methods of optimization

## Memory fragmentation
Python doesn't natively support vectorization
- Python lists store pointers to the actual data -> good because it allows us to store whatever type of data inside a list, however when it comes to vector and matrix operations, this is a source of performance degradation
- Python bytecode is not optimized for vectorization -> `for` loops cannot predict when using vectorization would be benefical

*von Neumann bottleneck*: limited bandwidth between memory and CPU as a result of the tiered memory architecture that modern computers use

`perf` Linux tool: insights into how the CPU is dealing with the program being run

`array` object is less suitable for math and more suitable for storing fixed-type data more efficiently in memory

## numpy
`numpy` has all of the features we need—it stores data in contiguous chunks of memory and supports vectorized operations on its data. As a result, any arithmetic we do on `numpy` arrays happens in chunks without us having to explicitly loop over each element. Not only is it much easier to do matrix arithmetic this way, but it is also faster

Vectorization from `numpy`: may run fewer instructions per cycle, but each instruction does much more work

## numexpr: making in-place operations faster and easier
- `numpy`'s optimization of vector operations: occurs on only one operation at a time
- `numexpr` is a module that can take an entire vector expression and compile it into very efficient code that is optimized to minimize cache misses and temporary space used. Expressions can utilize multiple CPU cores
- Easy to change code to use `numexpr`: rewrite the expressions as strings with references to local variables

## Lessons from matrix optimizations
Always take care of any administrative things the code must do during initialization
- allocating memory
- reading a configuration from a file
- precomputing values that will be needed throughout the lifetime of a program

## Pandas


