<template>
  <v-sheet style="background: transparent !important">
    <div class="banner-container" style="position: relative; margin: -10px">
      <div class="banner-overlay">
        <div class="d-flex" style="justify-content: center">
          <img
            :src="require(`@/v2/assets/banner_help_left.svg`)"
            height="210px"
          />
          <div style="width: 4vw"></div>
          <div
            class="text-white font-weight-bold"
            style="align-content: center; font-size: 32px; letter-spacing: 1px"
          >
            Need some <br />
            Help ?
          </div>
          <div style="width: 3vw"></div>
          <img
            :src="require(`@/v2/assets/banner_help_left.svg`)"
            height="210px"
          />
        </div>
      </div>
      <div class="banner">
        <!-- Red gradient overlay -->
      </div>
    </div>

    <p
      v-if="route.name === 'v2.help'"
      class="text-center text-28 text-blueTheme mt-10"
      style="font-family: 'Poppins'; font-weight: 900"
    >
      Browse Topics
    </p>

    <v-sheet
      style="background: transparent; place-items: center"
      v-if="route.name === 'v2.help'"
    >
      <v-container>
        <v-row no-gutters>
          <!-- Shimmer skeleton cards while loading -->
          <template v-if="isLoading">
            <v-col
              cols="3"
              v-for="n in 8"
              :key="`shimmer-${n}`"
              class="pr-4 pl-4"
            >
              <div
                class="shimmer-card rounded-lg mt-5 elevation-4 pa-5"
                style="width: 100%; height: 130px"
              >
                <div class="d-flex align-center">
                  <div class="shimmer-box shimmer-icon mr-3"></div>
                  <div style="flex: 1">
                    <div class="shimmer-box shimmer-line-long mb-2"></div>
                    <div class="shimmer-box shimmer-line-short"></div>
                  </div>
                </div>
              </div>
            </v-col>
          </template>

          <!-- Actual topic cards -->
          <template v-else>
            <v-col
              cols="3"
              v-for="(item, index) in topics.filter((t) => t.isActive)"
              :key="index"
              class="pr-4 pl-4"
            >
              <v-card
                :to="{
                  name: 'v2.faq',
                  query: {
                    category: item.topicName,
                    identity: item.idTopics,
                  },
                }"
                style="
                  width: 100%;
                  height: 130px;
                  cursor: pointer;
                  align-content: center;
                  margin-right: 10px;
                "
                class="pa-5 rounded-lg mt-5 elevation-4"
                router
              >
                <div class="d-flex text-center" style="align-items: center">
                  <img
                    :src="item.topicIconLink || loadIcon(item.iconName)"
                    width="30px"
                    height="30px"
                    class="d-flex mr-3 align-center justify-center"
                  />
                  <p
                    class="text-18 text-blueTheme font-weight-medium"
                    style="text-align: start"
                  >
                    {{ item.topicName }}
                  </p>
                </div>
              </v-card>
            </v-col>
          </template>
        </v-row>

        <!-- Contact card shimmer -->
        <div
          v-if="isLoading"
          class="shimmer-card mt-10 pa-10 mb-10 ml-4 mr-4"
          style="border-radius: 12px; height: 120px"
        ></div>

        <!-- Contact card actual -->
        <v-card
          v-else
          class="mt-10 pa-10 mb-10 ml-4 mr-4 elevation-4"
          style="border-radius: 12px"
        >
          <v-row no-gutters>
            <v-col cols="6" class="px-4">
              <div class="d-flex justify-start">
                <img :src="require('@/v2/assets/faq/faq1.png')" width="100px" />
                <div class="ml-4 py-2">
                  <p class="text-20 font-weight-bold text-blueTheme">
                    Hubungi DMST-MRDG
                  </p>
                  <p class="text-14 text-blueTheme">
                    Jika ada pertanyaan atau Kendala terkait Proses Bisnis RDG
                  </p>
                </div>
              </div>
            </v-col>
            <v-col cols="6" class="px-4">
              <div class="d-flex justify-start">
                <img :src="require('@/v2/assets/faq/faq2.png')" width="150px" />
                <div class="ml-4 py-2">
                  <p class="text-20 font-weight-bold text-blueTheme">
                    Helpdesk TI 8000
                  </p>
                  <p class="text-14 text-blueTheme">
                    Jika ada pertanyaan atau Kendala terkait Aplikasi DWP
                  </p>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-container>

      <!-- Main dynamic content area -->
    </v-sheet>
    <router-view class="mt-8" />
  </v-sheet>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const route = useRoute();

type TTopics = {
  idTopics: string;
  iconName: string;
  isActive: boolean;
  order: number;
  topicName: string;
  topicIconLink: string;
};

const topics = ref<TTopics[]>([]);
const isLoading = ref(true);

onMounted(() => {
  store.dispatch("userStore/getListTopics").then((res) => {
    if (res.responseCode == "011000") {
      const data = res.responseData;
      topics.value = data;
    }
    isLoading.value = false;
  });
});

const loadIcon = (iconName: string) => {
  try {
    return require(`@/v2/assets/icon/faq_${iconName}.svg`);
  } catch (e) {
    return require("@/v2/assets/icon/faq_general.svg"); // fallback icon
  }
};
</script>
<style scoped>
.banner {
  /* background-image: url("@/v2/assets/banner_help3.svg"); */
  background-image: url("@/v2/assets/batik/pola-batik.png");
  background-repeat: repeat;
  background-size: contain;
  height: 200px;
  border-radius: 20px;
  position: relative;
  opacity: 0.07;
  z-index: 2;
}

.banner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 1;
  background-image: url("@/v2/assets/batik/bg-gradient-history.jpg");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  height: 200px;
  z-index: 1;
}

/* ── Shimmer Loading ── */
@keyframes shimmer {
  0% {
    background-position: -600px 0;
  }
  100% {
    background-position: 600px 0;
  }
}

.shimmer-card {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  display: flex;
  align-items: center;
}

.shimmer-box {
  border-radius: 6px;
  background: linear-gradient(90deg, #e8e8e8 25%, #f5f5f5 50%, #e8e8e8 75%);
  background-size: 1200px 100%;
  animation: shimmer 1.4s infinite linear;
}

.shimmer-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  flex-shrink: 0;
}

.shimmer-line-long {
  height: 14px;
  width: 70%;
}

.shimmer-line-short {
  height: 12px;
  width: 45%;
}
</style>
