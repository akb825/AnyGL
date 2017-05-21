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

class GLXWHeaderGenerator(OutputGenerator):
	def __init__(self, systemIncludes, define, systemDefines = [], extensionsOnly = True,
		errFile = sys.stderr, warnFile = sys.stderr, diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.systemIncludes = systemIncludes
		self.define = define
		self.systemDefines = systemDefines
		self.extensionsOnly = extensionsOnly
		self.curFunctions = []
		self.curFeature = None
		self.extension = False

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
		self.write('#include "gl.h"')
		self.newLine()
		self.write('#if ANYGL_LOAD ==', self.define)
		for define in self.systemDefines:
			self.write('#define', define)
		for include in self.systemIncludes:
			self.write('#include <' + include + '>')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()

		self.write('#ifdef __cplusplus')
		self.write('extern "C" {')
		self.write('#endif')
		self.newLine()

	def endFile(self):
		self.newLine()
		self.write('#ifdef __cplusplus')
		self.write('}')
		self.write('#endif')

		self.newLine()
		self.write('#endif /* ANYGL_LOAD */')
		self.newLine()

		if self.genOpts.filename:
			self.write('#endif')

		OutputGenerator.endFile(self)

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		self.extension = interface.tag == 'extension'
		if emit:
			self.curFeature = interface.get('name')
			# Special case for GLX version 1.0.
			if self.curFeature == 'GLX_VERSION_1_0':
				self.write('#ifndef GLX_EXTENSION_NAME')
			else:
				self.write('#ifndef', self.curFeature)
			self.write('#define', self.curFeature, '1')
			self.write('#define ANY' + self.curFeature, '1')
			self.newLine()

	def endFeature(self):
		self.newLine()

		if self.curFeature:
			self.write('#endif', '/*', self.curFeature, '*/')
			self.curFeature = None

		if self.curFunctions:
			if self.extension or not self.extensionsOnly:
				# Function types
				for function in self.curFunctions:
					if not function.alias:
						self.write(function.getTypeDecl())
				self.newLine()

				# Function pointers
				for function in self.curFunctions:
					if not function.alias:
						self.write('ANYGL_EXPORT extern', function.type, 'AnyGL_' + \
							function.name + ';')
				self.newLine()

				# Function defines.
				self.write('#ifndef ANYGL_NO_FUNCTION_DEFINES')
				for function in self.curFunctions:
					name = function.name
					if function.alias:
						name = function.alias
					self.write('#define', function.name, 'AnyGL_' + name)
				self.write('#endif /* ANYGL_NO_FUNCTION_DEFINES */')
			else:
				for function in self.curFunctions:
					self.write(function.getFunctionDecl())

		self.newLine()
		self.curFunctions = []
		OutputGenerator.endFeature(self)

	def genType(self, typeinfo, name):
		OutputGenerator.genType(self, typeinfo, name)

		typeElem = typeinfo.elem
		s = noneStr(typeElem.text)
		for elem in typeElem:
			if (elem.tag == 'apientry'):
				s += 'APIENTRY' + noneStr(elem.tail)
			else:
				s += noneStr(elem.text) + noneStr(elem.tail)
		if (len(s) > 0):
			self.write(s)

	def genEnum(self, enuminfo, name):
		OutputGenerator.genEnum(self, enuminfo, name)

		s = '#define ' + name.ljust(33) + ' ' + enuminfo.elem.get('value')
		#
		# Handle non-integer 'type' fields by using it as the C value suffix
		t = enuminfo.elem.get('type')
		if (t != '' and t != 'i'):
			s += enuminfo.type
		self.write(s)

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		self.curFunctions.append(FunctionInfo(cmdinfo.elem))
