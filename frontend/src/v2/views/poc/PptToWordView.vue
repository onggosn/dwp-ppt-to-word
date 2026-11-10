<template>
  <!-- POC: PPT to Word Convert (Figma "Sprint 18 - DWP P7 Web" > Upload PPT & Word Convertion / Replace PPT & Convert) -->
  <v-sheet
    class="pl-10 pt-3 pb-3 d-flex justify-space-between align-center"
    style="background: #e0efff"
  >
    <div class="d-flex align-center">
      <v-btn
        density="default"
        icon="mdi-arrow-left"
        style="color: #267dc2"
        :to="{ name: 'v2.home' }"
      />
      <p class="ml-3 font-weight-bold text-18" style="color: #267dc2">
        {{ EVENT_NAME }}
      </p>
    </div>
  </v-sheet>

  <div class="poc-container">
    <div class="left-side">
      <div class="d-flex justify-end align-center mb-1" style="gap: 8px">
        <v-chip
          size="small"
          class="font-weight-bold px-3"
          :style="statusChip.style"
        >
          {{ statusChip.label }}
        </v-chip>
        <v-btn
          size="small"
          variant="outlined"
          color="#065695"
          style="border-radius: 10px"
          prepend-icon="mdi-account-plus-outline"
          @click="toastInfo('Edit Access is not part of this POC.')"
        >
          Edit Access
        </v-btn>
      </div>

      <p class="text-14 fw-500 mb-1">
        Title<span style="color: #e53935">*</span>
      </p>
      <div class="title-field text-14 mb-4">{{ DOC_TITLE }}</div>

      <template v-if="loading">
        <v-card class="poc-card pa-10 d-flex justify-center">
          <v-progress-circular indeterminate color="#267dc2" />
        </v-card>
      </template>

      <v-card v-else-if="loadError" class="poc-card pa-6">
        <div
          class="info-box d-flex align-center"
          style="background: #fdecea; border-color: #f5c2c0"
        >
          <v-icon color="#e53935" class="mr-3">mdi-alert-circle</v-icon>
          <span class="text-13">{{ loadError }}</span>
          <v-spacer />
          <v-btn
            size="small"
            variant="text"
            color="#065695"
            @click="refresh(true)"
            >Retry</v-btn
          >
        </div>
      </v-card>

      <!-- 1. Start: no PowerPoint yet -->
      <v-card v-else-if="!doc?.ppt" class="poc-card pa-8 text-center">
        <div class="hero mx-auto mb-3">
          <v-icon size="64" color="#267dc2">mdi-file-powerpoint-box</v-icon>
        </div>
        <p class="font-weight-bold text-16 mb-3">Start With Powerpoint</p>
        <PocStepper :steps="stepper" class="mx-auto mb-4" compact />
        <p class="text-13 mb-4" style="color: #6b6b6b">
          Upload the Book 2D PowerPoint file to convert it into an editable Word
          document.<br />
          You can review, comment on, and revise the document before uploading
          the finalized version in PDF format.
        </p>
        <div class="mx-auto" style="max-width: 560px">
          <PocDropzone v-model="newFile" @update:model-value="checkPicked" />
          <v-progress-linear
            v-if="uploading"
            :model-value="uploadPct"
            color="#267dc2"
            height="6"
            rounded
            class="mt-3"
          />
          <p v-if="uploading" class="text-12 mt-1" style="color: #6b6b6b">
            Uploading {{ uploadPct }}%
          </p>
        </div>
        <div v-if="newFile" class="d-flex justify-end mt-6" style="gap: 8px">
          <v-btn
            variant="outlined"
            class="rounded-lg text-none"
            :disabled="uploading"
            @click="newFile = null"
          >
            Cancel
          </v-btn>
          <v-btn
            class="rounded-lg text-none primary-gradient"
            color="#065695"
            :loading="uploading"
            @click="startUpload(newFile)"
          >
            Upload &amp; Convert
          </v-btn>
        </div>
      </v-card>

      <!-- 2. PowerPoint uploaded: PowerPoint / Word / Final PDF -->
      <template v-else>
        <v-card class="poc-card py-3 mb-3">
          <PocStepper :steps="stepper" class="mx-auto" />
        </v-card>

        <v-card class="poc-card pa-4 mb-3">
          <p class="text-14 fw-500 mb-3">1. Powerpoint</p>
          <div class="d-flex align-center">
            <FileBadge ext="pptx" />
            <div class="ml-3">
              <p class="text-13 fw-500 mb-0">{{ doc.ppt.name }}</p>
              <p class="text-11 mb-0 meta">
                {{ doc.ppt.visibleSlides }} slides ·
                {{ formatSize(doc.ppt.size) }} · Uploaded by
                {{ doc.ppt.uploadedBy }} ·
                {{ formatDateTime(doc.ppt.uploadedAt) }}
              </p>
            </div>
            <v-spacer />
            <v-btn
              size="small"
              variant="outlined"
              class="rounded-lg text-none"
              color="#065695"
              @click="openReplace"
            >
              Replace PPT
            </v-btn>
          </div>
        </v-card>

        <v-card ref="wordCard" class="poc-card pa-4 mb-3">
          <div class="d-flex align-center mb-3">
            <p class="text-14 fw-500 mb-0">2. Word (Conversion)</p>
            <v-chip
              v-if="conv"
              size="x-small"
              class="ml-3 px-3 font-weight-bold"
              :style="convChip.style"
            >
              {{ convChip.label }}
            </v-chip>
          </div>

          <!-- converting -->
          <template v-if="conv?.status === 'converting'">
            <p class="text-12 mb-1 meta">
              <template v-if="conv.progress > 0">
                Slide {{ conv.currentSlide }} of {{ conv.totalSlides }} ·
                {{ formatEta(conv.etaSeconds) }} left
              </template>
              <template v-else>
                Estimated finish in
                {{ formatEta(conv.etaSeconds ?? conv.estimateSeconds) }}
              </template>
            </p>
            <v-progress-linear
              :model-value="Math.max(2, conv.progress * 100)"
              color="#267dc2"
              bg-color="#e0e0e0"
              height="8"
              rounded
              class="mb-3"
            />
            <div
              v-for="(st, i) in conv.steps"
              :key="i"
              class="d-flex align-center step-row"
            >
              <v-icon v-if="st.state === 'done'" size="16" color="#2bc244"
                >mdi-check</v-icon
              >
              <v-progress-circular
                v-else-if="st.state === 'running'"
                size="14"
                width="2"
                indeterminate
                color="#267dc2"
              />
              <v-icon v-else size="16" color="#bdbdbd"
                >mdi-clock-outline</v-icon
              >
              <span
                class="ml-2 text-12"
                :class="{
                  'text-grey': st.state === 'waiting',
                  'fw-500': st.state === 'running',
                }"
              >
                {{ stepLabel(st.label, i) }}
              </span>
            </div>
            <div class="info-box d-flex align-center mt-3">
              <v-icon color="#267dc2" class="mr-3">mdi-information</v-icon>
              <span class="text-13"
                >You can close this page. We will send a notification when the
                word file is ready</span
              >
            </div>
          </template>

          <!-- complete -->
          <template v-else-if="conv?.status === 'complete' && doc.word">
            <div class="d-flex align-center">
              <FileBadge ext="docx" />
              <div class="ml-3">
                <p class="text-13 fw-500 mb-0">{{ doc.word.name }}</p>
                <p class="text-11 mb-0 meta">
                  {{ formatSize(doc.word.size) }} ·
                  {{ doc.word.comments }} Comment by {{ doc.word.author }}
                </p>
              </div>
              <v-spacer />
              <v-btn
                size="small"
                class="rounded-lg text-none primary-gradient"
                color="#065695"
                prepend-icon="mdi-download"
                @click="downloadWord"
              >
                Download Word
              </v-btn>
            </div>
            <div v-if="tokenUsage" class="info-box mt-4 text-12">
              <p class="fw-500 mb-1">LLM token usage (this conversion)</p>
              <p class="mb-1">
                Total: {{ tokenUsage.total_tokens.toLocaleString() }} tokens |
                Input: {{ tokenUsage.input_tokens.toLocaleString() }} | Output:
                {{ tokenUsage.output_tokens.toLocaleString() }}
              </p>
              <p class="mb-1">
                Cache read:
                {{ tokenUsage.cache_read_input_tokens.toLocaleString() }} |
                Cache write:
                {{ tokenUsage.cache_creation_input_tokens.toLocaleString() }} |
                Responses: {{ tokenUsage.responses.toLocaleString() }}
              </p>
              <p v-if="tokenUsage.models.length" class="mb-1">
                Model: {{ tokenUsage.models.join(", ") }}
              </p>
              <p class="mb-0 meta">
                Reported API usage only. Local cache hits use no new tokens.
                Interrupted requests may not report usage.
              </p>
              <p v-if="tokenUsage.missing_usage" class="mb-0">
                Usage unavailable for {{ tokenUsage.missing_usage }} responses;
                totals are incomplete.
              </p>
            </div>
            <p v-else class="text-12 mt-4 meta">
              Token usage is unavailable for this conversion.
            </p>
            <div class="info-box d-flex align-start mt-4">
              <v-icon color="#267dc2" class="mr-3">mdi-information</v-icon>
              <span class="text-12">
                Check every comment in Word (Review, Comments). Each comment
                names the source slide and the reason.<br />
                The Word file is now archived in DWP, you can download it again
                until the PPT is replaced.
              </span>
            </div>
          </template>

          <!-- error -->
          <template v-else-if="conv?.status === 'error'">
            <div
              class="info-box d-flex align-start"
              style="background: #fdecea; border-color: #f5c2c0"
            >
              <v-icon color="#e53935" class="mr-3">mdi-alert-circle</v-icon>
              <span class="text-12">
                The conversion failed: {{ conv.error }}<br />
                Use Replace PPT to upload the PowerPoint again.
              </span>
            </div>
          </template>
        </v-card>

        <v-card class="poc-card pa-4 mb-3">
          <p class="text-14 fw-500 mb-2">3. Final PDF</p>
          <p class="text-13 mb-3 meta">
            After revising the word file, export it to PDF and upload the final
            version here
          </p>
          <div v-if="doc.finalPdf" class="d-flex align-center mb-3">
            <FileBadge ext="pdf" />
            <div class="ml-3">
              <p class="text-13 fw-500 mb-0">{{ doc.finalPdf.name }}</p>
              <p class="text-11 mb-0 meta">
                {{ formatSize(doc.finalPdf.size) }} · Uploaded by
                {{ doc.finalPdf.uploadedBy }} ·
                {{ formatDateTime(doc.finalPdf.uploadedAt) }}
              </p>
            </div>
          </div>
          <input
            ref="pdfInput"
            type="file"
            accept=".pdf"
            class="d-none"
            @change="onPdfPicked"
          />
          <v-btn
            size="small"
            class="rounded-lg text-none"
            :class="{ 'primary-gradient': !!doc.word }"
            :color="doc.word ? '#065695' : undefined"
            :disabled="!doc.word"
            :loading="uploadingPdf"
            @click="pdfInput?.click()"
          >
            {{ doc.finalPdf ? "Replace Final PDF" : "Upload Final PDF" }}
          </v-btn>
        </v-card>
      </template>

      <div class="text-end mb-6">
        <v-btn
          size="x-small"
          variant="text"
          color="grey"
          class="text-none"
          @click="resetDemo"
        >
          Reset POC demo
        </v-btn>
      </div>
    </div>

    <div class="right-side">
      <PocContentPanel :active-doc="ACTIVE_DOC" />
    </div>
  </div>

  <!-- Replace PPT -->
  <v-dialog v-model="replace.open" width="620" persistent>
    <v-card class="pa-5" style="border-radius: 12px">
      <div class="d-flex align-center mb-2">
        <v-spacer />
        <p class="font-weight-bold text-16 mb-0">Replace PPT</p>
        <v-spacer />
        <v-btn
          icon="mdi-close"
          size="small"
          variant="text"
          @click="replace.open = false"
        />
      </div>
      <v-divider class="mb-4" />
      <p class="text-13 fw-500 mb-1">
        Upload PPT<span style="color: #e53935">*</span>
      </p>
      <PocDropzone v-model="replace.file" @update:model-value="checkPicked" />
      <div class="d-flex justify-end mt-6" style="gap: 8px">
        <v-btn
          variant="outlined"
          class="rounded-lg text-none"
          @click="replace.open = false"
          >Cancel</v-btn
        >
        <v-btn
          class="rounded-lg text-none"
          :class="{ 'primary-gradient': !!replace.file }"
          color="#065695"
          :disabled="!replace.file"
          @click="replace.confirm = true"
        >
          Replace
        </v-btn>
      </div>
    </v-card>
  </v-dialog>

  <!-- Replace confirmation -->
  <v-dialog v-model="replace.confirm" width="560" persistent>
    <v-card class="pa-6 text-center" style="border-radius: 12px">
      <v-btn
        icon="mdi-close"
        size="small"
        variant="outlined"
        class="close-btn"
        @click="replace.confirm = false"
      />
      <div class="warn-icon mx-auto mb-3">
        <v-icon size="30" color="#f5a623">mdi-exclamation-thick</v-icon>
      </div>
      <p class="font-weight-bold text-16 mb-2">Replace the Powerpoint</p>
      <p class="text-13 mb-3 meta">
        The current PPT will be replaced and is not kept.<br />
        A new conversion starts from the beginning<template v-if="doc?.ppt">
          (about
          {{ Math.max(1, Math.round((doc.ppt.visibleSlides * 9) / 60)) }} min
          for {{ doc.ppt.visibleSlides }} slides)</template
        >.
      </p>
      <div v-if="wordDownloaded" class="warn-box text-start mb-4">
        <p class="text-13 font-weight-bold mb-1">
          <v-icon size="18" color="#906e2c" class="mr-1">mdi-alert</v-icon>The
          Word file was already downloaded
        </p>
        <p class="text-12 mb-0">
          Revisions you made in the word file are not carried into the new
          conversion. Keep your revised word file before continuing.
        </p>
      </div>
      <div class="d-flex" style="gap: 8px">
        <v-btn
          variant="outlined"
          class="rounded-lg text-none flex-grow-1"
          @click="replace.confirm = false"
          >Cancel</v-btn
        >
        <v-btn
          class="rounded-lg text-none flex-grow-1 primary-gradient"
          color="#065695"
          :loading="uploading"
          @click="confirmReplace"
        >
          Replace &amp; Convert
        </v-btn>
      </div>
    </v-card>
  </v-dialog>

  <!-- Upload errors: not .pptx / over 150MB / no access -->
  <v-dialog v-model="alert.open" width="420">
    <v-card class="pa-6 text-center" style="border-radius: 12px">
      <v-btn
        icon="mdi-close"
        size="small"
        variant="outlined"
        class="close-btn"
        @click="alert.open = false"
      />
      <div class="warn-icon mx-auto mb-3">
        <v-icon size="30" color="#f5a623">mdi-exclamation-thick</v-icon>
      </div>
      <p class="font-weight-bold text-16 mb-2">{{ alert.title }}</p>
      <p class="text-13 mb-5 meta">{{ alert.message }}</p>
      <v-btn
        block
        class="rounded-lg text-none primary-gradient"
        color="#065695"
        @click="alert.open = false"
        >OK</v-btn
      >
    </v-card>
  </v-dialog>

  <!-- "Word File is Ready" notification -->
  <transition name="slide-fade">
    <div v-if="notify" class="notify-card d-flex" @click="openFromNotification">
      <div class="notify-icon mr-3">
        <v-icon color="#267dc2">mdi-file-word-box</v-icon>
      </div>
      <div style="flex: 1">
        <p class="text-13 font-weight-bold mb-1">Word File is Ready</p>
        <p class="text-12 mb-1">
          {{ DOC_SHORT }} was converted ({{ notify.slides }} Slide,
          {{ notify.comments }} Review Comment). Click to Open
        </p>
        <p class="text-11 mb-0 meta">Just Now</p>
      </div>
      <span class="notify-dot" />
      <v-btn
        icon="mdi-close"
        size="x-small"
        variant="text"
        @click.stop="notify = null"
      />
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref } from "vue";
import { useRoute } from "vue-router";
import { useStore } from "vuex";
import { useToast } from "vue-toastification";
import PocContentPanel from "@/v2/components/poc/PocContentPanel.vue";
import PocDropzone from "@/v2/components/poc/PocDropzone.vue";
import PocStepper from "@/v2/components/poc/PocStepper.vue";
import FileBadge from "@/v2/components/poc/FileBadge.vue";
import {
  PocDocument,
  getDocument,
  resetDocument,
  toPocError,
  uploadFinalPdf,
  uploadPpt,
  wordDownloadUrl,
} from "@/v2/poc/pocApi";
import { formatDateTime, formatEta, formatSize } from "@/v2/poc/format";

