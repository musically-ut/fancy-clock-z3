# Fancy clock

This is a way to produce a clock face such that most common times can be
displayed on it by lighting up words on the face. The words can be placed
vertically or horizontally.

Instead of writing a custom brute-force algorithm or attempting to code in
heuristics myself, I decided to use a SAT Solver (i.e.
[Z3](https://github.com/Z3Prover/z3)) to produce a model for me to show how
much simpler it is to off load combinatorial optimization or satisfiability
problems off to a tool designed to do it.

## Requirements

To install Z3:

  - **Windows**: Install it from the source.
  - **Linux**: `pip install angr-z3` should install it
  - **Mac OSX**: 

        pip install git+https://github.com/zardus/z3.git@pypy-and-python3-setup
        # or
        pip install git:https://github.com/angr/angr-z3.git

However, these instructions are neither exhaustive, nor official.

## Usage

You can directly run the file in the following way:

    [148]: %run -i fancy-clock.py
    Q U A R T E R B T
    H A L F W F I V E
    T W E N T Y F S N
    X I P A S T O E D
    F T W E L V E T E
    I E S E V E N W I
    V N F O U R I O G
    E L E V E N N N H
    S I X T H R E E T


Read the source to see how the SAT problem was modelled. A more detailed
writeup will come soon.

