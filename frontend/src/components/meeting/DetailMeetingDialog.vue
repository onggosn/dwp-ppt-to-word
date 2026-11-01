<template>
  <v-dialog v-model="showDialog" persistent width="70%">
    <v-card>
      <v-card-title
        class="text-center mt-4 mb-2 font-weight-medium"
        style="color: #4b4b4b"
      >
        <div v-if="loading" style="text-align: -webkit-center">
          <free-style-shimmer
            :is-loading="true"
            height="20px"
            width="400px"
            border-radius="10px"
            color="#d3d3d3"
          />
        </div>
        <div v-else>
          <div class="text-h6">{{ meeting.meetingName }}</div>
        </div>
        <v-btn
          class="mr-5 mt-3"
          style="position: absolute; right: 0; top: 0"
          text
          fab
          small
          elevation="0"
          @click="close()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-btn
        elevation="0"
        class="d-block separator-horizontal"
        style="cursor: none"
      />
      <v-card-text>
        <div v-if="loading">
          <paragraph-shimmer
            :is-loading="true"
            :lines="7"
            :random-size="true"
          />
        </div>
        <div v-else>
          <v-container no-gutters>
            <v-row
              class="container"
              style="overflow-x: hidden; overflow-y: auto"
            >
              <v-col cols="7">
                <v-row>
                  <v-col>
                    <div>
                      <v-icon color="#267DC2" size="20" class="mr-3">
                        mdi-clock-outline</v-icon
                      >
                      {{ reformatTime(meeting.startDate) }} -
                      {{ reformatTime(meeting.endDate) }}
                      <div class="ml-9">
                        {{ reformatDate(meeting.startDate) }}
                      </div>
                    </div>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-icon color="#267DC2" class="mr-3"
                      >mdi-map-marker-outline</v-icon
                    >
                    {{ meeting.platform }}
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="1">
                    <v-icon color="#267DC2" size="25" class="mr-3"
                      >mdi-account-outline</v-icon
                    >
                  </v-col>
                  <v-col>
                    <span
                      v-for="(item, index) in meeting.memberMeeting"
                      :key="index"
                    >
                      <template v-if="!seeMore">
                        <span v-if="index < 4">
                          <span
                            v-if="
                              checkLastIndex(
                                meeting.memberMeeting.length < 4
                                  ? meeting.memberMeeting.length
                                  : 4,
                                index
                              )
                            "
                            >{{ item.name }}</span
                          >
                          <span v-else>{{ item.name }}, </span>
                        </span>
                        <span
                          style="cursor: pointer"
                          class="text-blueTheme-gradien"
                          v-if="
                            index == 4 &&
                            meeting.memberMeeting.length - 1 > index
                          "
                          @click="seeMore = true"
                        >
                          See All Member >>
                        </span>
                      </template>
                      <template v-else>
                        <span
                          v-if="
                            checkLastIndex(meeting.memberMeeting.length, index)
                          "
                        >
                          {{ item.name }}
                        </span>
                        <span v-else> {{ item.name }}, </span>
                      </template>
                    </span>
                  </v-col>
                </v-row>
              </v-col>
              <v-col class="mt-5" cols="5">
                <v-row justify="center" style="margin-bottom: 22px"
                  ><v-btn
                    rounded="lg"
                    color="#1b6fb2"
                    class="btn mt-7"
                    block
                    @click="openMeeting"
                    >Join Meeting</v-btn
                  ></v-row
                >
                <div v-if="meeting.isOwner">
                  <v-row justify="center" class="mb-3"
                    ><v-btn
                      rounded="lg"
                      color="#588e44"
                      class="btn"
                      block
                      @click="edit"
                      >Edit Meeting</v-btn
                    ></v-row
                  >
                  <v-row justify="center"
                    ><v-btn
                      rounded="lg"
                      color="#e9111c"
                      class="btn"
                      block
                      @click="deleteMeeting(meeting.id)"
                      >Delete Meeting</v-btn
                    ></v-row
                  >
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <div class="mx-2 my-2">
                  <div ref="myEditor" />
                </div>
              </v-col>
            </v-row>
          </v-container>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
  <DeleteMeetingDialog
    ref="deleteMeetingDialog"
    @refrehAfterDelete="showTaskMeeting"
  />
  <edit-meeting-dialog
    ref="editMeeting"
    :item="meeting"
    @refreshAfterEdit="refreshPage(meeting)"
  ></edit-meeting-dialog>
