#include "gl.h"
#include <string.h>

int AnyGL_queryExtension(const char* name)
{
	if (glGetStringi)
	{
		GLint count = 0, i;
		glGetIntegerv(GL_NUM_EXTENSIONS, &count);
		for (i = 0; i < count; ++i)
		{
			if (strcmp((const char*)glGetStringi(GL_EXTENSIONS, i), name) == 0)
				return 1;
		}

		return 0;
	}
	else if (glGetString)
	{
		const char* extensions = glGetString(GL_EXTENSIONS);
		size_t begin = 0, end = 0;
		if (!extensions)
			return 0;

		while (extensions[begin])
		{
			for (end = begin; extensions[end] && extensions[end] != ' '; ++end)
				/* empty */
			if (strncmp(extensions + begin, name, end - begin) == 0)
				return 1;

			begin = extensions[end] == ' ' ? end + 1 : end;
		}

		return 0;
	}
	else
		return 0;
}
