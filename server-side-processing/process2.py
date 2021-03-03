def processData2(allSDK, sdkappData, selectedSDKs):
    
    hashtable = {}
    for sdkapp in sdkappData:
        if sdkapp['app_id'] in hashtable:
            if sdkapp['installed'] == 0:
                hashtable[sdkapp['app_id']]['not_installed'].append(sdkapp['sdk_id'])
            elif sdkapp['installed'] == 1:
                hashtable[sdkapp['app_id']]['installed'].append(sdkapp['sdk_id'])
        else:
            hashtable[sdkapp['app_id']] = {}
            hashtable[sdkapp['app_id']]['installed'] = []
            hashtable[sdkapp['app_id']]['not_installed'] = []
            hashtable[sdkapp['app_id']]['value'] = 0

            if sdkapp['installed'] == 0:
                hashtable[sdkapp['app_id']]['not_installed'].append(sdkapp['sdk_id'])
            elif sdkapp['installed'] == 1:
                hashtable[sdkapp['app_id']]['installed'].append(sdkapp['sdk_id'])

    matrix = []
    matrix.append({'from_id': 0, 'to_id': 0, 'from_name': '(none)', 'to_name': '(none)', 'value': 0})

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

    for app in hashtable.values():
        print(app['installed'])
        # for installed in app['installed']:
        #     for sdk in matrix:
        #         if sdk['from_id'] == installed['sdk_id'] and sdk['to_id'] == installed['sdk_id']:
        #             sdk['value'] += 1
        # for not_installed in app['not_installed']:
        #     for installed in app['installed']:
        #         for sdk in matrix:
        #             if sdk['from_id'] == not_installed['sdk_id'] and sdk['to_id'] == installed['sdk_id']:
        #                 sdk['value'] += 1
