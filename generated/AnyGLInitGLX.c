#include "AnyGLConfig.h"

#if ANYGL_HAS_GLX
#include <GL/glx.h>
#define ANYGL_NO_DEFINES
#include "glx.h"

/* Generated by AnyGL. */

ANYGL_EXPORT PFNANYGLXCHOOSEVISUALPROC AnyGL_glXChooseVisual;
ANYGL_EXPORT PFNANYGLXCREATECONTEXTPROC AnyGL_glXCreateContext;
ANYGL_EXPORT PFNANYGLXDESTROYCONTEXTPROC AnyGL_glXDestroyContext;
ANYGL_EXPORT PFNANYGLXMAKECURRENTPROC AnyGL_glXMakeCurrent;
ANYGL_EXPORT PFNANYGLXCOPYCONTEXTPROC AnyGL_glXCopyContext;
ANYGL_EXPORT PFNANYGLXSWAPBUFFERSPROC AnyGL_glXSwapBuffers;
ANYGL_EXPORT PFNANYGLXCREATEGLXPIXMAPPROC AnyGL_glXCreateGLXPixmap;
ANYGL_EXPORT PFNANYGLXDESTROYGLXPIXMAPPROC AnyGL_glXDestroyGLXPixmap;
ANYGL_EXPORT PFNANYGLXQUERYEXTENSIONPROC AnyGL_glXQueryExtension;
ANYGL_EXPORT PFNANYGLXQUERYVERSIONPROC AnyGL_glXQueryVersion;
ANYGL_EXPORT PFNANYGLXISDIRECTPROC AnyGL_glXIsDirect;
ANYGL_EXPORT PFNANYGLXGETCONFIGPROC AnyGL_glXGetConfig;
ANYGL_EXPORT PFNANYGLXGETCURRENTCONTEXTPROC AnyGL_glXGetCurrentContext;
ANYGL_EXPORT PFNANYGLXGETCURRENTDRAWABLEPROC AnyGL_glXGetCurrentDrawable;
ANYGL_EXPORT PFNANYGLXWAITGLPROC AnyGL_glXWaitGL;
ANYGL_EXPORT PFNANYGLXWAITXPROC AnyGL_glXWaitX;
ANYGL_EXPORT PFNANYGLXUSEXFONTPROC AnyGL_glXUseXFont;
ANYGL_EXPORT PFNANYGLXQUERYEXTENSIONSSTRINGPROC AnyGL_glXQueryExtensionsString;
ANYGL_EXPORT PFNANYGLXQUERYSERVERSTRINGPROC AnyGL_glXQueryServerString;
ANYGL_EXPORT PFNANYGLXGETCLIENTSTRINGPROC AnyGL_glXGetClientString;
ANYGL_EXPORT PFNANYGLXGETCURRENTDISPLAYPROC AnyGL_glXGetCurrentDisplay;
ANYGL_EXPORT PFNANYGLXGETFBCONFIGSPROC AnyGL_glXGetFBConfigs;
ANYGL_EXPORT PFNANYGLXCHOOSEFBCONFIGPROC AnyGL_glXChooseFBConfig;
ANYGL_EXPORT PFNANYGLXGETFBCONFIGATTRIBPROC AnyGL_glXGetFBConfigAttrib;
ANYGL_EXPORT PFNANYGLXGETVISUALFROMFBCONFIGPROC AnyGL_glXGetVisualFromFBConfig;
ANYGL_EXPORT PFNANYGLXCREATEWINDOWPROC AnyGL_glXCreateWindow;
ANYGL_EXPORT PFNANYGLXDESTROYWINDOWPROC AnyGL_glXDestroyWindow;
ANYGL_EXPORT PFNANYGLXCREATEPIXMAPPROC AnyGL_glXCreatePixmap;
ANYGL_EXPORT PFNANYGLXDESTROYPIXMAPPROC AnyGL_glXDestroyPixmap;
ANYGL_EXPORT PFNANYGLXCREATEPBUFFERPROC AnyGL_glXCreatePbuffer;
ANYGL_EXPORT PFNANYGLXDESTROYPBUFFERPROC AnyGL_glXDestroyPbuffer;
ANYGL_EXPORT PFNANYGLXQUERYDRAWABLEPROC AnyGL_glXQueryDrawable;
ANYGL_EXPORT PFNANYGLXCREATENEWCONTEXTPROC AnyGL_glXCreateNewContext;
ANYGL_EXPORT PFNANYGLXMAKECONTEXTCURRENTPROC AnyGL_glXMakeContextCurrent;
ANYGL_EXPORT PFNANYGLXGETCURRENTREADDRAWABLEPROC AnyGL_glXGetCurrentReadDrawable;
ANYGL_EXPORT PFNANYGLXQUERYCONTEXTPROC AnyGL_glXQueryContext;
ANYGL_EXPORT PFNANYGLXSELECTEVENTPROC AnyGL_glXSelectEvent;
ANYGL_EXPORT PFNANYGLXGETSELECTEDEVENTPROC AnyGL_glXGetSelectedEvent;
ANYGL_EXPORT PFNANYGLXGETPROCADDRESSPROC AnyGL_glXGetProcAddress;
ANYGL_EXPORT PFNANYGLXCREATECONTEXTATTRIBSARBPROC AnyGL_glXCreateContextAttribsARB;
ANYGL_EXPORT PFNANYGLXGETGPUIDSAMDPROC AnyGL_glXGetGPUIDsAMD;
ANYGL_EXPORT PFNANYGLXGETGPUINFOAMDPROC AnyGL_glXGetGPUInfoAMD;
ANYGL_EXPORT PFNANYGLXGETCONTEXTGPUIDAMDPROC AnyGL_glXGetContextGPUIDAMD;
ANYGL_EXPORT PFNANYGLXCREATEASSOCIATEDCONTEXTAMDPROC AnyGL_glXCreateAssociatedContextAMD;
ANYGL_EXPORT PFNANYGLXCREATEASSOCIATEDCONTEXTATTRIBSAMDPROC AnyGL_glXCreateAssociatedContextAttribsAMD;
ANYGL_EXPORT PFNANYGLXDELETEASSOCIATEDCONTEXTAMDPROC AnyGL_glXDeleteAssociatedContextAMD;
ANYGL_EXPORT PFNANYGLXMAKEASSOCIATEDCONTEXTCURRENTAMDPROC AnyGL_glXMakeAssociatedContextCurrentAMD;
ANYGL_EXPORT PFNANYGLXGETCURRENTASSOCIATEDCONTEXTAMDPROC AnyGL_glXGetCurrentAssociatedContextAMD;
ANYGL_EXPORT PFNANYGLXBLITCONTEXTFRAMEBUFFERAMDPROC AnyGL_glXBlitContextFramebufferAMD;
ANYGL_EXPORT PFNANYGLXGETCURRENTDISPLAYEXTPROC AnyGL_glXGetCurrentDisplayEXT;
ANYGL_EXPORT PFNANYGLXQUERYCONTEXTINFOEXTPROC AnyGL_glXQueryContextInfoEXT;
ANYGL_EXPORT PFNANYGLXGETCONTEXTIDEXTPROC AnyGL_glXGetContextIDEXT;
ANYGL_EXPORT PFNANYGLXIMPORTCONTEXTEXTPROC AnyGL_glXImportContextEXT;
ANYGL_EXPORT PFNANYGLXFREECONTEXTEXTPROC AnyGL_glXFreeContextEXT;
ANYGL_EXPORT PFNANYGLXSWAPINTERVALEXTPROC AnyGL_glXSwapIntervalEXT;
ANYGL_EXPORT PFNANYGLXBINDTEXIMAGEEXTPROC AnyGL_glXBindTexImageEXT;
ANYGL_EXPORT PFNANYGLXRELEASETEXIMAGEEXTPROC AnyGL_glXReleaseTexImageEXT;
ANYGL_EXPORT PFNANYGLXGETAGPOFFSETMESAPROC AnyGL_glXGetAGPOffsetMESA;
ANYGL_EXPORT PFNANYGLXCOPYSUBBUFFERMESAPROC AnyGL_glXCopySubBufferMESA;
ANYGL_EXPORT PFNANYGLXCREATEGLXPIXMAPMESAPROC AnyGL_glXCreateGLXPixmapMESA;
ANYGL_EXPORT PFNANYGLXQUERYCURRENTRENDERERINTEGERMESAPROC AnyGL_glXQueryCurrentRendererIntegerMESA;
ANYGL_EXPORT PFNANYGLXQUERYCURRENTRENDERERSTRINGMESAPROC AnyGL_glXQueryCurrentRendererStringMESA;
ANYGL_EXPORT PFNANYGLXQUERYRENDERERINTEGERMESAPROC AnyGL_glXQueryRendererIntegerMESA;
ANYGL_EXPORT PFNANYGLXQUERYRENDERERSTRINGMESAPROC AnyGL_glXQueryRendererStringMESA;
ANYGL_EXPORT PFNANYGLXRELEASEBUFFERSMESAPROC AnyGL_glXReleaseBuffersMESA;
ANYGL_EXPORT PFNANYGLXSET3DFXMODEMESAPROC AnyGL_glXSet3DfxModeMESA;
ANYGL_EXPORT PFNANYGLXGETSWAPINTERVALMESAPROC AnyGL_glXGetSwapIntervalMESA;
ANYGL_EXPORT PFNANYGLXSWAPINTERVALMESAPROC AnyGL_glXSwapIntervalMESA;
ANYGL_EXPORT PFNANYGLXCOPYBUFFERSUBDATANVPROC AnyGL_glXCopyBufferSubDataNV;
ANYGL_EXPORT PFNANYGLXNAMEDCOPYBUFFERSUBDATANVPROC AnyGL_glXNamedCopyBufferSubDataNV;
ANYGL_EXPORT PFNANYGLXCOPYIMAGESUBDATANVPROC AnyGL_glXCopyImageSubDataNV;
ANYGL_EXPORT PFNANYGLXDELAYBEFORESWAPNVPROC AnyGL_glXDelayBeforeSwapNV;
ANYGL_EXPORT PFNANYGLXENUMERATEVIDEODEVICESNVPROC AnyGL_glXEnumerateVideoDevicesNV;
ANYGL_EXPORT PFNANYGLXBINDVIDEODEVICENVPROC AnyGL_glXBindVideoDeviceNV;
ANYGL_EXPORT PFNANYGLXJOINSWAPGROUPNVPROC AnyGL_glXJoinSwapGroupNV;
ANYGL_EXPORT PFNANYGLXBINDSWAPBARRIERNVPROC AnyGL_glXBindSwapBarrierNV;
ANYGL_EXPORT PFNANYGLXQUERYSWAPGROUPNVPROC AnyGL_glXQuerySwapGroupNV;
ANYGL_EXPORT PFNANYGLXQUERYMAXSWAPGROUPSNVPROC AnyGL_glXQueryMaxSwapGroupsNV;
ANYGL_EXPORT PFNANYGLXQUERYFRAMECOUNTNVPROC AnyGL_glXQueryFrameCountNV;
ANYGL_EXPORT PFNANYGLXRESETFRAMECOUNTNVPROC AnyGL_glXResetFrameCountNV;
ANYGL_EXPORT PFNANYGLXBINDVIDEOCAPTUREDEVICENVPROC AnyGL_glXBindVideoCaptureDeviceNV;
ANYGL_EXPORT PFNANYGLXENUMERATEVIDEOCAPTUREDEVICESNVPROC AnyGL_glXEnumerateVideoCaptureDevicesNV;
ANYGL_EXPORT PFNANYGLXLOCKVIDEOCAPTUREDEVICENVPROC AnyGL_glXLockVideoCaptureDeviceNV;
ANYGL_EXPORT PFNANYGLXQUERYVIDEOCAPTUREDEVICENVPROC AnyGL_glXQueryVideoCaptureDeviceNV;
ANYGL_EXPORT PFNANYGLXRELEASEVIDEOCAPTUREDEVICENVPROC AnyGL_glXReleaseVideoCaptureDeviceNV;
ANYGL_EXPORT PFNANYGLXGETVIDEODEVICENVPROC AnyGL_glXGetVideoDeviceNV;
ANYGL_EXPORT PFNANYGLXRELEASEVIDEODEVICENVPROC AnyGL_glXReleaseVideoDeviceNV;
ANYGL_EXPORT PFNANYGLXBINDVIDEOIMAGENVPROC AnyGL_glXBindVideoImageNV;
ANYGL_EXPORT PFNANYGLXRELEASEVIDEOIMAGENVPROC AnyGL_glXReleaseVideoImageNV;
ANYGL_EXPORT PFNANYGLXSENDPBUFFERTOVIDEONVPROC AnyGL_glXSendPbufferToVideoNV;
ANYGL_EXPORT PFNANYGLXGETVIDEOINFONVPROC AnyGL_glXGetVideoInfoNV;
ANYGL_EXPORT PFNANYGLXGETSYNCVALUESOMLPROC AnyGL_glXGetSyncValuesOML;
ANYGL_EXPORT PFNANYGLXGETMSCRATEOMLPROC AnyGL_glXGetMscRateOML;
ANYGL_EXPORT PFNANYGLXSWAPBUFFERSMSCOMLPROC AnyGL_glXSwapBuffersMscOML;
ANYGL_EXPORT PFNANYGLXWAITFORMSCOMLPROC AnyGL_glXWaitForMscOML;
ANYGL_EXPORT PFNANYGLXWAITFORSBCOMLPROC AnyGL_glXWaitForSbcOML;
ANYGL_EXPORT PFNANYGLXGETTRANSPARENTINDEXSUNPROC AnyGL_glXGetTransparentIndexSUN;

