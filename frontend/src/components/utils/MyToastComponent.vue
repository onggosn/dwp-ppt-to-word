<template>
  <table width="100%">
    <tr>
      <td width="13%" color="red">
        <img src="/images/login/logoDMP.png" width="35" height="35" />
      </td>
      <td width="87%">
        <p class="text-title">{{ title }}</p>
        <p class="text-content ellipsis" v-html="body"></p>
      </td>
    </tr>
  </table>
</template>
<script>
export default {
  props: ["title", "body"],
  methods: {},
};
</script>
<style>
.text-title {
  font-family: Poppins;
  font-size: 18px;
  font-weight: 600;
  line-height: 27px;
  letter-spacing: 0em;
  text-align: left;
  color: #3a416f;
}

.text-content {
  font-family: Poppins;
  font-size: 13px;
  line-height: 20px;
  letter-spacing: 0em;
  text-align: left;
  color: #3a416f;
}
.ellipsis {
  white-space: pre-wrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  position: absolute;
  z-index: 1;
  bottom: 150%;
  left: 50%;
  margin-left: -60px;
}

.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: black transparent transparent transparent;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>
