<template>
  <div class="d-flex flex-row px-2 mr-4 gradient-box">
    <v-btn @click="$emit('click')">
      <img src="/images/createWorkspace2.svg" />
      <span
        class="text-blueRedTheme-gradien ml-3"
        style="font-size: 14px; font-weight: 600"
      >
        {{ label }}
      </span>
    </v-btn>
  </div>
</template>

<script>
export default {
  props: ["label"],
};
</script>
<style lang="scss" scoped>
.gradient-box {
  display: flex;
  align-items: center;
  margin: auto;

  position: relative;
  box-sizing: border-box;

  $border: 2px;
  background: #fff;
  background-clip: padding-box; /* !important */
  border: solid $border transparent; /* !important */
  border-radius: 15px;

  &:before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: -1;
    margin: -$border; /* !important */
    border-radius: inherit; /* !important */
    background: linear-gradient(to right, #267dc2, #ff000d);
  }
}

.text-blueRedTheme-gradien {
  background: -webkit-linear-gradient(left, #267dc2, #ff000d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
