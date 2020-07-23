# Clean Code: A Handbook of Agile Software Craftsmanship

Author: Robert C. Martin

[Available here](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

![clean_code](clean_code.jpeg)

# Ch1. Clean Code
> "Most managers want good code, even when they are obsessing about the schedule (...) It's *your* job to defend the code with equal passion"

- Clean code is *focused*: each function, each class, each module exposes a single-minded attitude that remains entirely undistracted, and upolluted, by the surrounding details
- Code, without tests, is not clean. No matter how elegant it is, no matter how readable and accessible, if it hath not tests, it be unclean
- You will read it, and it will be pretty much what you expected. It will be obvious, simple, and compelling

## Reading vs. Writing
- The ratio of time spent reading vs. writing is well over 10:1
- We are constantly reading old code as part of the effort to write new code
- **We want the reading of code to be easy, even if it makes the writing harder**
- You cannot write code if you cannot read the surrounding code
- If you want to go fast, get done quickly, if you want your code to be easy to write, make it easy to read

# Ch2. Meaningful Names

## Use intention-revealing names
> Choosing good names takes time, but saves more than it takes. Take care with your names and change them when you find better ones

## Avoid disinformation
- Avoid leaving false clues that obscure the meaning of code
- Avoid words whose entrenched meanings vary from our intended meaning

## Make meaningful distinctions
If names must be different, then they should also mean something different

## Use pronounceable names
- Humans are good at words
- Words are, by definition, pronounceable

## Use searchable names
Single-letter names and numeric constants have a particular problem in that they are not easy to locate across a body of text

## Avoid encodings
Encoding type or scope information into names simply adds an extra burden of deciphering

## Avoid mental mapping
> Clarity is king

## Class names
- Classes and objects should have noun or noun phrase names
- A class name should not be a verb

## Method names
Methods should have verb or verb phrase names

## Don't be cute
- Choose clarity over entertainment value
- Say what you mean. Mean what you say

## Pick one word per concept
A consistent lexicon is a great boon to the programmers who must use your code

## Don't pun
Avoid using the same word for two purposes -> essentially a pun

## Use solution domain names
- People who read your code will be programmers
- Use CS terms, algorithm names, pattern names, math terms

## Use problem domain names
- Separate solution and problem domain concepts
- Code that has more to do with problem domain concepts should have names drawn from the problem domain

## Add meaningful context
Most names are not meaningful in and of themselves

## Don't add gratuitous context
- Shorter names are generally better than long ones, so long as they are clear
- Add no more context to a name than is necessary

> Choosing good names requires good descriptive skills and a shared cultural background. This is a teaching issue rather than a technical, business, or management issue

# Ch3. Functions
## Small
Functions should be small

### Blocks and Indenting
- Blocks within `if` statements, `else` statements, `while` statements should be on line long -> probably a function call
- Keep the enclosing function small, adds documentary value
- Functions should not be large enough to hold nested structures -> makes easier to read and understand

## Do one thing
> Functions should do one thing. They should do it well. They should do it only

- Reasons to write functions: decompose a larger concept (the name of the function) into a set of steps at the next level of abstraction
- Functions that do one thing cannot be divided into sections

## One level of abstraction per function
- Once details are mixed with essential concepts, more details tend to accrete within the function

### The Stepdown rule
- We want code to be read like a top-down narrative
- A set of TO paragraphs, each describing the current level of abstraction and referencing subsequent TO paragraphs at the next level down

## Use descriptive names
Ward's principle: *"You know you are working on clean code when each routine turns out to be pretty much what you expected"*

- Spend time choosing a name
- You should try several different names and read the code with each in place

## Function arguments
Ideal number of arguments for a function:
- zero (niladic)
- one (monadic)
- two (dyadic)
- more than that should be avoided where possible

- **Arguments are hard from a testing point of view** -> test cases for all combinations of arguments
- Output arguments are harder to understand than input arguments
- **Passing a boolean into a function (flag arguments) is a terrible practice** -> loudly proclaiming that this function does more than one thing -> does one thing if the flag is true and another if the flag is false!
- When a function seems to need more than two or three arguments, it is likely that some of those arguments ought to be wrapped into a class of their own -> When groups of variables are passed together, they are likely part of a concept that deserves a name of its own
- Side effects are lies -> your functions promises to do one thing, but it also does other *hidden* things
- Either your function should change the state of an object, or it should return some information about the object
- **Prefer Exceptions to returing error codes**
- Extract try/catch blocks into functions of their own
- Functions should do one thing -> error handling is one thing
- Don't repeat yourself -> duplication may be the root of all evil in software

## How do you write functions like this?
Writing software is like any other kind of writing
1. Get your thoughts down first
2. Massage it until it reads well

The first draft might be clumsy and disorganized, so you restructure it and refine it until it reads the way you want it to read

> Every system is built from a domain-specific language designed by the programmers to describe the system. Functions are the verbs of that language, and classes are the nouns.

# Ch4. Comments
- Comments are always failures. We must have them because we cannot always figure out how to express ourselves without them, but their use is not a cause for celebration
- Comments lie. Not always, and not intentionally, but too often
- The older a comment is, and the farther away it is from the code it describes, the more likely it is to be wrong
- **Truth can only be found in the code**
- Explain your intent in code: **create a function that says the same thing as the comment you want to write**
- A comment may be used to amplify the importance of something that may otherwise seem inconsequential
- We have good source code control systems now. Those systems will remember the code for us. We don’t have to comment it out any more. Just delete the code
- Short functions don't need much description -> well-chosen name for a small function that does one thing is better than a comment header

# Ch5. Formatting
Code formatting
- Too important to ignore
- Is about communication -> developer's first order of business

> Small files are easier to understand than large files are

## The newspaper metaphor
Source file should be like a newspaper article
- Name should be simple but explanatory
- The name, by itself, should be sufficient to tell us whether we are in the right module or not

## Vertical formatting
- Avoid forcing the reader to hop around through the source files and classes
- **Dependent functions**: if one function calls another, they should be vertically close, and the caller should be above the callee

## Horizontal formatting
- Strive to keep your lines short
- Beyond 100~120 isn't advisable

# Ch6. Objects and Data Structures

## Data/Object anti-symmetry
> Objects hide their data behind abstractions and expose functions that operate on that data. Data structure expose their data and have no meaningful functions

- Procedural code (code using data structures) makes it easy to add new functions without changing the existing data structures. OO code makes it easy to add new classes without changing existing functions
- Procedural code makes it hard to add new data structures because all the functions must change. OO code makes it hard to add new functions because all the classes must change

> Mature programmers know that the idea that *everything is an object is a myth*. Sometimes you really do want simple data structures with procedures operating on them

## Data transfer objects (DTO)
DTO: quintessential form of a data structure -> a class with public variables and no functions

### Active records
- Special forms of DTOs
- Data structures with public (or bean-accessed) variables; but they typically have navigational methods like `save` and `find`

## Objects 
- expose behavior and hide data
- easy to add new kinds of objects without changing existing behaviors 
- hard to add new behaviors to existing objects 

## Data Structures 
- expose data and have no significant behavior
- easy to add new behaviors to existing data structures
- hard to add new data structures to existing functions

# Ch7. Error Handling
> Things can go wrong, and when they do, we as programmers are responsible for making sure that our code what it needs to do

- Error handling is important, but if it obscures logic, it's wrong
- It is better to throw an exception when you encounter an error. The calling code is cleaner. Its logic is not obscured by error handling

## Write your `Try-Catch-Finally` statement first
- `try` blocks are like transactions
- Your `catch` has to leave your program in a consistent state, no matter what happens in the `try`
- Try to write tests to force exceptions, and then add behavior to your handler to satisfy your tests -> cause you to build the transaction scope of the `try` block first and help maintain the transaction nature of that scope

## Provide context with exceptions
- Create informative error messages and pass them along with your exceptions
- Mention the operation that failed and the type of failure
- If you are logging in your application, pass along enough information to be able to log the error in your `catch`

> Wrapping third-party APIs is a best practice -> minimize your dependencies upon it: you can choose to move to a different library in the future without much penalty; makes it easier to mock out third-party calls when you are testing your own code

## Define the normal flow
**Special case pattern**: you create a class or configure an object so that it handles a special case for you -> the client code doesn't have to deal with exceptional behavior 

# Ch8. Boundaries
- It's not our job to test the third-party code, but it may be in our best interest to write tests for the third-party code we use
- **Learning tests**: call the third-party API, as we expect to use it in our application -> controlled experiments that check our understanding of that API
- **Clean Boundaries**: code at the boundaries needs clear separation and tests that define expectations

> Avoid letting too much of our code know about the third-party particulars. It's betters to depend on something you control than on something you don't control, lest it end up controlling you

# Ch9. Unit Tests
## The three laws of TDD
- **First Law**: You may not write production code until you have written a failing unit test
- **Second Law**: You may not write more of a unit test than is sufficient to fail, and not compiling is failing
- **Third Law**: You may not write more production code than is sufficient to pass the current failing test

## Keeping tests clean
- Having dirty tests is equivalent to, if not worse than, having no tests
- Tests must change as the production code evolves -> the dirtier the tests, the harder they are to change
- If your tests are dirty, you begin to lose the ability to improve the structure of that code
> Test code is just as important as production code. It requires thought, design, and care. It must be kept as clean as production code

## Clean tests
Readability is perhaps even more important in unit tests than it is in production code
- Clarity
- Simplicity
- Density of expression (say a lot with as few expressions as possible)

**BUILD-OPERATE-CHECK** pattern:
- First part builds up the test data
- Second part operates on that test data
- Third part checks that the operation yielded the expected results

**Domain-Specific Testing Language**: testing language (specialized API used by the tests) -> make tests expressive and succint -> make the tests more convenient to write and easier to read

**given-when-then** convention: makes the tests even easier to read

**TEMPLATE METHOD** pattern -> putting the given/when parts in the base classs, and the then parts in different derivatives

- The number of asserts in a test ought to be minimized
- We want to test a single concept in each test function

## F.I.R.S.T.
- **Fast**: when tests run slow, you won't want to run them frequently
- **Independent**: you should be able to run each test independently and run the tests in any order you like
- **Repeatable**: if your tests aren't repeatable in any environment, then you'll always have an excuse for why they fail
- **Self-Validating**: you should not have to read through a log file to tell whether the tests pass (should have a boolean output -> pass/fail)
- **Timely**: unit tests should be written just before the production code that makes them pass

# Ch10. Classes
- Smaller is the primary rule when it comes to designing classes
- Name of the class = describe what responsibilities it fulfills
- If we cannot derive a concise name for a class, then it's likely too large -> the more ambiguous the class name, the more likely it has too many responsibilities

## The Single Responsibility Principle
- **SRP** is one of the more important concepts in OO design
- States that a class or module should have one and only one, *reason to change*
- Definition of responsibility
- Guidelines for class size
- A system with many small classes has no more moving parts than a system with a few large classes

> Trying to identify responsibilities (reasons to change) often helps us recognize and create better abstractions in our code

## Cohesion
- Classes should have a small number of instance variables
- Each of the methods of a class should manipulate one or more of those variables
- A class in which each variable is used by each method is **maximally cohesive**
- Maintaining cohesion results in many small classes

## Organizing for change
- Change is continual
- Every change -> risk that the remainder of the system no longer works as intended
- Clean system -> organize our classes to reduce the risk of change

> **Open-Closed Principle (OCP)**: another key OO class design principle -> Classes should be open for extension but closed for modification

- Ideal system -> we incorporate new features by extending the system, not by making modifications to existing code

> **Dependency Inversion Principle (DIP)** -> classes should depend upon abstractions, not on concrete details

# Ch11. Systems
## Separate constructing a system from using it
> Software systems should separate the startup process, when the application objects are constructed and the dependencies are "wired" together, from the runtime logic that takes over after startup

- Startup process: *concern* that any application must address
- *Separation of concerns*: one of the most important design techniques
- Never let little, convenient idioms lead to modularity breakdown

## Separation of main
### Factories
- **ABSTRACT FACTORY**: pattern -> give the application control of *when* to build the object, but keep the details of that construction separate from the application code

### Dependency injection (DI)
- Powerful mechanism for separating construction from use
- Application of *Inversion of Control* (IoC) to dependency management
- Moves secondary responsibilities from an object to other objects that are dedicated to the purpose (supporting SRP)
- The invoking object doesn't control what kind of object is actually returned, but the invoking object still actively resolves the dependency
> An object should not take responsibility for instantiating dependencies itself. Instead, it should pass this responsibility to another "authoritative" mechanism (inverting control). Setup is a global concern, this authoritative mechanism will be either the "main" routine or a special-purpose container 

## Scaling up
- **Myth**: we can get systems "right the first time"
- Implement only today's stories -> then refactor and expand the system to implement new stories tomorrow = essence of iterative and incremental agility
- TDD, refactoring, and the clean code they produce make this work at the code level
- Software systems are unique compared to physical systems. Their archiectures can grow incrementally, **if we maintain the proper separation of concerns**

## Test drive the system architecture
- **Big Design Up Front (BDUF)**: harmful because it inhibits adapting to change, due to psychological resistance to discarding prior effort and because of the way architecture choices influence subsequent thinking about the design

## Optimize decision making
- Modularity and separation of concerns make decentralized management and decision making possible
- Give responsibilities to the most qualified persons
- **It is best to postpone decisions until the last possible moment** -> lets us make informed choices with the best possible information. A premature decision is a decision made with suboptimal knowledge

> Whether you are designing systems or individual modules, never forget to use **the simplest thing that can possibly work**

# Ch12. Emergence

# Ch13. Concurrency

# Ch14. Successive Refinement
