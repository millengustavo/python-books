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