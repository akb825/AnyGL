#pragma once
#ifndef __AnyGLConfig_h_
#define __AnyGLConfig_h_ 1

#if defined(_WIN32)
#	define ANYGL_WINDOWS 1
#elif defined(__ANDROID__)
#	define ANYGL_ANDROID 1
#elif defined(__APPLE__)
#	define ANYGL_APPLE 1
#	include "TargetConditionals"
#	if TARGET_OS_IPHONE
#		define ANYGL_IOS 1
#	endif
#endif

#ifndef ANYGL_WINDOWS
#define ANYGL_WINDOWS 0
#endif

#ifndef ANYGL_ANDROID
#define ANYGL_ANDROID 0
#endif

#ifndef ANYGL_APPLE
#define ANYGL_APPLE 0
#endif

#ifndef ANYGL_IOS
#define ANYGL_IOS 0
#endif

/* #define this to override whether or not to use OpenGL ES. */
#ifndef ANYGL_GLES
#define ANYGL_GLES ANYGL_ANDROID || ANYGL_IOS
#endif

/* Libraries for loading OpenGL functions. */
#define ANYGL_LOAD_APPLE 0
#define ANYGL_LOAD_EGL   1
#define ANYGL_LOAD_WGL   2
#define ANYGL_LOAD_GLX   3

/* #define this to override the default library. */
#ifndef ANYGL_LOAD
#ifdef ANYGL_APPLE
#	define ANYGL_LOAD ANYGL_LOAD_APPLE
#elif ANYGL_GLES
#	define ANYGL_LOAD ANYGL_LOAD_EGL
#elif ANYGL_WINDOWS
#	define ANYGL_LOAD ANYGL_LOAD_WGL
#else
#	define ANYGL_LOAD ANYGL_LOAD_GLX
#endif
#endif

/*
 * #define ANYGL_DYNAMIC to use dynamic linking.
 * #define ANYGL_BUILD to export symbols, otherwise they will be imported.
 */
#ifndef ANYGL_EXPORT
#if ANYGL_DYNAMIC
#	ifdef _MSC_VER
#		ifdef ANYGL_BUILD
#			define ANYGL_EXPORT __declspec(dllexport)
#		else
#			define ANYGL_EXPORT __declspec(dllimport)
#		endif
#	else
#		define ANYGL_EXPORT __attribute__((visibility("default")))
#	endif
#else
#	define ANYGL_EXPORT
#endif
#endif

/* #define this to override the calling convention. */
#ifndef APIENTRY
#if ANYGL_WINDOWS && !defined(__CYGWIN__)
#	define APIENTRY __stdcall
#else
#	define APIENTRY
#endif
#endif

/* #define this to 0 if you don't want to build the debug functions, reducing compiled size. */
#ifndef ANYGL_ALLOW_DEBUG
#define ANYGL_ALLOW_DEBUG 1
#endif
