<template>
  <v-row>
    <v-col cols="12" class="pl-6">
      <h5 class="fw-600 text-18 ls-1 text-blackTheme pt-2 mobile-font-2">
        Document In Progress
      </h5>
      <api-loader :apiMethod="getDocumentLatest" :hasOverlay="false">
        <template v-slot:default="props">
          <p class="text-blackTheme fw-400 text-13 ls-1 mt-2">
            See documents that currently in progress
          </p>
          <div v-if="!props.response.plainData.length">
            <span class="text-18 fw-600 text-grayTheme-gradien font-italic">
              No Data Available...
            </span>
          </div>
          <template v-else>
            <div v-for="(item, index) in props.response.plainData" :key="index">
              <HomeListDocument :item="item"></HomeListDocument>
            </div>
          </template>
        </template>
        <template v-slot:loading>
          <free-style-shimmer
            height="20px"
            width="300px"
            border-radius="10px"
            color="#DCDCDC"
            class="ml-2 mt-2 mb-4"
          />
          <free-style-shimmer
            v-for="n in 3"
            :key="n"
            width="93%"
            height="60px"
            border-radius="10px"
            color="#DCDCDC"
            class="ml-2 mt-2"
          />
        </template>
      </api-loader>
    </v-col>
  </v-row>
</template>
<script>
import client from "@/library/ApiClient";
import ApiLoader from "@/components/ApiLoader.vue";
import HomeListDocument from "@/components/home/HomeListDocument.vue";

export default {
  components: {
    ApiLoader,
    HomeListDocument,
  },
  data() {
    return {};
  },
  mounted() {
    undefined;
  },
  methods: {
    getDocumentLatest() {
      let result = client.GetListDocumentAsApprovalByUsername({
        store: this.$store,
        data: {
          username: this.$store.state.username,
        },
      });
      return result;
    },
  },
};
</script>
<style scoped></style>
