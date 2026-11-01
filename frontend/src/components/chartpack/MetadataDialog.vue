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
          <div class="text-h6">Detail Chartpack</div>
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
          <v-container no-gutters class="container">
            <v-row>
              <v-col>
                <div class="text-grey fw-600 text-15">Nama Chartpack</div>
                <div class="fw-600 text-17">{{ item.documentTitle }}</div>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <div class="text-grey fw-400 text-15">Area</div>
                <div class="fw-400 text-14">{{ item.area }}</div>
              </v-col>
              <v-col>
                <div class="text-grey fw-400 text-15">Sektor</div>
                <div class="fw-400 text-14">{{ item.sektor }}</div>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <div class="text-grey fw-400 text-15">Periode</div>
                <div class="fw-400 text-14">{{ item.periode }}</div>
              </v-col>
              <v-col>
                <div class="text-grey fw-400 text-15">Created</div>
                <div class="fw-400 text-14">
                  {{ $filters.formatTimeEngToIndNoDays(item.createdDate) }}
                  {{ $filters.formatTimeAmPm(item.createdDate) }}
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <div class="text-grey fw-400 text-15">Last Update</div>
                <div class="fw-400 text-14">
                  {{ $filters.formatTimeEngToIndNoDays(item.lastModifiedDate) }}
                  {{ $filters.formatTimeAmPm(item.lastModifiedDate) }}
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <div class="text-grey fw-400 text-15">Keyword</div>
                <div class="fw-400 text-14">{{ item.keyword }}</div>
              </v-col>
            </v-row>
          </v-container>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script>
import { defineComponent } from "vue";

export default defineComponent({
  components: {},
  data() {
    return {
      showDialog: false,
      loading: false,
    };
  },
  props: {
    item: Object,
  },
  mounted() {
    // this.checkOwner();
  },
  methods: {
    start() {
      this.showDialog = true;
    },
    close() {
      this.showDialog = false;
      // this.$store.state.isDetailTaskShow = true;
    },
  },
});
</script>
<style scoped>
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

.btn {
  width: 15vw;
  color: white;
}

.text-grey {
  color: #a6abc7;
}
</style>
