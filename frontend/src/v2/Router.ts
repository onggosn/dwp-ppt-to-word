import { RouteRecordRaw } from "vue-router";
import { omWorkspaceManagementChildren } from "@/v2/modules/omPro/Router";

const router: Array<RouteRecordRaw> = [
  {
    // POC: PPT to Word Convert (Sprint 18 mockup), backend backend/app.py
    path: "ppt-to-word/:docId?",
    name: "v2.ppt-to-word",
    component: () => import("@v2/views/poc/PptToWordView.vue"),
  },
  {
    path: "home",
    name: "v2.home",
    component: () => import("@v2/views/home/HomeView.vue"),
  },
  {
    path: "help",
    name: "v2.help",
    component: () => import("@v2/views/HelpView.vue"),
    children: [
      {
        path: "faq",
        name: "v2.faq",
        component: () => import("@v2/components/faq/ContentView.vue"),
      },
    ],
  },
  {
    path: "hnk",
    name: "v2.hnk",
    component: () => import("@v2/views/admin-management/HnkPlayGroundView.vue"),
    meta: {
      restrictedUsername: "dmpdemo",
    },
  },
  {
    path: "mydashboard",
    name: "v2.mydashboard",
    redirect: "/app/v2/mydashboard/workspace",
    component: () => import("@v2/views/dashboard/DashboardView.vue"),
    children: [
      {
        path: "assignment",
        name: "dashboard.assignment.v2",
        redirect: "/app/v2/mydashboard/assignment/penugasan",
        component: () => import("@v2/views/dashboard/DashboardAssignment.vue"),
        children: [
          {
            path: "penugasan",
            name: "dashboard.assignment.v2.penugasan",
            component: () =>
              import("@/v2/components/dashboard/DhsListPenugasan.vue"),
            children: [
              {
                path: ":id",
                name: "dashboard.assignment.v2.penugasan.id",
                component: () =>
                  import("@/v2/components/dashboard/DhsListPenugasan.vue"),
              },
            ],
          },
          {
            path: "arahan",
            name: "dashboard.assignment.v2.arahan",
            component: () =>
              import("@/v2/components/dashboard/DhsListArahan.vue"),
            children: [
              {
                path: ":id",
                name: "dashboard.assignment.v2.arahan.id",
                component: () =>
                  import("@/v2/components/dashboard/DhsListArahan.vue"),
              },
            ],
          },
        ],
      },
      {
        path: "assignment",
        name: "dashboard.assignment.v2.search",
        component: () => import("@/v2/views/search/SearchView.vue"),
        children: [
          {
            path: "penugasan/search",
            name: "dashboard.assignment.v2.penugasan.search",
            component: () =>
              import("@/v2/components/dashboard/DhsListPenugasan.vue"),
            children: [
              {
                path: ":id",
                name: "dashboard.assignment.v2.penugasan.search.id",
                component: () =>
                  import("@/v2/components/dashboard/DhsListPenugasan.vue"),
              },
            ],
          },
          {
            path: "arahan/search",
            name: "dashboard.assignment.v2.arahan.search",
            component: () =>
              import("@/v2/components/dashboard/DhsListArahan.vue"),
            children: [
              {
                path: ":id",
                name: "dashboard.assignment.v2.arahan.id.search",
                component: () =>
                  import("@/v2/components/dashboard/DhsListArahan.vue"),
              },
            ],
          },
        ],
      },
      {
        path: "document",
        name: "dashboard.document.v2",
        redirect: "/app/v2/mydashboard/document/materi",
        component: () => import("@v2/views/dashboard/DashboardDocument.vue"),
        children: [
          {
            path: "materi",
            name: "dashboard.document.v2.materi",
            component: () =>
              import("@/v2/components/dashboard/DhsListMateri.vue"),
          },
          {
            path: "hasil",
            name: "dashboard.document.v2.hasil",
            component: () =>
              import("@/v2/components/dashboard/DhsListHasil.vue"),
          },
        ],
      },
      {
        path: "document",
        name: "dashboard.document.v2.search",
        component: () => import("@/v2/views/search/SearchView.vue"),
        children: [
          {
            path: "materi/search",
            name: "dashboard.document.v2.materi.search",
            component: () =>
              import("@/v2/components/dashboard/DhsListMateri.vue"),
          },
          {
            path: "hasil/search",
            name: "dashboard.document.v2.hasil.search",
            component: () =>
              import("@/v2/components/dashboard/DhsListHasil.vue"),
          },
        ],
      },
      {
        path: "workspace",
        name: "dashboard.workspace.v2",
        component: () => import("@v2/views/dashboard/DashboardWorkspace.vue"),
      },
      {
        path: "workspace/search",
        name: "dashboard.workspace.v2.search",
        component: () => import("@/v2/views/search/SearchView.vue"),
      },
    ],
  },
  {
    path: "profile",
    name: "home.profile",
    component: () => import("@/views/ProfileView.vue"),
  },
  {
    path: "admin-management",
    name: "v2.admin-management",
    component: () => import("@v2/views/admin-management/AdminViewTab.vue"),
    redirect: "/app/v2/admin-management/content/predefine",
    children: [
      {
        path: "meeting",
        name: "meeting-admin",
        component: () =>
          import("@/v2/components/admin/meeting/ListMeeting.vue"),
        children: [
          {
            path: "meeting",
            name: "meeting-admin-meeting",
            component: () =>
              import("@/v2/components/admin/meeting/MeetingListSection.vue"),
          },
          {
            path: "presentation-material",
            name: "meeting-admin-presentation-material",
            component: () =>
              import(
                "@/v2/components/admin/meeting/PresentationMaterialListSection.vue"
              ),
          },
        ],
      },
      {
        path: "meeting",
        name: "meeting-admin-search",
        component: () => import("@/v2/views/search/SearchView.vue"),
        children: [
          {
            path: "meeting/search",
            name: "meeting-admin-meeting-search",
            component: () =>
              import("@/v2/components/admin/meeting/MeetingListSection.vue"),
          },
          {
            path: "presentation-material/search",
            name: "meeting-admin-presentation-material-search",
            component: () =>
              import(
                "@/v2/components/admin/meeting/PresentationMaterialListSection.vue"
              ),
          },
        ],
      },
      {
        path: "content",
        name: "content-admin",
        component: () => import("@/v2/components/admin/ContentAdmin.vue"),
        children: [
          {
            path: "predefine",
            name: "content-admin-predefine",
            component: () => import("@/v2/components/admin/ListDocument.vue"),
          },
          {
            path: "ongoing",
            name: "content-admin-ongoing",
            component: () => import("@/v2/components/admin/ListOGDocument.vue"),
          },
        ],
      },
      {
        path: "content",
        name: "content-admin-search",
        component: () => import("@/v2/views/search/SearchView.vue"),
        children: [
          {
            path: "predefine/search",
            name: "content-admin-predefine-search",
            component: () => import("@/v2/components/admin/ListDocument.vue"),
          },
          {
            path: "ongoing/search",
            name: "content-admin-ongoing-search",
            component: () => import("@/v2/components/admin/ListOGDocument.vue"),
          },
        ],
      },
      {
        path: "role",
        name: "role-admin",
        component: () => import("@/v2/components/admin/RoleAdmin.vue"),
        redirect: "/app/v2/admin-management/role/role",
        children: [
          {
            path: "role",
            name: "role-admin-role",
            component: () => import("@/v2/components/admin/role/ListRole.vue"),
          },
          {
            path: "user",
            name: "role-admin-user",
            component: () => import("@/v2/components/admin/role/ListUser.vue"),
          },
          {
            path: "adg",
            name: "role-admin-adg",
            component: () => import("@/v2/components/admin/role/ListAdg.vue"),
          },
        ],
      },
      {
        path: "role",
        name: "role-admin-search",
        component: () => import("@/v2/views/search/SearchView.vue"),
        children: [
          {
            path: "role/search",
            name: "role-admin-role-search",
            component: () => import("@/v2/components/admin/role/ListRole.vue"),
          },
          {
            path: "user/search",
            name: "role-admin-user-search",
            component: () => import("@/v2/components/admin/role/ListUser.vue"),
          },
        ],
      },
      // {
      //   path: "operasional",
      //   name: "operasional-admin",
      //   component: () =>
      //     import("@/v2/components/admin/operasional/ContentOperasional.vue"),
      //   children: [
      //     {
      //       path: "user",
      //       name: "operasional-admin-user",
      //       component: () =>
      //         import(
      //           "@/v2/components/admin/operasional/ListUserOperasional.vue"
      //         ),
      //     },
      //   ],
      // },
      {
        path: "faq",
        name: "faq-admin",
        component: () => import("@/v2/components/admin/faq/ListFAQ.vue"),
      },
      {
        path: "faq",
        name: "faq-admin-search",
        component: () => import("@/v2/views/search/SearchView.vue"),
        children: [
          {
            path: "search",
            name: "faq-admin-list-search",
            component: () => import("@/v2/components/admin/faq/ListFAQ.vue"),
          },
        ],
      },
      {
        path: "notification",
        name: "notification-admin",
        component: () =>
          import("@/v2/components/admin/notification/ListNotification.vue"),
      },
      // {
      //   path: "operasional/user/search",
      //   name: "operasional-admin-search",
      //   component: () => import("@/v2/views/search/SearchView.vue"),
      // },
      {
        path: "notification/search",
        name: "notification-admin-search",
        component: () => import("@/v2/views/search/SearchView.vue"),
      },
    ],
  },
  {
    path: "workspace-management",
    name: "v2.workspace-management",
    redirect: "/app/v2/workspace-management/rdgb",
    component: () =>
      import("@/v2/views/workspace-management/WorkspaceManagementView.vue"),
    children: [
      {
        path: "rdgb",
        name: "v2.rdgb",
        component: () =>
          import("@/v2/views/workspace-management/WorkspaceRDGBView.vue"),
      },
      {
        path: "rdgtk",
        name: "v2.rdgtk",
        component: () =>
          import("@/v2/views/workspace-management/WorkspaceRDGTKView.vue"),
      },
      ...omWorkspaceManagementChildren,
    ],
  },
  {
    path: "workspace-management/:typeRDG/search-result/:keyword",
    name: "v2.search-result",
    component: () =>
      import("@/v2/views/workspace-management/WorkspaceSearchResult.vue"),
    props: true,
  },
  {
    path: "/app/v2/workspace-management/:typeRDG/:idEvent",
    name: "v2.workspace-rdg-detail",
    meta: {
      requiresAuth: true,
    },
    component: () =>
      import(
        "@/v2/views/workspace-management/detail/WorkspaceDetailRDGView.vue"
      ),
  },
  {
    path: "/app/v2/workspace-management/:typeRDG/:idEvent/doc-view",
    name: "v2.rdg-collaboration-all",
    component: () =>
      import("@/v2/views/workspace-management/ViewAllDocument.vue"),
  },
  {
    path: "/app/v2/workspace-management/:typeRDG/:idEvent/doc/:idDoc",
    name: "v2.rdg-collaboration",
    component: () =>
      import("@/v2/views/workspace-management/CollaborationView.vue"),
  },
  // {
  //   path: "assignment-management",
  //   name: "assignment-management",
  //   component: () =>
  //     import("@/v2/views/assignment-management/AssignmentView.vue"),
  //   meta: {
  //     showMobileMenu: false,
  //     hasMobileView: false,
  //   },
  // },
  {
    path: "meeting-management",
    name: "v2.meeting-management",
    component: () =>
      import("@/v2/views/meeting-management/MeetingManagementView.vue"),
    children: [
      {
        path: "filter",
        name: "v2.meeting-management.search",
        component: () =>
          import(
            "@/v2/views/meeting-management/MeetingManagementSearchResult.vue"
          ),
      },
      {
        path: "detail/:idEvent",
        name: "v2.meeting-detail",
        meta: {
          requiresAuth: true,
        },
        component: () => import("@/v2/views/meeting-management/DetailView.vue"),
        children: [
          {
            path: "",
            name: "v2.meeting-detail-description",
            component: () =>
              import(
                "@/v2/views/meeting-management/detail/MeetingDescription.vue"
              ),
          },
          {
            path: "material",
            name: "v2.meeting-detail-material",
            component: () =>
              import(
                "@/v2/views/meeting-management/detail/MeetingMaterial.vue"
              ),
          },
          {
            path: "material/:idMaterial",
            name: "v2.meeting-detail-material-preview",
            component: () =>
              import(
                "@/v2/views/meeting-management/detail/MeetingMaterial.vue"
              ),
          },
          {
            path: "organizer",
            name: "v2.meeting-detail-organizer",
            component: () =>
              import(
                "@/v2/views/meeting-management/detail/MeetingOrganizer.vue"
              ),
          },
          {
            path: "agenda",
            name: "v2.meeting-detail-agenda",
            component: () =>
              import("@/v2/views/meeting-management/detail/MeetingAgenda.vue"),
          },
          {
            path: "result",
            name: "v2.meeting-detail-result",
            component: () =>
              import("@/v2/views/meeting-management/detail/MeetingResult.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "assignmentmanagement-new",
    name: "v2.assignmentmanagement-new",
    component: () =>
      import("@/v2/views/assignment-management/AssignmentView.vue"),
  },
  {
    path: "assignmentmanagement-new/assignment/search",
    name: "assignmentmanagement-new-assignment-search",
    component: () =>
      import("@/v2/views/assignment-management/AssignmentSearchMain.vue"),
  },
  {
    path: "assignmentmanagement-new/arahan/search",
    name: "assignmentmanagement-new-arahan-search",
    component: () =>
      import("@/v2/views/assignment-management/AssignmentSearchMain.vue"),
  },
  {
    path: "suptechbisma",
    name: "v2.suptechbisma",
    component: () => import("@/views/SuptechView.vue"),
    meta: {
      showMobileMenu: false,
      hasMobileView: false,
    },
    children: [
      {
        path: "sektor/:idSektor",
        name: "v2.suptechbisma.sektor",
        component: () => import("@/components/suptech/SuptechPbiComponent.vue"),
        meta: {
          showMobileMenu: true,
        },
      },
    ],
  },
  {
    path: "executive-summary",
    name: "v2.executive-summary",
    component: () => import("@/views/suptech/SuptechExecutiveSummaryView.vue"),
    meta: {
      showMobileMenu: false,
      hasMobileView: false,
    },
  },
  {
    path: "liquidity",
    name: "v2.liquidity",
    component: () => import("@/views/suptech/SuptechLiquidityView.vue"),
    meta: {
      showMobileMenu: false,
      hasMobileView: false,
    },
  },
  {
    path: "credit",
    name: "v2.credit",
    component: () => import("@/views/suptech/SuptechCreditView.vue"),
    meta: {
      showMobileMenu: false,
      hasMobileView: false,
    },
  },
  {
    path: "poltech",
    name: "v2.poltech",
    component: () => import("@/views/PoltechView.vue"),
    meta: {
      showMobileMenu: false,
      hasMobileView: false,
    },
    children: [
      {
        path: "sektor/:idSektor",
        name: "v2.poltech.sektor",
        component: () =>
          import("@/components/poltech/PoltechMenuComponent.vue"),
        children: [
          {
            path: "area/:idArea",
            name: "v2.poltech.sektor.area",
            component: () =>
              import("@/components/poltech/PoltechPbiComponent.vue"),
          },
        ],
      },
    ],
  },
  {
    path: "history",
    name: "v2.history",
    component: () => import("@v2/views/HistoryView.vue"),
  },
  {
    path: "history/search",
    name: "v2-history-search",
    component: () => import("@/v2/views/search/SearchView.vue"),
  },
];
export default router;
