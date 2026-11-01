<template>
  <div class="d-flex py-1" @click="openNotif" style="cursor: pointer">
    <div class="my-auto">
      <v-avatar rounded="0" :image="getIconUrl(item.type)" size="55"></v-avatar>
    </div>
    <div class="d-flex flex-column ml-4">
      <span class="text-body-2 mb-1">
        {{ item.description }}<br />
        <span class="font-weight-bold"> {{ item.notificationObject }}</span>
        by
        {{ item.notifyFrom }}
      </span>
      <p class="text-caption text--secondary mb-0">
        <i class="fa fa-clock me-1"></i>
        {{ checkDate(item.createdDate) }}
      </p>
    </div>
  </div>
</template>

<script>
import { checkDate } from "@/library/DateHelper";
export default {
  name: "rowNotification",
  props: ["item"],
  methods: {
    openNotif() {
      if (this.item.type == "Chartpack") {
        this.$router.replace({
          name: "chartpack",
          params: {
            idChartpack: this.item.eventId,
            searchKeyword: this.item.notifyFrom,
          },
        });
      }
    },
    getIconUrl(type) {
      if (type == "Diskusi") {
        return "/images/notif/diskusi.png";
      } else if (type == "Dokumen") {
        return "/images/notif/Cryptocurrency-Certificate.png";
      } else if (type == "Meeting") {
        return "/images/notif/Detail-Calendar.png";
      } else if (type == "Task") {
        return "/images/notif/Puzzle.png";
      } else if (type == "Member") {
        return "/images/notif/member.png";
      } else if (type == "Chartpack") {
        return "/images/notif/chartpack.png";
      } else if (type == "Member Meeting") {
        return "/images/notif/member.png";
      } else if (type == "Assignment") {
        return "/images/notif/assignment-3d.png";
      } else {
        return "/images/notif/Puzzle.png";
      }
    },
    checkDate,
  },
};
</script>
