export function formatSize(bytes?: number | null): string {
  if (!bytes && bytes !== 0) return "";
  if (bytes >= 1024 * 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
  return `${Math.max(1, Math.round(bytes / 1024))} KB`;
}

/** "29 October 2026, 8:33 WIB" */
export function formatDateTime(iso?: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const date = d.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
  const time = `${d.getHours()}:${String(d.getMinutes()).padStart(2, "0")}`;
  return `${date}, ${time} WIB`;
}

/** "about 6 min" */
export function formatEta(seconds?: number | null): string {
  if (seconds === undefined || seconds === null) return "";
  if (seconds < 60) return "less than a minute";
  return `about ${Math.round(seconds / 60)} min`;
}
