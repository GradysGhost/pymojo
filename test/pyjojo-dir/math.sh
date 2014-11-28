#!/bin/bash

# -- jojo --
# description: Solves simple math expressions
# param: expr - The expression to solve
# tags: math, solve
# http_method: POST
# output: split
# -- jojo --

solution=`echo $EXPR | bc`
echo "$EXPR = $solution"
echo "jojo_return_value solution=$solution"
echo "jojo_return_value expr=$EXPR"
# echo $solution
