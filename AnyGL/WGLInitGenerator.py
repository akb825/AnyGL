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

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)

		write('#include "AnyGLConfig.h"', file = self.outFile)
		self.newLine()
		write('#if ANYGL_LOAD == ANYGL_LOAD_WGL', file = self.outFile)

	def endFile(self):
		write('#define WIN32_LEAN_AND_MEAN', file = self.outFile)
		write('#include <Windows.h>', file = self.outFile)
		write('#include <GL/gl.h>', file = self.outFile)
		self.newLine()

		write('#define ANYGL_IMPL', file = self.outFile)
		write('#include "wgl.h"', file = self.outFile)
		self.newLine()

		write('/* Generated by AnyGL. */', file = self.outFile)

		# Type declarations.
		self.newLine()
		for feature in self.extensionFeatures:
			for function in feature.functions:
				write(function.getTypeDecl(), file = self.outFile)

		# Function pointer declarations.
		self.newLine()
		for feature in self.extensionFeatures:
			for function in feature.functions:
				write('ANYGL_EXPORT', function.type, 'AnyGL_' + function.name + ';',
					file = self.outFile)

		self.newLine()
		write('int AnyGL_init(void)\n{', file = self.outFile)

		# May need to create a dummy context in order to load the exensions.
		createContextCode = \
			'\tHWND window = NULL;\n' \
			'\tHDC dc = NULL;\n' \
			'\tHGLRC context = NULL;\n' \
			'\tif (!wglGetCurrentContext())\n' \
			'\t{\n' \
			'\t\tHINSTANCE hinst = GetModuleHandle(NULL);\n' \
			'\t\tWNDCLASSA windowClass = {};\n' \
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
			'\t\twindowClass.style = CS_OWNDC;\n' \
			'\t\twindowClass.lpfnWndProc = &DefWindowProc;\n' \
			'\t\twindowClass.hInstance = hisnt;\n' \
			'\t\twindowClass.lpszClassName = "AnyGLDummyWindow";\n' \
			'\t\tif (!RegisterClassA(&windowClass))\n' \
			'\t\t\treturn 0;\n\n' \
			'\t\twindow = CreateWindowA(windowClass.lpszClassName, "Dummy", 0, 0, 0, 0, 0, NULL, ' \
				'NULL, hinst, NULL);\n' \
			'\t\tif (!window)\n' \
			'\t\t\treturn 0;\n\n' \
			'\t\tdc = GetDC(window);\n' \
			'\t\tpixelFormat = ChoosePixelFormat(dc, &pfd);\n' \
			'\t\tif (!pixelFormat || !SetPixelFormat(dc, pixelFormat, &pfd))\n' \
			'\t\t{\n' \
			'\t\t\tReleaseDC(dc);\n' \
			'\t\t\tDestroyWindow(window);\n' \
			'\t\t\treturn 0;\n' \
			'\t\t}\n\n' \
			'\t\tcontext = wglCreateContext(dc);\n' \
			'\t\tif (!context || !wglMakeCurrent(dc, context))\n' \
			'\t\t{\n' \
			'\t\t\tReleaseDC(dc);\n' \
			'\t\t\tDestroyWindow(window);\n' \
			'\t\t\treturn 0;\n' \
			'\t\t}\n' \
			'\t}'
		write(createContextCode, file = self.outFile)

		self.newLine()
		for feature in self.extensionFeatures:
			write('\t/*', feature.name, '*/', file = self.outFile)
			for function in feature.functions:
				write('\tAnyGL_' + function.name + ' = (' + function.type + \
					')wglGetProcAddress("' + function.name + '");', file = self.outFile)
			self.newLine()

		write('\tif (context)', file = self.outFile)
		write('\t{', file = self.outFile)
		write('\t\twglMakeCurrent(NULL, NULL);', file = self.outFile)
		write('\t\twglDeleteContext(context);', file = self.outFile)
		write('\t\tReleaseDC(dc);', file = self.outFile)
		write('\t\tDestroyWindow(window);', file = self.outFile)
		write('\t}', file = self.outFile)

		write('\treturn 1;\n}', file = self.outFile)

		self.newLine()
		write('#endif /* ANYGL_LOAD */', file = self.outFile)

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
		self.curFeature.functions.append(FunctionInfo(cmdinfo.elem, 'ANYGL'))
