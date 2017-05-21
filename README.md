# Introduction

AnyGL is a generator that creates the API and headers and function loading code for OpenGL. The goal is to support the _features_ of various versions rather than specific versions. This makes it easier to support multiple versions of OpenGL on multiple platforms, dynamically determining whether to use newer or older functionality.

* When a core feature is exposed as an extension in older versions, the undecorated name (i.e. without the ARB or EXT suffix) is used.
* Functions that aren't supported will be NULL.
* Both OpenGL and OpenGL ES are supported, allowing shared implementations for the similar portions of both APIs.

# Dependencies

The following software is required to run AnyGL:

* [Python](https://www.python.org/)
* [lxml](http://lxml.de/)

These dependencies are only required to run AnyGL to generate the APIs. There are no requirements other than a C compiler and a platform that supports OpenGL to use the generated code. The following libraries will need to be linked:

* `OpenGL`
* `dl` when loading with `EGL`.
* `X11` and `GLX` when loading with `GLX`.
* `EGL` when loading with `EGL`.

# Usage

In order to generate the APIs, you must first ensure that the submodules are downloaded.

	git submodule init
	git submodule update

This pulls down the OpenGL registry repository, which is used to provide the OpenGL API information.

The `AnyGL.py` python script can be run to generate the AnyGL headers and sources. Once you have generated the source files, you may embed them in your project. The public interface is proved by:

* `AnyGLConfig.h`: Configuration for AnyGL. The #defines may be used to change which library is used to load OpenGL or override whether or not to use OpenGL ES.
* `AnyGL.h`: Interface for interfacing with the AnyGL library, including initialization, shutting down, and enabling debug mode if desired.
* `gl.h`: OpenGL header. This isncludes all of the OpenGL types and functions.
* `glx.h`: GLX header for X11 integration with OpenGL, including extensions.
* `wgl.h`: WGL header for Windows integration with OpenGL, including extensions.

When checking if a function is supported, you may use the `ANYGL_SUPPORTED()` macro, passing in the function name. Global variables are provided to determine what extensions are available on the current OpenGL version. For example, to check if `GL_ARB_draw_indirect` is supported, you can check the variable `AnyGL_ARB_draw_indirect`. This shouldn't be confused with the `ANYGL_ARB_draw_indirect` macro, is defined if AnyGL's `gl.h` header declared the extension. (useful when combinging the system `gl.h` with AnyGL's `gl.h`)

## Debugging

When `ANYGL_ENABLE_DEBUG` is defined to 1 (default when `NDEBUG` isn't defined), the debugging feature may be enabled. Once you call `AnyGL_setDebugEnabled(1)` the OpenGL function pointers will be replaced with debug versions. These will check if any OpenGL occurred after the function was called, and if so will call the error function with a string version of the call, including the values of the parameters. (such as resolving enum names) By default, this will print to the console.

> **Note:** Enabling debugging will degrade performance. Compiling in debug support also increases the final compiled binary size, so it's recommended to disable this for final release builds.

When debugging is allowed, even when it's not enabled, the callsite of each OpenGL function is recorded. This can be queried with `AnyGL_getLastCallsite()`, and can be useful when hooking into OpenGL's builtin debugging functionality with `glDebugMessageCallback()`.

# License

The generation code is under the Apache license. The generated C code, including the hand-written portions used with the generated code, is under the public domain.