const EVENT_NAME = "RDGB Cakupan Bulanan September 2026";
const DOC_TITLE =
  "Buku 2D - Ringkasan Asesmen dan Rekomendasi Bauran Kebijakan BI";
const DOC_SHORT = "Buku 2D_ RDG Bulanan September 2026";
const ACTIVE_DOC = "RDGB_Bulan Tahun_Buku 2d Bauran Kebijakan BI";
const MAX_MB = 150;

const route = useRoute();
const store = useStore();
const toast = useToast();
const docId = computed(() => (route.params.docId as string) || "buku-2d");
// ?access=none shows the "no access" case from the mockup
const hasAccess = computed(() => route.query.access !== "none");
const userName = computed(() => store.state.fullname || "Unknown");

const doc = ref<PocDocument | null>(null);
const loading = ref(true);
const loadError = ref("");
const newFile = ref<File | null>(null);
const uploading = ref(false);
const uploadPct = ref(0);
const uploadingPdf = ref(false);
const pdfInput = ref<HTMLInputElement>();
const wordCard = ref<any>();
const notify = ref<null | { slides: number; comments: number }>(null);
const downloadTick = ref(0);
const replace = reactive({
  open: false,
  confirm: false,
  file: null as File | null,
});
const alert = reactive({ open: false, title: "", message: "" });

