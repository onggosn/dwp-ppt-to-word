<template>
  <v-dialog v-model="dialog" persistent width="1024">
    <v-card style="border-radius: 15px">
      <v-card-title>
        <v-sheet class="d-block pt-3 pr-5 text-end" style="align-self: end">
          <v-btn
            icon="mdi-close"
            color="white"
            elevation="0"
            size="small"
            @click="close()"
          ></v-btn>
        </v-sheet>
        <v-sheet class="bg-white d-block text-center mt-n9">
          List Participant</v-sheet
        >
      </v-card-title>
      <v-divider class="mt-2"></v-divider>
      <v-card-text>
        <v-container>
          <v-autocomplete
            id="focus"
            :disabled="!isOwner"
            v-model="selected_participant"
            v-model:search="search"
            :loading="loading"
            :items="items"
            item-title="inputName"
            :item-value="items"
            return-object
            variant="solo"
            append-inner-icon="mdi-magnify"
            :label="isOwner ? 'Search name' : 'You are not owner in this task'"
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="''" class="pt-5 pb-5">
                <v-row align="center" class="spacer" no-gutters>
                  <v-col class="text-center">
                    <v-avatar color="#eaeaea" size="42">
                      <v-icon
                        color="#1f75b7"
                        :icon="
                          item?.raw?.isGrup
                            ? 'mdi-account-multiple'
                            : 'mdi-account'
                        "
                      ></v-icon>
                    </v-avatar>
                  </v-col>
                  <v-col cols="8" class="text-left ms-2">
                    <p style="color: #3a416f">
                      {{ item?.raw?.inputName }}
                    </p>
                    <p class="text-12 text-grey">
                      {{ item?.raw?.inputEmail }}
                    </p>
                  </v-col>
                  <v-col class="hidden-xs-only text-center ms-2">
                    <v-icon icon="mdi-plus-circle-outline" color="#1f75b7">
                    </v-icon>
                  </v-col>
                </v-row>
              </v-list-item>
            </template>
          </v-autocomplete>
          <v-sheet class="text-grey mb-4"> Participant </v-sheet>
          <api-loader
            :apiMethod="getListMemberTask"
            ref="memberLoader"
            @loadingEnded="handleLoadingEnded"
          >
            <!-- <pre>{{ listParticipant }}</pre> -->
            <v-sheet style="height: 60vh; overflow: scroll">
              <template v-slot:default="">
                <!-- <pre>{{ listParticipant }}</pre> -->
                <template v-for="item in listParticipant" :key="item.id">
                  <v-sheet class="d-flex flex-nowrap align-self-center mt-4">
                    <v-sheet class="align-self-center" width="10%">
                      <v-avatar color="#eaeaea" size="42">
                        <v-icon
                          color="#1f75b7"
                          :icon="
                            item.user ? 'mdi-account' : 'mdi-account-multiple'
                          "
                        ></v-icon>
                      </v-avatar>
                    </v-sheet>
                    <v-sheet
                      class="align-self-center"
                      width="70%"
                      v-if="item.user"
                    >
                      {{ item.user.name }}
                      <span v-if="item.memberType == 1" style="color: #02aa59"
                        >(PIC)</span
                      >
                      <span
                        v-else-if="item.memberType == 2"
                        style="color: #02aa59"
                        >(Contributor)</span
                      >
                      <span v-else class="text-blueTheme" style="color: #02aa59"
                        >(Participant)</span
                      >
                    </v-sheet>
                    <v-sheet class="align-self-center" width="70%" v-else>
                      {{ item.groupName }}
                      <span v-if="item.memberType == 1" style="color: #02aa59"
                        >(PIC)</span
                      >
                      <span
                        v-else-if="item.memberType == 2"
                        style="color: #02aa59"
                        >(Contributor)</span
                      >
                      <span v-else class="text-blueTheme" style="color: #02aa59"
                        >(Participant)</span
                      >
                    </v-sheet>

                    <v-sheet
                      class="align-self-center mr-2"
                      style="text-align: right"
                      width="10%"
                    >
                      <v-menu location="right">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            v-if="isOwner"
                            v-bind="props"
                            color="#fff"
                            elevation="1"
                            style="
                              border-radius: 5px;
                              border: 0.5px solid #d3d3d3;
                            "
                          >
                            <v-icon icon="mdi-cog" color="#065695"></v-icon>
                          </v-btn>
                        </template>

                        <v-list>
                          <v-list-item>
                            <v-btn
                              density="default"
                              variant="text"
                              style="letter-spacing: -0.1px"
                              @click="changeStatus(item, 1)"
                              >Make as PIC</v-btn
                            >
                            <v-list-item-title></v-list-item-title>
                          </v-list-item>
                          <v-list-item>
                            <v-btn
                              density="default"
                              variant="text"
                              style="letter-spacing: -0.1px"
                              @click="changeStatus(item, 2)"
                              >Make as Contributor</v-btn
                            >
                          </v-list-item>
                          <v-list-item>
                            <v-btn
                              density="default"
                              variant="text"
                              style="letter-spacing: -0.1px"
                              @click="changeStatus(item, 3)"
                              >Make as Participant</v-btn
                            >
                          </v-list-item>
                        </v-list>
                      </v-menu>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="10%">
                      <delete-button
                        v-if="isOwner"
                        :item="item"
                        @onSuccess="refresh"
                      />
                    </v-sheet>
                  </v-sheet>
                </template>
              </template>
            </v-sheet>
            <template v-slot:loading>
              <free-style-shimmer
                v-for="i in 4"
                :key="i"
                height="5.5vh"
                width="100%"
                border-radius="5px"
                color="#DCDCDC"
                class="ml-0 mt-0 mb-4"
              />
            </template>
          </api-loader>
        </v-container>
      </v-card-text>
    </v-card>
    <v-overlay
      :model-value="isLoading"
      class="align-center justify-center"
      persistent
    >
      <v-card
        color="#065695"
        class="pl-10 pr-10 pt-0 pb-0"
        style="border-radius: 10px"
      >
        <v-card-text>
          <p class="text-white">Please stand by</p>
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0 mt-2"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-overlay>
  </v-dialog>
