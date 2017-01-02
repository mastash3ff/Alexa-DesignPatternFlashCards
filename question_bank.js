'use strict';

var questions = [
    {
        "Provides an interface for creating families of related or dependent objects without specifying their concrete classes.": [
            "abstract factory"
        ]
    },
    {
        "Convert the interface of a class into another interface clients expect.": [
            "adapter"
            
        ]
    },
    {
        "Decouple an abstraction from an implementation so the two can vary independently.": [
            "bridge"
        ]
    },
    {
        "Separate the construction of a complex object from its representation so that the same construction process can create different representations.": [
            "builder"
        ]
    },
    {
        "Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.": [
            "chain of Responsibility"
        ]
    },
    {
        "Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.": [
            "command"
        ]
    },
    {
        "Compose objects into tree structures to represent part-whole hierarchies.": [
            "composite"
        ]
    },
    {
        "Attach additional responsibilities to an object dynamically.": [
            "decorator"
        ]
    },
    {
        "Provide a unified interface to a set of interfaces in a subsystem.": [
            "facade"
        ]
    },
    {
        "Define an interface for creating an object, but let subclasses decide which class to instantiate.": [
            "factory method"
        ]
    },
    {
        "Use sharing to support large numbers of fine-grained objects efficiently.": [
            "flyweight"
        ]
    },
    {
        "Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.": [
            "interpreter"
        ]
    },
    {
        "Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.": [
            "iterator"
        ]
    },
    {
        "Define an object that encapsulates how a set of objects interact.": [
            "mediator"
        ]
    },
    {
        "Without violating encapsulation, capture and externalize an objects internal state so that the object can be resored to this state later.": [
            "memento"
        ]
    },
    {
        "Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.": [
            "observer"
        ]
    },
    {
        "Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.": [
            "prototype"
        ]
    },
    {
        "Provide a surrogate or placeholder for another object to control access to it.": [
            "proxy"
        ]
    },
    {
        "Ensure a class only has one instance, and provide a global point of access to it.": [
            "singleton"
        ]
    },
    {
        "Allow an object to alter its behaviour when its internal state changes.": [
            "state"
        ]
    },
    {
        "Define a family of algorithms, encapsulate each one, and make them interchangeable.": [
            "strategy"
        ]
    },
    {
        "Define the skeleton of an algorithm in an operation, deferring some steps to subclasses.": [
            "template method"
        ]
    },
    {
        "Represent an operation to be performed on the elements of an object structure.": [
            "visitor"
        ]
    },
];

module.exports = questions;
