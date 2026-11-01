export function documentNameToDB(
  documentId,
  userName,
  fileName,
  fileExtension
) {
  var documentName =
    fileName + "_" + documentId + "_" + userName + "_web." + fileExtension;
  return documentName;
}
