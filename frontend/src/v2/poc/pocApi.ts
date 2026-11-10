/**
 * Client for the PPT to Word conversion backend (backend/app.py), reached through the
 * dev-server proxy /poc-api. Own axios instance with the real XHR adapter, so the POC mock
 * adapter (pocMock.ts) does not answer these calls.
 */
import axios from "axios";

const http = axios.create({ baseURL: "/poc-api", adapter: "xhr" });

export type StepState = "waiting" | "running" | "done";

export interface TokenUsage {
  responses: number;
  missing_usage: number;
  input_tokens: number;
  output_tokens: number;
  cache_read_input_tokens: number;
  cache_creation_input_tokens: number;
  total_tokens: number;
  models: string[];
}

export interface PocDocument {
  id: string;
  status: "not_started" | "in_progress" | "done";
  ppt: null | {
    name: string;
    size: number;
    slides: number;
    visibleSlides: number;
    uploadedBy: string;
    uploadedAt: string;
  };
  conversion: null | {
    runId: string;
    status: "converting" | "complete" | "error";
    progress: number;
    currentSlide: number;
    totalSlides: number;
    message: string;
    ai: null | { done: number; total: number };
    estimateSeconds: number;
    etaSeconds?: number;
    steps: Array<{ label: string; state: StepState }>;
    error: string | null;
    stats?: { token_usage?: TokenUsage; [key: string]: unknown };
  };
  word: null | {
    name: string;
    size: number;
    comments: number;
    author: string;
    createdAt: string;
  };
  finalPdf: null | {
    name: string;
    size: number;
    uploadedBy: string;
    uploadedAt: string;
  };
}

export interface PocError {
  code: string;
  message: string;
}

export function toPocError(e: any): PocError {
  const data = e?.response?.data;
  if (data?.code) return data;
  if (e?.response?.status === 413) {
    return { code: "TOO_LARGE", message: "File lebih dari 150MB." };
  }
  return {
    code: "NETWORK",
    message: "Server konversi tidak bisa dihubungi. Jalankan backend/app.py.",
  };
}

export async function getDocument(docId: string): Promise<PocDocument> {
  return (await http.get(`/documents/${docId}`)).data;
}

function upload(
  url: string,
  file: File,
  uploadedBy: string,
  onProgress?: (pct: number) => void
) {
  const form = new FormData();
  form.append("file", file);
  form.append("uploadedBy", uploadedBy);
  return http.post(url, form, {
    onUploadProgress: (e) => {
      if (onProgress && e.total)
        onProgress(Math.round((e.loaded / e.total) * 100));
    },
  });
}

export async function uploadPpt(
  docId: string,
  file: File,
  uploadedBy: string,
  onProgress?: (pct: number) => void
): Promise<PocDocument> {
  return (await upload(`/documents/${docId}/ppt`, file, uploadedBy, onProgress))
    .data;
}

export async function uploadFinalPdf(
  docId: string,
  file: File,
  uploadedBy: string,
  onProgress?: (pct: number) => void
): Promise<PocDocument> {
  return (
    await upload(`/documents/${docId}/final-pdf`, file, uploadedBy, onProgress)
  ).data;
}

export function wordDownloadUrl(docId: string) {
  return `/poc-api/documents/${docId}/word`;
}

export async function resetDocument(docId: string): Promise<PocDocument> {
  return (await http.post(`/documents/${docId}/reset`)).data;
}
