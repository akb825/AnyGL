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

class FunctionPointerGenerator(OutputGenerator):
	def __init__(self, errFile = sys.stderr, warnFile = sys.stderr, diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.curFeature = None
		self.functions = []

	def newLine(self):
		write('', file = self.outFile)

	def write(self, *args):
		write(*args, file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)
		self.write('#include "gl.h"')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()
		self.write('ANYGL_EXPORT GLenum AnyGL_HALF_FLOAT = GL_HALF_FLOAT;')
		self.newLine()

	def endFile(self):
		self.newLine()

		self.write('void AnyGL_clearFunctionPointers(void)')
		self.write('{')
		for function in self.functions:
			self.write('\tAnyGL_' + function + ' = NULL;')
		self.write('}')
		OutputGenerator.endFile(self)

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		if emit:
			self.curFeature = interface.get('name')
			if interface.tag == 'extension':
				self.write('ANYGL_EXPORT int', 'Any' + self.curFeature + ';')

	def endFeature(self):
		self.curFeature = None
		OutputGenerator.endFeature(self)

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		function = FunctionInfo(cmdinfo.elem, self.curFeature)
		if not function.alias:
			self.write('ANYGL_EXPORT', function.type, 'AnyGL_' + function.name + ';')
			self.functions.append(function.name)
