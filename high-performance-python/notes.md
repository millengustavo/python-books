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
### Pandas's internal model
- Operations on columns often generate temporary intermediate arrays which consume RAM: expect a temporary memory usage of up to 3-5x your current usage
- Operations can be single-threaded and limited by Python's global interpreter lock (GIL)
- Columns of the same `dtype` are grouped together by a `BlockManager` -> make row-wise operations on columns of the same datatype faster
- Operations on data of a single common block -> *view*; different `dtypes` -> can cause a *copy* (slower)
- Pandas uses a mix of NumPy datatypes and its own extension datatypes
- numpy `int64` isn't NaN aware -> Pandas `Int64` uses two columns of data: integers and NaN bit mask
- numpy `bool` isn't NaN aware -> Pandas `boolean`

> More safety makes things run slower (checking passing appropriate data) -> **Developer time (and sanity) x Execution time**. Checks enabled: avoid painful debugging sessions, which kill developer productivity. If we know that our data is of the correct form for our chosen algorithm, these checks will add a penalty

## Building DataFrames and Series from partial results rather than concatenating
- Avoid repeated calls to `concat` in Pandas (and to the equivalent `concatenate` in NumPy)
- Build lists of intermediate results and then construct a Series or DataFrame from this list, rather than concatenating to an existing object

## Advice for effective pandas development
- Install the optional dependencies `numexpr` and `bottleneck` for additional performance improvements
- Caution against chaining too many rows of pandas operations in sequence: difficult to debug, chain only a couple of operations together to simplify your maintenance
- **Filter your data before calculating** on the remaining rows rather than filtering after calculating
- Check the schema of your DataFrames as they evolve -> tool like `bulwark`, you can visualize confirm that your expectations are being met
- Large Series with low cardinality: `df['series_of_strings'].astype('category')` -> `value_counts` and `groupby` run faster and the Series consume less RAM
- Convert 8-byte `float64` and `int64` to smaller datatypes -> 2-byte `float16` or 1-byte `int8` -> smaller range to further save RAM
- Use the `del` keyword to delete earlier references and clear them from memory
- Pandas `drop` method to delete unused columns
- Persist the prepared DataFrame version to disk by using `to_pickle`
- Avoid `inplace=True` -> are scheduled to be removed from the library over time
- `Modin`, `cuDF`
- `Vaex`: work on very large datasets that exceed RAM by using lazy evaluation while retaining a similar interface to Pandas -> large datasets and string-heavy operations

# Ch7. Compiling to C
To make code run faster:
- Make it do less work
- Choose good algorithms
- Reduce the amount of data you're processing
- Execute fewer instructions -> compile your code down to machine code

## Python offers
- `Cython`: pure C-based compiling
- `Numba`: LLVM-based compiling
- `PyPy`: replacement virtual machine which includes a built-in just-in-time (JIT) compiler

## What sort of speed gains are possible?
Compiling generate more gains when the code:
- is mathematical
- has lots of loops that repeat the same operations many times

Unlikely to show speed up:
- calls to external libraries (regexp, string operations, calls to database)
- programs that are I/O-bound

## JIT versus AOT compilers
- **AOT (ahead of time)**: `Cython` -> you'll have a library that can instantly be used -> best speedups, but requires the most manual effort
- **JIT (just in time)**: `Numba`, `PyPy` -> you don't have to do much work up front, but you have a "cold start" problem -> impressive speedups with little manual intervention

## Why does type information help the code run faster?
Python is dynamically typed -> keeping the code generic makes it run more slowly

> “Inside a section of code that is CPU-bound, it is often the case that the types of variables do not change. This gives us an opportunity for **static compilation and faster code execution**”

## Using a C compiler
`Cython` uses `gcc`: good choice for most platforms; well supported and quite advanced

## Cython
- Compiler that converts type-annotaded (C-like) Python into a compiled extension module
- Wide used and mature
- `OpenMP` support: possible to convert parallel problems into multiprocessing-aware modules
- `pyximport`: simplified build system
- Annotation option that output an HTML file -> more yellow = more calls into the Python virtual machine; more white = more non-Python C code

Lines that cost the most CPU time:
- inside tight inner loops
- dereferencing `list`, `array` or `np.array` items
- mathematical operations

`cdef` keyword: declare variables inside the function body. These must be declared at the top of the function, as that’s a requirement from the C language specification

> **Strength reduction**: writing equivalent but more specialized code to solve the same problem. Trade worse flexibility (and possibly worse readability) for faster execution

`memoryview`: allows the same low-level access to any object that implements the buffer interface, including `numpy` arrays and Python arrays

