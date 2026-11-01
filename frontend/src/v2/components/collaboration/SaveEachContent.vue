<template>
  <v-btn
    variant="outlined"
    rounded
    color="#065695"
    class="mr-2"
    size="small"
    @click="handleSaveContent"
    >Save
    <template #prepend>
      <v-icon>mdi-content-save</v-icon>
    </template>
  </v-btn>
</template>

<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from "vue";
import { useStore } from "vuex";
import { responsePromise } from "@v2/helpers/utils";
const store = useStore();
const { root } = getCurrentInstance() as any;
const response = responsePromise(root);

const props = defineProps<{
  idFormEditor: string;
}>();

function handleSaveContent() {
  store
    .dispatch("eFormStore/saveEachContentEForm", props)
    .then(() => {
      root.refs.toast.show({
        message: "Successfully Saved",
        color: "success",
        timeout: 3000,
      });
    })
    .catch(response.error);
}
</script>

<style scoped></style>
