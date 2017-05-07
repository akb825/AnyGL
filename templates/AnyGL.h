#pragma once
#ifndef __AnyGLConfig_h_
#define __AnyGLConfig_h_ 1

#include "AnyGLConfig.h"

/**
 * @brief Initializes the AnyGL library.
 *
 * This will initialize the loading library, such as GLX or WGL. On some platforms this is
 * necessary to load extensions in the loading library required to properly create an OpenGL
 * context.
 *
 * @return 1 if the initialization succeeded, 0 if it failed.
 */
ANYGL_EXPORT int AnyGL_initialize(void);

/**
 * @brief Loads the OpenGL functions based on the currently bound context.
 * @return 1 if the load succeedd, 0 if it failed.
 */
ANYGL_EXPORT int AnyGL_load(void);

/**
 * @brief Gets the version of OpenGL.
 * @param[out] major The major version.
 * @param[out] minor The minor viersion.
 * @param[out] es 1 if OpenGL ES, 0 if desktop OpenGL.
 */
ANYGL_EXPORT void AnyGL_getGLVersion(int* major, int* minor, int* es);

/**
 * @brief Shuts down the AnyGL library, freeing any persistently held resources.
 */
ANYGL_EXPORT void AnyGL_shutdown(void);

#endif
