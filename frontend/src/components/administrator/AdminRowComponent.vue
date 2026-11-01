<template>
  <v-expansion-panels v-model="panel" class="pr-1 pt-1">
    <v-expansion-panel
      :value="item.id"
      class="panel-expansion mb-5"
      :key="item.id"
      :style="[
        getTypeBoolean('default')
          ? {
              'border-left': '5px solid rgb(6, 86, 149)',
              'border-bottom-left-radius': '15px',
            }
          : {},
      ]"
    >
      <v-expansion-panel-title
        class="panel-header"
        :class="getTypeBoolean('type-1') ? 'primary-gradient' : ''"
      >
        <template v-slot:actions="{ expanded }">
          <v-icon
            :icon="
              expanded
                ? 'mdi-chevron-up-circle-outline'
                : 'mdi-chevron-down-circle-outline'
            "
            color="rgb(38 105 158 / 80%)"
          ></v-icon>
        </template>
        <v-row class="pr-3" align="center" justify="space-between">
          <v-col>
            <h6
              class="fw-600 text-14 py-2 pl-3"
              :style="[getTypeBoolean('default') ? { color: '#3a416f' } : {}]"
            >
              {{
                item.name.length > 150
                  ? item.name.substring(0, 150) + "..."
                  : item.name
              }}
            </h6>
          </v-col>
        </v-row>
      </v-expansion-panel-title>
      <v-expansion-panel-text
        class="panel-content"
        :style="[
          !getTypeBoolean('default')
            ? { 'border-left': '5px solid rgb(6, 86, 149)' }
            : {},
        ]"
      >
        <slot />
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  name: "dashboardRowComponent",
  props: {
    item: {
      type: Object,
      default: function () {
        return {};
      },
    },
    type: {
      type: String,
      default: "default",
    },
  },
  created() {
    this.getPanelSelected();
  },
  data() {
    return {
      panel: [],
    };
  },
  methods: {
    getColor(statusId) {
      let colorStatus = {
        1: "danger",
        2: "warning",
        3: "success",
        8: "warning",
        9: "danger",
        10: "warning",
        11: "success",
        12: "danger",
        13: "danger",
        16: "warning",
        17: "success",
      };
      return colorStatus[statusId] ?? "danger";
    },
    getTypeBoolean(type) {
      return this.type == type;
    },
    getPanelSelected() {
      const paramId =
        typeof this.$route.params.id === "undefined"
          ? ""
          : this.$route.params.id;
      return this.panel.push(paramId);
    },
  },
};
</script>

<style scoped>
:deep(.v-expansion-panel__shadow) {
  box-shadow: 0px 4px 18px 0px rgba(192, 192, 192, 0.25) !important;
}
.panel-expansion {
  margin-bottom: 20px;
  border-radius: 15px !important;
  background: #fff;
}

.panel-expansion .panel-header {
  border-radius: 15px;
  background-color: #fff;
}

.panel-expansion .panel-content {
  /* border-top: 1px solid #eeeeee !important; */
  padding-bottom: 15px;
  /* background-color: #fff; */
  border-bottom-left-radius: 15px;
}

.border-icon-expansion-default {
  display: inline-block;
  border-radius: 100px;
  box-shadow: 0 0 0 1px #065695;
}

.border-icon-expansion-n-default {
  display: inline-block;
  border-radius: 100px;
  background: #fff;
  color: #065695;
  box-shadow: 0 0 0 1px #065695;
}

.label-status {
  margin-right: 20px;
  border-radius: 10px;
  color: white !important;
  letter-spacing: -0.7px;
  font-weight: 900;
  height: 30px !important;
  font-size: 13px;
  width: 130px;
}

.btn-danger {
  background: linear-gradient(180deg, #d6212a 0%, #ff000d 100%) !important;
}
.btn-success {
  background: linear-gradient(180deg, #00783e 0%, #02aa59 100%) !important;
}
.btn-warning {
  background: linear-gradient(
    179.16deg,
    #e2650b 0.79%,
    #fe7411 99.34%
  ) !important;
}

:deep(.v-expansion-panel-title__overlay) {
  background-color: #fff;
  border-bottom: 1px solid !important;
}
:deep(.v-expansion-panel-title__icon) {
  margin-left: 2vh;
}

:deep(.v-expansion-panel--active > .v-expansion-panel-title) {
  border-bottom-left-radius: 0px !important;
  border-bottom-right-radius: 0px !important;
}

/* :deep(.v-expansion-panel-title.panel-header) {
  align-items: flex-start;
} */
</style>
