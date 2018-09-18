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

class EnumInfo:
	def __init__(self, enum, name):
		self.name = name
		self.value = int(enum.elem.get('value'), 16)

	def __eq__(self, other):
		return self.value == other.value

	def __lt__(self, other):
		return self.value < other.value

	def __hash__(self):
		return hash(self.value)

class DebugGenerator(OutputGenerator):
	def __init__(self, registry, errFile = sys.stderr, warnFile = sys.stderr,
			diagFile = sys.stdout):
		OutputGenerator.__init__(self, errFile, warnFile, diagFile)
		self.registry = registry
		self.curFeature = None
		self.functions = []
		self.enums = []

	def newLine(self):
		write('', file = self.outFile)

	def write(self, *args):
		write(*args, file = self.outFile)

	def beginFile(self, genOpts):
		OutputGenerator.beginFile(self, genOpts)
		self.write('#include "AnyGL.h"')
		self.write('#include "gl.h"')
		self.write('#if ANYGL_WINDOWS')
		self.write('#define WIN32_LEAN_AND_MEAN')
		self.write('#ifndef _CRT_SECURE_NO_DEPRECATE')
		self.write('#define _CRT_SECURE_NO_DEPRECATE')
		self.write('#endif')
		self.write('#ifndef _CRT_NONSTDC_NO_DEPRECATE')
		self.write('#define _CRT_NONSTDC_NO_DEPRECATE')
		self.write('#endif')
		self.write('#undef APIENTRY')
		self.write('#include <Windows.h>')
		self.write('#undef near')
		self.write('#undef far')
		self.write('#if _MSC_VER < 1400')
		self.write('#define snprintf _snprintf')
		self.write('#endif')
		self.write('#endif')
		self.write('#include <stdio.h>')
		self.write('#include <string.h>')
		self.newLine()
		self.write('#define PRINT_BUFFER_SIZE 1024')
		self.write('#ifdef _MSC_VER')
		self.write('#define ANYGL_THREAD __declspec(thread)')
		self.write('#define SIZET_FORMAT "I"')
		self.write('#else')
		self.write('#define ANYGL_THREAD __thread')
		self.write('#define SIZET_FORMAT "z"')
		self.write('#endif')
		self.write('#if ANYGL_APPLE')
		self.write('#define HANDLE_FORMAT "p"')
		self.write('#else')
		self.write('#define HANDLE_FORMAT "u"')
		self.write('#endif')
		self.newLine()

		self.write('/* Generated by AnyGL. */')
		self.newLine()

	def outputEnums(self, groupName, enums):
		orderedEnums = sorted(set(enums))
		self.write('static const char* get' + groupName + 'EnumStr(GLenum e)\n{')

		self.write('\tstatic const char* enumNames[] =\n\t{')
		for enum in orderedEnums:
			self.write('\t\t"' + enum.name + '",')
		self.write('\t};')
		self.newLine()

		firstIndex = 0
		lastValue = None
		for i in range(len(orderedEnums)):
			enum = orderedEnums[i]
			if lastValue != None and (enum.value != lastValue + 1):
				firstValue = orderedEnums[firstIndex].value
				if firstValue:
					self.write('\tif (e >=', hex(firstValue), '&& e <=', hex(lastValue) + ')')
				else:
					self.write('\tif (e <=', hex(lastValue) + ')')
				self.write('\t\treturn enumNames[e -', hex(firstValue), '+', str(firstIndex) + '];')
				firstIndex = i
			lastValue = enum.value

		if lastValue != None:
			firstValue = orderedEnums[firstIndex].value
			if firstValue:
				self.write('\tif (e >=', hex(firstValue), '&& e <=', hex(lastValue) + ')')
			else:
				self.write('\tif (e <=', hex(lastValue) + ')')
			self.write('\t\treturn enumNames[e -', hex(firstValue), '+', str(firstIndex) + '];')

		self.write('\treturn "INVALID";\n}')
		self.newLine()

	def getFormatStr(self, param, groups):
		ptype = param.type
		if ptype == 'GLenum' or ptype == 'GLboolean' or ptype == 'const GLchar *' or \
			(param.group and param.group in groups and ptype[-1] != '*'):
			return '%s'
		elif ptype[-1] == '*' or (len(ptype) > 4 and ptype[-4:] == 'PROC') or \
			ptype == 'GLsync' or ptype == 'GLeglImageOES' or ptype == 'GLeglClientBufferEXT':
			return '%p'
		elif ptype == 'GLbyte' or ptype == 'GLshort' or ptype == 'GLint' or ptype == 'GLsizei':
			return '%i'
		elif ptype == 'GLubyte' or ptype == 'GLushort' or ptype == 'GLuint':
			return '%u'
		elif ptype == 'GLint64':
			return '%lli'
		elif ptype == 'GLuint64' or ptype == 'GLuint64EXT':
			return '%llu'
		elif ptype == 'GLfloat' or ptype == 'GLdouble' or ptype == 'GLclampf' or ptype == 'GLclampd':
			return '%f'
		elif ptype == 'GLbitfield' or ptype == 'GLhalf' or ptype == 'GLhalfARB' or \
			ptype == 'GLfixed':
			return '0x%x'
		elif ptype == 'GLchar' or ptype == 'GLcharARB':
			return '%c'
		elif ptype == 'GLintptr' or ptype == 'GLsizeiptr':
			return '%" SIZET_FORMAT "i'
		elif ptype == 'GLhandleARB':
			return '%" HANDLE_FORMAT "'
		else:
			raise Exception('Unknown type: ' + ptype)

	def getFormatArg(self, param, groups):
		if param.group and param.group in groups and param.type[-1] != '*':
			return 'get' + param.group + 'EnumStr(' + param.name + ')'
		elif param.type == 'GLboolean':
			return 'getBooleanEnumStr(' + param.name + ')'
		elif param.type == 'GLenum':
			return 'getAnyEnumStr(' + param.name + ')'
		elif param.type == 'GLint64':
			return '(long long)' + param.name
		elif param.type == 'GLuint64' or param.type == 'GLuint64EXT':
			return '(unsigned long long)' + param.name
		else:
			return param.name

	def outputDebugFunction(self, function, groups):
		self.write('static', function.returnType, 'APIENTRY debug_' + function.name + \
			function.getArgList())
		self.write('{')
		self.write('\tconst CallsiteInfo* _curCallsiteInfo = &callsiteInfo;')

		params = function.getParamList()
		paramForward = ''
		formatStr = function.name + '('
		formatArgs = ''
		for i in range(len(params)):
			if i > 0:
				paramForward += ', '
				formatStr += ', '
			paramForward += params[i].name
			formatStr += self.getFormatStr(params[i], groups)
			formatArgs += ', ' + self.getFormatArg(params[i], groups)
		formatStr += ')'
		if function.returnType == 'void':
			self.write('\t' + 'default_' + function.name + '(' + paramForward + ');')
		else:
			self.write('\t' + function.returnType, 'retVal =', 'default_' + function.name + '(' + \
				paramForward + ');')

		self.write('\tif (!_curCallsiteInfo->disableErrorChecks)\n\t{')
		self.write('\t\tGLenum _error = AnyGL_glGetError();')
		self.write('\t\tif (_error != GL_NO_ERROR)\n\t\t{')
		self.write('\t\t\tchar _buffer[PRINT_BUFFER_SIZE];')
		self.write('\t\t\tint _length = snprintf(_buffer, PRINT_BUFFER_SIZE,',
			'"' + formatStr + '"' + formatArgs + ');')
		self.write('\t\t\tif (_length < 0 || _length >= PRINT_BUFFER_SIZE)')
		self.write('\t\t\t\tstrncpy(_buffer, "' + function.name + '()", PRINT_BUFFER_SIZE);')
		self.write('\t\t\terrorFunc(_curCallsiteInfo->lastFile, _curCallsiteInfo->lastFunction, ' \
			'_curCallsiteInfo->lastLine, _error, _buffer);')
		self.write('\t\t}\n\t}')

		if function.returnType != 'void':
			self.write('\treturn retVal;')
		self.write('}')
		self.newLine()

	def hasAllEnums(self, group, enumDict):
		for enum in group.enums:
			if enum not in enumDict:
				return False
		return True

	def endFile(self):
		self.write('#if ANYGL_ALLOW_DEBUG')
		self.newLine()

		# Function pointers for default functions.
		for function in self.functions:
			self.write('static', function.type, 'default_' + function.name + ';')
		self.newLine()

		# Enum value to string mappings.
		enumDict = {}
		for enum in self.enums:
			enumDict[enum.name] = enum
		usedGroups = set()
		for function in self.functions:
			for param in function.getParamList():
				if (param.type == 'GLenum' or param.type == 'GLboolean') and param.group:
					usedGroups.add(param.group)

		self.outputEnums('Any', self.enums)
		groups = set()
		for groupName, group in self.registry.groupdict.items():
			if groupName in usedGroups and self.hasAllEnums(group, enumDict):
				groups.add(groupName)
				enums = []
				for groupEnum in group.enums:
					enums.append(enumDict[groupEnum])
				self.outputEnums(groupName, enums)

		self.write('static void defaultErrorFunc(const char* file, const char* function, ' \
			'unsigned int line, unsigned int glError, const char* glFunction)\n{')
		self.write('#if ANYGL_WINDOWS')
		self.write('\tchar buffer[PRINT_BUFFER_SIZE];')
		self.write('\tint length = snprintf(buffer, PRINT_BUFFER_SIZE, "%s(%u) %s(): [%s] %s\\n", ' \
			'file, line, function, AnyGL_errorString(glError), glFunction);')
		self.write('\tif (length >= 0 && length < PRINT_BUFFER_SIZE)\n\t{')
		self.write('\t\tfwrite(buffer, sizeof(char), strlen(buffer), stderr);')
		self.write('\t\tOutputDebugStringA(buffer);')
		self.write('\t}')
		self.write('\telse')
		self.write('\t\tfprintf(stderr, "%s(%u) %s(): [%s] %s\\n", file, line, function, ' \
			'AnyGL_errorString(glError), glFunction);')
		self.write('#else')
		self.write('\tfprintf(stderr, "%s:%u %s(): [%s] %s\\n", file, line, function, ' \
			'AnyGL_errorString(glError), glFunction);')
		self.write('#endif')
		self.write('}')
		self.newLine()
		self.write('static AnyGLErrorFunc errorFunc = defaultErrorFunc;')
		self.write('typedef struct CallsiteInfo\n{')
		self.write('\tint disableErrorChecks;')
		self.write('\tconst char* lastFile;')
		self.write('\tconst char* lastFunction;')
		self.write('\tunsigned int lastLine;')
		self.write('} CallsiteInfo;')
		self.write('static ANYGL_THREAD CallsiteInfo callsiteInfo;')
		self.newLine()

		# Wrapper functions.
		for function in self.functions:
			self.outputDebugFunction(function, groups)

		# Initialization.
		self.write('void AnyGL_initDebug(void)\n{')
		for function in self.functions:
			self.write('\tdefault_' + function.name, '=', 'AnyGL_' + function.name + ';')
		self.write('}')
		self.newLine()

		# Public API.
		self.write('void AnyGL_setErrorFunc(AnyGLErrorFunc func)\n{')
		self.write('\tif (func)')
		self.write('\t\terrorFunc = func;')
		self.write('\telse')
		self.write('\t\terrorFunc = &defaultErrorFunc;')
		self.write('}')
		self.newLine()

		self.write('int AnyGL_getDebugEnabled(void)\n{')
		self.write('\treturn AnyGL_glGetIntegerv == &debug_glGetIntegerv;')
		self.write('}')
		self.newLine()
		self.write('void AnyGL_setDebugEnabled(int enabled)\n{')
		self.write('\tif (enabled)\n\t{')
		for function in self.functions:
			self.write('\t\tif (default_' + function.name + ')')
			self.write('\t\t\tAnyGL_' + function.name, '= &debug_' + function.name + ';')
		self.write('\t}\n\telse\n\t{')
		for function in self.functions:
			self.write('\t\tAnyGL_' + function.name, '= default_' + function.name + ';')
		self.write('\t}\n}')
		self.newLine()

		self.write('int AnyGL_getErrorCheckingEnabled(void)\n{')
		self.write('\treturn !callsiteInfo.disableErrorChecks;')
		self.write('}')
		self.newLine()

		self.write('void AnyGL_setErrorCheckingEnabled(int enabled)\n{')
		self.write('\tcallsiteInfo.disableErrorChecks = !enabled;')
		self.write('}')
		self.newLine()

		self.write('void AnyGL_getLastCallsite(const char** file, const char** function,' \
			'unsigned int* line)\n{')
		self.write('\tconst CallsiteInfo* curCallsiteInfo = &callsiteInfo;')
		self.write('\tif (file)')
		self.write('\t\t*file = curCallsiteInfo->lastFile;')
		self.write('\tif (function)')
		self.write('\t\t*function = curCallsiteInfo->lastFunction;')
		self.write('\tif (line)')
		self.write('\t\t*line = curCallsiteInfo->lastLine;')
		self.write('}')
		self.newLine()

		self.write('void AnyGL_setLastCallsite(const char* file, const char* function,' \
			'unsigned int line)\n{')
		self.write('\tCallsiteInfo* curCallsiteInfo = &callsiteInfo;')
		self.write('\tcurCallsiteInfo->lastFile = file;')
		self.write('\tcurCallsiteInfo->lastFunction = function;')
		self.write('\tcurCallsiteInfo->lastLine = line;')
		self.write('}')
		self.newLine()

		self.write('#else')
		self.newLine()

		self.write('void AnyGL_initDebug(void) {}')
		self.write('void ANyGL_setErrorFunc(AnyGLErrorFunc func) {(void)func;}')
		self.write('int AnyGL_getDebugEnabled(void) {return 0;}')
		self.write('void AnyGL_setDebugEnabled(int enabled) {(void)enabled;}')
		self.write('int AnyGL_getErrorCheckingEnabled(void) {return 0;}')
		self.write('void AnyGL_setErrorCheckingEnabled(int enabled) {(void)enabled;}')
		self.write('void AnyGL_getLastCallsite(const char** file, const char** function,' \
			'unsigned int* line)\n{')
		self.write('\t(void)file;')
		self.write('\t(void)function;')
		self.write('\t(void)line;')
		self.write('}')
		self.write('void AnyGL_setLastCallsite(const char* file, const char* function,' \
			'unsigned int line)\n{')
		self.write('\t(void)file;')
		self.write('\t(void)function;')
		self.write('\t(void)line;')
		self.write('}')
		self.newLine()

		self.write('#endif /* ANYGL_ALLOW_DEBUG */')
		OutputGenerator.endFile(self)

	def beginFeature(self, interface, emit):
		OutputGenerator.beginFeature(self, interface, emit)
		if emit:
			self.curFeature = interface.get('name')

	def endFeature(self):
		self.curFeature = None
		OutputGenerator.endFeature(self)

	def genCmd(self, cmdinfo, name):
		OutputGenerator.genCmd(self, cmdinfo, name)
		function = FunctionInfo(cmdinfo.elem, self.curFeature)
		if not function.alias and function.name != 'glGetError':
			self.functions.append(function)

	def genEnum(self, enuminfo, name):
		OutputGenerator.genEnum(self, enuminfo, name)
		if not enuminfo.type:
			self.enums.append(EnumInfo(enuminfo, name))