## Numba
- JIT compiler that specializes in `numpy` code, which it compiles via LLVM compiler at runtime
- You provide a decorator telling it which functions to focus on and then you let Numba take over
- `numpy` arrays and nonvectorized code that iterates over many items: Numba should give you a quick and very painless win. 
- Numba does not bind to external C libraries (which Cython can do), but it can automatically generate code for GPUs (which Cython cannot).
- OpenMP parallelization support with `prange`
- Break your code into small (<10 line) and discrete functions and tackle these one at a time

```
from numba import jit

@jit()
def my_fn():
```

## PyPy
- Alternative implementation of the Python language that includes a tracing just-in-time compiler
- Offers a faster experience than CPython
- Uses a different type of garbage collector (modified mark-and-sweep) than CPython (reference counting) = may clean up an unused object much later
- PyPy can use a lot of RAM
- `vmprof`: lightweight sampling profiler

## When to use each technology
![compiler_options](./compiler_options.png)

- `Numba`: quick wins for little effort; young project
- `Cython`: best results for the widest set of prolbmes; requires more effort; mix Python and C annotations
- `PyPy`: strong option if you're not using `numpy` or other hard-to-port C extensions

### Other upcoming projects
- Pythran
- Transonic
- ShedSkin
- PyCUDA
- PyOpenCL
- Nuitka

## Graphics Processing Units (GPUs)
Easy-to-use GPU mathematics libraries:
- TensorFlow
- PyTorch

### Dynamic graphs: PyTorch
Static computational graph tensor library that is particularly user-friendly and has a very intuitive API for anyone familiar with `numpy`

> *Static computational graph*: performing operations on `PyTorch` objects creates a dynamic definition of a program that gets compiled to GPU code in the background when it is executed -> changes to the Python code automatically get reflected in changes in the GPU code without an explicit compilation step needed

### Basic GPU profiling
- `nvidia-smi`: inspect the resource utilization of the GPU
- Power usage is a good proxy for judging how much of the GPU's compute power is being used -> more power the GPU is drawing = more compute it is currently doing

### When to use GPUs
- Task requires mainly linear algebra and matrix manipulations (multiplication, addition, Fourier transforms)
- Particularly true if the calculation can happen on the GPU uninterrupted for a period of time before being copied back into system memory
- GPU can run many more tasks at once than the CPU can, but each of those tasks run more slowly on the GPU than on the CPU
- Not a good tool for tasks that require exceedingly large amounts of data, many conditional manipulations of the data, or changing data

1. Ensure that the memory use of the problem will fit withing the GPU
2. Evaluate whether the algorithm requires a lot of branching conditions versus vectorized operations
3. Evaluate how much data needs to be moved between the GPU and the CPU

# Ch8. Asynchronous I/O
*I/O bound program*: the speed is bounded by the efficiency of the input/output

Asynchronous I/O helps utilize the wasted *I/O wait* time by allowing us to perform other operations while we are in that state

## Introduction to asynchronous programming
- *Context switch*: when a program enters I/O wait, the execution is paused so that the kernel can perform the low-level operations associated with the I/O request
- **Callback paradigm**: functions are called with an argument that is generally called the callback -> instead of the function returing its value, it call the callback function with the value instead -> long chains = "callback hell"
- **Future paradigm**: an asynchronous function returns a `Future` object, which is a promise of a future result
- `asyncio` standard library module and PEP 492 made the future's mechanism native to Python

## How does async/await work?
- `async` function (defined with `async def`) is called a *coroutine*
- Coroutines are implemented with the same philosophies as generators
- `await` is similar in function to a `yield` -> the execution of the current function gets paused while other code is run

### Gevent
- Patches the standard library with asynchronous I/O functions, 
- Has a `Greenlets` object that can be used for concurrent execution
- Ideal solution for mainly CPU-based problems that sometimes involve heavy I/O

### tornado
- Frequently used package for asynchronous I/O in Python
- Originally developed by Facebook primarily for HTTP clients and servers
- Ideal for any application that is mostly I/O-bound and where most of the application should be asynchronous
- Performant web server

### aiohttp
- Built entirely on the `asyncio` library
- Provides both HTTP client and server functionality
- Uses a similar API to `tornado`
  
### Batched results
- *Pipelining*: batching results -> can help lower the burden of an I/O task
- Good compromise between the speeds of asynchronous I/O and the ease of writing serial programs

