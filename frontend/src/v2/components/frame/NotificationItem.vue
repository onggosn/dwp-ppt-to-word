<template>
  <v-list-item :class="[props.item.seenByUser ? 'bg-notif-click' : '']">
    <div class="d-flex py-1" style="cursor: pointer" @click="handleClick">
      <div class="my-auto">
        <v-avatar
          rounded="0"
          :image="getIconUrl(props.item?.title)"
          size="35"
        ></v-avatar>
      </div>
      <div class="d-flex flex-column ml-4">
        <span
          class="font-weight-bold text-12"
          v-if="
            props.item?.data?.heading != '' || props.item?.data?.heading != null
          "
          >{{ props.item?.data?.heading }}</span
        >
        <span
          class="mb-1 text-12"
          v-html="messagesWithFormattedText(props.item.data.message)"
        ></span>
        <span class="text-10 mb-0 blue-grey-darken-1" style="color: #797979e5">
          {{ checkDate(props.item.createdAt) }}
        </span>
      </div>
    </div>
  </v-list-item>
</template>
<style scoped>
.bg-notif-click {
  background-color: rgb(220 220 220);
}
</style>
<script setup lang="ts">
import { checkDate } from "@v2/helpers/DateHelper";
import { getCurrentInstance } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { responsePromise } from "@v2/helpers/utils";
import sanitizeHtml from "sanitize-html";

const emit = defineEmits(["readLocal"]);
const props = defineProps({
  item: {
    type: Object,
    default: () => {
      return {};
    },
  },
});
const router = useRouter();
const { root } = getCurrentInstance() as any;
const response = responsePromise(root);
const store = useStore();

function getIconUrl(type: string) {
  if (!type || typeof type !== "string" || type.trim() === "") {
    return "/images/notif/Puzzle.png";
  }

  const iconMap: Record<string, string> = {
    diskusi: "/images/notif/diskusi.png",
    dokumen: "/images/notif/Cryptocurrency-Certificate.png",
    meeting: "/images/notif/Detail-Calendar.png",
    task: "/images/notif/Puzzle.png",
    member: "/images/notif/member.png",
    chartpack: "/images/notif/chartpack.png",
    "member meeting": "/images/notif/member.png",
    assignment: "/images/notif/assignment-new.svg",
    reminder: "/images/notif/reminder-icon.png",
  };

  return iconMap[type.toLowerCase()] ?? "/images/notif/Puzzle.png";
}

async function handleClick() {
  const link = props.item.data.web;
  const payload = {
    notificationId: props.item.id,
  };

  if (!props.item.seenByUser) {
    emit("readLocal", props.item.id);
    await store
      .dispatch("userStore/updateNotificationViewById", payload)
      .catch(response.error);
  }

  if (link) {
    const allowedWorkspaces = [
      "app/v2/workspace-management/rdgb",
      "app/v2/workspace-management/rdgtk",
      "app/v2/workspace-management/om/rdgm",
    ];

    // Cek apakah 'link' mengandung salah satu dari daftar di atas
    const shouldRefresh = allowedWorkspaces.some((workspace) =>
      link.includes(workspace)
    );

    if (shouldRefresh) store.commit("globalStore/setNeedRefreshTOC", true);
    router.push({ path: "/" + link });
  }
}

function messagesWithFormattedText(
  messages: { isBold: boolean; message: string }[]
): string {
  const formattedMessages = messages
    .reduce((acc, item) => {
      const formattedMessage = item.isBold
        ? `<b>${item.message}</b>`
        : item.message;
      return acc + " " + formattedMessage;
    }, "")
    .trim();

  return sanitizeHtml(formattedMessages);
}
</script>
