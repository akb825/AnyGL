#!/bin/python
#
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

class FunctionInfo:
	def __init__(self, cmd, typePrefix = ''):
		self.proto = cmd.find('proto')
		self.params = cmd.findall('param')
		alias = cmd.find('alias')
		if alias == None:
			self.alias = None
		else:
			self.alias = alias.get('name')

		self.type = None
		for elem in self.proto:
			if elem.tag == 'name':
				text = noneStr(elem.text)
				tail = noneStr(elem.tail)
				self.name = noneStr(elem.text)

		if self.alias:
			self.type = typePrefix + 'PFN' + self.alias.upper() + 'PROC'
		else:
			self.type = typePrefix + 'PFN' + self.name.upper() + 'PROC'

	def getArgList(self):
		n = len(self.params)
		decl = '('
		for i in range(0, n):
			decl += str().join([t for t in self.params[i].itertext()])
			if i < n - 1:
				decl += ', '
		decl += ')'
		return decl

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
