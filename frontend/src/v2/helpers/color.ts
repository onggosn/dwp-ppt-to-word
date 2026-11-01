interface ChipEventStatus {
  background: string;
  color: string;
}

interface ChipStyle {
  "background-color": string;
  color: string;
}

const eventStatusColors: Record<string, ChipEventStatus> = {
  "in progress": {
    background: "#FFEECA",
    color: "#906E2C",
  },
  "not started": {
    background: "#EBEDEB",
    color: "#5B5D5F",
  },
  done: {
    background: "#E8F6EB",
    color: "#2BC244",
  },
};

export function getEventStatusColor(
  status: string
): ChipEventStatus | undefined {
  const key = status?.toLowerCase().trim();
  return eventStatusColors[key] || { background: "#fff", color: "#000" };
}

export function getColorChip(eventSubType: string): string {
  let bgColor = "grey";
  if (eventSubType !== null) {
    const lowerCaseEventSubType: string = eventSubType.toLowerCase();

    if (lowerCaseEventSubType === "rdg") {
      bgColor = "blue";
    } else if (
      lowerCaseEventSubType === "komite" ||
      lowerCaseEventSubType === "komite gabungan"
    ) {
      bgColor = "red";
    }
  }

  return bgColor;
}

export function getBusinessStageProgressColor(stage: string) {
  if (stage == "Asesmen") {
    return "#FF4E76";
  } else if (stage == "Rekomendasi" || stage == "Asesmen & Rekomendasi") {
    return "#E3B43B";
  } else if (stage == "Persetujuan") {
    return "#21CC44";
  }
  return "#ededed";
}

export function getColorChipEditor(label: string) {
  label = label?.toLowerCase();
  if (
    [
      "in progress",
      "need for review",
      "need for approval",
      "need for review delete",
      "need for approval delete",
      "need for review cancel",
      "need for review cancel\r\n",
      "need for approval cancel",
      "approval in progress",
      "approval revision in progress",
    ].includes(label)
  ) {
    return {
      "background-color": "#ffeeca",
      color: "#906e2c",
      icon: "mdi-cog",
    };
  } else if (["approved", "published"].includes(label)) {
    return {
      "background-color": "#e8f6eb",
      color: "#2bc244",
      icon: "mdi-check-circle-outline",
    };
  } else if (["need for review cancel"].includes(label)) {
    return {
      "background-color": "#e8f6eb",
      color: "#2bc244",
      icon: "mdi-check-circle-outline",
    };
  } else if (["rejected"].includes(label)) {
    return {
      "background-color": "#f7bcc0",
      color: "#b30b15",
      icon: "mdi-close-circle-outline",
    };
  } else if (["canceled"].includes(label)) {
    return {
      "background-color": "#f7bcc0",
      color: "#b30b15",
      icon: "mdi-close-circle-outline",
    };
  } else {
    return {
      "background-color": "#EBEDEB",
      color: "#5B5D5F",
      icon: "mdi-cog-off",
    };
  }
}

export function getDocumentColor(label: string | null) {
  label = (label ?? "").toLowerCase();
  return [
    { "text-success": ["approved"].includes(label) },
    { "text-danger": ["rejected"].includes(label) },
    { "text-warning": !["approved", "rejected"].includes(label) },
  ];
}

export const chipStyles: Record<string, ChipStyle> = {
  "in progress": {
    "background-color": "rgba(255, 238, 202, 1)",
    color: "rgba(144, 110, 44, 1)",
  },
  "in progress revision": {
    "background-color": "rgba(255, 238, 202, 1)",
    color: "rgba(144, 110, 44, 1)",
  },
  "need for approval": {
    "background-color": "rgba(255, 238, 202, 1)",
    color: "rgba(144, 110, 44, 1)",
  },
  "need for review": {
    "background-color": "rgba(255, 238, 202, 1)",
    color: "rgba(144, 110, 44, 1)",
  },
  done: {
    "background-color": "rgba(232, 246, 235, 1)",
    color: "rgba(28, 163, 51, 1)",
  },
  approved: {
    "background-color": "rgba(232, 246, 235, 1)",
    color: "rgba(28, 163, 51, 1)",
  },
  published: {
    "background-color": "rgba(232, 246, 235, 1)",
    color: "rgba(28, 163, 51, 1)",
  },
  deleted: {
    "background-color": "#f7bcc0",
    color: "#b30b15",
  },
  "not started": {
    "background-color": "rgba(235, 237, 235, 1)",
    color: "black",
  },
};

