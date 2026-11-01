<template>
  <v-dialog v-model="dialog" persistent width="768">
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
      <v-divider class="mt-2"></v-divider>
      <v-card-text>
        <v-container>
          <v-autocomplete
            label="Enter a name"
            v-model:search="search"
            @update:modelValue="insertParticipant"
            :items="items"
            item-title="inputName"
            item-value="inputId"
            variant="solo"
            return-object
            append-inner-icon="mdi-magnify"
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
            :apiMethod="getListMemberAssignment"
            ref="memberLoader"
            @loadingEnded="handleLoadingEnded"
          >
            <v-sheet style="height: 60vh; overflow: scroll">
              <template v-slot:default="">
                <template v-for="item in listParticipant" :key="item.id">
                  <v-sheet class="d-flex flex-nowrap align-self-center mt-4">
                    <v-sheet class="align-self-center" width="10%">
                      <v-avatar color="#eaeaea" size="42">
                        <span class="text-h7">{{
                          initialName(item.name)
                        }}</span>
                      </v-avatar>
                    </v-sheet>
                    <v-sheet class="align-self-center" width="70%">
                      {{ item.name }}
                      <span v-if="item.memberType == 2" style="color: #02aa59"
                        >(Contributor)</span
                      >
                      <span v-else class="text-blueTheme" style="color: #02aa59"
                        >(Participant)</span
                      >
                      <div
                        class="text-grey-theme fw-500 text-15"
                        style="color: #a6abc7"
                      >
                        {{ item.email }}
                      </div>
                    </v-sheet>

                    <v-sheet
                      class="align-self-center mr-2"
                      style="text-align: right"
                      width="10%"
                    >
                      <v-menu
                        location="right"
                        transition="slide-y-transition"
                        bottom
                      >
                        <template v-slot:activator="{ props }">
                          <v-btn
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
                      <!-- <delete-button :item="item" @onSuccess="refresh" /> -->
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
  <modal-confirm-component
    :formConfirm="formConfirm"
    ref="modal_confirm"
    @action-confirm="deleteAssignmentMemberByUserName"
  />
</template>

<script>
import client from "@/library/ApiClient";
import ApiLoader from "../ApiLoader.vue";
import { initialName } from "@/helpers/utils";
// import DeleteButton from "@/components/assignment/DeleteAssignmentMember.vue";
import ModalConfirmComponent from "../utils/ModalConfirmComponent.vue";

export default {
  name: "editAccessAssignmentDialog",
  emits: ["closeModal"],
  components: { ApiLoader, ModalConfirmComponent },
  data() {
    return {
      loading: false,
      search: null,
      select: null,
      dialog: false,
      selected_participant: "",
      isLoading: false,
      idAssignment: "",
      items: [],
      listParticipant: [],
      isOwner: false,
      formConfirm: {},
      formData: {
        idAssignmentType: null,
      },
    };
  },
  methods: {
    initialName: initialName,
    show(idAssignment) {
      this.idAssignment = idAssignment;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.$emit("closeModal");
    },
    changeStatus(item, status) {
      this.isLoading = true;
      client
        .editAssignmentMemberByUserName({
          store: this.$store,
          data: {
            idAssignment: this.idAssignment,
            id: item.id,
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
          this.$refs.memberLoader.callApi();
        })
        .finally(() => {
          this.isLoading = false;
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
    deleteAssignmentMemberByUserName(item) {
      let requestData = {
        idAssignment: this.idAssignment,
        // username: item.username,
        id: item.id,
      };
      client
        .deleteAssignmentMemberByUserName({
          store: this.$store,
          data: requestData,
        })
        .then(() => {
          this.$refs.memberLoader.callApi();
          this.$refs.modal_confirm.hide();
          this.$root.toast.show({
            message: "User successfully deleted",
            color: "success",
            timeout: 3000,
            icon: "mdi-check",
          });
        });
    },
    deleteAccess(item) {
      this.formConfirm = {
        title: "Delete Access",
        width: 500,
        btnSubmitLabel: "Delete",
        icon: {},
        message: `<div class="text-center">Are you sure delete this participant ?</div>`,
      };
      this.$refs.modal_confirm.start(item, 0);
    },
    getListMemberAssignment() {
      return client.getListAssignmentMemberByIdAssignment({
        store: this.$store,
        data: {
          idAssignment: this.idAssignment,
        },
      });
    },
    handleLoadingEnded({ success, response }) {
      if (success) {
        this.listParticipant = response.plainData.responseData;
      }
    },
    refresh() {
      this.$refs.memberLoader.callApi();
    },
    alreadyExist(val) {
      let index = this.listParticipant.findIndex(
        (x) => x.username === val.inputId
      );
      if (index == -1) {
        return false;
      } else {
        return true;
      }
    },
    insertParticipant(item) {
      if (item) {
        if (!this.alreadyExist(item)) {
          this.isLoading = true;
          let requestData = {
            idAssignment: this.idAssignment,
            username: item.isGrup ? "" : item.inputId,
            groupName: item.isGrup ? item.inputId : "",
            memberType: 3,
          };
          client
            .insertListAssignmentMember({
              store: this.$store,
              data: requestData,
            })
            .then(() => {
              this.$root.toast.show({
                message: "User successfully added",
                color: "success",
                timeout: 3000,
                icon: "mdi-check",
              });
              this.selected_participant = null;
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
              this.search = null;
            });
        } else {
          alert("This participant is already on this assignment");
          this.selected_participant = null;
        }
      }
    },
  },
  watch: {
    search(val) {
      val && val !== this.select && this.querySelections(val);
    },
  },
};
</script>

<style scoped>
.overflowyhid {
  overflow-y: hidden;
  padding-bottom: 5px;
}

.buttonSave {
  background: linear-gradient(180deg, #065695, #267dc2);
  font-size: 12px;
  font-weight: 900;
  text-align: center;
}

.select-empty {
  cursor: pointer;
}
</style>
