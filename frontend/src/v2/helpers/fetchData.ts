async function fetchData(apiCall: any, requestData: any) {
  try {
    const res = await apiCall(requestData);
    switch (res.responseCode) {
      case "011000":
        if (res.responseData) {
          return res.responseData;
        } else {
          return true;
        }
      default:
        return {};
    }
  } catch (error) {
    return {};
  }
}

export default fetchData;
