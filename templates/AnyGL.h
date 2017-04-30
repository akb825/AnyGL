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
 * @return 1 if the initialization succeeded.
 */
ANYGL_EXPORT int AnyGL_init(void);

#endif
