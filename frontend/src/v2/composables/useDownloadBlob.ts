import { TExtension } from "../Type";
import { mimeTypes } from "../mock/Contants";

export const useDownloadBlob = (
  data: Blob,
  name: string,
  extension?: TExtension
) => {
  type SupportedExtensions = keyof typeof mimeTypes;

  const ext = extension ? extension.toLowerCase() : name.split(".").pop();

  const blob = new Blob([data], {
    type: data?.type || mimeTypes[ext as SupportedExtensions] || mimeTypes.xlsx,
  });

  const fileName = name?.length ? name : `file.${ext}`;
  const link = document.createElement("a");
  const url = window.URL.createObjectURL(blob);
  link.href = url;
  link.download = fileName.endsWith(`.${ext}`)
    ? fileName
    : `${fileName}.${ext}`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};
