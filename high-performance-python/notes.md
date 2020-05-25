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