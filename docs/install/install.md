# Install guide

## Install task language files

### Work with the repository
Installing the task language is quite easy. You just need to clone the TaskLanguage repository and excecute the following command in the src folder:

```
java -jar antlr-4.7.2-complete.jar -Dlanguage=Python3 -visitor TaskLexer.g4 TaskParser.g4
```

This will generate antlr files from the LoTLan grammar.

To test a written LoTLan program just run 

```
python TaskLanguage.py {your_file}
```

If there are Syntax pr/and semantic errors the program will print them in the console.


### Use the extension
If you dont want to clone the repository you can install the LoTLan VS Code extension instead. Syntax and semantic errors are shown and you have many more features. Installing the extension is highly recommended. To learn more about the extension and how to install it, go to the next section.