# Ch9. The multiprocessing module
- Additional process = more communication overhead = decrease available RAM -> rarely get a full *n*-times speedup
- If you run out of RAM and the system reverts to using the disk’s swap space, any parallelization advantage will be massively lost to the slow paging of RAM back and forth to disk
- Using hyperthreads: CPython uses a lot of RAM -> hyperthreading is not cache friendly. Hyperthreads = added bonus and not a resource to be optimized against -> adding more CPUs is more economical than tuning your code
- **Amdahl's law**: if only a small part of your code can be parallelized, it doesn't matter how many CPUs you throw at it; it still won't run much faster overall
- `multiprocessing` module: process and thread-based parallel processing, share work over queues, and share data among processes -> focus: single-machine multicore parallelism
- `multiprocessing`: higher level, sharing Python data structures
- `OpenMP`: works with C primitive objects once you've compiled to C

> Keep the parallelism as simple as possible so that your development velocity is kept high

- *Embarrassingly parallel*: multiple Python processes all solving the same problem without communicating with one another -> not much penalty will be incurred as we add more and more Python processes

Typical jobs for the `multiprocessing` module:
- Parallelize a CPU-bound task with `Process` or `Pool` objects
- Parallelize an I/O-bound task in a `Pool` with threads using the `dummy` module
- Share pickled work via a `Queue`
- Share state between parallelized workers, including bytes, primitive datatypes, dictionaries, and lists

> `Joblib`: stronger cross-platform support than `multiprocessing`

## Replacing multiprocessing with Joblib
- `Joblib` is an improvement on `multiprocessing` 
- Enables lightweight pipelining with a focus on:
  - easy parallel computing 
  - transparent disk-based caching of results 
- It focuses on NumPy arrays for scientific computing
- Quick wins:
  - process a loop that could be embarrassingly parallel
  - expensive functions that have no side effect
  - able to share `numpy` data between processes
- `Parallel` class: sets up the process pool
- `delayed` decorator: wraps our target function so it can be applied to the instantiated `Parallel` object via an iterator

### Intelligent caching of function call results
`Memory` cache: decorator that caches functions results based on the input arguments to a disk cache

### Using numpy
- `numpy` is more cache friendly
- `numpy` can achieve some level of additional speedup around threads by working outside the GIL

## Asynchronous systems
Require a special level of patience. Suggestions:
- K.I.S.S.
- Avoiding asynchronous self-contained systems if possible, as they will grow in complexity and quickly become hard to maintain
- Using mature libraries like `gevent` that give you tried-and-tested approaches to dealing with certain problem sets

## Interprocess Communication (IPC)
- Cooperation cost can be high: synchronizing data and checking the shared data
- Sharing state tends to make things complicated
- IPC is fairly easy but generally comes with a cost

### multiprocessing.Manager()
- Lets us share higher-level Python objects between processes as managed shared objects; the lower-level objects are wrapped in proxy objects 
- The wrapping and safety have a speed cost but also offer great flexibility. 
- You can share both lower-level objects (e.g., integers and floats) and lists and dictionaries.

### Redis
- **Key/value in-memory storage engine**. It provides its own locking and each operation is atomic, so we don’t have to worry about using locks from inside Python (or from any other interfacing language).
- Lets you share state not just with other Python processes but also other tools and other machines, and even to expose that state over a web-browser interface
- Redis lets you store: Lists of strings; Sets of strings; Sorted sets of strings; Hashes of strings
- Stores everything in RAM and snapshots to disk
- Supports master/slave replication to a cluster of instances
- Widely used in industry and is mature and well trusted

## mmap
- Memory-mapped (shared memory) solution
- The bytes in a shared memory block are not synchronized and they come with very little overhead
- Bytes act like a file -> block of memory with a file-like interface

# Ch10. Clusters and Job Queues
*Cluster*: collection of computers working together to solve a common task

Before moving to a clustered solution:
- Profile your system to understand the bottlenecks
- Exploit compile solutions (Numba, Cython)
- Exploit multiple cores on a single machine (Joblib, multiprocessing)
- Exploit techniques for using less RAM
- Really need a lot of CPUs, high resiliency, rapid speed of response, ability to process data from disks in parallel

## Benefits of clustering
- Easily scale computing requirements
- Improve reliability
- Dynamic scaling

## Drawbacks of clustering
- Change in thinking
- Latency between machines
- Sysadmin problems: software versions between machines, are other machines working?
- Moving parts that need to be in sync
- "If you don't have a documented restart plan, you should assume you'll have to write one at the worst possible time"

> Using a cloud-based cluster can mitigate a lot of these problems, and some cloud providers also offer a spot-priced market for cheap but temporary computing resources.

- A system that's easy to debug *probably* beats having a faster system
- Engineering time and the cost of downtime are *probably* your largest expenses

## Parallel Pandas with Dask
- Provide a suite of parallelization solutions that scales from a single core on a laptop to multicore machines to thousands of cores in a cluster.
- "Apache Spark lite” 
- For `Pandas` users: larger-than-RAM datasets and desire for multicore parallelization

