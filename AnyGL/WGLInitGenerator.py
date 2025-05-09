# Copyright 2017 Aaron Barany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .reg import *
from .FunctionInfo import *

class FeatureInfo:
	def __init__(self, interface):
		self.name = interface.get('name')
		self.extension = interface.tag == 'extension'
		self.functions = []

class WGLInitGenerator(OutputGenerator):
	def __init__(self, errFile = sys.stderr, warnFile = sys.stderr, diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.extensionFeatures = []
		self.curFeature = None

	def newLine(self):
		write('', file = self.outFile)

	def write(self, *args):
		write(*args, file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)

		self.write('#include "AnyGLConfig.h"')
		self.newLine()
		self.write('#if ANYGL_HAS_WGL')
		self.write('#define WIN32_LEAN_AND_MEAN')
		self.write('#undef APIENTRY')
		self.write('#include <Windows.h>')
		self.write('#include <GL/gl.h>')
		self.newLine()

		self.write('#define ANYGL_NO_DEFINES')
		self.write('#include "wgl.h"')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()

		self.write('void AnyGL_shutdown(void);')
		self.write('HMODULE AnyGL_gllib;')
		self.newLine()

	def endFile(self):
		# Function pointers.
		for feature in self.extensionFeatures:
			for function in feature.functions:
				self.write('ANYGL_EXPORT', function.type, 'AnyGL_' + function.name + ';')
		self.newLine()

		self.write('int AnyGL_WGL_initialize(void)\n{')

		# May need to create a dummy context in order to load the exensions.
		createContextCode = \
			'\tHWND window = NULL;\n' \
			'\tHDC dc = NULL;\n' \
			'\tHGLRC context = NULL;\n' \
			'\tif (AnyGL_gllib)\n' \
			'\t\treturn 1;\n\n' \
			'\tAnyGL_gllib = LoadLibraryA("opengl32.dll");\n' \
			'\tif (!AnyGL_gllib)\n' \
			'\t\treturn 0;\n\n' \
			'\tif (!wglGetCurrentContext())\n' \
			'\t{\n' \
			'\t\tHINSTANCE hinst = GetModuleHandle(NULL);\n' \
			'\t\tWNDCLASSA windowClass = {0};\n' \
			'\t\tPIXELFORMATDESCRIPTOR pfd =\n' \
			'\t\t{\n' \
			'\t\t\tsizeof(PIXELFORMATDESCRIPTOR),\n' \
			'\t\t\t1,\n' \
			'\t\t\tPFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER,\n' \
			'\t\t\tPFD_TYPE_RGBA,\n' \
			'\t\t\t32,\n' \
			'\t\t\t0, 0, 0, 0, 0, 0,\n' \
			'\t\t\t0,\n' \
			'\t\t\t0,\n' \
			'\t\t\t0,\n' \
			'\t\t\t0, 0, 0, 0,\n' \
			'\t\t\t0,\n' \
			'\t\t\t0,\n' \
			'\t\t\t0,\n' \
			'\t\t\tPFD_MAIN_PLANE,\n' \
			'\t\t\t0,\n' \
			'\t\t\t0, 0, 0\n' \
			'\t\t};\n' \
			'\t\tunsigned int pixelFormat;\n\n' \
			'\t\tif (!GetClassInfo(hinst, "AnyGLDummyWindow", &windowClass))\n' \
			'\t\t{\n' \
			'\t\t\twindowClass.style = CS_OWNDC;\n' \
			'\t\t\twindowClass.lpfnWndProc = &DefWindowProc;\n' \
			'\t\t\twindowClass.hInstance = hinst;\n' \
			'\t\t\twindowClass.lpszClassName = "AnyGLDummyWindow";\n' \
			'\t\t\tif (!RegisterClassA(&windowClass))\n' \
			'\t\t\t{\n' \
			'\t\t\t\tAnyGL_shutdown();\n' \
			'\t\t\t\treturn 0;\n' \
			'\t\t\t}\n' \
			'\t\t}\n\n' \
			'\t\twindow = CreateWindowA(windowClass.lpszClassName, "Dummy", 0, 0, 0, 0, 0, NULL, ' \
				'NULL, hinst, NULL);\n' \
			'\t\tif (!window)\n' \
			'\t\t{\n' \
			'\t\t\tAnyGL_shutdown();\n' \
			'\t\t\treturn 0;\n\n' \
			'\t\t}\n' \
			'\t\tdc = GetDC(window);\n' \
			'\t\tpixelFormat = ChoosePixelFormat(dc, &pfd);\n' \
			'\t\tif (!pixelFormat || !SetPixelFormat(dc, pixelFormat, &pfd))\n' \
			'\t\t{\n' \
			'\t\t\tReleaseDC(window, dc);\n' \
			'\t\t\tDestroyWindow(window);\n' \
			'\t\t\tAnyGL_shutdown();\n' \
			'\t\t\treturn 0;\n' \
			'\t\t}\n\n' \
			'\t\tcontext = wglCreateContext(dc);\n' \
			'\t\tif (!context || !wglMakeCurrent(dc, context))\n' \
			'\t\t{\n' \
			'\t\t\tReleaseDC(window, dc);\n' \
			'\t\t\tDestroyWindow(window);\n' \
			'\t\t\tAnyGL_shutdown();\n' \
			'\t\t\treturn 0;\n' \
			'\t\t}\n' \
			'\t}'
		self.write(createContextCode)

		self.newLine()
		for feature in self.extensionFeatures:
			self.write('\t/*', feature.name, '*/')
			for function in feature.functions:
				self.write('\tAnyGL_' + function.name + ' = (' + function.type + \
					')wglGetProcAddress("' + function.name + '");')
			self.newLine()

		self.write('\tif (context)')
		self.write('\t{')
		self.write('\t\twglMakeCurrent(NULL, NULL);')
		self.write('\t\twglDeleteContext(context);')
		self.write('\t\tReleaseDC(window, dc);')
		self.write('\t\tDestroyWindow(window);')
		self.write('\t}')

		self.newLine()
		self.write('\treturn 1;\n}')

		self.newLine()
		self.write('void AnyGL_WGL_shutdown(void)\n{')
		self.write('\tif (AnyGL_gllib)\n\t{')
		self.write('\t\tFreeLibrary(AnyGL_gllib);')
		self.write('\t\tAnyGL_gllib = NULL;')
		self.write('\t}\n}')

		self.newLine()
		self.write('#endif /* ANYGL_LOAD */')

		OutputGenerator.endFile(self)

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		if emit:
			self.curFeature = FeatureInfo(interface)

	def endFeature(self):
		if self.curFeature:
			if self.curFeature.extension:
				self.extensionFeatures.append(self.curFeature)
			self.curFeature = None
		OutputGenerator.endFeature(self)

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		self.curFeature.functions.append(FunctionInfo(cmdinfo.elem))
