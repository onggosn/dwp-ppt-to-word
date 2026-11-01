<template>
  <v-sheet
    class="pl-10 pt-3 pb-3 d-flex justify-space-between align-center"
    style="background: #e0efff"
  >
    <div class="d-flex align-center">
      <v-btn
        density="default"
        icon="mdi-arrow-left"
        style="color: #267dc2"
        :to="{
          name: 'v2.workspace-rdg-detail',
          params: { typeRDG: 'rdgb', idEvent: $route.params.idEvent },
        }"
      ></v-btn>
      <p class="ml-3 font-weight-bold text-18" style="color: #267dc2">
        {{ $store.getters["collaborationStore/getEventName"] }}
      </p>
    </div>
  </v-sheet>
  <div style="padding-left: 20px; display: flex; width: 100%">
    <div class="left-side">
      <ScrollObserver />
    </div>
    <div class="right-side">
      <v-card
        class="mx-auto overflow-auto"
        style="
          border-radius: 5px 15px 15px 5px;
          position: sticky;
          top: 1rem;
          max-height: 100vh;
        "
      >
        <div
          class="d-flex justify-space-between mb-6 align-center ml-4 mt-3 align-start"
        >
          <p class="font-weight-bold">Content</p>
        </div>
        <v-divider />
        <TableOfContent
          :isApproved="true"
          :onRegisterRefresh="registerRefreshHandler"
        />
      </v-card>
    </div>
  </div>
  <!-- <v-sheet class="d-flex bg-transparent ml-10" min-height="100%">
    <v-sheet
      class="ma-2 pa-2 bg-transparent flex-fill"
      style="text-align: -webkit-center"
    >
      <ScrollObserver />
    </v-sheet>

    <v-sheet class="ma-2 pa-2 bg-transparent" width="400px">
      <v-card
        class="mx-auto overflow-auto"
        height="calc(100vh - 2rem)"
        style="border-radius: 5px 15px 15px 5px; position: sticky; top: 1rem"
      >
        <div
          class="d-flex justify-space-between mb-6 align-center ml-4 mt-3 align-start"
        >
          <p class="font-weight-bold">Content</p>
        </div>
        <v-divider />
        <TableOfContent
          :isApproved="true"
          :onRegisterRefresh="registerRefreshHandler"
        />
      </v-card>
    </v-sheet>
  </v-sheet> -->
  <!-- Hide dulu -->
  <!-- <ModalLeave :can-leave="edited" /> -->
</template>
<script lang="js">
import TableOfContent from "@v2/components/contentManagement/TableOfContent.vue";
import ScrollObserver from "@v2/components/collaboration/ScrollObserver.vue";
import store from "@/store";
import { useRoute }from "vue-router";

export default {
  data() {
    return {
      typeRDG: this.$route.params.typeRDG,
      route: useRoute(),
    };
  },
  components: {
    TableOfContent,
    ScrollObserver,
  },
  methods: {
    registerRefreshHandler() {
     undefined;
    }
  },
  async beforeRouteEnter(to, from, next) {
    try {
      await store.dispatch("contentStore/getTableOfContent", {
        idEvent: to.params.idEvent,
      });
      next();
    } catch (error) {
      return false;
    }
  },
  mounted() {
    store.dispatch("meetingStore/fetchDashboardSummary", {
    idEvent: this.route.params.idEvent,
  });

    if (!["rdgb", "rdgtk"].includes(this.typeRDG.toLowerCase())) {
      this.$router.push({
        name: "v2.rdgb",
      });
    }
  },
};
</script>

<style scoped>
.left-side {
  background-color: transparent;
  padding: 20px;
  font-size: 1rem;
}

.right-side {
  background-color: transparent;
  padding: 3px;
  margin-bottom: 18px;
  font-size: 1rem;
}

@media (min-width: 1600px) {
  .left-side {
    width: 60vw;
  }

  .right-side {
    width: 40vw;
  }
}

@media (min-width: 1400px) and (max-width: 1599px) {
  .left-side {
    width: 65vw;
  }

  .right-side {
    width: 35vw;
  }
}

@media (min-width: 1300px) and (max-width: 1399px) {
  .left-side {
    width: 70vw;
  }

  .right-side {
    width: 30vw;
  }
}

@media (min-width: 768px) and (max-width: 1299px) {
  .left-side {
    width: 80vw;
  }
  .right-side {
    width: 20vw;
  }
}

/* For screens that are 767px or narrower */
@media (max-width: 767px) {
  .right-side {
    width: 100%;
  }
}
</style>
