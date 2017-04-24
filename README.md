# Introduction

AnyGL is a generator that creates the API and headers and function loading code for OpenGL. The goal is to support the _features_ of various versions rather than specific versions. This makes it easier to support multiple versions of OpenGL on multiple platforms, dynamically determining whether to use newer or older functionality.

* When a core feature is exposed as an extension in older versions, the undecorated name (i.e. without the ARB or EXT suffix) is used.
* Functions that aren't supported will be NULL.
* Both OpenGL and OpenGL ES are supported, allowing shared implementations for the similar portions of both APIs.

# Dependencies

The following software is required to run AnyGL:

* [Python](https://www.python.org/)
* [lxml](http://lxml.de/)

These dependencies are only required to run AnyGL to generate the APIs. There are no requirements other than a C compiler and a platform that supports OpenGL to use the generated code.

# Usage

In order to generate the APIs, you must first ensure that the submodules are downloaded.

	git submodule init
	git submodule update

This pulls down the OpenGL registry repository, which is used to provide the OpenGL API information.

# License

The generation code is under the Apache license. The generated C code, including the hand-written portions used with the generated code, is under the public domain.