const conv = computed(() => doc.value?.conversion || null);
const tokenUsage = computed(() => conv.value?.stats?.token_usage);

const statusChip = computed(() => {
  const s = doc.value?.status || "not_started";
  if (s === "done")
    return {
      label: "Completed",
      style: { background: "#e8f6eb", color: "#2bc244" },
    };
  if (s === "in_progress")
    return {
      label: "In Progress",
      style: { background: "#ffeeca", color: "#906e2c" },
    };
  return {
    label: "Not Started",
    style: { background: "#eeeeee", color: "#6b6b6b" },
  };
});

const convChip = computed(() => {
  const s = conv.value?.status;
  if (s === "complete")
    return {
      label: "Complete",
      style: { background: "#e8f6eb", color: "#2bc244" },
    };
  if (s === "error")
    return {
      label: "Failed",
      style: { background: "#fdecea", color: "#e53935" },
    };
  return {
    label: "Converting",
    style: { background: "#ffeeca", color: "#906e2c" },
  };
});

const stepper = computed(() => {
  const d = doc.value;
  const done = [!!d?.ppt, !!d?.word, !!d?.finalPdf];
  const active = done.indexOf(false);
  return ["PowerPoint", "Word", "Final PDF"].map((label, i) => ({
    label,
    state: done[i] ? "done" : i === active ? "active" : "todo",
  })) as Array<{ label: string; state: "done" | "active" | "todo" }>;
});

