import { onMounted, onUnmounted } from "vue";

export function useEventListener(
  target: Window | HTMLElement,
  event: string,
  fn?: any,
  options?: boolean | AddEventListenerOptions | undefined
) {
  // Register using addEventListener on mounted, and removeEventListener on unmounted.
  onMounted(() => target.addEventListener(event, fn, options));
  onUnmounted(() => target.removeEventListener(event, fn, options));
}
