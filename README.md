# autonomousCarControlSynthesis
*For optimal viewing of this document (and all `*.md` files), try opening it in a text editor that supports syntax highlighting for markdown `*.md` files (e.g. Sublime Text 2+).*

LTL to Control Synthesis (using formal methods concepts) Framework for a Basic Highway Driving Scenario.

[Nicholas Rennninger](https://github.com/nicholasRenninger) and [Richard Moon](https://github.com/RichardWasTaken)

---

## How to Run the Code


### Dependencies
This module was built in raw **python 3+**. the only external modules used were:

* `collections`: for their implementation of a queue
* `numpy`: for the matrix representation of the occupancy set
* `random`: for randomly generating traffic patterns through the occupancy set

To get these dependencies, simply type:
* `pip3 install collections`
* `pip3 install numpy` 
* `pip3 install random` 

into a terminal that has the `*/PYTHON_3XX_INSTALL_DIR/Scripts/` and `*/PYTHON_3XX_INSTALL_DIR/` directories on its path, and you should be able to get these dependencies if you do not have them already.


## Running the Source Code

Navigate to the `autonomousCarControlSynthesis` directory and from a terminal with the current path being: `*/autonomousCarControlSynthesis/`, simply type `python3 main.py` to run our code.

---

## Results

Unfortunately, we ran into a nasty python / system level error that was unresolveable after much research:

```powershell
Traceback (most recent call last):                                             File ".\main.py", line 71, in <module>
    main()                                                                     File ".\main.py", line 63, in main
        acceptingGoalNode = DFA.formAndSolveProduct(TS=TS, LDBA=LDBAObj)       

SystemError: error return without exception set
```

We believe our algorithms were correct, but their inherent exponential blowup may have strained system level libraries and caused unexpected, unhandled faults that give little information to debug with.
