<template>
  <free-style-shimmer
    :is-loading="true"
    height="60px"
    width="60px"
    border-radius="100px"
    color="#DCDCDC"
    class="ml-2 mt-2 pb-5"
  />
  <free-style-shimmer
    :is-loading="true"
    height="30px"
    width="70vw"
    border-radius="10px"
    color="#DCDCDC"
    class="ml-4 mt-2 pb-5"
  />
  <v-sheet class="d-flex flex-wrap ml-5" style="background: transparent">
    <free-style-shimmer
      :is-loading="true"
      height="70vh"
      width="22vw"
      border-radius="10px"
      color="#DCDCDC"
      class="pl-0 mt-2"
    />
    <free-style-shimmer
      v-for="n in 2"
      :key="n"
      :is-loading="true"
      height="70vh"
      width="22vw"
      border-radius="10px"
      color="#DCDCDC"
      class="ml-6 mt-2"
    />
  </v-sheet>
</template>
