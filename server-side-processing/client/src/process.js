export const processData = (allSDK, selectedSDK, sdkappData) => {
  // Traverse all sdks once to generate:
  // 1) A matrix in which every element corresponds to a box in the heatmap and holds the accumulated value
  // 2) An array of objects (sdks_table) where every element corresponds to a sdk and holds an array of related apps

  let matrix = [];

  // First insert None/None

  matrix.push({
    from_id: 0,
    to_id: 0,
    from_name: "(none)",
    to_name: "(none)",
    value: 0,
  });

  const sdks_table = allSDK.map(function (sdk_element) {
    if (selectedSDK.includes(sdk_element.id)) {
      matrix.push(
        {
          from_id: sdk_element.id,
          to_id: 0,
          from_name: sdk_element.name,
          to_name: "(none)",
          value: 0,
        },
        {
          from_id: 0,
          to_id: sdk_element.id,
          from_name: "(none)",
          to_name: sdk_element.name,
          value: 0,
        }
      );

      allSDK.map(function (sdk_element_iter) {
        // Cycle over all the sdks and check if they are included in the selection
        // If "from" and "to" are both included, then add to the matrix

        if (selectedSDK.includes(sdk_element_iter.id)) {
          matrix.push({
            from_id: sdk_element.id,
            to_id: sdk_element_iter.id,
            from_name: sdk_element.name,
            to_name: sdk_element_iter.name,
            value: 0,
          });
        }
      });
    }

    return {
      id: sdk_element.id,
      not_installed: sdkappData.filter(
        (app_sdk_element) =>
          app_sdk_element.sdk_id == sdk_element.id &&
          app_sdk_element.installed == 0
      ),
      still_installed: sdkappData.filter(
        (app_sdk_element) =>
          app_sdk_element.sdk_id == sdk_element.id &&
          app_sdk_element.installed == 1
      ),
    };
  });

  // Traverse sdks_table and for each sdk:
  // 1) For each app still using the sdk add 1 to the value of the corresponding node in the matrix (hence corresponding box)
  // 2) For each app not using the sdk anymore, find what sdks now have the customer and add 1 to the corresponding node

  sdks_table.forEach(function (sdks_table_element) {
    sdks_table_element.still_installed.forEach(function (installed) {
      matrix.forEach(function (sdk) {
        if (sdk.from_id == installed.sdk_id && sdk.to_id == installed.sdk_id) {
          sdk.value += 1;
        }
      });
    });

    sdks_table_element.not_installed.forEach(function (not_installed) {
      sdks_table.forEach(function (sdks_table_element_iter) {
        sdks_table_element_iter.still_installed.forEach(function (installed) {
          if (installed.app_id == not_installed.app_id) {
            if (
              selectedSDK.includes(not_installed.sdk_id) &&
              selectedSDK.includes(installed.sdk_id)
            ) {
              matrix.forEach(function (sdk) {
                if (
                  sdk.from_id == not_installed.sdk_id &&
                  sdk.to_id == installed.sdk_id
                ) {
                  sdk.value += 1;
                }
              });
            } else if (
              selectedSDK.includes(not_installed.sdk_id) &&
              !selectedSDK.includes(installed.sdk_id)
            ) {
              matrix.forEach(function (sdk) {
                if (sdk.from_id == not_installed.sdk_id && sdk.to_id == 0) {
                  sdk.value += 1;
                }
              });
            } else if (
              !selectedSDK.includes(not_installed.sdk_id) &&
              selectedSDK.includes(installed.sdk_id)
            ) {
              matrix.forEach(function (sdk) {
                if (sdk.from_id == 0 && sdk.to_id == installed.sdk_id) {
                  sdk.value += 1;
                }
              });
            } else if (
              !selectedSDK.includes(not_installed.sdk_id) &&
              !selectedSDK.includes(installed.sdk_id)
            ) {
              matrix.forEach(function (sdk) {
                if (sdk.from_id == 0 && sdk.to_id == 0) {
                  sdk.value += 1;
                }
              });
            }
          }
        });
      });
    });
  });

  return matrix;
};
