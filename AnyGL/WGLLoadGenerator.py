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
		if self.extension:
			self.version = None
		else:
			self.version = interface.get('number')

		self.loadFirst = self.version != None and float(self.version) <= 1.1
		self.functions = []

class WGLLoadGenerator(OutputGenerator):
	def __init__(self, errFile = sys.stderr, warnFile = sys.stderr, diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.firstFeatures = []
		self.coreFeatures = []
		self.extensionFeatures = []
		self.curFeature = None

	def newLine(self):
		write('', file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)
		write('#include "AnyGL.h"', file = self.outFile)
		write('#include "gl.h"', file = self.outFile)
		self.newLine()
		write('#if ANYGL_LOAD == ANYGL_LOAD_WGL', file = self.outFile)
		write('#include "wgl.h"', file = self.outFile)
		self.newLine()

		write('/* Generated by AnyGL. */', file = self.outFile)
		self.newLine()

		write('int AnyGL_updateGLVersion(void);', file = self.outFile)
		write('int AnyGL_queryExtension(const char* name);', file = self.outFile)
		write('extern HMODULE AnyGL_gllib;', file = self.outFile)
		self.newLine()

	def endFile(self):
		write('int AnyGL_load(void)\n{', file = self.outFile)
		write('\tif (!AnyGL_gllib || !wglGetCurrentContext())', file = self.outFile)
		write('\t\treturn 0;', file = self.outFile)

		# Load these features from the OpenGL library.
		for feature in self.firstFeatures:
			self.newLine()
			write('\t/*', feature.name, '*/', file = self.outFile)
			for function in feature.functions:
				write('\tAnyGL_' + function.name, '= (' + function.type + \
					')GetProcAddress(AnyGL_gllib, "' + function.name + '");', file = self.outFile)

		# Get the OpenGL version.
		self.newLine()
		write('\tif (!AnyGL_updateGLVersion())', file = self.outFile)
		write('\t\treturn 0;', file = self.outFile)

		# Load the core features.
		for feature in self.coreFeatures:
			self.newLine()
			write('\t/*', feature.name, '*/', file = self.outFile)
			write('\tif (AnyGL_atLeastVersion(' + feature.version[0] + ',', feature.version[2] + \
				', 0))\n\t{', file = self.outFile)
			for function in feature.functions:
				write('\t\tAnyGL_' + function.name, '= (' + function.type + \
					')wglGetProcAddress("' + function.name + '");', file = self.outFile)
			write('\t}\n\telse\n\t{', file = self.outFile)
			for function in feature.functions:
				write('\t\tAnyGL_' + function.name, '= NULL;', file = self.outFile)
			write('\t}', file = self.outFile)

		# Load the extensions.
		for feature in self.extensionFeatures:
			self.newLine()
			write('\t/*', feature.name, '*/', file = self.outFile)
			write('\tAny' + feature.name, '= AnyGL_queryExtension("' + feature.name + '");',
				file = self.outFile)
			if not feature.functions:
				continue
			write('\tif (Any' + feature.name + ')\n\t{', file = self.outFile)
			for function in feature.functions:
				if function.alias:
					write('\t\tif (!AnyGL_' + function.alias + ')', file = self.outFile)
					write('\t\t\tAnyGL_' + function.alias, '= (' + function.type + \
						')wglGetProcAddress("' + function.name + '");', file = self.outFile)
				else:
					write('\t\tAnyGL_' + function.name, '= (' + function.type + \
						')wglGetProcAddress("' + function.name + '");', file = self.outFile)
			write('\t}\n\telse\n\t{', file = self.outFile)
			for function in feature.functions:
				if not function.alias:
					write('\t\tAnyGL_' + function.name, '= NULL;', file = self.outFile)
			write('\t}', file = self.outFile)

		self.newLine()
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
		function = FunctionInfo(cmdinfo.elem, self.curFeature.name)
		self.curFeature.functions.append(function)
