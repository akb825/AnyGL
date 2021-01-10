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

compatibilityFuncs = \
[ \
	'glVertexP',
	'glTexCoordP',
	'glMultiTexCoordP',
	'glNormalP',
	'glColorP',
	'glSecondaryColorP',
]

# Functions that aren't always available based on the extension they're registered under.
ignoreFuncs = \
{ \
	'glDepthRangeArraydvNV',
	'glDepthRangeIndexeddNV'
}

class FptrFunctionInfo(FunctionInfo):
	def __init__(self, command, feature):
		FunctionInfo.__init__(self, command, feature)

		self.compatibility = False
		for compatibilityFunc in compatibilityFuncs:
			if self.name.startswith(compatibilityFunc) and \
				self.name[len(compatibilityFunc)].isdigit():
				self.compatibility = True
				break

class FeatureInfo:
	def __init__(self, interface, coreVesion):
		self.name = interface.get('name')
		self.extension = interface.tag == 'extension'
		if self.extension:
			self.version = None
		else:
			self.version = interface.get('number')

		self.loadFirst = self.version != None and self.version == coreVesion
		self.functions = []

class FptrLoadGenerator(OutputGenerator):
	def __init__(self, errFile = sys.stderr, warnFile = sys.stderr, diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.firstFeatures = []
		self.coreFeatures = []
		self.extensionFeatures = []
		self.curFeature = None
		self.allowDuplicateEntries = True

	def newLine(self):
		write('', file = self.outFile)

	def write(self, *args):
		write(*args, file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)
		self.isGles = genOpts.apiname == ['gles2']

		self.write('#include "AnyGL.h"')
		self.newLine()
		if self.isGles:
			self.coreVersion = '2.0'
			self.write('#if ANYGL_LOAD == ANYGL_LOAD_FPTR && ANYGL_GLES')
			self.write('#define GL_GLEXT_PROTOTYPES')
			self.write('#if ANYGL_APPLE')
			self.write('#  if ANYGL_GLES_VERSION >= 32')
			self.write('#    include <OpenGLES/ES3/gl32.h>')
			self.write('#  elif ANYGL_GLES_VERSION == 31')
			self.write('#    include <OpenGLES/ES3/gl31.h>')
			self.write('#  elif ANYGL_GLES_VERSION == 30')
			self.write('#    include <OpenGLES/ES3/gl3.h>')
			self.write('#  else')
			self.write('#    include <OpenGLES/ES2/gl2.h>')
			self.write('#  endif')
			self.newLine()
			self.write('#  if ANYGL_GLES_VERSION >= 30')
			self.write('#    include <OpenGLES/ES3/gl3ext.h>')
			self.write('#  endif')
			self.write('#  include <OpenGLES2/gl2ext.h>')
			self.write('#else')
			self.write('#  if ANYGL_GLES_VERSION >= 32')
			self.write('#    include <GLES3/gl32.h>')
			self.write('#  elif ANYGL_GLES_VERSION == 31')
			self.write('#    include <GLES3/gl31.h>')
			self.write('#  elif ANYGL_GLES_VERSION == 30')
			self.write('#    include <GLES3/gl3.h>')
			self.write('#  else')
			self.write('#    include <GLES2/gl2.h>')
			self.write('#  endif')
			self.newLine()
			self.write('#  if ANYGL_GLES_VERSION >= 30')
			self.write('#    include <GLES3/gl3ext.h>')
			self.write('#  endif')
			self.write('#  include <GLES2/gl2ext.h>')
			self.write('#endif')
			self.newLine()
		else:
			self.coreVersion = '1.0'
			self.write('#if ANYGL_LOAD == ANYGL_LOAD_FPTR && !ANYGL_GLES')
			self.write('#define GL_GLEXT_PROTOTYPES')
			self.write('#if ANYGL_APPLE')
			self.write('#  if ANYGL_GL_VERSION >= 30')
			self.write('#    define GL_DO_NOT_WARN_IF_MULTI_GL_VERSION_HEADERS_INCLUDED')
			self.write('#    include <OpenGL/gl3.h>')
			self.write('#    include <OpenGL/gl3ext.h>')
			self.write('#  endif')
			self.write('#  include <OpenGL/gl.h>')
			self.write('#  include <OpenGL/glext.h>')
			self.write('#else')
			self.write('#  include <GL/gl.h>')
			self.write('#  include <GL/glext.h>')
			self.write('#endif')
		self.newLine()

		self.write('#define ANYGL_NO_DEFINES')
		self.write('#include "gl.h"')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()

		self.write('int AnyGL_updateGLVersion(void);')
		self.write('int AnyGL_queryExtension(const char* name);')
		self.write('void AnyGL_initDebug(void);')
		self.write('void AnyGL_clearFunctionPointers(void);')
		self.newLine()

	def endFile(self):
		self.write('int AnyGL_initialize(void)\n{\n\treturn 1;\n}')
		self.write('void AnyGL_shutdown(void) {}')
		self.newLine()

		self.write('int AnyGL_load(void)\n{')

		self.write('\tAnyGL_clearFunctionPointers();')
		self.newLine()

		# Alwyas load first features.
		for feature in self.firstFeatures:
			self.write('\t/*', feature.name, '*/');
			for function in feature.functions:
				self.write('\tAnyGL_' + function.name, '= &' + function.name + ';')
			self.newLine()

		# Get the OpenGL version.
		self.write('\tif (!AnyGL_updateGLVersion())')
		self.write('\t\treturn 0;')
		
		if self.isGles:
			glEsBool = '1'

			# GL_HALF_FLOAT workaround
			self.write('\tif (AnyGL_atLeastVersion(3, 0, 1))')
			self.write('\t\tAnyGL_HALF_FLOAT = GL_HALF_FLOAT;')
			self.write('\telse')
			self.write('\t\tAnyGL_HALF_FLOAT = GL_HALF_FLOAT_OES;')
			self.newLine()
		else:
			glEsBool = '0'

		# Check OpenGL version for core features in addition to the #define.
		for feature in self.coreFeatures:
			self.write('#ifndef ANY' + feature.name)
			self.write('\tif (AnyGL_atLeastVersion(' + feature.version[0] + ',', feature.version[2] + \
				',', glEsBool + '))\n\t{')
			compatibility = False
			for function in feature.functions:
				if function.compatibility != compatibility:
					if function.compatibility:
						self.write('#if !ANYGL_APPLE')
					else:
						self.write('#endif')
					compatibility = function.compatibility
				self.write('\t\tAnyGL_' + function.name + ' = (' + function.type + ')&' + \
					function.name + ';')
			if compatibility:
				self.write('#endif')
			self.write('\t}\n#endif', '/*', feature.name, '*/')
			self.newLine()

		# Check for extension presense for extension features in addition to #define.
		for feature in self.extensionFeatures:
			self.write('#ifndef ANY' + feature.name)
			self.write('\tAny' + feature.name, '= AnyGL_queryExtension("' + feature.name + '");')
			if feature.functions:
				self.write('\tif (Any' + feature.name + ')\n\t{')
				compatibility = False
				for function in feature.functions:
					if function.name in ignoreFuncs:
						continue

					if function.compatibility != compatibility:
						if function.compatibility:
							self.write('#if !ANYGL_APPLE')
						else:
							self.write('#endif')
						compatibility = function.compatibility
					if function.alias:
						self.write('\t\tif (!AnyGL_' + function.alias + ')')
						self.write('\t\t\tAnyGL_' + function.alias + ' = (' + \
							function.type + ')&' + function.name + ';')
					else:
						self.write('\t\tAnyGL_' + function.name + ' = (' + function.type + ')&' + \
							function.name + ';')
				if compatibility:
					self.write('#endif')
				self.write('\t}')
			self.write('#endif', '/*', feature.name, '*/')
			self.newLine()

		self.write('\tAnyGL_initDebug();')
		self.write('\treturn 1;\n}')

		self.newLine()
		self.write('#endif /* ANYGL_LOAD */')

		OutputGenerator.endFile(self)

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		if emit:
			self.curFeature = FeatureInfo(interface, self.coreVersion)

	def endFeature(self):
		if self.curFeature:
			if self.curFeature.loadFirst:
				self.firstFeatures.append(self.curFeature)
			elif self.curFeature.extension:
				self.extensionFeatures.append(self.curFeature)
			else:
				self.coreFeatures.append(self.curFeature)
			self.curFeature = None
		OutputGenerator.endFeature(self)

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		self.curFeature.functions.append(FptrFunctionInfo(cmdinfo.elem, self.curFeature.name))
