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

	def write(self, *args):
		write(*args, file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)
		self.write('#include "AnyGL.h"')
		self.write('#include "gl.h"')
		self.newLine()
		self.write('#if ANYGL_LOAD == ANYGL_LOAD_WGL')
		self.write('#include "wgl.h"')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()

		self.write('int AnyGL_updateGLVersion(void);')
		self.write('int AnyGL_queryExtension(const char* name);')
		self.write('void AnyGL_initDebug(void);')
		self.write('extern HMODULE AnyGL_gllib;')
		self.newLine()

	def endFile(self):
		self.write('int AnyGL_load(void)\n{')
		self.write('\tif (!AnyGL_gllib || !wglGetCurrentContext())')
		self.write('\t\treturn 0;')

		# Load these features from the OpenGL library.
		for feature in self.firstFeatures:
			self.newLine()
			self.write('\t/*', feature.name, '*/')
			for function in feature.functions:
				self.write('\tAnyGL_' + function.name, '= (' + function.type + \
					')GetProcAddress(AnyGL_gllib, "' + function.name + '");')

		# Get the OpenGL version.
		self.newLine()
		self.write('\tif (!AnyGL_updateGLVersion())')
		self.write('\t\treturn 0;')

		# Load the core features.
		for feature in self.coreFeatures:
			self.newLine()
			self.write('\t/*', feature.name, '*/')
			self.write('\tif (AnyGL_atLeastVersion(' + feature.version[0] + ',', feature.version[2] + \
				', 0))\n\t{')
			for function in feature.functions:
				self.write('\t\tAnyGL_' + function.name, '= (' + function.type + \
					')wglGetProcAddress("' + function.name + '");')
			self.write('\t}\n\telse\n\t{')
			for function in feature.functions:
				self.write('\t\tAnyGL_' + function.name, '= NULL;')
			self.write('\t}')

		# Load the extensions.
		for feature in self.extensionFeatures:
			self.newLine()
			self.write('\t/*', feature.name, '*/')
			self.write('\tAny' + feature.name, '= AnyGL_queryExtension("' + feature.name + '");')
			if not feature.functions:
				continue
			self.write('\tif (Any' + feature.name + ')\n\t{')
			for function in feature.functions:
				if function.alias:
					self.write('\t\tif (!AnyGL_' + function.alias + ')')
					self.write('\t\t\tAnyGL_' + function.alias, '= (' + function.type + \
						')wglGetProcAddress("' + function.name + '");')
				else:
					self.write('\t\tAnyGL_' + function.name, '= (' + function.type + \
						')wglGetProcAddress("' + function.name + '");')
			self.write('\t}\n\telse\n\t{')
			for function in feature.functions:
				if not function.alias:
					self.write('\t\tAnyGL_' + function.name, '= NULL;')
			self.write('\t}')

		self.newLine()
		self.write('\tAnyGL_initDebug();')
		self.write('\treturn 1;\n}')

		self.newLine()
		self.write('#endif /* ANYGL_LOAD */')

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
