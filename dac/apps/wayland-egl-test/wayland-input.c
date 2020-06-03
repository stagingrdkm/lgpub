//    GL: gcc -o wayland-input wayland-input.c $(pkg-config --cflags --libs wayland-client wayland-egl glesv2 egl xkbcommon)
// epoxy: gcc -DHAVE_EPOXY -o wayland-input wayland-input.c $(pkg-config --cflags --libs epoxy wayland-client wayland-egl xkbcommon)


#ifdef HAVE_EPOXY
#  include <epoxy/egl.h>
#else
#  include <EGL/egl.h>
#  include <GLES2/gl2.h>
#endif
#include <assert.h>
#include <wayland-client.h>
#include <wayland-egl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <xkbcommon/xkbcommon.h>
#include <string.h>
#include <stdio.h>
#include <poll.h>
#include <errno.h>

#define WIDTH 256
#define HEIGHT 256

static struct wl_display *display;
static int fd;
static struct wl_compositor *compositor = NULL;
static struct wl_shell *shell = NULL;
static struct wl_seat *seat = NULL;
static EGLDisplay egl_display;
static struct xkb_context *xkb_context;
static struct xkb_keymap *keymap = NULL;
static struct xkb_state *xkb_state = NULL;
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
static void pointer_enter (void *data, struct wl_pointer *pointer, uint32_t serial, struct wl_surface *surface, wl_fixed_t surface_x, wl_fixed_t surface_y) {
	printf ("pointer enter\n");
}
static void pointer_leave (void *data, struct wl_pointer *pointer, uint32_t serial, struct wl_surface *surface) {
	printf ("pointer leave\n");
}
static void pointer_motion (void *data, struct wl_pointer *pointer, uint32_t time, wl_fixed_t x, wl_fixed_t y) {
	printf ("pointer motion %f %f\n", wl_fixed_to_double(x), wl_fixed_to_double(y));
}
static void pointer_button (void *data, struct wl_pointer *pointer, uint32_t serial, uint32_t time, uint32_t button, uint32_t state) {
	printf ("pointer button (button %d, state %d)\n", button, state);
}
static void pointer_axis (void *data, struct wl_pointer *pointer, uint32_t time, uint32_t axis, wl_fixed_t value) {
	printf ("pointer axis\n");
}
static struct wl_pointer_listener pointer_listener = {&pointer_enter, &pointer_leave, &pointer_motion, &pointer_button, &pointer_axis};

static void keyboard_keymap (void *data, struct wl_keyboard *keyboard, uint32_t format, int32_t fd, uint32_t size) {
	char *keymap_string = mmap (NULL, size, PROT_READ, MAP_SHARED, fd, 0);
	xkb_keymap_unref (keymap);
	keymap = xkb_keymap_new_from_string (xkb_context, keymap_string, XKB_KEYMAP_FORMAT_TEXT_V1, XKB_KEYMAP_COMPILE_NO_FLAGS);
	munmap (keymap_string, size);
	close (fd);
	xkb_state_unref (xkb_state);
	xkb_state = xkb_state_new (keymap);
}
static void keyboard_enter (void *data, struct wl_keyboard *keyboard, uint32_t serial, struct wl_surface *surface, struct wl_array *keys) {
	printf ("keyboard enter\n");
}
static void keyboard_leave (void *data, struct wl_keyboard *keyboard, uint32_t serial, struct wl_surface *surface) {
	printf ("keyboard leave\n");
}
static void keyboard_key (void *data, struct wl_keyboard *keyboard, uint32_t serial, uint32_t time, uint32_t key, uint32_t state) {
	if (state == WL_KEYBOARD_KEY_STATE_PRESSED) {
		xkb_keysym_t keysym = xkb_state_key_get_one_sym (xkb_state, key+8);
		uint32_t utf32 = xkb_keysym_to_utf32 (keysym);
		if (utf32) {
			if (utf32 >= 0x21 && utf32 <= 0x7E) {
				printf ("the key %c was pressed\n", (char)utf32);
				if (utf32 == 'q') running = 0;
			}
			else {
				printf ("the key U+%04X was pressed\n", utf32);
				if (utf32 == 8) running = 0;
			}
		}
		else {
			char name[64];
			xkb_keysym_get_name (keysym, name, 64);
			printf ("the key %s was pressed\n", name);
		}
	}
}
static void keyboard_modifiers (void *data, struct wl_keyboard *keyboard, uint32_t serial, uint32_t mods_depressed, uint32_t mods_latched, uint32_t mods_locked, uint32_t group) {
	xkb_state_update_mask (xkb_state, mods_depressed, mods_latched, mods_locked, 0, 0, group);
}
static struct wl_keyboard_listener keyboard_listener = {&keyboard_keymap, &keyboard_enter, &keyboard_leave, &keyboard_key, &keyboard_modifiers};

