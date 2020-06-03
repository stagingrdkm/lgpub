//    GL: gcc -o wayland-egl wayland-egl.c $(pkg-config --cflags --libs wayland-client wayland-egl glesv2 egl)
// epoxy: gcc -DHAVE_EPOXY -o wayland-egl wayland-egl.c $(pkg-config --cflags --libs epoxy wayland-client wayland-egl)

#ifdef HAVE_EPOXY
#  include <epoxy/egl.h>
#else
#  include <EGL/egl.h>
#  include <GLES2/gl2.h>
#endif

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <wayland-client.h>
#include <wayland-egl.h>

static EGLint swap_interval = 1;
static int32_t width = 1920;
static int32_t height = 1080;

static struct wl_display *display;
static struct wl_compositor *compositor = NULL;
static struct wl_shell *shell = NULL;
static EGLDisplay egl_display;
static char running = 1;

struct window {
	EGLContext egl_context;
	struct wl_surface *surface;
	struct wl_shell_surface *shell_surface;
	struct wl_egl_window *egl_window;
	EGLSurface egl_surface;
	int color;
};

// listeners
static void registry_add_object (void *data, struct wl_registry *registry, uint32_t name, const char *interface, uint32_t version) {
	if (!strcmp(interface,"wl_compositor")) {
		compositor = wl_registry_bind (registry, name, &wl_compositor_interface, 1);
	}
	else if (!strcmp(interface,"wl_shell")) {
		shell = wl_registry_bind (registry, name, &wl_shell_interface, 1);
	}
}
static void registry_remove_object (void *data, struct wl_registry *registry, uint32_t name) {

}
static struct wl_registry_listener registry_listener = {&registry_add_object, &registry_remove_object};

static void shell_surface_ping (void *data, struct wl_shell_surface *shell_surface, uint32_t serial) {
	wl_shell_surface_pong (shell_surface, serial);
}
static void shell_surface_configure (void *data, struct wl_shell_surface *shell_surface, uint32_t edges, int32_t width, int32_t height) {
	struct window *window = data;
	wl_egl_window_resize (window->egl_window, width, height, 0, 0);
}
static void shell_surface_popup_done (void *data, struct wl_shell_surface *shell_surface) {

}
static struct wl_shell_surface_listener shell_surface_listener = {&shell_surface_ping, &shell_surface_configure, &shell_surface_popup_done};

static void show_fps() {
	struct timeval curTime;
	time_t nowMs;
	static time_t lastPrintTime = 0;
	static time_t lastPrintFrame = 0;
	static unsigned long frame = 0;

	gettimeofday(&curTime, NULL);
	nowMs =  curTime.tv_usec / 1000;
	nowMs += curTime.tv_sec  * 1000;

	frame++;

	if (nowMs - lastPrintTime >= 5000 || lastPrintFrame == 0) {
		if (nowMs - lastPrintTime != 0 && lastPrintTime != 0) {
			const float fps = (float) (frame - lastPrintFrame) / ((nowMs - lastPrintTime) / 1000.0f);
			printf("FPS: %.2f\n", fps);
		}

		lastPrintFrame = frame;
		lastPrintTime  = nowMs;
	}
}

static void create_window (struct window *window, int32_t width, int32_t height) {
	eglBindAPI (EGL_OPENGL_ES_API);
	EGLint attributes[] = {
		EGL_RED_SIZE, 8,
		EGL_GREEN_SIZE, 8,
		EGL_BLUE_SIZE, 8,
	EGL_NONE};
	EGLConfig config;
	EGLint num_config;
	EGLint contextAttributes[] = { EGL_CONTEXT_MAJOR_VERSION, 2, EGL_NONE };
	eglChooseConfig (egl_display, attributes, &config, 1, &num_config);
	window->egl_context = eglCreateContext (egl_display, config, EGL_NO_CONTEXT, contextAttributes);
	
	window->surface = wl_compositor_create_surface (compositor);
	window->shell_surface = wl_shell_get_shell_surface (shell, window->surface);
	wl_shell_surface_add_listener (window->shell_surface, &shell_surface_listener, window);
	wl_shell_surface_set_toplevel (window->shell_surface);
	window->egl_window = wl_egl_window_create (window->surface, width, height);
	window->egl_surface = eglCreateWindowSurface (egl_display, config, window->egl_window, NULL);
	eglMakeCurrent (egl_display, window->egl_surface, window->egl_surface, window->egl_context);
	window->color = 0;
}
static void delete_window (struct window *window) {
	eglDestroySurface (egl_display, window->egl_surface);
	wl_egl_window_destroy (window->egl_window);
	wl_shell_surface_destroy (window->shell_surface);
	wl_surface_destroy (window->surface);
	eglDestroyContext (egl_display, window->egl_context);
}
static void draw_window (struct window *window) {
	window->color = (window->color + 1) % 256;
	float c = window->color / 255.0;
	glClearColor (0.0, c, 0.0, 1.0);
	glClear (GL_COLOR_BUFFER_BIT);
	eglSwapBuffers (egl_display, window->egl_surface);

	show_fps();
}

void load_env() {
	const char *swap_str = getenv("SWAP_INTERVAL");
	const char *width_str = getenv("WIDTH");
	const char *height_str = getenv("HEIGHT");

	if (swap_str) {
		swap_interval = atoi(swap_str);
	}

	if (width_str) {
		width = atoi(width_str);
	}

	if (height_str) {
		height = atoi(height_str);
	}
}

int main () {
	load_env();

	display = wl_display_connect (NULL);
	struct wl_registry *registry = wl_display_get_registry (display);
	wl_registry_add_listener (registry, &registry_listener, NULL);
	wl_display_roundtrip (display);
	
	egl_display = eglGetDisplay (display);
	eglInitialize (egl_display, NULL, NULL);
	
	struct window window;
	create_window (&window, width, height);
	printf("width: %u\nheight: %u\n", width, height);

	EGLBoolean rv = eglSwapInterval(egl_display, swap_interval);
	printf("%s = eglSwapInterval(%p, %d)\n", rv == EGL_TRUE ? "EGL_TRUE" : "EGL_FALSE", egl_display, swap_interval);

	while (running) {
		wl_display_dispatch_pending (display);
		wl_display_roundtrip (display);
		draw_window (&window);
	}
	
	delete_window (&window);
	eglTerminate (egl_display);
	wl_display_disconnect (display);
	return 0;
}
