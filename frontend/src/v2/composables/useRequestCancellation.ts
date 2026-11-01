import { ref, onUnmounted } from "vue";

const activeRequests = new Map<string, AbortController>();

export function useRequestCancellation() {
  const componentControllers = ref(new Set<AbortController>());
  function createRequestController(endpoint: string): AbortController {
    const existingController = activeRequests.get(endpoint);
    if (existingController) {
      console.log(
        `[RequestCancellation] Canceling duplicate request to: ${endpoint}`
      );
      existingController.abort("Duplicate request detected");
    }

    // Create new controller for this request
    const controller = new AbortController();

    // Track this endpoint
    activeRequests.set(endpoint, controller);

    // Track this controller for this component instance
    componentControllers.value.add(controller);

    // Clean up when request completes (success or error)
    const originalAbort = controller.abort.bind(controller);
    controller.abort = function (reason?: any) {
      activeRequests.delete(endpoint);
      componentControllers.value.delete(controller);
      originalAbort(reason);
    };

    return controller;
  }

  function isRequestCanceled(error: any): boolean {
    return (
      error?.name === "AbortError" ||
      error?.name === "CanceledError" ||
      error?.message?.includes("canceled") ||
      error?.message?.includes("aborted")
    );
  }

  function cleanupRequest(endpoint: string): void {
    const controller = activeRequests.get(endpoint);
    if (controller) {
      activeRequests.delete(endpoint);
      componentControllers.value.delete(controller);
    }
  }

  function getRequestSignal(endpoint: string): AbortSignal {
    const controller = createRequestController(endpoint);
    return controller.signal;
  }

  onUnmounted(() => {
    componentControllers.value.forEach((controller) => {
      if (!controller.signal.aborted) {
        controller.abort("Component unmounted");
      }
    });

    // Remove all tracked controllers for this component from active requests
    activeRequests.forEach((controller, endpoint) => {
      if (componentControllers.value.has(controller)) {
        activeRequests.delete(endpoint);
      }
    });

    // Clear component tracking
    componentControllers.value.clear();
  });

  return {
    createRequestController,
    isRequestCanceled,
    cleanupRequest,
    getRequestSignal,
    activeRequests: activeRequests, // For debugging purposes
  };
}
