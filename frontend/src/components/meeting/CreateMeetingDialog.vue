<template>
  <v-dialog v-model="dialog" persistent width="60%">
    <v-card>
      <v-card-title
        class="text-center mt-4 mb-2 font-weight-medium"
        style="color: #4b4b4b"
      >
        <div class="text-h6">{{ labelDialog }}</div>
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
        <form>
          <div class="subtitle-2">Members</div>
          <v-autocomplete
            v-model="formData.members"
            clearable
            chips
            :items="listMemberShow"
            item-value="username"
            item-title="name"
            multiple
            closable-chips
            hide-selected
            search
            variant="underlined"
            :loading="isLoading"
            @input="v$.formData.members.$touch"
            :error-messages="e(v$.formData.members)"
          ></v-autocomplete>

          <div class="subtitle-2">Subject</div>
          <v-text-field
            v-model="formData.meetingName"
            :error-messages="e(v$.formData.meetingName)"
            placeholder="Masukan judul meeting"
            required
            variant="solo"
            @input="v$.formData.meetingName.$touch"
            @blur="v$.formData.meetingName.$touch"
          ></v-text-field>

          <div class="subtitle-2">Media</div>
          <v-select
            v-model="formData.platform"
            :disabled="isDisabled"
            item-title="platform"
            item-value="platform"
            :items="meetingPlatformItem"
            :error-messages="e(v$.formData.platform)"
            placeholder="Choose meeting platform"
            required
            variant="solo"
            @change="v$.formData.platform.$touch"
            @blur="v$.formData.platform.$touch"
            @update:modelValue="canInputLink()"
          ></v-select>
          <div v-if="isInputLink">
            <div class="subtitle-2">Link</div>
            <v-text-field
              v-model="formData.linkMeeting"
              :error-messages="e(v$.formData.linkMeeting)"
              placeholder="link"
              required
              variant="solo"
              @input="v$.formData.linkMeeting.$touch"
            ></v-text-field>
          </div>

          <div>Start Time</div>
          <v-row>
            <v-col cols="6">
              <VueDatePicker
                v-model="formData.startDate"
                :enable-time-picker="false"
                :month-change-on-scroll="false"
                auto-apply
              >
                <template #trigger>
                  <v-text-field
                    :value="
                      $filters.formatTimeEngToIndNoDays(formData.startDate)
                    "
                    append-inner-icon="mdi-calendar"
                    variant="solo"
                    placeholder="DD/MM/YYYY"
                    @change="v$.formData.startDate.$touch"
                    @blur="v$.formData.startDate.$touch"
                    :error-messages="e(v$.formData.startDate)"
                    class="cursor-pointer"
                  >
                  </v-text-field>
                </template>
              </VueDatePicker>
            </v-col>
            <v-col cols="6">
              <v-select
                v-model="formData.startTime"
                :items="timeItems"
                variant="solo"
                placeholder="Choose time"
                :error-messages="e(v$.formData.startTime)"
                @change="v$.formData.startTime.$touch"
                @blur="v$.formData.startTime.$touch"
              ></v-select>
            </v-col>
          </v-row>
          <div>End Time</div>
          <v-row>
            <v-col cols="6">
              <VueDatePicker
                v-model="formData.endDate"
                :enable-time-picker="false"
                :month-change-on-scroll="false"
                auto-apply
              >
                <template #trigger>
                  <v-text-field
                    :value="$filters.formatTimeEngToIndNoDays(formData.endDate)"
                    append-inner-icon="mdi-calendar"
                    variant="solo"
                    placeholder="DD/MM/YYYY"
                    @change="v$.formData.endDate.$touch"
                    @blur="v$.formData.endDate.$touch"
                    :error-messages="e(v$.formData.endDate)"
                    class="cursor-pointer"
                  >
                  </v-text-field>
                </template>
              </VueDatePicker>
            </v-col>
            <v-col cols="6">
              <v-select
                v-model="formData.endTime"
                :items="timeItems"
                variant="solo"
                placeholder="Choose time"
                :error-messages="e(v$.formData.endTime)"
                @change="v$.formData.endTime.$touch"
                @blur="v$.formData.endTime.$touch"
              ></v-select>
            </v-col>
          </v-row>
          <div class="subtitle-2">Body</div>
          <div class="mx-2 my-2">
            <div ref="myEditor" id="editors" />
          </div>
        </form>
      </v-card-text>
      <v-card-actions>
        <v-row class="pa-5">
          <v-col class="text-right">
            <v-btn @click="close" class="btn-default" elevation="2">
              Back
            </v-btn>
            <v-btn class="me-4 btn-primary" @click="create">
              {{ labelButton }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <loading-dialog v-if="isSubmit"></loading-dialog>
</template>
<script>
import { getErrorMessages, isError } from "@/library/ValidationHelper";
import client from "@/library/ApiClient";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import { format } from "date-fns";
import LoadingDialog from "@/components/LoadingDialog.vue";
import { getOnlyDate } from "@/library/DateHelper";
import EditorOutput from "@/v2/components/side-project/ckeditor/build/ckeditor";

const timeItems = [
  "00:00",
  "00:30",
  "01:00",
  "01:30",
  "02:00",
  "02:30",
  "03:00",
  "03:30",
  "04:00",
  "04:30",
  "05:00",
  "05:30",
  "06:00",
  "06:30",
  "07:00",
  "07:30",
  "08:00",
  "08:30",
  "09:00",
  "09:30",
  "10:00",
  "10:30",
  "11:00",
  "11:30",
  "12:00",
  "12:30",
  "13:00",
  "13:30",
  "14:00",
  "14:30",
  "15:00",
  "15:30",
  "16:00",
  "16:30",
  "17:00",
  "17:30",
  "18:00",
  "18:30",
  "19:00",
  "19:30",
  "20:00",
  "20:30",
  "21:00",
  "21:30",
  "22:00",
  "22:30",
  "23:00",
  "23:30",
];

export default {
  name: "AddMeetingForm",
  components: { LoadingDialog },
  emits: ["showCreateMeetingDialog", "refreshAfterEdit"],
  setup: () => ({ v$: useVuelidate() }),
  validations() {
    let formData = {
      members: { required },
      meetingName: { required },
      platform: { required },
      linkMeeting: { required },
      startDate: { required },
      startTime: { required },
      endDate: {
        required,
        moreThanStartDate: (value, vm) => {
          return new Date(value) >= new Date(vm.startDate);
        },
      },
      endTime: {
        required,
        moreThanStartTime: (value, vm) => {
          const timeStart = new Date(
            getOnlyDate(new Date(vm.startDate)) + " " + vm.startTime
          );
          const timeEnd = new Date(
            getOnlyDate(new Date(vm.endDate)) + " " + vm.endTime
          );

          if (Date.parse(vm.startDate) === Date.parse(vm.endDate)) {
            if (timeStart.getTime() >= timeEnd.getTime()) return false;
            else return true;
          } else {
            return true;
          }
        },
      },
      body: {},
    };

    if (this.isGenerateLink) delete formData.linkMeeting;

    return { formData };
  },
  props: { item: Object },
  data() {
    return {
      isDisabled: false,
      labelDialog: "Schedule Meeting",
      isLoading: false,
      isSubmit: false,
      isInputLink: true,
      dialog: false,
      labelButton: "Create",
      editorConfig: {
        toolbar: {
          items: [
            "|",
            "bold",
            "italic",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "undo",
            "redo",
          ],
        },
        table: {
          contentToolbar: ["tableColumn", "tableRow", "mergeTableCells"],
        },
        language: "en",
      },
      members: [],
      // newMembers: [],
      listMemberShow: [],
      itemMembers: [],
      // itemMembersId: [],
      meetingPlatformItem: [],
      timeItems,
      formData: {
        members: {
          username: null,
          groupName: null,
          name: null,
        },
        meetingName: null,
        platform: [],
        linkMeeting: "",
        startDate: null,
        startTime: null,
        endDate: null,
        endTime: null,
        body: "",
      },
      format: null,
    };
  },
  created() {
    this.getPlatform();
  },
  computed: {
    isGenerateLink() {
      return ["Ms Teams", "Zoom"].includes(this.formData.platform);
    },
  },
  mounted() {
    this.$watch(
      () => {
        return this.dialog;
      },
      (val) => {
        if (val)
          // menunggu HTML nya ke render
          setTimeout(() => {
            this.initEditor();
          }, 500);
      }
    );
  },
  methods: {
    e: getErrorMessages,
    isError: isError,
    start() {
      this.dialog = true;
      this.getMemberTask();

      if (typeof this.item !== "undefined") {
        // edit
        this.labelDialog = "Edit Meeting";
        this.labelButton = "Save";
        this.getMeetingById();
      }
    },
    close() {
      this.emptyState();
      this.v$.$reset();
      this.dialog = false;
    },
    getMemberTask() {
      this.isLoading = true;
      client
        .getListTaskMemberDataByIdTask({
          store: this.$store,
          data: {
            id:
              typeof this.item !== "undefined"
                ? this.item.idTask
                : this.$route.params.taskId,
          },
        })
        .then((response) => {
          this.listMemberShow = response.plainData.map((e) => {
            if (e.user == null) {
              return {
                username: e.groupName + "|" + true,
                groupName: true,
                name: e.groupName,
              };
            } else {
              return {
                username: e.user.username + "|" + false,
                groupName: false,
                name: e.user.name,
              };
            }
          });

          this.members = response.plainData;
          let uniqMember = [
            ...new Map(
              this.listMemberShow.map((e) => [e.username, e])
            ).values(),
          ];
          this.listMemberShow = uniqMember;

          // untuk edit jangan assign member
          if (typeof this.item === "undefined")
            this.formData.members = this.listMemberShow.map((m) => m.username);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getPlatform() {
      client
        .MeetingPlatform({
          store: this.$store,
        })
        .then((res) => {
          this.meetingPlatformItem = res.plainData;
        });
    },
    canInputLink() {
      let media = this.formData.platform;
      if (["Ms Teams", "Zoom"].includes(media)) {
        this.isInputLink = false;
      } else {
        this.isInputLink = true;
      }
    },
    create() {
      this.v$.$validate().then((res) => {
        if (res) {
          let listMember = this.formData.members.map((m) => {
            let arrMembers = m.split("|");
            if (arrMembers[1] === "true") {
              return {
                username: "",
                groupName: arrMembers[0],
              };
            } else {
              return {
                username: arrMembers[0],
                groupName: "",
              };
            }
          });

          let reqData = {
            ...this.formData,
            listMember: listMember,
            idTask:
              typeof this.item !== "undefined"
                ? this.item.idTask
                : this.$route.params.taskId,
            createdBy: this.$store.state.username,
            startDate:
              format(new Date(this.formData.startDate), "yyyy-MM-dd") +
              "T" +
              this.formData.startTime +
              ":00",
            endDate:
              format(new Date(this.formData.endDate), "yyyy-MM-dd") +
              "T" +
              this.formData.endTime +
              ":00",
          };

          if (typeof this.item === "undefined") this.doInsert(reqData);
          else this.doUpdate(reqData);
        }
      });
    },
    doInsert(data) {
      this.isSubmit = true;
      client
        .insertTaskMeeting({
          store: this.$store,
          data: {
            ...data,
          },
        })
        .then((res) => {
          if (res.status == 200) {
            this.isSubmit = false;
            this.close();
            this.$emit("showCreateMeetingDialog");
            this.$root.toast.show({
              message: "Meeting successfully created",
              color: "success",
              timeout: 5000,
              icon: "mdi-check",
            });
          } else {
            this.isSubmit = false;
            this.$root.toast.show({
              message: res.data.message,
              color: "error",
              timeout: 5000,
              icon: "mdi-check",
            });
          }
        })
        .catch((e) => {
          this.isSubmit = false;
          this.$root.toast.show({
            message: e.response.data.message,
            color: "error",
            timeout: 5000,
            icon: "mdi-check",
          });
        });
    },
    emptyState() {
      this.formData = {
        members: {
          username: null,
          groupName: null,
          name: null,
        },
        meetingName: null,
        platform: [],
        linkMeeting: "",
        startDate: null,
        startTime: null,
        endDate: null,
        endTime: null,
        body: "",
      };
    },
    getMeetingById() {
      this.isDisabled = true;
      if (["Ms Teams", "Zoom"].includes(this.item.platform))
        this.isInputLink = false;
      else this.isInputLink = true;

      let memberMeeting = this.item.memberMeeting.map((m) => {
        if (m.username != "" && m.username != null) {
          return m.username + "|" + false;
        } else {
          return m.groupName + "|" + true;
        }
      });
      let arrStartDate = this.item.startDate.slice(0, -3).split("T");
      let arrEndDate = this.item.endDate.slice(0, -3).split("T");

      this.formData = {
        meetingName: this.item.meetingName,
        platform: [this.item.platform],
        linkMeeting: this.item.linkMeeting,
        startDate: arrStartDate[0],
        startTime: arrStartDate[1],
        endDate: arrEndDate[0],
        endTime: arrEndDate[1],
        body: this.item.body,
        members: memberMeeting,
      };
    },
    doUpdate(data) {
      this.isSubmit = true;

      client
        .updateTaskMeeting({
          store: this.$store,
          data: {
            ...data,
            id: this.item.id,
            platform: this.formData.platform[0],
          },
        })
        .then((res) => {
          if (res.status == 200) {
            this.isSubmit = false;
            this.close();
            this.$emit("refreshAfterEdit", this.item);
            this.$root.toast.show({
              message: "Meeting successfully updated",
              color: "success",
              timeout: 5000,
              icon: "mdi-check",
            });
          }
        })
        .catch(() => {
          this.$root.toast.show({
            message: "[500] Meeting failed updated",
            color: "error",
            timeout: 5000,
            icon: "mdi-check",
          });
        });
    },
    async initEditor() {
      this.editorConfig = await EditorOutput.CustomClassic.create(
        this.$refs.myEditor,
        {
          initialData: this.formData.body,
          updateSourceElementOnDestroy: false,
          toolbar: {
            items: [
              "|",
              "bold",
              "italic",
              "|",
              "bulletedList",
              "numberedList",
              "|",
              "undo",
              "redo",
            ],
          },
          table: {
            contentToolbar: ["tableColumn", "tableRow", "mergeTableCells"],
          },
          language: "en",
          licenseKey:
            this.$store.getters["userStore/getInitializeConfig"]?.ckEditor
              ?.license || "",
        }
      ).then((editor) => {
        editor.model.document.on("change:data", () => {
          this.formData.body = editor.getData();
        });
      });
    },
  },
};
</script>
<style>
.ck-balloon-panel {
  z-index: 9999 !important;
}
.ck-content .table {
  width: 100%;
}
.ck input.ck-input.ck-input-text {
  box-shadow: var(--ck-inner-shadow), 0 0;
  background: var(--ck-color-input-background);
  border: 1px solid var(--ck-color-input-border);
  padding: var(--ck-spacing-extra-tiny) var(--ck-spacing-medium);
  transition-property: box-shadow, border;
  transition: 0.2s ease-in-out;

  height: inherit;
  width: inherit;
  font-size: inherit;
  margin: 0;
  box-sizing: border-box;
}

.ck input.ck-input.ck-input-text:focus {
  border: var(--ck-focus-ring);
  box-shadow: var(--ck-focus-outer-shadow), var(--ck-inner-shadow);
}
.ck.ck-content ul,
.ck.ck-content ul li {
  list-style-type: inherit;
}

.ck.ck-content ul {
  /* Default user agent stylesheet, you can change it to your needs. */
  padding-left: 40px;
}

.ck.ck-content ol,
.ck.ck-content ol li {
  list-style-type: decimal;
}

.ck.ck-content ol {
  /* Default user agent stylesheet, you can change it to your needs. */
  padding-left: 40px;
}

.formatted ul,
.formatted ol {
  margin-left: 2.666em;
  margin-bottom: 0.8em;
}
</style>
<style scoped>
:deep(
    .selectMemberMeeting
      .v-input__control
      .v-input__slot
      .v-select__slot
      .v-input__append-inner
  ) {
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

.btn-primary {
  background: linear-gradient(180deg, #065695 0%, #267dc2 100%);
  color: white;
}

.btn-default {
  background: linear-gradient(
    92.09deg,
    rgb(255, 255, 255) -46.47%,
    rgb(255, 255, 255) 157.9%
  );
  color: red;
}
:deep(.v-chip.v-chip--size-small) {
  --v-chip-size: 0.75rem;
  --v-chip-height: 35px;
  font-size: 0.8rem;
  padding: 0 10px;
  background: #121c5b !important;
  color: white;
}

:deep(.cursor-pointer input) {
  cursor: pointer !important;
}
:deep(.ck-editor__editable_inline) {
  min-height: 200px;
}
</style>
