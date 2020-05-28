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