static void seat_capabilities (void *data, struct wl_seat *seat, uint32_t capabilities) {
	printf("seat_capabilities(data:%p, seat:%p, capabilities:0x%x)\n", data, seat, capabilities);

	if (capabilities & WL_SEAT_CAPABILITY_POINTER) {
		printf("seat_capabilities - pointer\n");
		struct wl_pointer *pointer = wl_seat_get_pointer (seat);
		wl_pointer_add_listener (pointer, &pointer_listener, NULL);
	}
	if (capabilities & WL_SEAT_CAPABILITY_KEYBOARD) {
		printf("seat_capabilities - keyboard\n");
		struct wl_keyboard *keyboard = wl_seat_get_keyboard (seat);
		wl_keyboard_add_listener (keyboard, &keyboard_listener, NULL);
	}
	if (capabilities & WL_SEAT_CAPABILITY_TOUCH) {
		printf("seat_capabilities - touch\n");
	}
}
static struct wl_seat_listener seat_listener = {&seat_capabilities};

static void registry_add_object (void *data, struct wl_registry *registry, uint32_t name, const char *interface, uint32_t version) {
	printf("registry_add_object(data:%p, registry:%p, name:%2u, interface:%s, version:%u)\n", data, registry, name, interface, version);

	if (!strcmp(interface,"wl_compositor")) {
		compositor = wl_registry_bind (registry, name, &wl_compositor_interface, 1);
	}
	else if (!strcmp(interface,"wl_shell")) {
		shell = wl_registry_bind (registry, name, &wl_shell_interface, 1);
	}
	else if (!strcmp(interface,"wl_seat")) {
		seat = wl_registry_bind (registry, name, &wl_seat_interface, 1);
		wl_seat_add_listener (seat, &seat_listener, NULL);
	}
}
static void registry_remove_object (void *data, struct wl_registry *registry, uint32_t name) {
	printf("registry_remove_object(data:%p, registry:%p, name:%2u)\n", data, registry, name);
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
}

int main () {
	xkb_context = xkb_context_new (XKB_CONTEXT_NO_FLAGS);
	assert(xkb_context != NULL);

	display = wl_display_connect (NULL);
	assert(display != NULL);
	fd = wl_display_get_fd(display);
	assert(fd != -1);

	struct wl_registry *registry = wl_display_get_registry (display);
	assert(registry != NULL);

	wl_registry_add_listener (registry, &registry_listener, NULL);
	wl_display_roundtrip (display);
	
	egl_display = eglGetDisplay (display);

	{
	    EGLint major;
	    EGLint minor;
	    EGLBoolean rv = eglInitialize (egl_display, &major, &minor);
	    assert(rv != EGL_FALSE);
	    printf("%d = eglInitialize(%p, %d, %d)\n", rv, egl_display, major, minor);
	}
	
	struct window window;
	create_window (&window, WIDTH, HEIGHT);
	
	while (running) {
	    int rv;
#ifndef SKIP_READING_EVENTS
	    while (wl_display_prepare_read(display) < 0) {
		wl_display_dispatch_pending(display);
	    }

	    wl_display_flush(display);

	    do {
	        struct pollfd fds = {
	    	    .fd = fd,
		    .events = POLLIN
	        };

		rv = poll(&fds, 1, 1);
	    } while(rv == -1 && rv == EINTR);

	    if (rv <= 0) {
		wl_display_cancel_read(display);
	    } else {
		wl_display_read_events(display);
	    }
#endif
	    wl_display_dispatch_pending (display);
	    draw_window (&window);
	}
	
	delete_window (&window);
	eglTerminate (egl_display);
	wl_display_disconnect (display);
	return 0;
}
