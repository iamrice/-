"""
1. 一个字典：{type:'', update_items:[],update_content:{}}，字典中的两个成员分别对应 TODO 中的两部分
			e.g.{type:'update',update_items:['001','008'],update_content:{'course':'math','time':'monday'}} 注：course和time应当是目标端的属性名，不是源端的。
			e.g.{type:'insert',update_items:[],update_content:{'course_id':'009','course_start_time':'2020-09-01'}}
			e.g.{type:'delete',update_items:['001','008'],update_content:{}}

			update_content['start_time'].strftime('%Y-%m-%d')
"""
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
        updateItem = update_unit['update_items']
        paramsTemp = []
        for i in updateItem:
            value = ""
            if i == "course_start_time" or i == "course_end_time": 
                value = updateItem[i].strftime('%Y-%m-%d')
            else:
                value = updateItem[i]
            paramsTemp.append(value)
        params = tuple(paramsTemp)
        target_db.pgsInsert(params)

    else update_unit['type'] == 'delete':
        updateContent = update_unit['update_content']
        for i in updateContent:
            target_db.pgsDelete(i)