</template>

<script>
import ApiLoader from "./ApiLoader.vue";
import client from "@/library/ApiClient";
import DeleteButton from "@/components/workspace/DeleteParticipantDialog.vue";
export default {
  components: { ApiLoader, DeleteButton },
  data() {
    return {
      loading: false,
      search: null,
      select: null,
      dialog: false,
      selected_participant: "",
      isLoading: false,
      idTask: "",
      items: [],
      listParticipant: [],
      isOwner: false,
      isPIC: false,
    };
  },
  methods: {
    start(idTask, isOwner) {
      this.isOwner = isOwner;
      this.idTask = idTask;
      this.dialog = true;
      this.getPIC();
    },
    close() {
      this.dialog = false;
    },
    changeStatus(item, status) {
      this.isLoading = true;
      client
        .updateTaskMember({
          store: this.$store,
          data: {
            id: item.id,
            idTasks: item.idTasks,
            username: item.user == null ? "" : item.user.username,
            groupName: item.groupName,
            createdDate: item.createdDate,
            createdBy: item.createdBy,
            memberType: status,
          },
        })
        .then(() => {
          this.$root.toast.show({
            message: "User successfully changed",
            color: "success",
            timeout: 3000,
            icon: "mdi-check",
          });
          this.getPIC();
          this.$refs.memberLoader.callApi();
        });
    },
    querySelections(query) {
      if (query) {
        this.loading = true;
        client
          .SearchUserByname({
            store: this.$store,
            data: {
              name: query,
            },
          })
          .then((response) => {
            this.items = response.plainData;
            this.loading = false;
          })
          .catch(() => {
            this.loading = false;
          });
      } else {
        this.items = [];
      }
    },
    getPIC() {
      return client
        .getTasksByIdTask({
          store: this.$store,
          data: {
            id: this.idTask,
            username: this.$store.state.username,
          },
        })
        .then((response) => {
          this.isOwner = response.plainData[0].isOwner;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getListMemberTask() {
      return client.getListTaskMemberDataByIdTask({
        store: this.$store,
        data: {
          id: this.idTask,
        },
      });
    },
    handleLoadingEnded({ success, response }) {
      if (success) {
        this.listParticipant = response.plainData;
      }
    },
    refresh() {
      this.$refs.memberLoader.callApi();
    },
  },
  watch: {
    search(val) {
      val && val !== this.select && this.querySelections(val);
    },
    selected_participant(val) {
      if (val) {
        this.isLoading = true;
        client
          .insertTaskMember({
            store: this.$store,
            data: {
              idTasks: this.idTask,
              username: val.isGrup ? "" : val.inputId,
              groupName: val.isGrup ? val.inputId : "",
              createdDate: new Date(
                new Date().toISOString().slice(0, 10) + "T00:00:00"
              ),
              createdBy: this.$store.state.username,
              memberType: 2,
            },
          })
          .then((response) => {
            this.$root.toast.show({
              message: response.plainData.responseMessage,
              color:
                response.plainData.responseCode == "011024"
                  ? "warning"
                  : "success",
              timeout: 3000,
              icon: "mdi-check",
            });
            this.selected_participant = "";
            this.$refs.memberLoader.callApi();
          })
          .catch(() => {
            this.$root.toast.show({
              message: "Something went wrong",
              color: "error",
              timeout: 3000,
              icon: "mdi-check",
            });
          })
          .finally(() => {
            this.isLoading = false;
            document.getElementById("focus").blur();
          });
      }
    },
  },
};
</script>

<style scoped>
.buttonSave {
  background: linear-gradient(180deg, #065695, #267dc2);
  font-size: 12px;
  font-weight: 900;
  text-align: center;
}
:deep(.v-autocomplete .v-field .v-field__append-inner > .v-icon) {
  transform: none;
}
</style>
