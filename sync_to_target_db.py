def sync_to_target_db(update_unit, target_db):
    
    updateItem = []
    updateContent = []

    if update_unit['type'] == 'update':
        updateItems = update_unit['update_items']
        updateContent = update_unit['update_content']
        for i in updateItems:
            for j in updateContent:
                cond = updateContent[j]
                target_db.pgsUpdate(j,(cond,i))

    elif update_unit['type'] == 'insert':
        updateContent = update_unit['update_content']
        print(updateContent)
        paramsTemp = []
        for i in updateContent:
            paramsTemp.append(updateContent[i])
        params = tuple(paramsTemp)
        target_db.pgsInsert(params)

    else:
        updateItems = update_unit['update_items']
        for i in updateItems:
            #print(i)
            target_db.pgsDelete(i)
