import { ref, Ref } from "vue";

export interface UseProgressAnimationReturn {
  loadingProgress: Ref<number>;
  targetProgress: Ref<number>;
  animateProgressTo: (target: number) => void;
  resetProgress: () => void;
  stopAnimation: () => void;
}

export function useProgressAnimation(): UseProgressAnimationReturn {
  const loadingProgress = ref(0);
  const targetProgress = ref(0);
  let smoothProgressInterval: any = null;

  const animateProgressTo = (target: number) => {
    targetProgress.value = target;

    if (smoothProgressInterval) {
      clearInterval(smoothProgressInterval);
    }

    smoothProgressInterval = setInterval(() => {
      const current = loadingProgress.value;
      const difference = targetProgress.value - current;

      if (Math.abs(difference) < 0.5) {
        loadingProgress.value = targetProgress.value;
        if (smoothProgressInterval) {
          clearInterval(smoothProgressInterval);
          smoothProgressInterval = null;
        }
      } else {
        const increment = difference * 0.2;
        loadingProgress.value = current + increment;
      }
    }, 16); // 60fps
  };

  const resetProgress = () => {
    if (smoothProgressInterval) {
      clearInterval(smoothProgressInterval);
      smoothProgressInterval = null;
    }
    loadingProgress.value = 0;
    targetProgress.value = 0;
  };

  const stopAnimation = () => {
    if (smoothProgressInterval) {
      clearInterval(smoothProgressInterval);
      smoothProgressInterval = null;
    }
  };

  return {
    loadingProgress,
    targetProgress,
    animateProgressTo,
    resetProgress,
    stopAnimation,
  };
}
