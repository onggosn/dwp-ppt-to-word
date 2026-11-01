<template>
  <div>
    <v-row>
      <v-col cols="12">
        <div class="view-chat" id="view_chat">
          <template v-if="isLoading">
            <free-style-shimmer
              v-for="idx in 4"
              :key="idx"
              :is-loading="true"
              width="100%"
              height="4.3rem"
              border-radius="10px"
              class="my-2"
            />
          </template>
          <template v-else>
            <row-discution-component
              v-for="(item, idx) in chatList"
              :key="idx"
              :item="item"
            />
          </template>
        </div>
      </v-col>
      <v-col cols="12" style="position: fixed; bottom: 20px; z-index: 1">
        <div class="d-flex justify-space-between align-center">
          <v-textarea
            rows="2"
            max-rows="3"
            placeholder="Type Message"
            variant="plain"
            style="border-radius: 20px; background: white"
            class="mx-1"
            v-model="chatMsg"
            @keydown.enter.exact.prevent="sendDiscution()"
            :hide-details="true"
          ></v-textarea>
          <v-btn
            style="color: #267dc2; background-color: white; margin-right: 20px"
            size="x-large"
            @click="sendDiscution()"
            icon="mdi-send"
          ></v-btn>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import RowDiscutionComponent from "@/components/discution/RowDiscutionComponent.vue";
import client from "@/library/ApiClient";

export default {
  name: "TaskDiscussionView",
  components: {
    RowDiscutionComponent,
  },
  data() {
    return {
      isLoading: false,
      task: {},
      chatMsg: null,
      chatList: [],
    };
  },
  methods: {
    getTask() {
      client
        .getTasksByIdTask({
          store: this.$store,
          data: {
            id: this.$route.params.taskId,
            username: this.$store.state.username,
          },
        })
        .then((res) => {
          let data = res.plainData.pop();
          this.task = data;
        });
    },
    getDiscution() {
      client
        .getTaskDiscussionViewByIdTask({
          store: this.$store,
          data: {
            taskId: this.$route.params.taskId,
          },
        })
        .then((res) => {
          this.chatList = res.plainData.map((e) => {
            return {
              message: e.content,
              datetime: e.createdDate,
              sender: e.name,
              username: e.createdBy,
            };
          });
        })
        .finally(() => {
          this.isLoading = false;
          this.scroolDown();
        });
    },
    sendDiscution() {
      if (this.task.status == 3) {
        alert("finished task can't use discussion anymore");
      } else if (this.chatMsg) {
        client
          .insertTaskDiscussion({
            store: this.$store,
            data: {
              taskId: this.$route.params.taskId,
              content: this.chatMsg,
              createdBy: this.$store.state.username,
              createdDate: new Date(
                new Date().toISOString().slice(0, 10) + "T00:00:00"
              ),
            },
          })
          .finally(() => {
            this.getDiscution();
          });
      }
      this.chatMsg = null;
    },
    scroolDown() {
      let el = document.getElementById("view_chat");
      if (el) {
        el.scrollTop = el.scrollHeight;
      }
    },
  },
  created() {
    this.getTask();
    this.getDiscution();
  },
};
</script>

<style scoped>
.view-chat {
  max-height: 56vh;
  overflow: hidden auto;
  margin-top: 0px;
  margin-bottom: 20px;
}
</style>
