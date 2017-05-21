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
			self.version = float(interface.get('number'))

		# glXGetProcAddress() was introduced in version 1.4, meaning that's the first version we
		# can be guaranteed to dynamically load newer functions.
		self.isCore = self.version != None and self.version <= 1.4
		self.functions = []

class GLXInitGenerator(OutputGenerator):
	def __init__(self, errFile = sys.stderr, warnFile = sys.stderr, diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.coreFeatures = []
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
		self.write('#if ANYGL_LOAD == ANYGL_LOAD_GLX')
		self.write('#include <GL/glx.h>')
		self.write('#define ANYGL_NO_FUNCTION_DEFINES')
		self.write('#include "glx.h"')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()

	def endFile(self):
		# Function pointers.
		for feature in self.coreFeatures:
			for function in feature.functions:
				self.write('ANYGL_EXPORT', function.type, 'AnyGL_' + function.name + ';')
		for feature in self.extensionFeatures:
			for function in feature.functions:
				self.write('ANYGL_EXPORT', function.type, 'AnyGL_' + function.name + ';')
		self.newLine()

		self.write('int AnyGL_initialize(void)\n{')

		self.write('\tstatic int initialized;')
		self.write('\tif (initialized)')
		self.write('\t\treturn 1;')
		self.newLine()

		# Core functions load from system pointers.
		for feature in self.coreFeatures:
			self.write('#ifndef', 'ANY' + feature.name)
			for function in feature.functions:
				self.write('\tAnyGL_' + function.name + ' = &' + function.name + ';')
			self.write('#endif', '/*', feature.name, '*/')
			self.newLine()

		# Special handling for glXGetProcAddressARB
		self.write('#ifndef ANYGLX_ARB_get_proc_address')
		self.write('\tif (!AnyGL_glXGetProcAddress)')
		self.write('\t\tAnyGL_glXGetProcAddress = &glXGetProcAddressARB;')
		self.write('#endif /* GLX_ARB_get_proc_address */')
		self.newLine()

		# Extension functions load from glXGetProcAddress.
		self.write('\tif (!AnyGL_glXGetProcAddress)')
		self.write('\t\treturn 0;')
		self.newLine()

		for feature in self.extensionFeatures:
			self.write('\t/*', feature.name, '*/')
			for function in feature.functions:
				self.write('\tAnyGL_' + function.name + ' = (' + function.type + \
					')AnyGL_glXGetProcAddress((const GLubyte*)"' + function.name + '");')
			self.newLine()

		self.write('\tinitialized = 1;')
		self.write('\treturn 1;\n}')

		self.newLine()
		self.write('void AnyGL_shutdown(void) {}')

		self.newLine()
		self.write('#endif /* ANYGL_LOAD */')

		OutputGenerator.endFile(self)

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		if emit:
			self.curFeature = FeatureInfo(interface)

	def endFeature(self):
		if self.curFeature:
			if self.curFeature.isCore:
				self.coreFeatures.append(self.curFeature)
			else:
				self.extensionFeatures.append(self.curFeature)
			self.curFeature = None
		OutputGenerator.endFeature(self)

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		self.curFeature.functions.append(FunctionInfo(cmdinfo.elem))
