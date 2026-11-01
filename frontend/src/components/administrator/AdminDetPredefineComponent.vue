<template>
  <template v-if="isLoading">
    <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
  </template>
  <v-row v-else class="mx-2">
    <v-col cols="12" class="mt-2">
      <v-row>
        <v-col cols="12" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Workspace Type</div>
          <div class="text-black-theme text-13">
            {{ item.workspaceTypeName ?? "-" }}
          </div>
        </v-col>
        <v-col cols="12" class="px-0">
          <div class="text-grey-theme fw-600 text-13">Nama</div>
          <div class="text-black-theme text-13">
            {{ item.name ?? "-" }}
          </div>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
  <template v-if="tag == 'predefine'">
    <hr style="margin-top: 40px" class="dotted" />
    <div class="mt-4" v-if="isLoading">
      <paragraph-shimmer :is-loading="true" :lines="4" :random-size="true" />
    </div>
    <div class="mx-2 mb-1">
      <v-row class="mt-2">
        <v-col cols="12">
          <div class="text-gradient-blue text-15">List Activity & Task</div>
        </v-col>
      </v-row>
      <template v-if="listItem.activityViewLists.length">
        <v-tabs v-model="tab">
          <div
            v-for="itemActivity in listItem.activityViewLists"
            :key="itemActivity.id"
          >
            <v-tab :value="itemActivity.activityName" class="tab-header">
              <p class="pt-4">
                {{ itemActivity.activityName.toUpperCase() }}
              </p>
            </v-tab>
          </div>
        </v-tabs>
        <v-window v-model="tab" class="mt-2">
          <v-window-item
            v-for="itemActivity in listItem.activityViewLists"
            :key="itemActivity.idActivityTemplate"
            :value="itemActivity.activityName"
          >
            <v-row>
              <v-col cols="12">
                <v-table style="width: 100%">
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-center label-header" width="5%">No</th>
                        <th width="30%" class="text-center label-header">
                          Task
                        </th>
                        <th width="40%" class="text-center label-header">
                          Description
                        </th>
                        <th width="15%" class="text-center label-header">
                          Participant
                        </th>
                        <th class="text-center" width="10%"></th>
                      </tr>
                    </thead>
                    <tbody>
                      <!-- Start Pengulanan untuk render task -->
                      <tr
                        class="text-13"
                        v-for="(itemTab, i) in itemActivity.taskWithMemberViews"
                        :key="itemTab.id"
                      >
                        <td width="5%" class="text-center">{{ i + 1 }}</td>
                        <td width="30%" class="text-11">
                          {{ itemTab.taskName }}
                        </td>
                        <td width="40%" class="text-11">
                          {{ itemTab.descriptions }}
                        </td>
                        <td width="20%" class="text-11">
                          <span class="ellipsis"
                            >{{ getParticipant(itemTab.members) }}
                            <v-tooltip activator="parent" location="top">{{
                              getParticipant(itemTab.members)
                            }}</v-tooltip></span
                          >
                        </td>
                        <td width="5%">
                          <v-btn
                            variant="outlined"
                            color="#1976d2"
                            class="btn-outline-rounded"
                            size="small"
                            @click="edit(itemTab)"
                            >Edit</v-btn
                          >
                        </td>
                      </tr>
                      <!-- End Pengulanan untuk render task -->
                    </tbody>
                  </template>
                </v-table>
              </v-col>
            </v-row>
          </v-window-item>
        </v-window>
      </template>
      <template v-else>
        <div class="text-black-theme text-13 mt-2">Data masih kosong</div>
      </template>
    </div>
  </template>

  <edit-workspace-dialog ref="modal_edit_workspace" @submit="reloadPage" />
</template>

<script>
import client from "@/library/ApiClient";
import EditWorkspaceDialog from "@/components/administrator/EditWorkspacePredefineDialog.vue";
import { capitalize } from "@/helpers/utils";

export default {
  name: "adminDetWorkspacePredefine",
  emits: ["reloadPage"],
  props: {
    item: {
      type: Object,
      default: function () {
        return {};
      },
    },
    tag: {
      type: String,
      default: "predefine",
    },
  },
  components: {
    EditWorkspaceDialog,
  },
  data() {
    return {
      tab: null,
      isLoading: false,
      listItem: {
        activityViewLists: [],
      },
    };
  },
  methods: {
    getDetailWorkspace() {
      // debugger;
      this.isLoading = true;
      client
        .getDetailListWorkspacePredefined({
          store: this.$store,
          data: {
            username: this.$store.state.username,
            idWorkspaceType: this.item.id,
          },
        })
        .then((result) => {
          let plainData = result.plainData;
          this.listItem = plainData;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    getParticipant(members) {
      let result = "";
      let participant = [];
      if (members) {
        members.map((el) => {
          participant.push(
            el.groupName != ""
              ? el.groupName
              : el.name != null
              ? this.stringToCapitalize(el.name.toLowerCase())
              : ""
          );
        });
        result = participant.join(", ");
      }
      return result;
    },
    stringToCapitalize(text) {
      return capitalize(text);
    },
    edit(item) {
      this.$refs.modal_edit_workspace.show(item);
    },
    reloadPage() {
      this.$emit("reloadPage");
    },
  },
  created() {
    if (this.tag == "predefine") {
      this.getDetailWorkspace();
    } else {
      this.isLoading = false;
    }
  },
};
</script>

<style scoped>
.text-danger {
  background: -webkit-linear-gradient(90.85deg, #d6212a 15.38%, #ff000d 81.89%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-waring {
  background: -webkit-linear-gradient(90.05deg, #c45b10 0.05%, #fe7411 99.96%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-success {
  background: -webkit-linear-gradient(180deg, #00783e 0%, #02aa59 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.text-grey-theme {
  color: #a6abc7;
}
.text-black-theme {
  color: #4b4b4b;
}

.text-gradient-blue {
  background: -webkit-linear-gradient(#065695, #267dc2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
  font-size: 15px;
}

.btn-outline-rounded {
  border-radius: 10px;
  letter-spacing: -0.5px;
}
.dotted {
  border: 2px dashed #065695;
  border-style: none none dashed;
  color: #fff;
  background-color: #fff;
}
:deep(.tab-header.v-slide-group-item--active) {
  color: #065695 !important;
  background: transparent;
  border: 0px;
  border-radius: 0px;
  border-bottom: 1.2px solid;
}

.bg-blue {
  background: -webkit-linear-gradient(#065695, #267dc2);
}
.label-header {
  color: #3a416f !important;
  font-size: 12px;
  font-weight: 600 !important;
}
.ellipsis {
  white-space: pre-wrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.btn-outline-rounded {
  border-radius: 10px;
  letter-spacing: -0.5px;
  width: auto;
}
</style>
