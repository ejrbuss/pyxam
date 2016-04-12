# The Pyxam Framework

Pyxam is built on top of a set of structures that follow a consistent design pattern. Each of the following structures
takes ownership over a collection of implementations. Similar to interfaces in object oriented programming the primary
function of these structures is to call a function provided by their children.

This design model is implemented to allow for easy extensibility whilst maintaining a consistent set of core tools and
design principles. All of these structures can be added to via plugins which are loaded dynamically at runtime.