</template>
<script>
import { defineComponent } from "vue";
import client from "@/library/ApiClient";
import { reformatDate, reformatTime } from "@/library/DateHelper";
import DeleteMeetingDialog from "@/components/meeting/DeleteMeetingDialog.vue";
import EditMeetingDialog from "@/components/meeting/CreateMeetingDialog.vue";
import sanitizeHtml from "sanitize-html";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";

export default defineComponent({
  components: { DeleteMeetingDialog, EditMeetingDialog },
  data() {
    return {
      showDialog: false,
      meeting: {},
      loading: false,
      seeMore: false,
      isAdmin: false,
      editor: EditorOutput.CustomClassic,
      editorDisabled: true,
      body: null,
      editorConfig: {
        toolbar: [],
      },
    };
  },
  emits: ["showDialogListMeeting"],
  computed: {
    cleanMessage() {
      const message = this.meeting.body;
      const hasDisallowedContent = /<\s*a[^>]*>(.*?)<\s*\/\s*a>/g.test(message);

      if (hasDisallowedContent) {
        return sanitizeHtml(message);
      } else {
        return message;
      }
    },
  },
  mounted() {
    this.$watch(
      () => {
        return this.loading;
      },
      (val) => {
        if (!val)
          // menunggu HTML nya ke render
          setTimeout(() => {
            this.initEditor();
          }, 500);
      }
    );
  },
  methods: {
    start(meeting) {
      this.showDialog = true;
      this.loading = true;
      client
        .getTaskMeetingByIdMeeting({
          store: this.$store,
          data: {
            id: meeting.id,
          },
        })
        .then((respone) => {
          this.meeting = respone.plainData[0];
          this.body = this.meeting.body;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
          this.showDialog = false;
        });
    },
    close() {
      this.showDialog = false;
    },
    async initEditor() {
      let config = await EditorOutput.CustomClassic.create(
        this.$refs.myEditor,
        {
          initialData: this.body,
          updateSourceElementOnDestroy: false,
          toolbar: {
            items: [],
          },
          licenseKey:
            this.$store.getters["userStore/getInitializeConfig"]?.ckEditor
              ?.license || "",
        }
      );
      config.enableReadOnlyMode("readonlyeditor");
    },
    reformatDate(value) {
      return reformatDate(value);
    },
    reformatTime(value) {
      return reformatTime(value);
    },
    openMeeting() {
      if (this.meeting.platform == "Zoom") {
        if (this.isAdmin) {
          window.open(this.meeting.linkMeeting2, "_blank").focus();
        } else {
          window.open(this.meeting.linkMeeting, "_blank").focus();
        }
      } else {
        window.open(this.meeting.linkMeeting, "_blank").focus();
      }
    },
    checkOwner() {
      this.isAdmin = client.checkOwner(
        {
          store: this.$store,
          data: {
            id: this.meeting.idTask,
          },
        },
        this.$store.state.username
      );
    },
    deleteMeeting(idMeeting) {
      this.$refs.deleteMeetingDialog.start(idMeeting);
      this.showDialog = false;
    },
    showTaskMeeting() {
      this.$emit("showDialogListMeeting");
    },
    edit() {
      this.$refs.editMeeting.start();
    },
    refreshPage(item) {
      this.start(item);
      this.showTaskMeeting();
    },
    checkLastIndex(length, index) {
      return length == index + 1;
    },
  },
});
</script>
<style>
.table table,
.table th,
.table td {
  border: 2px solid !important;
  border-collapse: collapse !important;
  padding: 3px 5px !important;
}
.table table {
  width: 100%;
}
</style>
<style scoped>
:deep(.ck.ck-editor__main > .ck-editor__editable:not(.ck-focused)) {
  border-color: transparent;
}
:deep(.ck-reset_all) {
  display: none;
}
.separator-horizontal {
  background: linear-gradient(
    270deg,
    rgba(255, 255, 252, 0.8) 0%,
    #a6abc7 51.56%,
    rgba(255, 255, 252, 0.8) 100%
  );
  height: 1.2px;
  width: 100%;
}
.container {
  border-radius: 15px;
  background-color: #f7fbfe;
}

.btn {
  width: 15vw;
  color: white;
}
</style>
