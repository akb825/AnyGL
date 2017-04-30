#include "AnyGLConfig.h"

#if ANYGL_LOAD == ANYGL_LOAD_SYSPTR || ANYGL_LOAD == ANYGL_LOAD_EGL

int AnyGL_init(void)
{
	return 1;
}

#endif
