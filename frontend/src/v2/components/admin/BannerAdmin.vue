<template>
  <div class="home-banner mx-6 my-3">
    <p class="pt-5 text-banner">Welcome to Dashboard Administrator!</p>
    <p class="pt-5 text-sub-banner">
      You can manage your workspace, task and role in this page!
    </p>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.home-banner {
  max-width: 100%;
  background-image: url("@v2/assets/home/banner_admin.png");
  background-size: 100% 100%;
  height: 125px;
  border-radius: 20px;
  border: 1px solid #f5f5f5;
}

.text-banner {
  text-align: left;
  padding-left: 4vw;
  font-size: 26px;
  color: white;
  font-weight: bold;
}
.text-sub-banner {
  text-align: left;
  padding-left: 4vw;
  padding-top: 0px !important;
  font-size: 16px;
  color: white;
}
</style>
