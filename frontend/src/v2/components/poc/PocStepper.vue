<template>
  <!-- POC: PowerPoint -> Word -> Final PDF stepper -->
  <div class="stepper d-flex align-center" :class="{ compact }">
    <template v-for="(s, i) in steps" :key="s.label">
      <div class="d-flex align-center step" :class="s.state">
        <v-icon v-if="s.state === 'done'" size="18" color="#2bc244"
          >mdi-check-circle</v-icon
        >
        <span v-else class="dot">{{ i + 1 }}</span>
        <span class="ml-2 label">{{ s.label }}</span>
      </div>
      <div
        v-if="i < steps.length - 1"
        class="line"
        :class="{ done: s.state === 'done' }"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  steps: Array<{ label: string; state: "done" | "active" | "todo" }>;
  compact?: boolean;
}>();
</script>

<style scoped>
.stepper {
  width: fit-content;
  font-size: 13px;
}
.stepper.compact {
  font-size: 11px;
}
.line {
  width: 120px;
  height: 2px;
  background: #d6d6d6;
  margin: 0 10px;
}
.compact .line {
  width: 70px;
}
.line.done {
  background: #2bc244;
}
.dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-size: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #d6d6d6;
  color: #fff;
}
.step.active .dot {
  background: #267dc2;
}
.step.done .label {
  color: #2bc244;
  font-weight: 600;
}
.step.active .label {
  color: #267dc2;
  font-weight: 600;
}
.step.todo .label {
  color: #9e9e9e;
}
</style>
