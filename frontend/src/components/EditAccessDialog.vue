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
          Edit Access</v-sheet
        >
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-sheet>
            <api-loader
              :apiMethod="getMemberTask"
              @loadingEnded="handleLoadingEnded"
            >
              <template v-slot:default="">
                <!-- <pre> {{ props.response.plainData }}</pre> -->
                <v-autocomplete
                  v-model="selected_newAccess"
                  clearable
                  label="Enter name"
                  placeholder="Enter name"
                  :items="items"
                  item-title="user.name"
                  item-value="user"
                  variant="solo"
                >
                  <template v-slot:item="{ props, item }">
                    <!-- <pre>{{ item }}</pre> -->
                    <v-list-item
                      v-bind="props"
                      :title="item?.raw?.name"
                      class="pt-5 pb-5"
                    >
                      <v-row align="center" class="spacer" no-gutters>
                        <v-col class="text-center">
                          <v-avatar color="#eaeaea" size="42">
                            <v-icon
                              color="#1f75b7"
                              :icon="
                                item?.raw?.user.email == 'Group'
                                  ? 'mdi-account-multiple'
                                  : 'mdi-account'
                              "
                            ></v-icon>
                          </v-avatar>
                        </v-col>

                        <v-col cols="8" class="text-left ms-2">
                          <p style="color: #3a416f">
                            {{ item?.raw?.user.name }}
                            <!-- {{ item.title }} -->
                          </p>
                          <p class="text-12 text-grey">
                            {{
                              item?.raw?.user.email == "Group"
                                ? "Group"
                                : item?.raw?.user.username + "@bi.go.id"
                            }}
                          </p>
                        </v-col>
                        <v-col class="hidden-xs-only text-center ms-2">
                          <v-icon
                            icon="mdi-plus-circle-outline"
                            color="#1f75b7"
                          >
                          </v-icon>
                        </v-col>
                      </v-row>
                    </v-list-item>
                  </template>
                </v-autocomplete>
              </template>
              <template v-slot:loading>
                <free-style-shimmer
                  height="5.5vh"
                  width="100%"
                  border-radius="5px"
                  color="#DCDCDC"
                  class="ml-0 mt-0 mb-4"
                />
              </template>
            </api-loader>
          </v-sheet>
          <v-sheet class="text-grey mb-4"> Participant </v-sheet>
          <v-sheet
            class="mb-4 d-flex flex-row-reverse flex-wrap"
            style="text-align-last: end; letter-spacing: -1px"
          >
            <div
              class="mb-4 d-flex flex-row-reverse flex-wrap"
              v-html="historyChip"
            />
          </v-sheet>

          <api-loader
            :apiMethod="getListAccessMember"
            ref="memberLoader"
            @loadingEnded="handleLoadingEndedAccess"
          >
            <v-sheet style="height: 40vh; overflow: scroll">
              <template v-slot:default="">
                <v-sheet class="d-flex flex-nowrap align-self-center mt-4">
                  <v-sheet class="align-self-center" width="52%"> </v-sheet>
                  <v-sheet class="align-self-center" width="18%">
                    <v-checkbox
                      v-model="allView"
                      @click="selectAllView()"
                      :label="!allView ? 'Select All' : 'Unselect All'"
                      color="success"
                      hide-details
                    ></v-checkbox
                  ></v-sheet>

                  <v-sheet class="align-self-center" width="20%">
                    <v-checkbox
                      :disabled="!allView"
                      :indeterminate="!allView"
                      v-model="allDownload"
                      @click="selectAllDownload()"
                      :label="!allDownload ? 'Select All' : 'Unselect All'"
                      color="success"
                      hide-details
                    ></v-checkbox>
                  </v-sheet>
                  <v-sheet class="align-self-center" width="10%"> </v-sheet>
                </v-sheet>
                <template v-for="item in listAccessMembers" :key="item.id">
                  <v-sheet class="d-flex flex-nowrap align-self-center mt-4">
                    <v-sheet class="align-self-center" width="7%">
                      <v-avatar color="#eaeaea" size="42">
                        <v-icon
                          color="#1f75b7"
                          :icon="
                            item.isGroup
                              ? 'mdi-account-multiple'
                              : 'mdi-account'
                          "
                        ></v-icon>
                      </v-avatar>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="23%">
                      <p>{{ item.fullName }}</p>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="10%">
                      <v-checkbox
                        :disabled="!item.isRead"
                        :indeterminate="!item.isRead"
                        :model-value="item.isEdit"
                        label="Edit"
                        color="success"
                        hide-details
                        @click="isEditClick(item)"
                      ></v-checkbox>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="12%">
                      <v-checkbox
                        :disabled="!item.isRead"
                        :indeterminate="!item.isRead"
                        :model-value="item.isDeleteDoc"
                        label="Delete"
                        color="success"
                        hide-details
                        @click="isDeleteClick(item)"
                      ></v-checkbox>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="18%">
                      <v-checkbox
                        :model-value="item.isRead"
                        label="View"
                        color="success"
                        hide-details
                        @click="isReadClick(item)"
                      ></v-checkbox>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="20%">
                      <v-checkbox
                        :disabled="!item.isRead"
                        :indeterminate="!item.isRead"
                        :model-value="item.isDownload"
                        label="Download"
                        color="success"
                        hide-details
                        @click="isDownloadClick(item)"
                      ></v-checkbox>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="10%">
                      <v-btn
                        variant="flat"
                        color="white"
                        elevation="2"
                        style="border-radius: 8px"
                        @click="deleteAccess(item)"
                      >
                        <v-icon color="#1f75b7">mdi-trash-can</v-icon>
                      </v-btn>
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
      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn
          color="white"
          elevation="3"
          class="rounded-lg mr-10 mb-4 buttonSave float-right"
          @click="saveAllChanges()"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-overlay
      :model-value="isLoading"
      class="align-center justify-center"
      persistent
    >
      <v-card
        color="#065695"
        class="pl-0 pr-0 pt-0 pb-0"
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
export default {
  components: { ApiLoader },
  props: {
    documentType: String,
  },
  data() {
    return {
      dialog: false,
      isLoading: false,
      title: "",
      message: "",
      documentId: "",
      documentName: "",
      isSendDocument: false,
      items: [],
      idTask: "",
      listAccessMembersIfDiscard: [],
      listAccessMembers: [],
      selected_newAccess: "",
      historyChip: "",
      cb_items: [],
      allView: false,
      allDownload: false,
    };
  },
  methods: {
    start(documentName, documentId) {
      document.getElementById("DetailTaskDialog").style.visibility = "hidden";
      this.documentName = documentName;
      this.documentId = documentId;
      this.dialog = true;
    },
    close() {
      document.getElementById("DetailTaskDialog").style.visibility = "visible";
      this.listAccessMembers = this.listAccessMembersIfDiscard;
      this.allView = false;
      this.allDownload = false;
      this.historyChip = "";
      this.dialog = false;
      this.$emit("reload");
    },
    deleteDoc() {
      this.dialog = false;
      this.$emit("deleteDoc", this.id);
    },
    getMemberTask() {
      return client.getListTaskMemberDataByIdTask({
        store: this.$store,
        data: {
          id: this.$route.params.taskId,
        },
      });
    },
    handleLoadingEnded({ success, response }) {
      if (success) {
        response.plainData.forEach((element) => {
          if (!element.user) {
            let temp = { name: element.groupName, email: "Group" };
            element.user = temp;
          }
          this.items.push(element);
        });
      }
    },
    getListAccessMember() {
      if (this.documentType == "pendukung") {
        return client.GetListAcessMemberDocumentSupportByIdDocument({
          store: this.$store,
          data: {
            id: this.documentId,
          },
        });
      } else {
        return client.GetListAcessMemberByIdDocument({
          store: this.$store,
          data: {
            id: this.documentId,
          },
        });
      }
    },
    handleLoadingEndedAccess({ success, response }) {
      if (success) {
        this.listAccessMembers = response.plainData;
        this.listAccessMembersIfDiscard = response.plainData;
      }
    },
    selectAllView() {
      this.allView = !this.allView;
      this.listAccessMembers.forEach((element) => {
        element.isRead = this.allView;
        if (this.allView == false) {
          element.isEdit = false;
          element.isDownload = false;
          element.isDeleteDoc = false;
          this.allDownload = false;
        }
      });
    },
    selectAllDownload() {
      this.allDownload = !this.allDownload;
      this.listAccessMembers.forEach((element) => {
        element.isDownload = this.allDownload;
      });
    },
    deleteAccess(item) {
      let index = -1;
      if (!item.isGroup) {
        index = this.listAccessMembers.findIndex(
          (x) => x.username === item.username
        );
      } else {
        index = this.listAccessMembers.findIndex(
          (x) => x.groupName === item.groupName
        );
      }
      this.listAccessMembers.splice(index, 1);
      this.historyChip +=
        '<div style="margin: 3px; background: #f6e3e5;align-self: center;border-radius: 25px;  padding: 3px 20px 3px 20px;  color: #b2142e;font-size: 14px;text-transform: lowecase"> ' +
        item.fullName +
        " deleted</div>";
    },
    saveAllChanges() {
      this.isLoading = true;
      if (this.$route.name == "support") {
        client
          .updateListTaskDocumentSupportAccess({
            store: this.$store,
            data: this.listAccessMembers,
          })
          .then(() => {
            this.$root.toast.show({
              message: "Successfully Changed",
              color: "success",
              timeout: 3000,
              icon: "mdi-check",
            });
            this.$refs.memberLoader.callApi();
            this.loading = false;
          })
          .catch(() => {
            this.$root.toast.show({
              message: "error",
              color: "error",
              timeout: 3000,
              icon: "mdi-check",
            });
            this.loading = false;
          })
          .finally(() => {
            this.historyChip = "";
            this.isLoading = false;
          });
      } else {
        client
          .updateListTaskDocumentAccess({
            store: this.$store,
            data: this.listAccessMembers,
          })
          .then(() => {
            this.$root.toast.show({
              message: "Successfully Changed",
              color: "success",
              timeout: 3000,
              icon: "mdi-check",
            });
            this.$refs.memberLoader.callApi();
            this.loading = false;
          })
          .catch(() => {
            this.$root.toast.show({
              message: "error",
              color: "error",
              timeout: 3000,
              icon: "mdi-check",
            });
            this.loading = false;
          })
          .finally(() => {
            this.historyChip = "";
            this.isLoading = false;
          });
      }
    },
    isReadClick(item) {
      let index = -1;
      if (item.isGroup) {
        index = this.listAccessMembers.findIndex(
          (x) => x.groupName === item.groupName
        );
      } else {
        index = this.listAccessMembers.findIndex(
          (x) => x.username === item.username
        );
      }

      this.listAccessMembers[index].isRead = !item.isRead;
      this.listAccessMembers[index].isDeleteDoc = false;
      this.listAccessMembers[index].isDownload = false;
      this.listAccessMembers[index].isEdit = false;
    },
    isDownloadClick(item) {
      let index = -1;
      if (item.isGroup) {
        index = this.listAccessMembers.findIndex(
          (x) => x.groupName === item.groupName
        );
      } else {
        index = this.listAccessMembers.findIndex(
          (x) => x.username === item.username
        );
      }
      this.listAccessMembers[index].isDownload = !item.isDownload;
    },
    isEditClick(item) {
      let index = -1;
      if (item.isGroup) {
        index = this.listAccessMembers.findIndex(
          (x) => x.groupName === item.groupName
        );
      } else {
        index = this.listAccessMembers.findIndex(
          (x) => x.username === item.username
        );
      }
      this.listAccessMembers[index].isEdit = !item.isEdit;
    },
    isDeleteClick(item) {
      let index = -1;
      if (item.isGroup) {
        index = this.listAccessMembers.findIndex(
          (x) => x.groupName === item.groupName
        );
      } else {
        index = this.listAccessMembers.findIndex(
          (x) => x.username === item.username
        );
      }
      this.listAccessMembers[index].isDeleteDoc = !item.isDeleteDoc;
    },
  },
  watch: {
    selected_newAccess: function (value) {
      // debugger;
      let index = -1;
      if (value !== null) {
        if (value.email == "Group") {
          index = this.listAccessMembers.findIndex(
            (x) => x.groupName === value.name
          );
        } else {
          index = this.listAccessMembers.findIndex(
            (x) => x.username === value.username
          );
        }

        if (index == -1) {
          this.historyChip +=
            '<div style="margin: 3px; background: #eaf5ea;align-self: center;border-radius: 25px;  padding: 3px 20px 3px 20px;  color: #58b35e;font-size: 14px;"> ' +
            value.name +
            " added</div>";
          if (value.email == "Group") {
            this.listAccessMembers.unshift({
              TaskDocumentId: this.documentId,
              fullName: value.name,
              username: "",
              groupName: value.name,
              isRead: false,
              isEdit: false,
              isDownload: false,
              isDeleteDoc: false,
              createdDate: new Date(
                new Date().toISOString().slice(0, 10) + "T00:00:00"
              ),
              createdBy: this.$store.state.username,
              isGroup: true,
            });
          } else {
            if (this.$route.name == "support") {
              this.listAccessMembers.unshift({
                TaskDocumentSupportId: this.documentId,
                fullName: value.name,
                username: value.username,
                groupName: "",
                isRead: true,
                isEdit: false,
                isDownload: false,
                isDeleteDoc: false,
                createdDate: new Date(
                  new Date().toISOString().slice(0, 10) + "T00:00:00"
                ),
                createdBy: this.$store.state.username,
                isGroup: false,
              });
            } else {
              this.listAccessMembers.unshift({
                TaskDocumentId: this.documentId,
                fullName: value.name,
                username: value.username,
                groupName: "",
                isRead: true,
                isEdit: false,
                isDownload: false,
                isDeleteDoc: false,
                createdDate: new Date(
                  new Date().toISOString().slice(0, 10) + "T00:00:00"
                ),
                createdBy: this.$store.state.username,
                isGroup: false,
              });
            }
          }
        } else {
          alert("User sudah terdaftar");
        }
        this.selected_newAccess = null;
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
::-webkit-scrollbar {
  width: 5px;
}
</style>
