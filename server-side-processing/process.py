def processData(allSDK, selectedSDKs, sdkappData):
    
    #Python doesn't allow multiline-lambda so I need to define lambdas as separate functions
    # def lambda1(sdk_element):
    #     if sdk_element['id'] in selectedSDKs:
    #         matrix.append({
    #             'from_id': sdk_element['id'],
    #             'to_id': 0,
    #             'from_name': sdk_element['name'],
    #             'to_name': "(none)",
    #             'value': 0,
    #         })
    #         matrix.append({
    #             'from_id': 0,
    #             'to_id': sdk_element['id'],
    #             'from_name': "(none)",
    #             'to_name': sdk_element['name'],
    #             'value': 0,
    #         })
        
    #     for sdk_element_iter in allSDK:
    #         #Cycle over all the sdks and check if they are included in the selection
    #         #If "from" and "to" are both included, then add to the matrix
    #         if sdk_element_iter['id'] in selectedSDKs:
    #             matrix.append({
    #                 'from_id': sdk_element['id'],
    #                 'to_id': sdk_element_iter['id'],
    #                 'from_name': sdk_element['name'],
    #                 'to_name': sdk_element_iter['name'],
    #                 'value': 0,
    #             })
        # def lambda2(sdk_element_iter):
        #     #Cycle over all the sdks and check if they are included in the selection
        #     #If "from" and "to" are both included, then add to the matrix
        #     if sdk_element_iter.id in selectedSDKs:
        #         matrix.append({
        #             'from_id': sdk_element.id,
        #             'to_id': sdk_element_iter.id,
        #             'from_name': sdk_element.name,
        #             'to_name': sdk_element_iter.name,
        #             'value': 0,
        #         })

        # print(lambda2())
        # map(lambda2, allSDK)
        
    #     return {
    #         'id': sdk_element['id'],
    #         'not_installed': list(filter(lambda app_sdk_element: app_sdk_element['sdk_id'] == sdk_element['id'] and app_sdk_element['installed'] == 0, sdkappData)),
    #         'still_installed': list(filter(lambda app_sdk_element: app_sdk_element['sdk_id'] == sdk_element['id'] and app_sdk_element['installed'] == 1, sdkappData))
    #     }
    
    # sdks_table = list(map(lambda1, allSDK))

    """ 
    Traverse all sdks once to generate:
    1) A matrix in which every element corresponds to a box in the heatmap and holds the accumulated value
    2) An array of objects (sdks_table) where every element corresponds to a sdk and holds an array of related apps 
    """
    
    matrix = []
    matrix.append({'from_id': 0, 'to_id': 0, 'from_name': '(none)', 'to_name': '(none)', 'value': 0})
    sdks_table = []
    for sdk_element in allSDK:
        if sdk_element['id'] in selectedSDKs:
            matrix.append({
                'from_id': sdk_element['id'],
                'to_id': 0,
                'from_name': sdk_element['name'],
                'to_name': "(none)",
                'value': 0,
            })
            matrix.append({
                'from_id': 0,
                'to_id': sdk_element['id'],
                'from_name': "(none)",
                'to_name': sdk_element['name'],
                'value': 0,
            })
            for sdk_element_iter in allSDK:
                if sdk_element_iter['id'] in selectedSDKs:
                    matrix.append({
                        'from_id': sdk_element['id'],
                        'to_id': sdk_element_iter['id'],
                        'from_name': sdk_element['name'],
                        'to_name': sdk_element_iter['name'],
                        'value': 0,
                    })
            sdks_table.append({
                'id': sdk_element['id'],
                'not_installed': list(filter(lambda app_sdk_element: app_sdk_element['sdk_id'] == sdk_element['id'] and app_sdk_element['installed'] == 0, sdkappData)),
                'still_installed': list(filter(lambda app_sdk_element: app_sdk_element['sdk_id'] == sdk_element['id'] and app_sdk_element['installed'] == 1, sdkappData))
            })

    """ 
    Traverse sdks_table and for each sdk:
    1) For each app still using the sdk add 1 to the value of the corresponding node in the matrix (hence corresponding box)
    2) For each app not using the sdk anymore, find what sdks now have the customer and add 1 to the corresponding node 
    """

    for sdks_table_element in sdks_table:
        for installed in sdks_table_element['still_installed']:
            for sdk in matrix:
                if sdk['from_id'] == installed['sdk_id'] and sdk['to_id'] == installed['sdk_id']:
                    sdk['value'] += 1
        for not_installed in sdks_table_element['not_installed']:
            for sdks_table_element_iter in sdks_table:
                for installed in sdks_table_element_iter['still_installed']:
                    if installed['app_id'] == not_installed['app_id']:
                        if not_installed['sdk_id'] in selectedSDKs and installed['sdk_id'] in selectedSDKs:
                            for sdk in matrix:
                                if sdk['from_id'] == not_installed['sdk_id'] and sdk['to_id'] == installed['sdk_id']:
                                    sdk['value'] += 1
                        elif not_installed['sdk_id'] in selectedSDKs and installed['sdk_id'] in selectedSDKs:
                            for sdk in matrix:
                                if sdk['from_id'] == not_installed['sdk_id'] and sdk['to_id'] == 0:
                                    sdk['value'] += 1
                        elif not_installed['sdk_id'] in selectedSDKs and installed['sdk_id'] in selectedSDKs:
                            for sdk in matrix:
                                if sdk['from_id'] == 0 and sdk['to_id'] == installed['sdk_id']:
                                    sdk['value'] += 1
                        elif not_installed['sdk_id'] in selectedSDKs and installed['sdk_id'] in selectedSDKs:
                            for sdk in matrix:
                                if sdk['from_id'] == 0 and sdk['to_id'] == 0:
                                    sdk_value += 1 
   
    return matrix