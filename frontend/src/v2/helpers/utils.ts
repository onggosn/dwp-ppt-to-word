import { TResponsePromise } from "@v2/Type.d";
import sanitizeHtml from "sanitize-html";
import store from "@/store";
import { encrypt, decrypt } from "@/library/CryptoHelper";

//local type
type TResponse = {
  success: (res: TResponsePromise, callback?: () => void) => void;
  error: (err: any) => void;
};

export function formatBytes(bytes: number, decimals = 2): string {
  if (!+bytes) return "0.00 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}

export function redirectToBisa(
  withCurrentPath = false,
  currentPath?: string
): void {
  const baseUrl = process.env.VUE_APP_URI_BISA;
  if (!baseUrl) {
    return;
  }
  if (!withCurrentPath) {
    window.location.href = `${baseUrl}`;
    return;
  }
  const resolvedCurrentPath =
    currentPath ?? window.location.pathname.replace(/^\/+/, "");
  window.location.href = resolvedCurrentPath
    ? `${baseUrl}?to=${encodeURIComponent(resolvedCurrentPath)}&from=DWP`
    : `${baseUrl}`;
}

// fungsi ini berguna untuk mempersingkat kodingan response dari BE
export function responsePromise(root: any): TResponse {
  return {
    success: function (res: TResponsePromise, callback?: () => void) {
      if (res.responseCode === "011000") {
        root.refs.toast.show({
          message: res.responseData?.description ?? "Successfully",
          color: "success",
          timeout: 3000,
        });
        if (typeof callback === "function") {
          callback();
        }
      } else if (["011024", "011002"].includes(res.responseCode)) {
        root.refs.toast.show({
          message: res.responseMessage ?? "internal server error",
          color: "warning",
          timeout: 3000,
        });
      } else if (["011016"].includes(res.responseCode)) {
        root.refs.toast.show({
          message: res.responseMessage ?? "internal server error",
          color: "error",
          timeout: 3000,
        });
      } else {
        root.refs.toast.show({
          message: res.responseMessage ?? "internal server error",
          color: "danger",
          timeout: 3000,
        });
      }
    },
    error: function (err: any) {
      err = err.response.data as TResponsePromise;
      root.refs.toast.show({
        message: err.responseMessage ?? "internal server error",
        color: "error",
        timeout: 3000,
      });
    },
  };
}

/**
 * Push number and ignore duplicates.
 * @param {number[]} originalArr - [1, 2, 3, 4, 5]
 * @param {number[]} arrToPush - [2, 3, 6]
 * @return {number[]} - [1, 2, 3, 4, 5, 6]
 */

export function addUniqueArr(originalArr: number[], arrToPush: number[]) {
  const uniqueNumbers = new Set(originalArr);

  arrToPush.forEach((num) => uniqueNumbers.add(num));

  const newArray = Array.from(uniqueNumbers);

  return newArray;
}

export function generateLabelMetadata(input: string) {
  return input == "" ? "-" : input;
}

export function formattedSectionName(input: string) {
  if (input) {
    const result = input.replace(/&lt;br\s*\/?&gt;/g, "<br>");
    return sanitizeHtml(result);
  }
  return "";
}

export function getFontFace(documentType: number) {
  return [3, 9].includes(documentType) ? "Tahoma" : "Frutiger 45 Light";
}

export function filterHTMLTag(text: string) {
  const htmlRegex = /<[^>]*>/;

  const result = text.replace(new RegExp(htmlRegex, "g"), "").trim();

  return result;
}

export function getMaxDay(dateString: string): number {
  const month = new Date(dateString).getMonth();
  const year = new Date(dateString).getFullYear();

  return new Date(year, month + 1, 0).getDate();
}

export function secureRandomFloat(min = 0, max = 10) {
  const array = new Uint32Array(1);
  window.crypto.getRandomValues(array);
  const randomNumber = array[0] / 0xffffffff;
  return min + randomNumber * (max - min);
}

export function isNotEmptyObject(obj: Record<string, any>) {
  return Object.keys(obj).length > 0;
}

export function getTitleTab(value: string) {
  const level = value
    .split(" ")[0]
    .split(".")
    .filter((el) => el).length;
  switch (level) {
    case 2:
      return "14px";
    case 3:
      return "36px";
    case 4:
      return "74px";
    case 5:
      return "104px";
    default:
      return "14px";
  }
}

export function getCkEditorLicense(store: any): string {
  return (
    store?.getters?.["userStore/getInitializeConfig"]?.ckEditor?.license || ""
  );
}

export function getEditorInlineConfig({ store, channelId, withCollab }) {
  const dynamicCkEditorLicense = getCkEditorLicense(store);

  const baseConfig: any = {
    placeholder: "",
    licenseKey: dynamicCkEditorLicense,
    updateSourceElementOnDestroy: false,
    cloudServices: {
      tokenUrl: () =>
        new Promise((resolve) => {
          // Use action instead of getter to properly handle async decryption
          store
            .dispatch("userStore/getDecryptedCKEditorToken")
            .then((tokenData) => {
              const token = tokenData?.ResponseData?.value;
              resolve(token);
            })
            .catch((error) => {
              console.error("Error getting CKEditor token:", error);
              // Fallback: try to get from getter (might be Promise)
              setTimeout(async () => {
                try {
                  const fallbackToken = await store.dispatch(
                    "userStore/getDecryptedCKEditorToken"
                  );
                  if (fallbackToken instanceof Promise) {
                    fallbackToken
                      .then((resolvedToken) => {
                        resolve(resolvedToken?.ResponseData?.value);
                      })
                      .catch((fallbackError) => {
                        console.error(
                          "Fallback token retrieval failed:",
                          fallbackError
                        );
                        resolve(null);
                      });
                  } else {
                    resolve(fallbackToken?.ResponseData?.value);
                  }
                } catch (fallbackError) {
                  console.error(
                    "Fallback token retrieval failed:",
                    fallbackError
                  );
                  resolve(null);
                }
              }, 1500);
            });
        }),
      webSocketUrl: process.env.VUE_APP_WEBSOCKET,
      bundleVersion: process.env.VUE_APP_CKEDITOR_BUNDLE_VERSION,
    },
    ckbox: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(async () => {
            const token = await store.dispatch(
              "userStore/getDecryptedCKBoxToken"
            );
            resolve(token);
          }, 1500);
        }),
      serviceOrigin: process.env.VUE_APP_CKBOX,
    },
    exportPdf: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(async () => {
            const token = await store.dispatch(
              "userStore/getDecryptedDocumentToken"
            );
            resolve(token);
          }, 1500);
        }),
      stylesheets: [
        "/doc/fonts.css",
        "/doc/style.css",
        "/doc/ckeditor5-premium-features.css",
        "/doc/ckeditor5.css",
      ],
      converterOptions: {
        format: "A4",
        margin_top: "20mm",
        margin_bottom: "20mm",
        margin_right: "24mm",
        margin_left: "24mm",
        page_orientation: "portrait",
      },
      converterUrl: process.env.VUE_APP_EXPORT_PDF,
    },
    importWord: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(async () => {
            const token = await store.dispatch(
              "userStore/getDecryptedDocumentToken"
            );
            resolve(token);
          }, 1500);
        }),
      converterUrl: process.env.VUE_APP_IMPORT_WORD,
      formatting: {
        resets: "none",
        defaults: "none",
        styles: "inline",
        comments: "none",
      },
    },
    exportWord: {
      fileName: "document.docx",
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(async () => {
            const token = await store.dispatch(
              "userStore/getDecryptedDocumentToken"
            );
            resolve(token);
          }, 1500);
        }),
      converterUrl: process.env.VUE_APP_EXPORT_WORD,
      stylesheets: [
        "/doc/fonts.css",
        "/doc/style.css",
        "/doc/ckeditor5-premium-features.css",
        "/doc/ckeditor5.css",
      ],
      converterOptions: {
        document: {
          size: "A4",
          orientation: "portrait",
          margin: {
            top: "20mm",
            bottom: "20mm",
            right: "12mm",
            left: "12mm",
          },
          language: "en",
        },
      },
      dataCallback: (editor) => editor.getData({ pagination: true }),
    },
    presenceList: {
      container: document.querySelector(`.presenceListRef-${channelId}`),
      collapseAt: 4,
      displayMe: true,
    },
    collaboration: {
      channelId: channelId,
    },
    revisionHistory: {
      editorContainer: document.querySelector(`.editorContainer-${channelId}`),
      viewerContainer: document.querySelector(
        `.revisionContainer-${channelId}`
      ),
      viewerEditorElement: document.querySelector(
        `.revisionEditorContainer-${channelId}`
      ),
      viewerSidebarContainer: document.querySelector(
        `.revisionSidebar-${channelId}`
      ),
      resumeUnsavedRevision: true,
    },
  };

  if (!withCollab) {
    baseConfig.removePlugins = [
      "Comments",
      "TrackChanges",
      "RevisionHistory",
      "RealTimeCollaborativeComments",
      "RealTimeCollaborativeTrackChanges",
      "RealTimeCollaborativeRevisionHistory",
      "RealTimeCollaborativeEditing",
    ];
    baseConfig.toolbar = [
      "undo",
      "redo",
      "heading",
      "|",
      "bold",
      "italic",
      "underline",
      "strikethrough",
      "formatPainter",
      "superscript",
      "subscript",
      "removeFormat",
      "|",
      "link",
      "imageInsert",
      "ckboxImageEdit",
      "ckbox",
      "insertTable",
      // "insertTableLayout",
      {
        label: "Fonts",
        icon: "text",
        items: [
          "fontFamily",
          "fontSize",
          "fontColor",
          "caseChange",
          "fontBackgroundColor",
        ],
      },
      "alignment",
      "|",
      "bulletedList",
      "numberedList",
      "outdent",
      "indent",
      "|",
      "findAndReplace",
      "specialCharacters",
      "blockQuote",
      "highlight",
      // "revisionHistory",
      // "comment",
      // "commentsArchive",
      "importWord",
      // "trackChanges",
    ];
  }
  return baseConfig;
}

