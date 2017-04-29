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

import errno, io, os, re, shutil, string, sys
from optparse import OptionParser
from lxml import etree

from AnyGL import *

options = OptionParser()
options.add_option('-i', '--input', dest = 'inDir', help = 'Input directory with the XML files.',
	default = 'OpenGLRegistry/xml')
options.add_option('-o', '--output', dest = 'outDir',
	help = 'Output directory for the generated files.', default = 'generated')
options.add_option('-t', '--template-dir', dest='templateDir',
	help = 'Directory with the template files. These will be copied to the generated output.',
	default = 'templates')
options.add_option('-p', '--profile', dest = 'profile',
	help = 'Profile to use, either core or compatibility.', default = 'core')
options.add_option('-e', '--extensions', dest = 'extensions',
	help = 'Regular expression for the extensions to include. ' \
	'Defaults to the ARB, EXT, OES and KHR extensions.',
	default = '(GL_ARB_.*)|(GL_EXT_.*)|(GL_OES_.*)|(GL_KHR_*)')
options.add_option('-v', '--verbose', dest = 'verbose', help = 'Verbose output.', default = False,
	action = 'store_true')
(args, argv) = options.parse_args()

glXml = os.path.join(args.inDir, 'gl.xml')
glxXml = os.path.join(args.inDir, 'glx.xml')
wglXml = os.path.join(args.inDir, 'wgl.xml')

try:
	os.makedirs(args.outDir)
except OSError as e:
	if e.errno != errno.EEXIST:
		raise

for entry in os.listdir(args.templateDir):
	if not entry or entry[0] == '.':
		continue
	path = os.path.join(args.templateDir, entry)
	if os.path.isfile(path):
		shutil.copy(path, args.outDir)

diagFile = None
if args.verbose:
	diagFile = sys.stdout

write('Parsing', glXml + '...')
glRegistry = Registry()
glRegistry.loadElementTree(etree.parse(glXml))

apiname = ['gl', 'gles2']
glHeaderOptions = GeneratorOptions(
	filename = os.path.join(args.outDir, 'gl.h'),
	apiname = apiname,
	profile = args.profile,
	addExtensions = args.extensions)
write('Outputting', glHeaderOptions.filename + '...')
glRegistry.setGenerator(GLHeaderGenerator(diagFile = diagFile))
glRegistry.apiGen(glHeaderOptions)

functionPointerOptions = GeneratorOptions(
	filename = os.path.join(args.outDir, 'AnyGLFunctions.c'),
	apiname = apiname,
	profile = args.profile,
	addExtensions = args.extensions)
write('Outputting', functionPointerOptions.filename + '...')
glRegistry.setGenerator(FunctionPointerGenerator(diagFile = diagFile))
glRegistry.apiGen(functionPointerOptions)

write('Parsing', glxXml + '...')
glxRegistry = Registry()
glxRegistry.loadElementTree(etree.parse(glxXml))

glxHeaderOptions = GeneratorOptions(
	filename = os.path.join(args.outDir, 'glx.h'),
	apiname = ['glx'],
	profile = args.profile,
	addExtensions = '.*',
	removeExtensions = 'GLX_ARB_get_proc_address')
write('Outputting', glxHeaderOptions.filename + '...')
glxRegistry.setGenerator(GLXWHeaderGenerator(['X11/Xlib.h', 'X11/Xutil.h'], 'ANYGL_LOAD_GLX',
	extensionsOnly = False, diagFile = diagFile))
glxRegistry.apiGen(glxHeaderOptions)

glxLoadOptions = GeneratorOptions(
	filename = os.path.join(args.outDir, 'AnyGLLoadGLX.c'),
	apiname = ['glx'],
	profile = args.profile,
	addExtensions = '.*',
	removeExtensions = '(GLX_ARB_get_proc_address)|(GLX_SGI.*)')
write('Outputting', glxLoadOptions.filename + '...')
glRegistry.apiReset()
glxRegistry.setGenerator(GLXLoadGenerator(diagFile = diagFile))
glxRegistry.apiGen(glxLoadOptions)

write('Parsing', wglXml + '...')
wglRegistry = Registry()
wglRegistry.loadElementTree(etree.parse(wglXml))

wglHeaderOptions = GeneratorOptions(
	filename = os.path.join(args.outDir, 'wgl.h'),
	apiname = ['wgl'],
	profile = args.profile,
	emitversions = None,
	addExtensions = '.*')
write('Outputting', wglHeaderOptions.filename + '...')
wglRegistry.setGenerator(GLXWHeaderGenerator(['Windows.h'], 'ANYGL_LOAD_WGL',
	systemDefines = ['WIN32_LEAN_AND_MEAN'], diagFile = diagFile))
wglRegistry.apiGen(wglHeaderOptions)

write('Done')
