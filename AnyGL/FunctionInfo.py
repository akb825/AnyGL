# Copyright 2017-2025 Aaron Barany
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

manualFeatureAliases = {
	'GL_OES_blend_equation_separate': 'OES',
	'GL_OES_blend_func_separate': 'OES',
	'GL_OES_blend_subtract': 'OES',
	'GL_OES_framebuffer_object': 'OES',
	'GL_EXT_framebuffer_object': 'EXT',
	'GL_ARB_robustness': 'ARB',
	'GL_EXT_robustness': 'EXT',
	'GL_EXT_blend_func_extended': 'EXT',
	'GL_EXT_disjoint_timer_query': 'EXT',
	'GL_EXT_occlusion_query_boolean': 'EXT',
	'GL_EXT_shader_image_load_store': 'EXT'
}

manualFunctionAliases = {
	'glDeleteTexturesEXT': 'EXT',
	'glGenTexturesEXT': 'EXT',
	'glIsTextureEXT': 'EXT',
	'glClipControlEXT': 'EXT',
	'glProgramParameteriARB': 'ARB',
	'glFramebufferTextureARB': 'ARB',
	'glFramebufferTextureLayerARB': 'ARB'
}

class ParamInfo:
	def __init__(self, element):
		self.group = element.get('group')
		self.type = noneStr(element.text)
		typeElem = element.find('ptype')
		if typeElem != None:
			self.type += noneStr(typeElem.text) + noneStr(typeElem.tail)
		self.type = self.type.strip()
		self.name = noneStr(element.find('name').text)

class FunctionInfo:
	def __init__(self, cmd, feature = None):
		self.proto = cmd.find('proto')
		self.params = cmd.findall('param')

		self.type = None
		self.returnType = noneStr(self.proto.text)
		for elem in self.proto:
			if elem.tag == 'name':
				self.name = noneStr(elem.text)
				break
			else:
				self.returnType += noneStr(elem.text) + noneStr(elem.tail)
		self.returnType = self.returnType.strip()

		alias = cmd.find('alias')
		if alias == None or alias.get('name') == self.name:
			self.alias = None
			if feature:
				if feature in manualFeatureAliases:
					self.alias = self.name[:-len(manualFeatureAliases[feature])]
			if self.name in manualFunctionAliases:
				self.alias = self.name[:-len(manualFunctionAliases[self.name])]
		else:
			self.alias = alias.get('name')

		if self.alias:
			self.type = 'PFNANY' + self.alias.upper() + 'PROC'
		else:
			self.type = 'PFNANY' + self.name.upper() + 'PROC'

	def getArgList(self):
		n = len(self.params)
		decl = '('
		for i in range(n):
			decl += str().join([t for t in self.params[i].itertext()])
			if i < n - 1:
				decl += ', '
		decl += ')'
		return decl

	def getParamList(self):
		params = []
		for param in self.params:
			params.append(ParamInfo(param))
		return params

	def getTypeDecl(self):
		decl = 'typedef ' + noneStr(self.proto.text)
		for elem in self.proto:
			text = noneStr(elem.text)
			tail = noneStr(elem.tail)
			if elem.tag == 'name':
				decl += '(APIENTRY* ' + self.type + ')'
			else:
				decl += text + tail

		return decl + self.getArgList() + ';'

	def getFunctionDecl(self):
		decl = 'APIENTRY ' + noneStr(self.proto.text)
		for elem in self.proto:
			text = noneStr(elem.text)
			tail = noneStr(elem.tail)
			decl += text + tail

		return decl + self.getArgList() + ';'
