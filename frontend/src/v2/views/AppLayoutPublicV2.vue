<template>
  <v-app class="public-app overflow-visible">
    <v-layout class="overflow-visible">
      <v-navigation-drawer
        permanent
        width="280"
        class="border-right documentation-sidebar"
      >
        <v-list density="compact" nav class="mt-4 px-3">
          <v-list-subheader class="text-overline pl-2">
            <img
              class="mb-4"
              width="280"
              :src="require('@/v2/assets/frame/logo_dwp_new.svg')"
              style="cursor: pointer"
              @click="$router.push({ name: 'login' })"
            />
          </v-list-subheader>
          <v-list-item
            v-for="(item, i) in navItems"
            :key="i"
            :value="item"
            class="mb-2 menu-item"
            :class="{ 'active-menu-item': activeId === item.id }"
            @click="scrollTo(item.id)"
          >
            <template v-slot:prepend>
              <v-icon
                :icon="item.icon"
                size="small"
                class="mr-2"
                :color="activeId === item.id ? 'white' : '#065695'"
              ></v-icon>
            </template>
            <v-list-item-title
              class="font-weight-medium"
              :class="activeId === item.id ? 'text-white' : 'text-darkBlue'"
            >
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main>
        <div>
          <img
            :src="require('@v2/assets/frame/batik_header.webp')"
            style="position: absolute; right: 0; z-index: -99; max-width: 600px"
          />
        </div>
        <div class="pa-8">
          <router-view />
        </div>
      </v-main>
    </v-layout>
    <v-footer app class="footer footer-with-pattern"> </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const activeId = ref("core-components");
let observer: IntersectionObserver | null = null;

const navItems = [
  {
    title: "Core Components",
    id: "core-components",
    icon: "mdi-view-dashboard",
  },
  { title: "Typography & Sizes", id: "typography", icon: "mdi-format-size" },
  { title: "Gradients & Colors", id: "gradients", icon: "mdi-palette" },
  { title: "Buttons Style", id: "buttons", icon: "mdi-gesture-tap-button" },
  { title: "Sections & Separators", id: "sections", icon: "mdi-view-agenda" },
  {
    title: "Common Form Elements",
    id: "form-elements",
    icon: "mdi-form-select",
  },
  { title: "Utilities", id: "utilities", icon: "mdi-hammer-wrench" },
];

const scrollTo = (id: string) => {
  activeId.value = id;
  const element = document.getElementById(id);
  if (element) {
    const top = element.getBoundingClientRect().top + window.pageYOffset - 100;
    window.scrollTo({ top, behavior: "smooth" });
  }
};

onMounted(() => {
  const options = {
    root: null,
    rootMargin: "-20% 0px -70% 0px", // Adjust this to trigger when section is roughly in the top part of screen
    threshold: 0,
  };

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        activeId.value = entry.target.id;
      }
    });
  }, options);

  navItems.forEach((item) => {
    const el = document.getElementById(item.id);
    if (el) observer?.observe(el);
  });
});

onUnmounted(() => {
  observer?.disconnect();
});
</script>

<style scoped>
.public-app {
  background-color: #f5f5f5;
}

.documentation-sidebar {
  position: fixed !important;
  top: 0px !important; /* Height of app bar */
  height: calc(100vh - 64px) !important;
  overflow-y: auto;
}

.active-menu-item {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%) !important;
  color: white !important;
  box-shadow: 0px 4px 10px rgba(6, 86, 149, 0.3);
}

.text-darkBlue {
  color: #3a416f !important;
}

.footer {
  background-color: #f5f5f5;
  z-index: 1 !important;
  padding: 0 !important;
}

.footer-with-pattern {
  background-image: url("@v2/assets/frame/batik_footer.webp");
  background-repeat: repeat-x;
  background-size: auto 60px;
  background-position: center bottom;
  min-height: 60px;
}
</style>