const wordDownloaded = computed(() => {
  void downloadTick.value;
  const run = conv.value?.runId;
  try {
    return !!run && localStorage.getItem(`poc-word-downloaded-${run}`) === "1";
  } catch {
    return false;
  }
});

function stepLabel(label: string, i: number) {
  const ai = conv.value?.ai;
  if (i === 2 && ai && ai.total) return `${label} (${ai.done} of ${ai.total})`;
  return label;
}

function toastInfo(msg: string) {
  toast.info(msg, { timeout: 2500 });
}

function showAlert(code: string, message?: string) {
  const texts: Record<string, [string, string]> = {
    INVALID_TYPE: [
      "File Not Supported",
      "Only PowerPoint (.pptx) files can be uploaded and converted.",
    ],
    TOO_LARGE: [
      "File Too Large",
      `The file is larger than ${MAX_MB}MB. Reduce the file size and try again.`,
    ],
    NO_ACCESS: [
      "No Access",
      "You don't have access to upload a PowerPoint for this document. Ask the document owner for edit access.",
    ],
  };
  const [title, msg] = texts[code] || [
    "Upload Failed",
    message || "Something went wrong.",
  ];
  Object.assign(alert, {
    open: true,
    title,
    message: texts[code] ? msg : message || msg,
  });
}

