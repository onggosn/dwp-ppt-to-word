export function getEventStatusColor(status: string) {
  if (status == "In Progress") {
    return {
      background: "#FFEECA",
      color: "#906E2C",
    };
  } else if (status == "Not Started") {
    return {
      background: "#EBEDEB",
      color: "#5B5D5F",
    };
  } else if (status == "Done") {
    return {
      background: "#E8F6EB",
      color: "#2BC244",
    };
  }

  return {
    background: "#fff",
    color: "#000",
  };
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
  } else if (stage == "Rekomendasi") {
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