### Dask
- *Bag*: enables parallelized computation on unstructured and semistructured data
- *Array*: enables distributed and larger-than-RAM `numpy` operations
- *Distributed DataFrame*: enables distributed and larger-than-RAM `Pandas` operations
- *Delayed*: parallelize chains of arbitrary Python functions in a lazy fashion
- *Futures*: interface that includes `Queue` and `Lock` to support task collaboration
- *Dask-ML*: scikit-learn-like interface for scalable machine learning

> You can use Dask (and Swifter) to parallelize any side-effect-free function that you’d usually use in an `apply` call

- `npartitions` = # cores

#### Swifter
Builds on Dask to provide three parallelized options with very simple calls: `apply`, `resample` and `rolling`

### Vaex
- String-heavy DataFrames
- Larger-than-RAM datasets
- Subsets of a DataFrame -> Implicit lazy evaluation

## NSQ for robust production clustering
- Highly performant distributed messaging platform
- *Queues*: type of buffer for messages
- *Pub/subs*: describes who gets what messages (*publisher/subscriber*)

# Ch11. Using less RAM
- Counting the amount of RAM used by Python object is tricky -> if we ask the OS for a count of bytes used, it will tell us the total amount allocated to the process
- Each unique object has a memory cost

## Objects for primitives are expensive
`memory_profiler`

```
%load_ext memory_profiler

%memit <operation>
```

### The `array` module stores many primitive objects cheaply
- Creates a contiguos block of RAM to hold the underlying data. Which data structures:
  - integers, floats and characters
  - *not* complex numbers or classes
- Good to pass the array to an external process or use only some of the data (not to compute on them)
- Using a regular `list` to store many numbers is much less efficient in RAM than using an `array` object
- `numpy` arrays are almost certainly a better choice if you are doing anything heavily numeric:
  - more datatype options
  - many specialized and fast functions

### Using less RAM in NumPy with NumExpr
`NumExpr` is a tool that both speeds up and reduces the size of intermediate operations

> Install the optional NumExpr when using Pandas (Pandas does not tell you if you haven’t installed NumExpr) -> calls to `eval` will run more quickly -> import numpexpr: if this fails, install it! 

- NumExpr breaks the long vectors into shorter, cache-friendly chunks and processes each in series, so local chunks of results are calculated in a cache-friendly way

## Bytes versus Unicode
- Python 3.x, all strings are Unicode by default, and if you want to deal in bytes, you'll explicitly create a `byte` sequence
- **UTF-8 encoding** of a Unicode object uses 1 byte per ASCII character and more bytes for less frequently seen characters

## More efficient tree structures to represent strings
- **Tries**: share common prefixes
- **DAWG**: share common prefixes and suffixes
- Overlapping sequences in your strings -> you'll likely see a RAM improvement
- Save RAM and time in exchange for a little additional effort in preparation
- Unfamiliar data structures to many developers -> isolate in a module to simplify maintenance

### Directed Acyclic Word Graph (DAWG)
Attemps to efficiently represent strings that share common prefixes and suffixes

### Marisa Trie
*Static trie* using Cython bindings to an external library -> it cannot be modified after construction

## Scikit-learn's DictVectorizer and FeatureHasher
- `DictVectorizer`: takes a dictionary of terms and their frequences and converts them into a variable-width sparse matrix -> it is possible to revert the process
- `FeatureHasher`: converts the same dictionary of terms and frequencies into a fixed-width sparse matrix -> it doesn't store a vocabulary and instead employs a hashing algorithm to assign token frequencies to columns -> can't convert it back to the original token from hash

## ScyPy's Sparse Matrices
- Matrix in which most matrix elements are 0
- `C00` matrices: simplest implementation: each non-zero element we store the value in addition to the location of the value -> each non-zero value = 3 numbers stored -> used only to contruct sparse matrices and not for actual computation
- `CSR/CSC` is preferred for computation

> Push and pull of speedups with sparse arrays: balance between losing the use of efficient caching and vectorization versus not having to do a lot of the calculations associated with the zero values of the matrix

Limitations:
- Low amount of support
- Multiple implementations with benefits and drawbacks
- May require expert knowledge

## Tips for using less RAM
> "If you can avoid putting it into RAM, do. Everything you load costs you RAM"

- Numeric data: switch to using `numpy` arrays
- Very sparse arrays: SciPy's sparse array functionality
- Strings: stick to `str` rather than `bytes`
- Many Unicode objects in a static structure: DAWG and trie structures
- Lots of bit strings: `numpy` and the `bitarray` package

## Probabilistic Data Structures