/** Client-side checks, same rules as the backend (it checks again). */
function validatePpt(file: File): string | null {
  if (!hasAccess.value) return "NO_ACCESS";
  if (!file.name.toLowerCase().endsWith(".pptx")) return "INVALID_TYPE";
  if (file.size > MAX_MB * 1024 * 1024) return "TOO_LARGE";
  return null;
}

function checkPicked(file: File | null) {
  if (!file) return;
  const code = validatePpt(file);
  if (code) {
    showAlert(code);
    newFile.value = null;
    replace.file = null;
  }
}

// ------------------------------------------------------------------ polling
let timer: number | undefined;

async function refresh(showSpinner = false) {
  if (showSpinner) loading.value = true;
  try {
    const before = doc.value?.conversion?.status;
    const next = await getDocument(docId.value);
    if (
      before === "converting" &&
      next.conversion?.status === "complete" &&
      next.word
    ) {
      notify.value = {
        slides: next.conversion.totalSlides,
        comments: next.word.comments,
      };
    }
    doc.value = next;
    loadError.value = "";
  } catch (e) {
    loadError.value = toPocError(e).message;
  } finally {
    loading.value = false;
  }
  schedule();
}

function schedule() {
  window.clearTimeout(timer);
  if (doc.value?.conversion?.status === "converting") {
    timer = window.setTimeout(() => refresh(), 2000);
  }
}

