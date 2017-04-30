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

	def newLine(self):
		write('', file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)
		write('#include "gl.h"', file = self.outFile)
		self.newLine()

		write('/* Generated by AnyGL. */', file = self.outFile)
		self.newLine()

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		if emit:
			self.curFeature = interface.get('name')
			if interface.tag == 'extension':
				write('ANYGL_EXPORT int', 'AnyGL_' + self.curFeature[3:] + ';', file = self.outFile)

	def endFeature(self):
		self.curFeature = None
		OutputGenerator.endFeature(self)

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		function = FunctionInfo(cmdinfo.elem, feature = self.curFeature)
		if not function.alias:
			write('ANYGL_EXPORT', function.type, 'AnyGL_' + function.name + ';',
				file = self.outFile)
