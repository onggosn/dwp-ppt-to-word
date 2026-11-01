<template>
  <div
    class="home-banner mx-5 my-3"
    @mouseenter="stopAutoSlide"
    @mouseleave="startAutoSlide"
  >
    <!-- Slides container -->
    <div class="slides-container">
      <div
        v-for="(banner, index) in bannerImages"
        :key="index"
        class="slide"
        :class="{ active: index === currentSlide }"
        :style="{ backgroundImage: `url(${banner.image})` }"
      >
        <!-- Banner content -->
        <div
          class="banner-content"
          :class="{ 'no-icon-content': !banner.iconImage }"
        >
          <div class="content-wrapper">
            <div v-if="banner.iconImage" class="banner-icon">
              <img
                :src="banner.iconImage"
                :alt="`Banner ${index + 1} icon`"
                class="banner-image anim-icon"
              />
            </div>
            <div class="text-content" :class="{ 'no-icon': !banner.iconImage }">
              <p v-if="banner.title" class="text-banner anim-title">
                {{ banner.title }}
              </p>
              <div
                style="z-index: 5; position: relative"
                :class="banner.title == null ? '' : 'mt-2'"
              >
                <p
                  class="text-sub-banner anim-subtitle"
                  style="display: inline; z-index: 5; position: relative"
                  :style="{ fontSize: banner.subtitleSize || '16px' }"
                  v-html="banner.subtitle"
                  @click="handleSubtitleClick"
                ></p>

                <p
                  v-if="!banner.title"
                  class="text-sub-banner clickable-history anim-subtitle"
                  style="display: inline"
                  :style="{
                    fontSize: banner.subtitleSize || '16px',
                    fontWeight: '900',
                  }"
                  @click="goToHistoryPage"
                >
                  <u>History Page</u>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation arrows -->
    <div class="carousel-nav">
      <button class="nav-arrow nav-arrow-left" @click="prevSlide">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M15 18L9 12L15 6"
            stroke="white"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
      <button class="nav-arrow nav-arrow-right" @click="nextSlide">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M9 18L15 12L9 6"
            stroke="white"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </button>
    </div>

    <!-- Slide indicators -->
    <!-- <div class="slide-indicators">
      <span
        v-for="(_, index) in bannerImages"
        :key="index"
        class="indicator"
        :class="{ active: index === currentSlide }"
        @click="goToSlide(index)"
      ></span>
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import store from "@/store";

const router = useRouter();

// Banner images data
const bannerImages = ref([
  {
    image: require("@/v2/assets/home/banner_gradient.jpg"),
    title: `Welcome Back, ${store.state.fullname}`,
    subtitle:
      "Here are some of the latest updates from the workplace and your latest schedule",
    subtitleSize: "16px", // Custom subtitle font size
  },
  {
    image: require("@/v2/assets/home/background_banner.png"),
    iconImage: require("@/v2/assets/home/image_banner.png"), // Icon image for first slide
    // title: "Stay Connected", // Optional title (commented out for demonstration)
    subtitle:
      "Workspaces from the 2022–2025 period on the <strong> Old DWP </strong> platform are now accessible via the ",
    subtitleSize: "21px", // Larger subtitle font size for this banner
  },
]);

// Current slide index
const currentSlide = ref(0);

// Auto-slide timer
let autoSlideTimer: ReturnType<typeof setInterval> | null = null;

// Start auto-slide
const startAutoSlide = () => {
  if (autoSlideTimer) {
    clearInterval(autoSlideTimer);
  }
  autoSlideTimer = setInterval(() => {
    nextSlide();
  }, 5000); // 5 seconds
};

// Stop auto-slide
const stopAutoSlide = () => {
  if (autoSlideTimer) {
    clearInterval(autoSlideTimer);
    autoSlideTimer = null;
  }
};

// Navigation methods
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % bannerImages.value.length;
};

const prevSlide = () => {
  currentSlide.value =
    currentSlide.value === 0
      ? bannerImages.value.length - 1
      : currentSlide.value - 1;
  // Restart auto-slide when manually navigating
  startAutoSlide();
};

const goToSlide = (index: number) => {
  currentSlide.value = index;
  // Restart auto-slide when manually navigating
  startAutoSlide();
};

// Navigation to history page
const goToHistoryPage = () => {
  router.push({ name: "v2.history" }); // Navigate to the history route by name
};

// Handle clicks on subtitle (for clickable elements)
const handleSubtitleClick = (event: Event) => {
  const target = event.target as HTMLElement;
  if (target && target.classList.contains("clickable-link")) {
    goToHistoryPage();
  }
};