export function removeIrregulerSpace(text: string): string {
  // replace irregular space in string html
  return text.replace(
    // eslint-disable-next-line no-control-regex
    /[\u000B\u000C\u00A0\u1680\u180E\u2000-\u200A\u200B\u2028\u2029\u202F\u205F\u3000\uFEFF]/g,
    ""
  );
}

export function getEditorDocumentConfig(store) {
  const baseConfig: any = {
    placeholder: "",
    initialData: "<p>Hello World!</p>",
    licenseKey: getCkEditorLicense(store),
    ckbox: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(async () => {
            const token = await store.dispatch(
              "userStore/getDecryptedCKBoxToken"
            );
            resolve(token);
          }, 1500);
        }),
      serviceOrigin: process.env.VUE_APP_CKBOX,
    },
    pagination: {
      // A4
      pageWidth: "210mm",
      pageHeight: "297mm",
      pageMargins: {
        top: "20mm",
        bottom: "20mm",
        right: "12mm",
        left: "12mm",
      },
    },
    removePlugins: [
      "SourceEditingEnhanced",
      "Comments",
      "PresenceList",
      "RealTimeCollaborativeComments",
      "RealTimeCollaborativeEditing",
      "RealTimeCollaborativeTrackChanges",
      "TrackChanges",
    ],
    htmlSupport: {
      allow: [
        {
          name: "figure",
          styles: true,
        },
        {
          name: "li",
          classes: ["type-heading"],
        },
        {
          name: "div",
          classes: [
            "title-level-1",
            "title-level-2",
            "title-level-3",
            "title-level-4",
            "title-level-5",
            "content-level-1",
            "content-level-2",
            "content-level-3",
            "content-level-4",
            "content-level-5",
            "title-document",
            "text-version-1",
            "chip-version",
            "justify-right",
          ],
          styles: true,
        },
        {
          name: "tr",
          classes: ["blank-space"],
          styles: true,
        },
        {
          name: "p",
          classes: ["spacing-1", "spacing-1-5", "spacing-2"],
          styles: true,
        },
        {
          name: /^h[1-6]$/,
          styles: true,
        },
        {
          name: "table",
          classes: [
            "table-kop-surat",
            "section-header-letter",
            "table-width-full",
            "layout-table",
          ],
        },
        {
          name: "ol",
          styles: true,
          attributes: {
            start: true,
          },
        },
        {
          name: "span",
          styles: true,
        },
      ],
      disallow: [],
    },
    exportPdf: {
      tokenUrl: () =>
        new Promise((resolve) => {
          setTimeout(async () => {
            const token = await store.dispatch(
              "userStore/getDecryptedDocumentToken"
            );
            resolve(token);
          }, 1500);
        }),
      stylesheets: [
        "/doc/fonts.css",
        "/doc/style.css",
        "/doc/ckeditor5-premium-features.css",
        "/doc/ckeditor5.css",
      ],
      converterOptions: {
        format: "A4",
        margin_top: "20mm",
        margin_bottom: "20mm",
        margin_right: "24mm",
        margin_left: "24mm",
        page_orientation: "portrait",
      },
      converterUrl: process.env.VUE_APP_EXPORT_PDF,
    },
  };

  return baseConfig;
}