// ------------------------------------------------------------------ actions
async function startUpload(file: File | null) {
  if (!file) return;
  const code = validatePpt(file);
  if (code) return showAlert(code);
  uploading.value = true;
  uploadPct.value = 0;
  try {
    doc.value = await uploadPpt(
      docId.value,
      file,
      userName.value,
      (p) => (uploadPct.value = p)
    );
    newFile.value = null;
    notify.value = null;
    schedule();
    return true;
  } catch (e) {
    const err = toPocError(e);
    showAlert(err.code, err.message);
    return false;
  } finally {
    uploading.value = false;
  }
}

function openReplace() {
  if (!hasAccess.value) return showAlert("NO_ACCESS");
  replace.file = null;
  replace.open = true;
}

async function confirmReplace() {
  const ok = await startUpload(replace.file);
  replace.confirm = false;
  if (ok) {
    replace.open = false;
    replace.file = null;
  }
}

function downloadWord() {
  const a = document.createElement("a");
  a.href = wordDownloadUrl(docId.value);
  a.download = doc.value?.word?.name || "document.docx";
  document.body.appendChild(a);
  a.click();
  a.remove();
  try {
    localStorage.setItem(`poc-word-downloaded-${conv.value?.runId}`, "1");
  } catch {
    /* storage unavailable */
  }
  downloadTick.value++;
}

async function onPdfPicked(e: Event) {
  const input = e.target as HTMLInputElement;
  const file = input.files?.[0];
  input.value = "";
  if (!file) return;
  if (!hasAccess.value) return showAlert("NO_ACCESS");
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    return showAlert(
      "PDF",
      "Only PDF files can be uploaded as the final version."
    );
  }
  uploadingPdf.value = true;
  try {
    doc.value = await uploadFinalPdf(docId.value, file, userName.value);
    toast.success("Final PDF uploaded.", { timeout: 2500 });
  } catch (err) {
    const pe = toPocError(err);
    showAlert(pe.code, pe.message);
  } finally {
    uploadingPdf.value = false;
  }
}

function openFromNotification() {
  notify.value = null;
  wordCard.value?.$el?.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function resetDemo() {
  doc.value = await resetDocument(docId.value);
  notify.value = null;
  newFile.value = null;
}

onMounted(() => refresh(true));
onUnmounted(() => window.clearTimeout(timer));
</script>

<style scoped>
.poc-container {
  display: flex;
  gap: 24px;
  padding: 16px 24px 0 40px;
}
.left-side {
  flex: 1;
  min-width: 0;
  height: calc(100vh - 140px);
  overflow-y: auto;
  padding-right: 5px;
}
.right-side {
  width: 340px;
  flex-shrink: 0;
}
.poc-card {
  border-radius: 12px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06) !important;
}
.title-field {
  background: #e6e6e6;
  border-radius: 8px;
  padding: 10px 14px;
  color: #4b4b4b;
}
.hero {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #e0efff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.meta {
  color: #6b6b6b;
}
.info-box {
  background: #eef6fd;
  border: 1px solid #c5def3;
  border-radius: 10px;
  padding: 12px 14px;
  color: #3a416f;
}
.warn-box {
  background: #fff8e6;
  border: 1px solid #f3dca4;
  border-radius: 10px;
  padding: 12px 14px;
  color: #6b5320;
}
.step-row {
  padding: 3px 0;
}
.warn-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: #fff3d6;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
}
.notify-card {
  position: fixed;
  top: 72px;
  right: 24px;
  width: 340px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.16);
  padding: 14px;
  z-index: 2000;
  cursor: pointer;
  align-items: flex-start;
}
.notify-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e0efff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.notify-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e53935;
  margin: 26px 4px 0;
}
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.25s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
@media (max-width: 1100px) {
  .right-side {
    display: none;
  }
}
</style>