int AnyGL_GLX_initialize(void)
{
	static int initialized;
	if (initialized)
		return 1;

#ifndef ANYGLX_VERSION_1_0
	AnyGL_glXChooseVisual = &glXChooseVisual;
	AnyGL_glXCreateContext = &glXCreateContext;
	AnyGL_glXDestroyContext = &glXDestroyContext;
	AnyGL_glXMakeCurrent = &glXMakeCurrent;
	AnyGL_glXCopyContext = &glXCopyContext;
	AnyGL_glXSwapBuffers = &glXSwapBuffers;
	AnyGL_glXCreateGLXPixmap = &glXCreateGLXPixmap;
	AnyGL_glXDestroyGLXPixmap = &glXDestroyGLXPixmap;
	AnyGL_glXQueryExtension = &glXQueryExtension;
	AnyGL_glXQueryVersion = &glXQueryVersion;
	AnyGL_glXIsDirect = &glXIsDirect;
	AnyGL_glXGetConfig = &glXGetConfig;
	AnyGL_glXGetCurrentContext = &glXGetCurrentContext;
	AnyGL_glXGetCurrentDrawable = &glXGetCurrentDrawable;
	AnyGL_glXWaitGL = &glXWaitGL;
	AnyGL_glXWaitX = &glXWaitX;
	AnyGL_glXUseXFont = &glXUseXFont;
#endif /* GLX_VERSION_1_0 */

#ifndef ANYGLX_VERSION_1_1
	AnyGL_glXQueryExtensionsString = &glXQueryExtensionsString;
	AnyGL_glXQueryServerString = &glXQueryServerString;
	AnyGL_glXGetClientString = &glXGetClientString;
#endif /* GLX_VERSION_1_1 */

#ifndef ANYGLX_VERSION_1_2
	AnyGL_glXGetCurrentDisplay = &glXGetCurrentDisplay;
#endif /* GLX_VERSION_1_2 */

#ifndef ANYGLX_VERSION_1_3
	AnyGL_glXGetFBConfigs = &glXGetFBConfigs;
	AnyGL_glXChooseFBConfig = &glXChooseFBConfig;
	AnyGL_glXGetFBConfigAttrib = &glXGetFBConfigAttrib;
	AnyGL_glXGetVisualFromFBConfig = &glXGetVisualFromFBConfig;
	AnyGL_glXCreateWindow = &glXCreateWindow;
	AnyGL_glXDestroyWindow = &glXDestroyWindow;
	AnyGL_glXCreatePixmap = &glXCreatePixmap;
	AnyGL_glXDestroyPixmap = &glXDestroyPixmap;
	AnyGL_glXCreatePbuffer = &glXCreatePbuffer;
	AnyGL_glXDestroyPbuffer = &glXDestroyPbuffer;
	AnyGL_glXQueryDrawable = &glXQueryDrawable;
	AnyGL_glXCreateNewContext = &glXCreateNewContext;
	AnyGL_glXMakeContextCurrent = &glXMakeContextCurrent;
	AnyGL_glXGetCurrentReadDrawable = &glXGetCurrentReadDrawable;
	AnyGL_glXQueryContext = &glXQueryContext;
	AnyGL_glXSelectEvent = &glXSelectEvent;
	AnyGL_glXGetSelectedEvent = &glXGetSelectedEvent;
#endif /* GLX_VERSION_1_3 */

#ifndef ANYGLX_VERSION_1_4
	AnyGL_glXGetProcAddress = &glXGetProcAddress;
#endif /* GLX_VERSION_1_4 */

#ifndef ANYGLX_ARB_get_proc_address
	if (!AnyGL_glXGetProcAddress)
		AnyGL_glXGetProcAddress = &glXGetProcAddressARB;
#endif /* GLX_ARB_get_proc_address */

	if (!AnyGL_glXGetProcAddress)
		return 0;

	/* GLX_ARB_context_flush_control */

	/* GLX_ARB_create_context */
	AnyGL_glXCreateContextAttribsARB = (PFNANYGLXCREATECONTEXTATTRIBSARBPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXCreateContextAttribsARB");

	/* GLX_ARB_create_context_no_error */

	/* GLX_ARB_create_context_profile */

	/* GLX_ARB_create_context_robustness */

	/* GLX_ARB_fbconfig_float */

	/* GLX_ARB_framebuffer_sRGB */

	/* GLX_ARB_multisample */

	/* GLX_ARB_robustness_application_isolation */

	/* GLX_ARB_robustness_share_group_isolation */

	/* GLX_ARB_vertex_buffer_object */

	/* GLX_3DFX_multisample */

	/* GLX_AMD_gpu_association */
	AnyGL_glXGetGPUIDsAMD = (PFNANYGLXGETGPUIDSAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetGPUIDsAMD");
	AnyGL_glXGetGPUInfoAMD = (PFNANYGLXGETGPUINFOAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetGPUInfoAMD");
	AnyGL_glXGetContextGPUIDAMD = (PFNANYGLXGETCONTEXTGPUIDAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetContextGPUIDAMD");
	AnyGL_glXCreateAssociatedContextAMD = (PFNANYGLXCREATEASSOCIATEDCONTEXTAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXCreateAssociatedContextAMD");
	AnyGL_glXCreateAssociatedContextAttribsAMD = (PFNANYGLXCREATEASSOCIATEDCONTEXTATTRIBSAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXCreateAssociatedContextAttribsAMD");
	AnyGL_glXDeleteAssociatedContextAMD = (PFNANYGLXDELETEASSOCIATEDCONTEXTAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXDeleteAssociatedContextAMD");
	AnyGL_glXMakeAssociatedContextCurrentAMD = (PFNANYGLXMAKEASSOCIATEDCONTEXTCURRENTAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXMakeAssociatedContextCurrentAMD");
	AnyGL_glXGetCurrentAssociatedContextAMD = (PFNANYGLXGETCURRENTASSOCIATEDCONTEXTAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetCurrentAssociatedContextAMD");
	AnyGL_glXBlitContextFramebufferAMD = (PFNANYGLXBLITCONTEXTFRAMEBUFFERAMDPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXBlitContextFramebufferAMD");

	/* GLX_EXT_buffer_age */

	/* GLX_EXT_context_priority */

	/* GLX_EXT_create_context_es2_profile */

	/* GLX_EXT_create_context_es_profile */

	/* GLX_EXT_fbconfig_packed_float */

	/* GLX_EXT_framebuffer_sRGB */

	/* GLX_EXT_get_drawable_type */

	/* GLX_EXT_import_context */
	AnyGL_glXGetCurrentDisplayEXT = (PFNANYGLXGETCURRENTDISPLAYEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetCurrentDisplayEXT");
	AnyGL_glXQueryContextInfoEXT = (PFNANYGLXQUERYCONTEXTINFOEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryContextInfoEXT");
	AnyGL_glXGetContextIDEXT = (PFNANYGLXGETCONTEXTIDEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetContextIDEXT");
	AnyGL_glXImportContextEXT = (PFNANYGLXIMPORTCONTEXTEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXImportContextEXT");
	AnyGL_glXFreeContextEXT = (PFNANYGLXFREECONTEXTEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXFreeContextEXT");

	/* GLX_EXT_libglvnd */

	/* GLX_EXT_no_config_context */

	/* GLX_EXT_stereo_tree */

	/* GLX_EXT_swap_control */
	AnyGL_glXSwapIntervalEXT = (PFNANYGLXSWAPINTERVALEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXSwapIntervalEXT");

	/* GLX_EXT_swap_control_tear */

	/* GLX_EXT_texture_from_pixmap */
	AnyGL_glXBindTexImageEXT = (PFNANYGLXBINDTEXIMAGEEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXBindTexImageEXT");
	AnyGL_glXReleaseTexImageEXT = (PFNANYGLXRELEASETEXIMAGEEXTPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXReleaseTexImageEXT");

	/* GLX_EXT_visual_info */

	/* GLX_EXT_visual_rating */

	/* GLX_INTEL_swap_event */

	/* GLX_MESA_agp_offset */
	AnyGL_glXGetAGPOffsetMESA = (PFNANYGLXGETAGPOFFSETMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetAGPOffsetMESA");

	/* GLX_MESA_copy_sub_buffer */
	AnyGL_glXCopySubBufferMESA = (PFNANYGLXCOPYSUBBUFFERMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXCopySubBufferMESA");

	/* GLX_MESA_pixmap_colormap */
	AnyGL_glXCreateGLXPixmapMESA = (PFNANYGLXCREATEGLXPIXMAPMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXCreateGLXPixmapMESA");

	/* GLX_MESA_query_renderer */
	AnyGL_glXQueryCurrentRendererIntegerMESA = (PFNANYGLXQUERYCURRENTRENDERERINTEGERMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryCurrentRendererIntegerMESA");
	AnyGL_glXQueryCurrentRendererStringMESA = (PFNANYGLXQUERYCURRENTRENDERERSTRINGMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryCurrentRendererStringMESA");
	AnyGL_glXQueryRendererIntegerMESA = (PFNANYGLXQUERYRENDERERINTEGERMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryRendererIntegerMESA");
	AnyGL_glXQueryRendererStringMESA = (PFNANYGLXQUERYRENDERERSTRINGMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryRendererStringMESA");

	/* GLX_MESA_release_buffers */
	AnyGL_glXReleaseBuffersMESA = (PFNANYGLXRELEASEBUFFERSMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXReleaseBuffersMESA");

	/* GLX_MESA_set_3dfx_mode */
	AnyGL_glXSet3DfxModeMESA = (PFNANYGLXSET3DFXMODEMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXSet3DfxModeMESA");

	/* GLX_MESA_swap_control */
	AnyGL_glXGetSwapIntervalMESA = (PFNANYGLXGETSWAPINTERVALMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetSwapIntervalMESA");
	AnyGL_glXSwapIntervalMESA = (PFNANYGLXSWAPINTERVALMESAPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXSwapIntervalMESA");

	/* GLX_NV_copy_buffer */
	AnyGL_glXCopyBufferSubDataNV = (PFNANYGLXCOPYBUFFERSUBDATANVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXCopyBufferSubDataNV");
	AnyGL_glXNamedCopyBufferSubDataNV = (PFNANYGLXNAMEDCOPYBUFFERSUBDATANVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXNamedCopyBufferSubDataNV");

	/* GLX_NV_copy_image */
	AnyGL_glXCopyImageSubDataNV = (PFNANYGLXCOPYIMAGESUBDATANVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXCopyImageSubDataNV");

	/* GLX_NV_delay_before_swap */
	AnyGL_glXDelayBeforeSwapNV = (PFNANYGLXDELAYBEFORESWAPNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXDelayBeforeSwapNV");

	/* GLX_NV_float_buffer */

	/* GLX_NV_multigpu_context */

	/* GLX_NV_multisample_coverage */

	/* GLX_NV_present_video */
	AnyGL_glXEnumerateVideoDevicesNV = (PFNANYGLXENUMERATEVIDEODEVICESNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXEnumerateVideoDevicesNV");
	AnyGL_glXBindVideoDeviceNV = (PFNANYGLXBINDVIDEODEVICENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXBindVideoDeviceNV");

	/* GLX_NV_robustness_video_memory_purge */

	/* GLX_NV_swap_group */
	AnyGL_glXJoinSwapGroupNV = (PFNANYGLXJOINSWAPGROUPNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXJoinSwapGroupNV");
	AnyGL_glXBindSwapBarrierNV = (PFNANYGLXBINDSWAPBARRIERNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXBindSwapBarrierNV");
	AnyGL_glXQuerySwapGroupNV = (PFNANYGLXQUERYSWAPGROUPNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQuerySwapGroupNV");
	AnyGL_glXQueryMaxSwapGroupsNV = (PFNANYGLXQUERYMAXSWAPGROUPSNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryMaxSwapGroupsNV");
	AnyGL_glXQueryFrameCountNV = (PFNANYGLXQUERYFRAMECOUNTNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryFrameCountNV");
	AnyGL_glXResetFrameCountNV = (PFNANYGLXRESETFRAMECOUNTNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXResetFrameCountNV");

	/* GLX_NV_video_capture */
	AnyGL_glXBindVideoCaptureDeviceNV = (PFNANYGLXBINDVIDEOCAPTUREDEVICENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXBindVideoCaptureDeviceNV");
	AnyGL_glXEnumerateVideoCaptureDevicesNV = (PFNANYGLXENUMERATEVIDEOCAPTUREDEVICESNVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXEnumerateVideoCaptureDevicesNV");
	AnyGL_glXLockVideoCaptureDeviceNV = (PFNANYGLXLOCKVIDEOCAPTUREDEVICENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXLockVideoCaptureDeviceNV");
	AnyGL_glXQueryVideoCaptureDeviceNV = (PFNANYGLXQUERYVIDEOCAPTUREDEVICENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXQueryVideoCaptureDeviceNV");
	AnyGL_glXReleaseVideoCaptureDeviceNV = (PFNANYGLXRELEASEVIDEOCAPTUREDEVICENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXReleaseVideoCaptureDeviceNV");

	/* GLX_NV_video_out */
	AnyGL_glXGetVideoDeviceNV = (PFNANYGLXGETVIDEODEVICENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetVideoDeviceNV");
	AnyGL_glXReleaseVideoDeviceNV = (PFNANYGLXRELEASEVIDEODEVICENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXReleaseVideoDeviceNV");
	AnyGL_glXBindVideoImageNV = (PFNANYGLXBINDVIDEOIMAGENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXBindVideoImageNV");
	AnyGL_glXReleaseVideoImageNV = (PFNANYGLXRELEASEVIDEOIMAGENVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXReleaseVideoImageNV");
	AnyGL_glXSendPbufferToVideoNV = (PFNANYGLXSENDPBUFFERTOVIDEONVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXSendPbufferToVideoNV");
	AnyGL_glXGetVideoInfoNV = (PFNANYGLXGETVIDEOINFONVPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetVideoInfoNV");

	/* GLX_OML_swap_method */

	/* GLX_OML_sync_control */
	AnyGL_glXGetSyncValuesOML = (PFNANYGLXGETSYNCVALUESOMLPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetSyncValuesOML");
	AnyGL_glXGetMscRateOML = (PFNANYGLXGETMSCRATEOMLPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetMscRateOML");
	AnyGL_glXSwapBuffersMscOML = (PFNANYGLXSWAPBUFFERSMSCOMLPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXSwapBuffersMscOML");
	AnyGL_glXWaitForMscOML = (PFNANYGLXWAITFORMSCOMLPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXWaitForMscOML");
	AnyGL_glXWaitForSbcOML = (PFNANYGLXWAITFORSBCOMLPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXWaitForSbcOML");

	/* GLX_SUN_get_transparent_index */
	AnyGL_glXGetTransparentIndexSUN = (PFNANYGLXGETTRANSPARENTINDEXSUNPROC)AnyGL_glXGetProcAddress((const GLubyte*)"glXGetTransparentIndexSUN");

	initialized = 1;
	return 1;
}

void AnyGL_GLX_shutdown(void) {}

#endif /* ANYGL_LOAD */