// Component lifecycle
onMounted(() => {
  startAutoSlide();
});

onUnmounted(() => {
  stopAutoSlide();
});
</script>

<style scoped>
.home-banner {
  max-width: 1000vw;
  height: 220px;
  border-radius: 20px !important;
  border: 1px solid #f5f5f5;
  position: relative;
  overflow: hidden;
}

/* Slides container for animation */
.slides-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: 100% 100%;
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  flex-direction: column;
  opacity: 0;
  transition: opacity 0.6s ease-in-out;
}

.slide.active {
  opacity: 1;
}

/* Entrance animations — triggered when slide is active */
.slide.active .anim-icon {
  animation: iconFloat 0.7s ease-out forwards,
    floatUpDown 3s ease-in-out 0.7s infinite;
}

.slide.active .anim-title {
  animation: slideInLeft 0.6s ease-out forwards;
}

.slide.active .anim-subtitle {
  animation: slideInLeft 0.6s ease-out 0.15s both;
}

/* Inactive slides reset animation state */
.anim-icon,
.anim-title,
.anim-subtitle {
  opacity: 0;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-28px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes iconFloat {
  from {
    opacity: 0;
    transform: translateY(18px) scale(0.92);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes floatUpDown {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.banner-content {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  align-items: center;
  padding: 20px 0;
}

.banner-content.no-icon-content {
  align-items: flex-start;
}

.content-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  padding-left: 5vw;
  padding-right: 5vw;
  gap: 25px;
}

.banner-icon {
  flex-shrink: 0;
}

.banner-image {
  width: 170px;
  height: 150px;
  border-radius: 16px;
  /* object-fit: cover; */
  /* border: 3px solid rgba(255, 255, 255, 0.3); */
  /* box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3); */
}

.text-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

.text-content.no-icon {
  justify-content: flex-start;
  padding-top: 40px;
}

.text-banner {
  text-align: left;
  font-size: 26px;
  color: white;
  font-weight: bold;
  margin: 0;
}

.text-sub-banner {
  text-align: left;
  font-size: 16px;
  color: white;
  margin: 8px 0 0 0;
  line-height: 1.5;
}

/* Ensure consistent alignment for both subtitle paragraphs */
/* .text-sub-banner.clickable-history {
  margin-top: 8px;
} */

/* When title is missing, remove top margin from subtitle */
.text-content:not(:has(.text-banner)) .text-sub-banner {
  margin-top: 0;
}

/* Clickable link styling */
.text-sub-banner :deep(.clickable-link) {
  cursor: pointer !important;
  transition: all 0.3s ease;
  display: inline;
}

.text-sub-banner :deep(.clickable-link:hover) {
  cursor: pointer !important;
  opacity: 0.8;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  transform: scale(1.02);
}

/* Standalone clickable history styling */
.clickable-history {
  cursor: pointer !important;
  transition: all 0.3s ease;
  color: white;
}

.clickable-history:hover {
  cursor: pointer !important;
  opacity: 0.8;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  transform: scale(1.02);
}

/* Carousel Navigation */
.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  left: 0;
  display: flex;
  justify-content: space-between;
  padding: 0 15px;
  z-index: 10;
  pointer-events: none;
}

.nav-arrow {
  background: transparent;
  border: none;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  pointer-events: auto;
  /* border: 2px solid rgba(255, 255, 255, 0.5); */
  /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3); */
}

.nav-arrow:hover {
  background: rgba(0, 0, 0, 0.5);
  transform: scale(1.1);
}

.nav-arrow:active {
  transform: scale(0.95);
}

.nav-arrow svg {
  width: 24px;
  height: 24px;
}

/* Slide Indicators */
.slide-indicators {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 3;
}

.indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
}

.indicator.active {
  background: white;
  transform: scale(1.2);
}

.indicator:hover {
  background: rgba(255, 255, 255, 0.7);
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    padding-left: 6vw;
    gap: 20px;
  }

  .banner-image {
    width: 90px;
    height: 90px;
    border-radius: 14px;
  }

  .text-banner {
    font-size: 22px;
  }

  /* Scale down custom subtitle sizes for tablet */
  .text-sub-banner {
    font-size: 14px !important;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .banner-image {
    width: 70px;
    height: 70px;
    border-radius: 12px;
  }

  .text-banner {
    font-size: 20px;
  }

  /* Scale down custom subtitle sizes for mobile */
  .text-sub-banner {
    font-size: 13px !important;
  }
}
</style>
