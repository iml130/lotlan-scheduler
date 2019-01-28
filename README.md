# sola-task
A simple Task Language how to describe a new task for intra-logistics...


## Execution

To Test the Text-File `examples.txt` you need to do the following:

First: generate Python-Files via:
> java -jar antlr-4.7.2-complete.jar -Dlanguage=Python2 TaskLexer.g4 TaskParser.g4 

Then just simply execute:
> python checkGrammar.py

Iff the `examples.txt`-File contains an error, `checkGrammar` will print it. The file has been succesfully parsed, if nothing was printed.