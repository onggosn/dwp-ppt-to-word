enum ContentType {
  PredefineContent = 0,
  OngoingContent = 1,
}

enum RoleType {
  Role = 0,
  User = 1,
  Adg = 2,
}

enum MappingStatus {
  deleted = "deleted",
  update = "updated",
  existing = "existing",
  new = "new",
}

enum MappingSector {
  buku2d = 8,
  buku1d = 20,
  buku4 = 21,
}

// Map from item flag (e.g. isDocBuku2d) to its MappingSector value.
// Add a new entry here whenever a new sector type is introduced.
export const DocTypeToSectorMap: Record<string, MappingSector> = {
  isDocBuku2d: MappingSector.buku2d,
  isDocBuku1d: MappingSector.buku1d,
  isDocBuku4: MappingSector.buku4,
};

enum MeetingType {
  Meeting = 0,
  PresentationMaterial = 1,
}

enum OperasionalType {
  User = 0,
}

enum idBpDocument {
  default = "00000000-0000-0000-0000-000000000000",
}

export default {
  ContentType,
  RoleType,
  MappingStatus,
  MappingSector,
  MeetingType,
  OperasionalType,
  idBpDocument,
};

export enum DocumentType {
  ringsek = 5,
}

// Gradient color lookup for document status
export const GradientStatusClass: Record<string, string> = {
  "not started": "gradient-text-none",
  "in progress": "gradient-text-progress",
  "need for review": "gradient-text-progress",
  "need for approval": "gradient-text-progress",
  approved: "gradient-text-finish",
  published: "gradient-text-finish",
};

export enum Stage {
  RakorRispatBulanan = 68,
  RakorRispatTriwulanan = 69,
  RakorRispatMingguan = 63,
}

export enum DashboardSort {
  TanggalRDG = "tanggalRDG",
}

export enum messageEditEvent {
  meetingDetails = "You've updated the meeting details.<br>Do you want to notify participants via Outlook?",
  meetingAttendees = "You've updated the attendees List.<br>Select who should receive the Outlook notification.",
  updateAgenda = "You’ve updated the meeting agenda details. Do you want to notify participants via Outlook?",
}
