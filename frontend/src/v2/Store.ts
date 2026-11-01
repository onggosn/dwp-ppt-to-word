//IMPORT MODULE SECTION
import meetingStore from "@v2/stores/Meeting";
import adminStore from "@v2/stores/Admin";
import workspaceStore from "@v2/stores/Workspace";
import eventStore from "@v2/stores/Event";
import userStore from "@v2/stores/User";
import contentStore from "@v2/stores/ContentManagement";
import documentStore from "@v2/stores/Document";
import eFormStore from "@v2/stores/EForm";
import collaborationStore from "@v2/stores/Collaboration";
import materialStore from "@v2/stores/Material";
import assignmentStore from "@v2/stores/Assignment";
import loadingStore from "@v2/stores/Loading";
import RoleMemberStore from "@v2/stores/RoleMember";
import documentsStore from "@v2/stores/Documents";
import historyStore from "@v2/stores/History";
import homeStore from "@v2/stores/Home";
import GlobalStore from "@v2/stores/Global";

const module = {
  eventStore: eventStore,
  userStore: userStore,
  meetingStore: meetingStore,
  workspaceStore: workspaceStore,
  contentStore: contentStore,
  documentStore: documentStore,
  eFormStore: eFormStore,
  collaborationStore: collaborationStore,
  materialStore: materialStore,
  loadingStore: loadingStore,
  adminStore: adminStore,
  assignmentStore: assignmentStore,
  RoleMemberStore: RoleMemberStore,
  documentsStore: documentsStore,
  historyStore: historyStore,
  homeStore: homeStore,
  globalStore: GlobalStore,
};

export default module;
