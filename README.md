# sola-task
It is a simple Task-Language to describe Intra-logistic processes. The language contains templates, instances of templates and tasks, which orchestrate those instances and trigger other tasks. 


# SolaTask-File
The `SolaTask`-File is composed by 3 different parts: Templates, Instances and Tasks. Each of them can be used and described arbitary complex. Also Comments can be annotated via `#`

## Templates
In each `SolaTask`-File at least one template needs to be specified, if you want to create instances or a task. They are the basis of the `SolaTask`-File and describe a collection of same instances. This can be the case for multiple palettes/storage places, mutliple conveyer belts, or like a fleet of robots with same capabilities. Therefor, a template summarizes and specifies a set of instances.

You can specify a template like this:

```text
template MyTemplate
    type
    value # readonly
    myValue # displays a number
    ...  # other values    
end
```
It is important that the attributes inside an template begin with a lowercase character. The name has to start with an uppercase character. Each value also needs to be prefixed with four spaces (or an `\t`). 

## Instances
An instance is the actual object of a Template. Each Instance with the same Template does not have to be identical as others. The actual values behind multiple instances also do not have to be from the same type. For example: Given a fleet of robots, which can transport something from A to B. Each robot could transport it differently. A vehicle could drive it to its destination whereby a drone can fly it. As long as they have the same capabilities, they can be categorized into the same template. 

Here are two example Instances of `MyTemplate`

```text
MyTemplate myTemplateCreator
    type = TemplateCreator
    value = "boolean" # displays whether it is ready to create a new one
    myValue = "integer"
    ...  # Other specified attributes as in MyTemplate 
end

MyTemplate myTemplateDestroyer
    type = TemplateDestoryer
    value = "boolean" # displays whether it is ready to destroy one
    myValue = "float"
    ...  # Other specified attributes as in MyTemplate 
end
```

As in template, each value also have to be prefixed with four spaces (or an `\t`). In addition to that, each value which was previously specified by a template needs to be set to an actual value. This value can be enclosed by `"`. Also the Instance-Name has to start with a lowercase character. 

## Tasks
The task orchestrates different instances via operations. It describes tasks which multiple instance have to do, triggers other tasks or can be triggered by an event. Their inner commands also need to be prefixed with four spaces (or an `\t`). Currently following operations are parsable: `Transport->From->To`, `TriggeredBy`, `OnDone`.

Here is anexample of a Task-chain:

```text
task CreationTask
    # Transport components to TemplateCreator
    Transport
    from components_palette1, components_palette2, components_palette3
    to myTemplateCreator

    TriggeredBy myTemplateCreator.value == True

    OnDone TransportTask
end

task TransportTask
    Transport 
    from myTemplateCreator
    to temporary_palette
end

task DestroyingTask
    # Transport freshly created Template to Destroyer
    Transport 
    from temporary_palette
    to myTemplateDestroyer

    TriggeredBy myTemplateDestroyer.value == True

    OnDone CreationTask
end
```
The operation `Transport->From->To` allows to move from multiple instances to one destination. The operation `TriggeredBy` even allows expressions.


# Execution

To Test the Text-File `examples.txt` you need to do the following:

First: generate Python-Files via:
> java -jar antlr-4.7.2-complete.jar -Dlanguage=Python2 TaskLexer.g4 TaskParser.g4 

Then just simply execute:
> python checkGrammar.py

Iff the `examples.txt`-File contains an error, `checkGrammar` will print it. The file has been succesfully parsed, if nothing was printed.