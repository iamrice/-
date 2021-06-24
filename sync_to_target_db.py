def sync_to_target_db(update_unit, target_db):
    '''
        TODO:
            1. 将内容更新至目标端
        Args:
            1. update_unit
            2. target_db
        Return:
            none
    '''    
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
        updateItem = update_unit['update_items']
        paramsTemp = []
        for i in updateItem:
            paramsTemp.append(updateItem[i])
        params = tuple(paramsTemp)
        target_db.pgsInsert(params)

    else update_unit['type'] == 'delete':
        updateContent = update_unit['update_content']
        for i in updateContent:
            target_db.pgsDelete(i)