export function getColorChipStyle(value: string): ChipStyle | undefined {
  const key = value?.toLocaleLowerCase().trim();
  return chipStyles[key];
}

export function matchChipStyle(value: string): ChipStyle | undefined {
  const key = value?.toLowerCase().trim();

  if (
    key?.includes("need for approval") ||
    key?.includes("need for review") ||
    key?.includes("in progress")
  ) {
    return {
      "background-color": "rgba(255, 238, 202, 1)",
      color: "rgba(144, 110, 44, 1)",
    };
  }

  if (key?.includes("approved") || key?.includes("published")) {
    return {
      "background-color": "rgba(232, 246, 235, 1)",
      color: "rgba(28, 163, 51, 1)",
    };
  }

  if (key?.includes("done")) {
    return {
      "background-color": "rgba(232, 246, 235, 1)",
      color: "rgba(28, 163, 51, 1)",
    };
  }

  if (
    key?.includes("deleted") ||
    key?.includes("canceled") ||
    key?.includes("rejected")
  ) {
    return {
      "background-color": "#f7bcc0",
      color: "#b30b15",
    };
  }

  return {
    "background-color": "rgba(235, 237, 235, 1)",
    color: "black",
  };
}

const chipTypeRdg: Record<string, ChipStyle> = {
  bulanan: {
    "background-color": "#E9F5FF",
    color: "#2279BD",
  },
  triwulanan: {
    "background-color": "#FFE1FD",
    color: "#BD22B8",
  },
  tahunan: {
    "background-color": "#ffeeca",
    color: "#906e2c",
  },
  default: {
    "background-color": "#FFEECA",
    color: "#E2650B",
  },
};

export function getColorChipTypeRdg(value: string): ChipStyle | undefined {
  const key = value?.toLocaleLowerCase().trim();
  return chipTypeRdg[key] || chipTypeRdg.default;
}

const chipTypeRdgHistory: Record<string, ChipStyle> = {
  rdgb: {
    "background-color": "#FFE1FD",
    color: "#BD22B8",
  },
  default: {
    "background-color": "#E9F5FF",
    color: "#2279BD",
  },
};

export function getColorChipTypeRdgHistory(
  value: string
): ChipStyle | undefined {
  const key = value?.toLocaleLowerCase().trim();
  return chipTypeRdgHistory[key] || chipTypeRdgHistory.default;
}

export function getStatusLabelColor(status: string): string {
  const key = status?.toLowerCase().trim();
  if (["not started"].includes(key)) {
    return "#5B5D5F"; // Gray
  } else if (
    [
      "in progress",
      "need for review",
      "need for approval",
      "in progress revisi",
      "need for review revisi",
      "need for approval revisi",
      "need for review cancel",
      "need for approval cancel",
      "need for review delete",
      "need for approval delete",
    ].includes(key)
  ) {
    return "#E2650B"; // Orange
  } else if (
    ["approved", "done", "approved revisi", "published"].includes(key)
  ) {
    return "#2BC244"; // Green
  } else if (["canceled", "deleted", "rejected"].includes(key)) {
    return "#ff0000"; // Red
  } else {
    return "#5B5D5F"; // Default to gray
  }
}

export function getActivityTaskLabelColor(status: string): string {
  const key = status?.toLowerCase().trim();
  if (["asesmen"].includes(key)) {
    return "#BD22B8";
  } else if (["rekomendasi"].includes(key)) {
    return "#2279BD";
  } else if (["persetujuan"].includes(key)) {
    return "#2BC244";
  } else if (["deleted"].includes(key)) {
    return "#b30b15";
  } else {
    return "#5B5D5F";
  }
}
