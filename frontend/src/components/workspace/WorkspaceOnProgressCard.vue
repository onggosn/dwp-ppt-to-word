<!-- <script>
import { defineComponent } from "vue";
import { reformatDateCard } from "@/library/DateHelper";
import { mWorkspaceInProgress } from "@/models/workspace";

export default defineComponent({
  name: "WorkspaceOnProgressCard",
  emits: [""],
  components: {},
  data: function () {
    return {
      isLoading: false,
      items: {},
      seeMore: false,
    };
  },
  mounted() {
    this.doGetWorkspaceInProgress();
  },
  methods: {
    doGetWorkspaceInProgress(level = 1) {
      this.isLoading = true;
      mWorkspaceInProgress(level)
        .then((result) => {
          this.items = result;
          if (result.length) {
            if (result.length > 3) {
              this.seeMore = true;
              let element = document.getElementById("button-seemore");
              if (element) {
                element.style.display = "block";
              }
            }
          }
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    reformatDateCard(endDate) {
      return reformatDateCard(endDate);
    },
    setLevel(level) {
      this.doGetWorkspaceInProgress(level);
    },
    seeAll() {
      const collection = document.getElementsByClassName("card-wp");
      for (let i = 0; i < collection.length; i++) {
        collection[i].style.display = "block";
      }
      document.getElementById("button-seemore").style.display = "none";
    },
  },
});
</script>
<template>
  <v-sheet class="d-flex flex-wrap bg-transparent mb-3">
    <v-sheet
      class="flex-1-0 ml-5 pa-2 font-weight-bold"
      style="background: transparent"
    >
      Workspace In Progress
    </v-sheet>
    <hr />
    <v-sheet
      class="bg-transparent pa-2"
      width="55vw"
      style="align-self: center"
    >
      <v-sheet
        style="
          height: 1px;
          background: linear-gradient(
            270deg,
            rgba(255, 255, 252, 0.8) 0%,
            #a6abc7 51.56%,
            rgba(255, 255, 252, 0.8) 100%
          );
        "
      />
    </v-sheet>
  </v-sheet>
  <v-sheet
    class="d-flex flex-wrap ml-5 mb-5"
    style="background: transparent"
    v-if="!isLoading"
  >
    <template v-if="items.length">
      <template v-for="(item, index) in items" :key="item.id">
        <v-card
          :style="{ display: index > 2 ? 'none' : 'block' }"
          color="#fff"
          class="ma-2 pt-4 pb-4 pl-1 pr-2 rounded-lg card-wp"
          elevation="4"
          style="
            width: 22vw;
            height: 16vh;
            border-left: solid 5px #0a5b9a;
            cursor: pointer;
          "
          :to="{
            name: 'workspace-detail',
            params: { workspaceId: item.idWorkspace },
          }"
        >
          <v-card-title
            class="text-redTheme-gradien font-weight-bold mt-n2"
            style="
              white-space: pre-wrap;
              overflow: hidden;
              text-overflow: ellipsis;
              display: -webkit-box;
              -webkit-line-clamp: 2;
              -webkit-box-orient: vertical;
              text-align: center;
              padding-bottom: 1px;
            "
            >{{ item.workspaceName }}
          </v-card-title>
          <div
            class="text-subtitle-3 mt-1 ml-2 fw-500 text-10"
            style="color: #3a416f; text-align: center"
          >
            Due: {{ reformatDateCard(item.endDate) }}
          </div>
          <v-card-actions
            class="text-subtitle-3 ml-2"
            style="color: #3a416f; place-content: center"
          >
            <!-- Due: {{ reformatDateCard(item.endDate) }} -->
          </v-card-actions>
        </v-card>
      </template>
    </template>
    <template v-else>
      <p class="ml-2 mb-10" style="color: grey">
        There's no in progress workspace data
      </p>
    </template>
  </v-sheet>
  <v-sheet
    class="d-flex flex-wrap ml-5"
    style="background: transparent"
    v-if="isLoading"
  >
    <free-style-shimmer
      v-for="n in 3"
      :key="n"
      :is-loading="true"
      width="22vw"
      height="15vh"
      border-radius="10px"
      color="#DCDCDC"
      class="ml-2 mt-2"
    />
  </v-sheet>

  <div
    v-if="seeMore && items.length"
    id="button-seemore"
    class="pa-2 text-red text-end mt-5 font-weight-bold"
    style="cursor: pointer; margin-right: 5vw"
    @click="seeAll()"
  >
    See more >>
  </div>
</template>

<style scoped>
.text-redTheme-gradien {
  background: -webkit-linear-gradient(#d6212a, #ff000d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 16px;
}

:deep(.v-card .v-card-title) {
  line-height: normal !important;
}
</style> -->
