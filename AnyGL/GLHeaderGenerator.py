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

class ElementInfo:
	def __init__(self, text, require):
		self.text = text
		self.require = require

class FeatureInfo:
	def __init__(self, interface):
		self.name = interface.get('name')
		self.extension = interface.tag == 'extension'
		self.types = []
		self.enums = []
		self.functions = []

class GLHeaderGenerator(OutputGenerator):
	def __init__(self, errFile = sys.stderr, warnFile = sys.stderr, diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.lastTypeRequire = None
		self.glesOnlyTypes = ['khrplatform']
		self.glOnlyTypes = \
			[
				'stddef',
				'inttypes',
				'GLfloat',
				'GLclampf',
			]
		self.curFeature = None
		self.features = []

	def newLine(self):
		write('', file = self.outFile)

	def write(self, *args):
		write(*args, file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)
		if self.genOpts.filename:
			headerSym = '__AnyGL_' + re.sub('\.h', '_h_', os.path.basename(self.genOpts.filename))
			self.write('#pragma once')
			self.write('#ifndef', headerSym)
			self.write('#define', headerSym, '1')
			self.newLine()

		self.write('#include "AnyGLConfig.h"')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()

		self.write('#ifdef __cplusplus')
		self.write('extern "C" {')
		self.write('#endif')
		self.newLine()

		self.write('#if defined(__clang__)')
		self.write('#pragma GCC diagnostic push')
		self.write('#pragma GCC diagnostic ignored "-Wmacro-redefined"')
		self.write('#elif defined(_MSC_VER)')
		self.write('#pragma warning(push)')
		self.write('#pragma warning(disable: 4005)')
		self.write('#endif')
		self.newLine()

		self.write('#define ANYGL_SUPPORTED(func) (AnyGL_ ## func != 0)')

		self.newLine()
		self.write('ANYGL_EXPORT void AnyGL_setLastCallsite(const char* file, ' \
			'const char* function, unsigned int line);')
		self.write('#if ANYGL_ALLOW_DEBUG')
		self.write('#define ANYGL_CALL(func) (AnyGL_setLastCallsite(__FILE__, __FUNCTION__,' \
			'__LINE__), (func))')
		self.write('#else')
		self.write('#define ANYGL_CALL(func) (func)')
		self.write('#endif')
		self.newLine()

	def endFile(self):
		self.write('/* handle include for standard gl.h */')
		for feature in self.features:
			self.write('#ifndef', feature.name)
			self.write('#define', feature.name, '1')
			self.write('#define ANY' + feature.name, '1')
			self.write('#endif')
			if feature.extension:
				self.write('ANYGL_EXPORT extern int Any' + feature.name + ';')
			self.newLine()

		self.write('/* Type declarations */')

		# Basic types are now use khrplatform with the latest spec, which is only guaranteed to be
		# available on GLES platforms. Need to manually declare them for desktop platforms.
		self.write('#if !ANYGL_GLES')
		self.write('#include <stddef.h>')
		self.write('#include <stdint.h>')
		self.write('typedef int8_t GLbyte;')
		self.write('typedef uint8_t GLubyte;')
		self.write('typedef int16_t GLshort;')
		self.write('typedef uint16_t GLushort;')
		self.write('typedef uint16_t GLushort;')
		self.write('typedef float GLfloat;')
		self.write('typedef float GLclampf;')
		self.write('typedef uint16_t GLhalf;')
		self.write('typedef int32_t GLfixed;')
		self.write('typedef ptrdiff_t GLintptr;')
		self.write('typedef ptrdiff_t GLsizeiptr;')
		self.write('typedef int64_t GLint64;')
		self.write('typedef uint64_t GLuint64;')
		self.write('#endif')
		self.newLine()

		for feature in self.features:
			if not feature.types:
				continue

			# These features have overlap between the types.
			if feature.name == 'GL_VERSION_1_0'  or feature.name == 'GL_ES_VERSION_2_0':
				self.write('#if defined(ANYGL_VERSION_1_0) || defined(ANYGL_ES_VERSION_2_0)')
			else:
				self.write('#ifdef ANY' + feature.name)
			curRequire = None
			for elem in feature.types:
				if elem.require != curRequire:
					if curRequire:
						self.write('#endif')
					if elem.require:
						self.write('#if', elem.require)
					curRequire = elem.require
				self.write(elem.text)
			if curRequire:
				self.write('#endif')
			self.write('#endif /*', feature.name, '*/')
			self.newLine()

		self.write('/* Enum definitions */')
		self.write('#ifndef ANYGL_NO_DEFINES')
		for feature in self.features:
			if not feature.enums:
				continue

			self.write('#ifdef ANY' + feature.name)
			curRequire = None
			for elem in feature.enums:
				if elem.require != curRequire:
					if curRequire:
						self.write('#endif')
					if elem.require:
						self.write('#if', elem.require)
					curRequire = elem.require
				self.write(elem.text)
			if curRequire:
				self.write('#endif')
			self.write('#endif /*', feature.name, '*/')
			self.newLine()
		self.write('#endif /* ANYGL_NO_DEFINES */')

		self.write('/* Workaround for GL_HALF_FLOAT_OES */')
		self.write('ANYGL_EXPORT extern GLenum AnyGL_HALF_FLOAT;')
		self.newLine()

		self.write('/* Function declarations */')
		for feature in self.features:
			self.write('/*', feature.name, '*/')
			for function in feature.functions:
				if not function.alias:
					self.write(function.getTypeDecl())
			self.newLine()

			for function in feature.functions:
				if not function.alias:
					self.write('ANYGL_EXPORT extern', function.type,
						'AnyGL_' + function.name + ';')
			self.newLine()

			self.write('#ifndef ANYGL_NO_DEFINES')
			for function in feature.functions:
				params = '('
				paramList = function.getParamList()
				for param in paramList:
					if param != paramList[0]:
						params += ', '
					params += param.name
				params += ')'

				if function.alias:
					self.write('#define', function.name + params, 'ANYGL_CALL(AnyGL_' + \
						function.alias + ')' + params)
				else:
					self.write('#define', function.name + params, 'ANYGL_CALL(AnyGL_' + \
						function.name + ')' + params)
			self.write('#endif /* ANYGL_NO_DEFINES */')
			self.newLine()

		self.write('#if defined(__clang__)')
		self.write('#pragma GCC diagnostic pop')
		self.write('#elif defined(_MSC_VER)')
		self.write('#pragma warning(pop)')
		self.write('#endif')
		self.newLine()

		self.write('#ifdef __cplusplus')
		self.write('}')
		self.write('#endif')

		if self.genOpts.filename:
			self.newLine()
			self.write('#endif')

		OutputGenerator.endFile(self)

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		if emit:
			self.curFeature = FeatureInfo(interface)

	def endFeature(self):
		self.features.append(self.curFeature)
		self.curFeature = None

	def genType(self, typeinfo, name):
		OutputGenerator.genType(self, typeinfo, name)

		# Types are declared differently between GLES and desktop GL.
		typeElem = typeinfo.elem
		require = None
		# Special cases.
		name = typeElem.get('name')
		if name == 'GLuint64EXT':
			typeElem.text = 'typedef GLuint64 '
		else:
			requires = typeElem.get('requires')
			if requires == 'khrplatform':
				require = 'ANYGL_GLES'
			elif requires in self.glOnlyTypes:
				require = '!ANYGL_GLES'
			else:
				if name in self.glesOnlyTypes:
					require = 'ANYGL_GLES'
				elif name in self.glOnlyTypes:
					require = '!ANYGL_GLES'

		s = noneStr(typeElem.text)
		for elem in typeElem:
			if (elem.tag == 'apientry'):
				s += 'APIENTRY' + noneStr(elem.tail)
			else:
				s += noneStr(elem.text) + noneStr(elem.tail)
		if (len(s) > 0):
			self.curFeature.types.append(ElementInfo(s, require))

	def genEnum(self, enuminfo, name):
		OutputGenerator.genEnum(self, enuminfo, name)

		s = '#define ' + name.ljust(33) + ' ' + enuminfo.elem.get('value')
		# Handle non-integer 'type' fields by using it as the C value suffix
		t = enuminfo.elem.get('type')
		if (t != '' and t != 'i'):
			s += enuminfo.type

		self.curFeature.enums.append(ElementInfo(s, None))

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		self.curFeature.functions.append(FunctionInfo(cmdinfo.elem, self.curFeature.name))