export function toSlug(input: string): string {
  if (typeof input !== "string") {
    return "";
  }

  return input.trim().toLowerCase().replace(/\s/g, "");
}

export function getFileExtension(filename) {
  if (!filename || typeof filename !== "string") {
    return "";
  }
  const parts = filename.split(".");
  return parts[parts.length - 1];
}

export function getEditorFAQConfig(store, channelId) {
  return {
    initialData: "",
    licenseKey: getCkEditorLicense(store),
    collaboration: {
      channelId: channelId,
    },
    presenceList: {
      container: null as HTMLElement | null, // Will be set dynamically
    },
    cloudServices: {
      tokenUrl: () =>
        new Promise((resolve) => {
          // Use action instead of getter to properly handle async decryption
          store
            .dispatch("userStore/getDecryptedCKEditorToken")
            .then((tokenData) => {
              const token = tokenData?.ResponseData?.value;
              resolve(token);
            })
            .catch((error) => {
              console.error("Error getting CKEditor token:", error);
              // Fallback: try to get from getter (might be Promise)
              setTimeout(async () => {
                try {
                  const fallbackToken = await store.dispatch(
                    "userStore/getDecryptedCKEditorToken"
                  );
                  if (fallbackToken instanceof Promise) {
                    fallbackToken
                      .then((resolvedToken) => {
                        resolve(resolvedToken?.ResponseData?.value);
                      })
                      .catch((fallbackError) => {
                        console.error(
                          "Fallback token retrieval failed:",
                          fallbackError
                        );
                        resolve(null);
                      });
                  } else {
                    resolve(fallbackToken?.ResponseData?.value);
                  }
                } catch (fallbackError) {
                  console.error(
                    "Fallback token retrieval failed:",
                    fallbackError
                  );
                  resolve(null);
                }
              }, 1500);
            });
        }),
      webSocketUrl: process.env.VUE_APP_WEBSOCKET,
      bundleVersion: process.env.VUE_APP_CKEDITOR_BUNDLE_VERSION,
    },
    removePlugins: [
      "MediaEmbed",
      "Comments",
      "TrackChanges",
      "RealTimeCollaborativeComments",
      "RealTimeCollaborativeTrackChanges",
    ],
  };
}

export function sanitizeUrl(url: string) {
  if (!url) return "";

  const sanitizedUrl = sanitizeHtml(url, {
    allowedTags: [],
    allowedAttributes: {},
    disallowedTagsMode: "discard",
    allowedSchemes: ["http", "https", "mailto", "tel"],
    allowedSchemesByTag: {},
  });

  if (sanitizedUrl.toLowerCase().includes("javascript:")) {
    return "#";
  }

  return sanitizedUrl;
}

export function sanitizeLinkText(text: string) {
  if (!text) return "";

  return sanitizeHtml(text, {
    allowedTags: [],
    allowedAttributes: {},
    disallowedTagsMode: "discard",
  });
}

export async function addApiVersion(
  text: string | undefined,
  apiVersion = "v1"
) {
  if (!text) return undefined;

  const decryptedData = await decrypt(text, store);
  const { json } = await encrypt({ ...decryptedData, apiVersion }, store);

  return json;
}

// content / document paper size (pixels)
export const paperSize = {
  A4: { width: 795, height: 1122 },
  letter: { width: 816, height: 1056 },
};
