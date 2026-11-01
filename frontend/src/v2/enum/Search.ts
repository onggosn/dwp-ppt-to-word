export enum AssignmentDashboardType {
  Penugasan = 0,
  Arahan = 1,
}
export enum DocumentDashboardType {
  Materi = 0,
  Hasil = 1,
}

export enum MeetingType {
  Meeting = 0,
  PresentationMaterial = 1,
}

export enum ContentType {
  PredefineContent = 0,
  OngoingContent = 1,
}

export enum RoleType {
  Role = 0,
  User = 1,
}

export enum SearchRouteName {
  "dashboard.assignment.v2.penugasan" = "dashboard.assignment.v2.penugasan.search",
  "dashboard.assignment.v2.arahan" = "dashboard.assignment.v2.arahan.search",
  "dashboard.document.v2.materi" = "dashboard.document.v2.materi.search",
  "dashboard.document.v2.hasil" = "dashboard.document.v2.hasil.search",
  "dashboard.workspace.v2" = "dashboard.workspace.v2.search",
  "content-admin-predefine" = "content-admin-predefine-search",
  "content-admin-ongoing" = "content-admin-ongoing-search",
  "faq-admin" = "faq-admin-list-search",
  "meeting-admin-meeting" = "meeting-admin-meeting-search",
  "meeting-admin-presentation-material" = "meeting-admin-presentation-material-search",
  "role-admin-role" = "role-admin-role-search",
  "role-admin-user" = "role-admin-user-search",
  "operasional-admin-user" = "operasional-admin-search",
  "notification-admin" = "notification-admin-search",
}

export enum searchLabel {
  "dashboard.assignment.v2.penugasan.search" = "List Penugasan",
  "dashboard.assignment.v2.arahan.search" = "List Arahan",
  "dashboard.document.v2.materi.search" = "List Document",
  "dashboard.document.v2.hasil.search" = "List Document",
  "dashboard.workspace.v2.search" = "List Workspace",
  "content-admin-predefine-search" = "List Content",
  "content-admin-ongoing-search" = "List Content",
  "meeting-admin-meeting-search" = "List Meeting",
  "meeting-admin-presentation-material-search" = "List Meeting",
  "role-admin-role-search" = "List Role",
  "role-admin-user-search" = "Pegawai",
  "v2-history-search" = "List Event",
  "operasional-admin-search" = "List User",
  "notification-admin-search" = "List Notification",
}
