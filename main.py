import pymssql
import os
from texttable import Texttable
import re

# 查询资料
def query(list_name):
    cursor = db.cursor()
    sql = f'SELECT * FROM {list_name}'
    cursor.execute(sql)
    list_data = cursor.fetchall()

    if list_data:
        # 获取列名
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        # 使用 texttable 创建表格
        table = Texttable()
        table.header(column_names)
        
        for item in list_data:
            table.add_row(item)
        
        print(table.draw())
        print(f"以上为全部{list_name}资料信息。")
    else:
        print(f"没有找到{list_name}资料。")

# 添加商品资料
def add_goods():
    while True:
        gid = input("请输入商品编号：")
        
        # 检查商品编号是否已存在
        cursor = db.cursor(as_dict=True)
        sql_check = u"SELECT * FROM Goods WHERE GID = %s"
        cursor.execute(sql_check, gid)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            print("商品编号已存在，请重新输入。")
        else:
            break

    name = input("请输入商品名称：")
    quantity = int(input("请输入库存数量："))
    min_quantity = int(input("请输入库存下限："))
    max_quantity = int(input("请输入库存上限："))
    remarks = input("请输入备注信息：")
    cursor = db.cursor()
    sql = u"INSERT INTO Goods (GID, GName, IQuantity, IMin, IMax, Remarks) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (gid, name, quantity, min_quantity, max_quantity, remarks))
    db.commit()
    cursor.close()
    print("商品资料添加成功。")

# 修改商品资料
def modify_goods():
    query('Goods')
    while True:
        gid = input("请输入要修改的商品编号：")
        
        # 检查商品编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = u"SELECT * FROM Goods WHERE GID = %s"
        cursor.execute(sql_check, gid)
        result = cursor.fetchone()
        cursor.close()
        
        if result == None:
            print("商品编号不存在，请重新输入。")
        else:
            break

    new_name = input("请输入新的商品名称：")
    new_quantity = int(input("请输入新的库存数量："))
    new_min = int(input("请输入新的库存下限："))
    new_max = int(input("请输入新的库存上限："))
    new_remarks = input("请输入新的备注信息：")
    cursor = db.cursor()
    sql = u"UPDATE Goods SET GName=%s, IQuantity=%s, IMin=%s, IMax=%s, Remarks=%s WHERE GID=%s"
    cursor.execute(sql, (new_name, new_quantity, new_min, new_max, new_remarks, gid))
    db.commit()
    cursor.close()
    print("商品资料修改成功。")

# 删除商品资料
def delete_goods():
    query('Goods')
    while True:
        gid = input("请输入要删除的商品编号：")
        
        # 检查商品编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = u"SELECT * FROM Goods WHERE GID = %s"
        cursor.execute(sql_check, gid)
        result = cursor.fetchone()
        cursor.close()
        
        if result == None:
            print("商品编号不存在，请重新输入。")
        else:
            break

    try:
        with db.cursor() as cursor:
            # 检查并删除所有引用该商品编号的记录
            tables = ['Purchase_updates_inventory', 'Return_updates_inventory', 'Sale_updates_inventory', 'Customer_return_updates_inventory']
            for table in tables:
                sql = f"DELETE FROM {table} WHERE GID=%s"
                cursor.execute(sql, gid)
            
            # 删除商品记录
            sql = "DELETE FROM Goods WHERE GID=%s"
            cursor.execute(sql, gid)
            db.commit()
        print("商品资料删除成功。")
    except pymssql.IntegrityError as e:
        db.rollback()
        print(f"删除失败，错误信息: {e}")

# 添加供应商资料
def add_supplier():
    while True:
        supplier_id = input("请输入供货商编号：")
        
        # 检查供货商编号是否已存在
        cursor = db.cursor(as_dict=True)
        sql_check = "SELECT * FROM Supplier WHERE SupplierID = %s"
        cursor.execute(sql_check, supplier_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            print("供货商编号已存在，请重新输入。")
        else:
            break

    name = input("请输入供货商名称：")
    contacts = input("请输入联系人姓名：")
    phone = input("请输入联系人电话：")
    addresses = input("请输入供货商地址：")
    remarks = input("请输入备注信息：")
    cursor = db.cursor()
    sql = "INSERT INTO Supplier (SupplierID, SName, Contacts, Phone, Addresses, Remarks) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (supplier_id, name, contacts, phone, addresses, remarks))
    db.commit()
    cursor.close()
    print("供货商资料添加成功。")

# 修改供应商资料
def modify_supplier():
    query('Supplier')
    while True:
        supplier_id = input("请输入要修改的供货商编号：")
        
        # 检查供货商编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = "SELECT * FROM Supplier WHERE SupplierID = %s"
        cursor.execute(sql_check, supplier_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result == None:
            print("供货商编号不存在，请重新输入。")
        else:
            break

    new_name = input("请输入新的供货商名称：")
    new_contacts = input("请输入新的联系人姓名：")
    new_phone = input("请输入新的联系人电话：")
    new_addresses = input("请输入新的供货商地址：")
    new_remarks = input("请输入新的备注信息：")
    cursor = db.cursor()
    sql = "UPDATE Supplier SET SName=%s, Contacts=%s, Phone=%s, Addresses=%s, Remarks=%s WHERE SupplierID=%s"
    cursor.execute(sql, (new_name, new_contacts, new_phone, new_addresses, new_remarks, supplier_id))
    db.commit()
    cursor.close()
    print("供货商资料修改成功。")

# 删除供应商资料
def delete_supplier():
    query('Supplier')
    while True:
        supplier_id = input("请输入要删除的供货商编号：")
        
        # 检查供货商编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = "SELECT * FROM Supplier WHERE SupplierID = %s"
        cursor.execute(sql_check, supplier_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result == None:
            print("供货商编号不存在，请重新输入。")
        else:
            break

    try:
        with db.cursor() as cursor:
            # 删除与供应商相关的进货单和退货单更新库存记录
            sql = f"DELETE FROM Purchase_updates_inventory WHERE PID IN (SELECT PID FROM Purchase_list WHERE SupplierID=%s)"
            cursor.execute(sql, supplier_id)

            sql = f"DELETE FROM Return_updates_inventory WHERE RID IN (SELECT RID FROM Return_list WHERE SupplierID=%s)"
            cursor.execute(sql, supplier_id)

            # 删除与供应商相关的进货单和退货单记录
            purchase_return_tables = ['Purchase_list', 'Return_list']
            for table in purchase_return_tables:
                sql = f"DELETE FROM {table} WHERE SupplierID=%s"
                cursor.execute(sql, supplier_id)

            # 删除供应商记录
            sql = "DELETE FROM Supplier WHERE SupplierID=%s"
            cursor.execute(sql, supplier_id)
            db.commit()
        print("供货商资料删除成功。")
    except pymssql.IntegrityError as e:
        db.rollback()
        print(f"删除失败，错误信息: {e}")

# 添加客户资料
def add_customer():
    while True:
        customer_id = input("请输入客户编号：")
        
        # 检查客户编号是否已存在
        cursor = db.cursor(as_dict=True)
        sql_check = "SELECT * FROM Customer WHERE CID = %s"
        cursor.execute(sql_check, customer_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            print("客户编号已存在，请重新输入。")
        else:
            break

    name = input("请输入客户名称：")
    contacts = input("请输入联系人姓名：")
    phone = input("请输入联系人电话：")
    addresses = input("请输入客户地址：")
    remarks = input("请输入备注信息：")
    cursor = db.cursor()
    sql = "INSERT INTO Customer (CID, CName, Contacts, Phone, Addresses, Remarks) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (customer_id, name, contacts, phone, addresses, remarks))
    db.commit()
    cursor.close()
    print("客户资料添加成功。")

# 修改客户资料
def modify_customer():
    query('Customer')
    while True:
        customer_id = input("请输入要修改的客户编号：")
        
        # 检查客户编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = "SELECT * FROM Customer WHERE CID = %s"
        cursor.execute(sql_check, customer_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result is None:
            print("客户编号不存在，请重新输入。")
        else:
            break

    new_name = input("请输入新的客户名称：")
    new_contacts = input("请输入新的联系人姓名：")
    new_phone = input("请输入新的联系人电话：")
    new_addresses = input("请输入新的客户地址：")
    new_remarks = input("请输入新的备注信息：")
    cursor = db.cursor()
    sql = "UPDATE Customer SET CName=%s, Contacts=%s, Phone=%s, Addresses=%s, Remarks=%s WHERE CID=%s"
    cursor.execute(sql, (new_name, new_contacts, new_phone, new_addresses, new_remarks, customer_id))
    db.commit()
    cursor.close()
    print("客户资料修改成功。")

# 删除客户资料
def delete_customer():
    query('Customer')
    while True:
        customer_id = input("请输入要删除的客户编号：")
        
        # 检查客户编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = "SELECT * FROM Customer WHERE CID = %s"
        cursor.execute(sql_check, customer_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result is None:
            print("客户编号不存在，请重新输入。")
        else:
            break

    try:
        with db.cursor() as cursor:
            # 删除与客户相关的销售单和客户退货单更新库存记录
            sql = "DELETE FROM Sale_updates_inventory WHERE SLID IN (SELECT SLID FROM Sale_list WHERE CID=%s)"
            cursor.execute(sql, customer_id)

            sql = "DELETE FROM Customer_return_updates_inventory WHERE CRID IN (SELECT CRID FROM Customer_return_list WHERE CID=%s)"
            cursor.execute(sql, customer_id)

            # 删除与客户相关的销售单和客户退货单记录
            sale_return_tables = ['Sale_list', 'Customer_return_list']
            for table in sale_return_tables:
                sql = f"DELETE FROM {table} WHERE CID=%s"
                cursor.execute(sql, customer_id)

            # 删除客户记录
            sql = "DELETE FROM Customer WHERE CID=%s"
            cursor.execute(sql, customer_id)
            db.commit()
        print("客户资料删除成功。")
    except pymssql.IntegrityError as e:
        db.rollback()
        print(f"删除失败，错误信息: {e}")

# 添加用户资料
def add_user():
    while True:
        user_id = input("请输入用户编号：")
        
        # 检查用户编号是否已存在
        cursor = db.cursor(as_dict=True)
        sql_check = u"SELECT * FROM Users WHERE UserID = %s"
        cursor.execute(sql_check, user_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            print("用户编号已存在，请重新输入。")
        else:
            break

    user_name = input("请输入用户名：")
    password = input("请输入用户密码：")

    while True:
        permission = input("请输入用户权限(A或U):")
        if permission in ['A', 'U']:
            break
        else:
            print("输入无效，请输入'A'或'U'。")

    remarks = input("请输入备注信息：")

    cursor = db.cursor()
    sql = u"INSERT INTO Users (UserID, UName, Passwords, Permission, Remarks) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, user_name, password, permission, remarks))
    db.commit()
    cursor.close()
    print("用户资料已成功添加。")

# 修改用户资料
def modify_user():
    query('Users')
    while True:
        user_id = input("请输入要修改的用户编号：")
        
        # 检查商品编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = u"SELECT * FROM Users WHERE UserID = %s"
        cursor.execute(sql_check, user_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result == None:
            print("用户编号不存在，请重新输入。")
        else:
            break

    new_name = input("请输入新的用户名：")
    new_password = input("请输入新的用户密码：")

    while True:
        new_permission = input("请输入用户权限(A或U):")
        if new_permission in ['A', 'U']:
            break
        else:
            print("输入无效，请输入'A'或'U'。")

    new_remarks = input("请输入新的备注信息：")
    cursor = db.cursor()
    sql = u"UPDATE Users SET UName=%s, Passwords=%s, Permission=%s, Remarks=%s WHERE UserID=%s"
    cursor.execute(sql, (new_name, new_password, new_permission, new_remarks, user_id))
    db.commit()
    cursor.close()
    print("用户资料修改成功。")

# 删除用户资料
def delete_user():
    query('Users')
    while True:
        user_id = input("请输入要删除的用户编号：")
        
        # 检查商品编号是否存在
        cursor = db.cursor(as_dict=True)
        sql_check = u"SELECT * FROM Users WHERE UserID = %s"
        cursor.execute(sql_check, user_id)
        result = cursor.fetchone()
        cursor.close()
        
        if result == None:
            print("用户编号不存在，请重新输入。")
        else:
            break

    try:
        with db.cursor() as cursor:
            # 删除用户记录
            sql = "DELETE FROM Users WHERE UserID=%s"
            cursor.execute(sql, user_id)
            db.commit()
        print("用户资料删除成功。")
    except pymssql.IntegrityError as e:
        db.rollback()
        print(f"删除失败，错误信息: {e}")

# 进货单明细查询
def query_purchase_details():
    cursor = db.cursor()
    cursor.execute("SELECT PID FROM Purchase_list")
    purchase_ids = cursor.fetchall()
    
    if purchase_ids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["可查询的进货订单号"])
        for pid in purchase_ids:
            table.add_row([pid[0]])
        
        print(table.draw())
    else:
        print("没有可查询的进货订单号。")
    
    while True:
        order_id = input("请输入要查询的进货订单号：")
        if (order_id,) not in purchase_ids:
            print("订单号不存在，请重新输入。")
        else:
            break
    
    query = "SELECT GID, GNum, Price FROM Purchase_updates_inventory WHERE PID = %s"
    cursor.execute(query, (order_id,))
    results = cursor.fetchall()
    
    if results:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "进货数量", "商品单价"])
        
        for row in results:
            table.add_row([row[0], row[1], row[2]])
        
        print(f"进货订单号 {order_id} 的商品详细信息如下：")
        print(table.draw())
    else:
        print("该订单号没有商品详细信息。")
    cursor.close()

# 退货单明细查询
def query_return_details():
    cursor = db.cursor()
    cursor.execute("SELECT RID FROM Return_list")
    return_ids = cursor.fetchall()
    
    if return_ids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["可查询的退货订单号"])
        for rid in return_ids:
            table.add_row([rid[0]])
        
        print(table.draw())
    else:
        print("没有可查询的退货订单号。")
    
    while True:
        order_id = input("请输入要查询的退货订单号：")
        if (order_id,) not in return_ids:
            print("订单号不存在，请重新输入。")
        else:
            break
    
    query = "SELECT GID, GNum, Price FROM Return_updates_inventory WHERE RID = %s"
    cursor.execute(query, (order_id,))
    results = cursor.fetchall()
    
    if results:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "退货数量", "商品单价"])
        
        for row in results:
            table.add_row([row[0], row[1], row[2]])
        
        print(f"退货订单号 {order_id} 的商品详细信息如下：")
        print(table.draw())
    else:
        print("该订单号没有商品详细信息。")
    cursor.close()

# 日期检验
def is_valid_date(date_str):
    # 使用正则表达式检查日期格式是否为 YYYY-MM-DD
    return re.match(r'^\d{4}-\d{2}-\d{2}$', date_str) is not None

# 添加进货单
def add_purchase_order():
    cursor = db.cursor()
    cursor.execute("SELECT PID FROM Purchase_list")
    existing_pids = cursor.fetchall()
    
    if existing_pids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的进货订单号"])
        for pid in existing_pids:
            table.add_row([pid[0]])
        
        print(table.draw())
    else:
        None
    
    # 获取用户输入的进货单信息
    while True:
        pid = input("请输入进货单编号: ")
        if (pid,) in existing_pids:
            print("进货单编号已存在，请重新输入。")
        else:
            break

    # 获取已有的供货商编号
    cursor.execute("SELECT SupplierID FROM Supplier")
    existing_supplier_ids = cursor.fetchall()
    
    if existing_supplier_ids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的供货商编号"])
        for sid in existing_supplier_ids:
            table.add_row([sid[0]])
        
        print(table.draw())
    else:
        print("没有供应商编号，请先添加供应商！")
        return
    
    # 获取用户输入的供货商编号
    while True:
        supplier_id = input("请输入供货商编号: ")
        if (supplier_id,) not in existing_supplier_ids:
            print("供货商编号不存在，请重新输入。")
        else:
            break

    # 暂时将金额设为0
    amount_paid = float(0)
    
    while True:
        pdate = input("请输入进货日期 (格式: YYYY-MM-DD): ")
        if not is_valid_date(pdate):
            print("日期格式错误，请重新输入。")
        else:
            break

    # 插入进货单信息到数据库
    query = "INSERT INTO Purchase_list (PID, SupplierID, Amount_paid, PDate) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (pid, supplier_id, amount_paid, pdate))
    db.commit()

    total_amount = 0

    while True:
        # 获取已有的商品编号和商品名称
        cursor.execute("SELECT GID, GName FROM Goods")
        existing_goods = cursor.fetchall()
        
        if existing_goods:
            table = Texttable()
            table.set_deco(Texttable.BORDER | Texttable.HEADER)
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.header(["商品编号", "商品名称"])
            for goods in existing_goods:
                table.add_row([goods[0], goods[1]])
            print(table.draw())
        else:
            print("不存在任何商品，请先添加商品！")
            return
        
        gid = input("请输入商品编号 (输入0结束): ")
        if gid == '0':
            break
        if gid not in [item[0] for item in existing_goods]:
            print("商品编号不存在，请重新输入。")
            continue

        gnum = int(input("请输入进货数量: "))
        price = float(input("请输入商品单价: "))

        # 检查组合主键 (PID, GID) 的唯一性
        cursor.execute("SELECT COUNT(*) FROM Purchase_updates_inventory WHERE PID = %s AND GID = %s", (pid, gid))
        if cursor.fetchone()[0] > 0:
            print("该商品已经在当前进货单中，请选择其他商品。")
            continue

        # 插入进货单更新库存信息到数据库
        query = "INSERT INTO Purchase_updates_inventory (PID, GID, GNum, Price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (pid, gid, gnum, price))
        db.commit()

        # 更新商品表中的库存数量
        query = "UPDATE Goods SET IQuantity = IQuantity + %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

        total_amount += gnum * price

    # 更新进货单的总金额
    query = "UPDATE Purchase_list SET Amount_paid = %s WHERE PID = %s"
    cursor.execute(query, (total_amount, pid))
    db.commit()

    print("进货单添加成功,库存更新成功！")
    cursor.close()

# 修改进货单
def modify_purchase_order():
    cursor = db.cursor()
    
    # 获取已有的进货单编号
    cursor.execute("SELECT PID FROM Purchase_list")
    existing_pids = cursor.fetchall()
    
    if existing_pids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的进货订单号"])
        for pid in existing_pids:
            table.add_row([pid[0]])
        
        print(table.draw())
    else:
        print("没有现有的进货订单号。")
        return
    
    # 获取用户输入的进货单编号
    while True:
        pid = input("请输入要修改的进货单编号: ")
        if (pid,) not in existing_pids:
            print("进货单编号不存在，请重新输入。")
        else:
            break
    
    # 显示当前进货单详细信息
    cursor.execute("SELECT SupplierID, PDate FROM Purchase_list WHERE PID = %s", (pid,))
    purchase_info = cursor.fetchone()
    print(f"当前供应商编号: {purchase_info[0]}")
    print(f"当前进货日期: {purchase_info[1]}")

    cursor.execute("SELECT GID, GNum, Price FROM Purchase_updates_inventory WHERE PID = %s", (pid,))
    purchase_items = cursor.fetchall()

    if purchase_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "进货数量", "商品单价"])
        for item in purchase_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该进货单没有商品信息。")

    # 获取新的供应商编号
    cursor.execute("SELECT SupplierID FROM Supplier")
    existing_supplier_ids = cursor.fetchall()
    
    if existing_supplier_ids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的供货商编号"])
        for sid in existing_supplier_ids:
            table.add_row([sid[0]])
        
        print(table.draw())
    else:
        print("没有供应商编号，请先添加供应商！")
        return
    
    while True:
        new_supplier_id = input("请输入新的供货商编号 (或按回车保持不变): ")
        if not new_supplier_id:
            new_supplier_id = purchase_info[0]
            break
        if (new_supplier_id,) not in existing_supplier_ids:
            print("供货商编号不存在，请重新输入。")
        else:
            break
    
    # 获取新的进货日期
    while True:
        new_pdate = input("请输入新的进货日期 (格式: YYYY-MM-DD，或按回车保持不变): ")
        if not new_pdate:
            new_pdate = purchase_info[1]
            break
        if not is_valid_date(new_pdate):
            print("日期格式错误，请重新输入。")
        else:
            break
    
    # 更新供应商编号和进货日期
    query = "UPDATE Purchase_list SET SupplierID = %s, PDate = %s WHERE PID = %s"
    cursor.execute(query, (new_supplier_id, new_pdate, pid))
    db.commit()

    total_amount = 0

    for item in purchase_items:
        gid, current_gnum, current_price = item

        while True:
            print(f"当前商品编号: {gid}, 进货数量: {current_gnum}, 商品单价: {current_price}")
            gnum = input("请输入新的进货数量 (或按回车保持不变): ")
            if not gnum:
                gnum = current_gnum
                break
            try:
                gnum = int(gnum)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        while True:
            price = input("请输入新的商品单价 (或按回车保持不变): ")
            if not price:
                price = current_price
                break
            try:
                price = float(price)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        # 更新商品信息
        query = "UPDATE Purchase_updates_inventory SET GNum = %s, Price = %s WHERE PID = %s AND GID = %s"
        cursor.execute(query, (gnum, price, pid, gid))
        db.commit()

        # 更新商品表中的库存数量
        quantity_difference = gnum - current_gnum
        query = "UPDATE Goods SET IQuantity = IQuantity + %s WHERE GID = %s"
        cursor.execute(query, (quantity_difference, gid))
        db.commit()

        total_amount += gnum * price

    # 重新计算所有商品的总金额
    cursor.execute("SELECT SUM(GNum * Price) FROM Purchase_updates_inventory WHERE PID = %s", (pid,))
    total_amount = cursor.fetchone()[0]

    # 更新进货单的总金额
    query = "UPDATE Purchase_list SET Amount_paid = %s WHERE PID = %s"
    cursor.execute(query, (total_amount, pid))
    db.commit()

    print("进货单修改成功,库存更新成功！")
    cursor.close()

# 删除进货单
def delete_purchase_order():
    cursor = db.cursor()
    
    # 获取已有的进货单编号
    cursor.execute("SELECT PID FROM Purchase_list")
    existing_pids = cursor.fetchall()
    
    if existing_pids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的进货订单号"])
        for pid in existing_pids:
            table.add_row([pid[0]])
        
        print(table.draw())
    else:
        print("没有现有的进货订单号。")
        return
    
    # 获取用户输入的进货单编号
    while True:
        pid = input("请输入要删除的进货单编号: ")
        if (pid,) not in existing_pids:
            print("进货单编号不存在，请重新输入。")
        else:
            break
    
    # 显示当前进货单详细信息
    cursor.execute("SELECT SupplierID, PDate FROM Purchase_list WHERE PID = %s", (pid,))
    purchase_info = cursor.fetchone()
    print(f"当前供应商编号: {purchase_info[0]}")
    print(f"当前进货日期: {purchase_info[1]}")

    cursor.execute("SELECT GID, GNum, Price FROM Purchase_updates_inventory WHERE PID = %s", (pid,))
    purchase_items = cursor.fetchall()

    if purchase_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "进货数量", "商品单价"])
        for item in purchase_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该进货单没有商品信息。")

    # 确认删除操作
    confirm = input("确定要删除这个进货单吗？(yes/no): ")
    if confirm.lower() != 'yes':
        print("取消删除操作。")
        cursor.close()
        return
    
    # 更新商品表中的库存数量
    for item in purchase_items:
        gid, gnum, _ = item
        query = "UPDATE Goods SET IQuantity = IQuantity - %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

    # 删除进货单相关记录
    query = "DELETE FROM Purchase_updates_inventory WHERE PID = %s"
    cursor.execute(query, (pid,))
    db.commit()

    query = "DELETE FROM Purchase_list WHERE PID = %s"
    cursor.execute(query, (pid,))
    db.commit()

    print("进货单删除成功,库存更新成功！")
    cursor.close()

# 添加退货单
def add_return_order():
    cursor = db.cursor()
    cursor.execute("SELECT RID FROM Return_list")
    existing_rids = cursor.fetchall()
    
    if existing_rids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的退货订单号"])
        for rid in existing_rids:
            table.add_row([rid[0]])
        
        print(table.draw())
    else:
        None
    
    # 获取用户输入的退货单信息
    while True:
        rid = input("请输入退货单编号: ")
        if (rid,) in existing_rids:
            print("退货单编号已存在，请重新输入。")
        else:
            break

    # 获取已有的供货商编号
    cursor.execute("SELECT SupplierID FROM Supplier")
    existing_supplier_ids = cursor.fetchall()
    
    if existing_supplier_ids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的供货商编号"])
        for sid in existing_supplier_ids:
            table.add_row([sid[0]])
        
        print(table.draw())
    else:
        print("没有供应商编号，请先添加供应商！")
        return
    
    # 获取用户输入的供货商编号
    while True:
        supplier_id = input("请输入供货商编号: ")
        if (supplier_id,) not in existing_supplier_ids:
            print("供货商编号不存在，请重新输入。")
        else:
            break

    # 暂时将金额设为0
    amount_paid = float(0)
    
    while True:
        rdate = input("请输入退货日期 (格式: YYYY-MM-DD): ")
        if not is_valid_date(rdate):
            print("日期格式错误，请重新输入。")
        else:
            break

    # 插入退货单信息到数据库
    query = "INSERT INTO Return_list (RID, SupplierID, Amount_paid, RDate) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (rid, supplier_id, amount_paid, rdate))
    db.commit()

    total_amount = 0

    while True:
        # 获取已有的商品编号和商品名称
        cursor.execute("SELECT GID, GName FROM Goods")
        existing_goods = cursor.fetchall()
        
        if existing_goods:
            table = Texttable()
            table.set_deco(Texttable.BORDER | Texttable.HEADER)
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.header(["商品编号", "商品名称"])
            for goods in existing_goods:
                table.add_row([goods[0], goods[1]])
            print(table.draw())
        else:
            print("不存在任何商品，请先添加商品！")
            return
        
        gid = input("请输入商品编号 (输入0结束): ")
        if gid == '0':
            break
        if gid not in [item[0] for item in existing_goods]:
            print("商品编号不存在，请重新输入。")
            continue

        gnum = int(input("请输入退货数量: "))
        price = float(input("请输入商品单价: "))

        # 检查组合主键 (RID, GID) 的唯一性
        cursor.execute("SELECT COUNT(*) FROM Return_updates_inventory WHERE RID = %s AND GID = %s", (rid, gid))
        if cursor.fetchone()[0] > 0:
            print("该商品已经在当前退货单中，请选择其他商品。")
            continue

        # 插入退货单更新库存信息到数据库
        query = "INSERT INTO Return_updates_inventory (RID, GID, GNum, Price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (rid, gid, gnum, price))
        db.commit()

        # 更新商品表中的库存数量
        query = "UPDATE Goods SET IQuantity = IQuantity - %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

        total_amount += gnum * price

    # 更新退货单的总金额
    query = "UPDATE Return_list SET Amount_paid = %s WHERE RID = %s"
    cursor.execute(query, (total_amount, rid))
    db.commit()

    print("退货单添加成功,库存更新成功！")
    cursor.close()

# 修改退货单
def modify_return_order():
    cursor = db.cursor()
    
    # 获取已有的退货单编号
    cursor.execute("SELECT RID FROM Return_list")
    existing_rids = cursor.fetchall()
    
    if existing_rids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的退货订单号"])
        for rid in existing_rids:
            table.add_row([rid[0]])
        
        print(table.draw())
    else:
        print("没有现有的退货订单号。")
        return
    
    # 获取用户输入的退货单编号
    while True:
        rid = input("请输入要修改的退货单编号: ")
        if (rid,) not in existing_rids:
            print("退货单编号不存在，请重新输入。")
        else:
            break
    
    # 显示当前退货单详细信息
    cursor.execute("SELECT SupplierID, RDate FROM Return_list WHERE RID = %s", (rid,))
    return_info = cursor.fetchone()
    print(f"当前供应商编号: {return_info[0]}")
    print(f"当前退货日期: {return_info[1]}")

    cursor.execute("SELECT GID, GNum, Price FROM Return_updates_inventory WHERE RID = %s", (rid,))
    return_items = cursor.fetchall()

    if return_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "退货数量", "商品单价"])
        for item in return_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该退货单没有商品信息。")

    # 获取新的供应商编号
    cursor.execute("SELECT SupplierID FROM Supplier")
    existing_supplier_ids = cursor.fetchall()
    
    if existing_supplier_ids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的供货商编号"])
        for sid in existing_supplier_ids:
            table.add_row([sid[0]])
        
        print(table.draw())
    else:
        print("没有供应商编号，请先添加供应商！")
        return
    
    while True:
        new_supplier_id = input("请输入新的供货商编号 (或按回车保持不变): ")
        if not new_supplier_id:
            new_supplier_id = return_info[0]
            break
        if (new_supplier_id,) not in existing_supplier_ids:
            print("供货商编号不存在，请重新输入。")
        else:
            break
    
    # 获取新的退货日期
    while True:
        new_rdate = input("请输入新的退货日期 (格式: YYYY-MM-DD，或按回车保持不变): ")
        if not new_rdate:
            new_rdate = return_info[1]
            break
        if not is_valid_date(new_rdate):
            print("日期格式错误，请重新输入。")
        else:
            break
    
    # 更新供应商编号和退货日期
    query = "UPDATE Return_list SET SupplierID = %s, RDate = %s WHERE RID = %s"
    cursor.execute(query, (new_supplier_id, new_rdate, rid))
    db.commit()

    total_amount = 0

    for item in return_items:
        gid, current_gnum, current_price = item

        while True:
            print(f"当前商品编号: {gid}, 退货数量: {current_gnum}, 商品单价: {current_price}")
            gnum = input("请输入新的退货数量 (或按回车保持不变): ")
            if not gnum:
                gnum = current_gnum
                break
            try:
                gnum = int(gnum)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        while True:
            price = input("请输入新的商品单价 (或按回车保持不变): ")
            if not price:
                price = current_price
                break
            try:
                price = float(price)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        # 更新商品信息
        query = "UPDATE Return_updates_inventory SET GNum = %s, Price = %s WHERE RID = %s AND GID = %s"
        cursor.execute(query, (gnum, price, rid, gid))
        db.commit()

        # 更新商品表中的库存数量
        quantity_difference = current_gnum - gnum
        query = "UPDATE Goods SET IQuantity = IQuantity + %s WHERE GID = %s"
        cursor.execute(query, (quantity_difference, gid))
        db.commit()

        total_amount += gnum * price

    # 重新计算所有商品的总金额
    cursor.execute("SELECT SUM(GNum * Price) FROM Return_updates_inventory WHERE RID = %s", (rid,))
    total_amount = cursor.fetchone()[0]

    # 更新退货单的总金额
    query = "UPDATE Return_list SET Amount_paid = %s WHERE RID = %s"
    cursor.execute(query, (total_amount, rid))
    db.commit()

    print("退货单修改成功,库存更新成功！")
    cursor.close()

# 删除退货单
def delete_return_order():
    cursor = db.cursor()
    
    # 获取已有的退货单编号
    cursor.execute("SELECT RID FROM Return_list")
    existing_rids = cursor.fetchall()
    
    if existing_rids:
        table = Texttable()
        # table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的退货订单号"])
        for rid in existing_rids:
            table.add_row([rid[0]])
        
        print(table.draw())
    else:
        print("没有现有的退货订单号。")
        return
    
    # 获取用户输入的退货单编号
    while True:
        rid = input("请输入要删除的退货单编号: ")
        if (rid,) not in existing_rids:
            print("退货单编号不存在，请重新输入。")
        else:
            break
    
    # 显示当前退货单详细信息
    cursor.execute("SELECT SupplierID, RDate FROM Return_list WHERE RID = %s", (rid,))
    return_info = cursor.fetchone()
    print(f"当前供应商编号: {return_info[0]}")
    print(f"当前退货日期: {return_info[1]}")

    cursor.execute("SELECT GID, GNum, Price FROM Return_updates_inventory WHERE RID = %s", (rid,))
    return_items = cursor.fetchall()

    if return_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "退货数量", "商品单价"])
        for item in return_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该退货单没有商品信息。")

    # 确认删除操作
    confirm = input("确定要删除这个退货单吗？(yes/no): ")
    if confirm.lower() != 'yes':
        print("取消删除操作。")
        cursor.close()
        return
    
    # 更新商品表中的库存数量
    for item in return_items:
        gid, gnum, _ = item
        query = "UPDATE Goods SET IQuantity = IQuantity + %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

    # 删除退货单相关记录
    query = "DELETE FROM Return_updates_inventory WHERE RID = %s"
    cursor.execute(query, (rid,))
    db.commit()

    query = "DELETE FROM Return_list WHERE RID = %s"
    cursor.execute(query, (rid,))
    db.commit()

    print("退货单删除成功,库存更新成功！")
    cursor.close()

# 销售单明细查询
def query_sale_details():
    cursor = db.cursor()
    cursor.execute("SELECT SLID FROM Sale_list")
    sale_ids = cursor.fetchall()
    
    if sale_ids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["可查询的销售订单号"])
        for sid in sale_ids:
            table.add_row([sid[0]])
        
        print(table.draw())
    else:
        print("没有可查询的销售订单号。")
    
    while True:
        order_id = input("请输入要查询的销售订单号：")
        if (order_id,) not in sale_ids:
            print("订单号不存在，请重新输入。")
        else:
            break
    
    query = "SELECT GID, GNum, Price FROM Sale_updates_inventory WHERE SLID = %s"
    cursor.execute(query, (order_id,))
    results = cursor.fetchall()
    
    if results:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "销售数量", "商品单价"])
        
        for row in results:
            table.add_row([row[0], row[1], row[2]])
        
        print(f"销售订单号 {order_id} 的商品详细信息如下：")
        print(table.draw())
    else:
        print("该订单号没有商品详细信息。")
    cursor.close()

# 添加销售单
def add_sale_order():
    cursor = db.cursor()
    cursor.execute("SELECT SLID FROM Sale_list")
    existing_slids = cursor.fetchall()
    
    if existing_slids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的销售订单号"])
        for slid in existing_slids:
            table.add_row([slid[0]])
        
        print(table.draw())
    else:
        None
    
    while True:
        slid = input("请输入销售单编号: ")
        if (slid,) in existing_slids:
            print("销售单编号已存在，请重新输入。")
        else:
            break

    cursor.execute("SELECT CID FROM Customer")
    existing_customer_ids = cursor.fetchall()
    
    if existing_customer_ids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的客户编号"])
        for cid in existing_customer_ids:
            table.add_row([cid[0]])
        
        print(table.draw())
    else:
        print("没有客户编号，请先添加客户！")
        return
    
    while True:
        customer_id = input("请输入客户编号: ")
        if (customer_id,) not in existing_customer_ids:
            print("客户编号不存在，请重新输入。")
        else:
            break

    total_amount = float(0)
    
    while True:
        sldate = input("请输入销售日期 (格式: YYYY-MM-DD): ")
        if not is_valid_date(sldate):
            print("日期格式错误，请重新输入。")
        else:
            break

    query = "INSERT INTO Sale_list (SLID, CID, Amount_paid, SLDate) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (slid, customer_id, total_amount, sldate))
    db.commit()

    total_amount = 0

    while True:
        cursor.execute("SELECT GID, GName FROM Goods")
        existing_goods = cursor.fetchall()
        
        if existing_goods:
            table = Texttable()
            table.set_deco(Texttable.BORDER | Texttable.HEADER)
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.header(["商品编号", "商品名称"])
            for goods in existing_goods:
                table.add_row([goods[0], goods[1]])
            print(table.draw())
        else:
            print("不存在任何商品，请先添加商品！")
            return
        
        gid = input("请输入商品编号 (输入0结束): ")
        if gid == '0':
            break
        if gid not in [item[0] for item in existing_goods]:
            print("商品编号不存在，请重新输入。")
            continue

        gnum = int(input("请输入销售数量: "))
        price = float(input("请输入商品单价: "))

        cursor.execute("SELECT COUNT(*) FROM Sale_updates_inventory WHERE SLID = %s AND GID = %s", (slid, gid))
        if cursor.fetchone()[0] > 0:
            print("该商品已经在当前销售单中，请选择其他商品。")
            continue

        query = "INSERT INTO Sale_updates_inventory (SLID, GID, GNum, Price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (slid, gid, gnum, price))
        db.commit()

        query = "UPDATE Goods SET IQuantity = IQuantity - %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

        total_amount += gnum * price

    query = "UPDATE Sale_list SET Amount_paid = %s WHERE SLID = %s"
    cursor.execute(query, (total_amount, slid))
    db.commit()

    print("销售单添加成功,库存更新成功！")
    cursor.close()

# 修改销售单
def modify_sale_order():
    cursor = db.cursor()
    
    # 获取已有的销售单编号
    cursor.execute("SELECT SLID FROM Sale_list")
    existing_slids = cursor.fetchall()
    
    if existing_slids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的销售订单号"])
        for slid in existing_slids:
            table.add_row([slid[0]])
        
        print(table.draw())
    else:
        print("没有现有的销售订单号。")
        return
    
    while True:
        slid = input("请输入要修改的销售单编号: ")
        if (slid,) not in existing_slids:
            print("销售单编号不存在，请重新输入。")
        else:
            break
    
    cursor.execute("SELECT CID, SLDate FROM Sale_list WHERE SLID = %s", (slid,))
    sale_info = cursor.fetchone()
    print(f"当前客户编号: {sale_info[0]}")
    print(f"当前销售日期: {sale_info[1]}")
    
    cursor.execute("SELECT GID, GNum, Price FROM Sale_updates_inventory WHERE SLID = %s", (slid,))
    sale_items = cursor.fetchall()
    
    if sale_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "销售数量", "商品单价"])
        for item in sale_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该销售单没有商品信息。")

    cursor.execute("SELECT CID FROM Customer")
    existing_customer_ids = cursor.fetchall()
    
    if existing_customer_ids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的客户编号"])
        for cid in existing_customer_ids:
            table.add_row([cid[0]])
        
        print(table.draw())
    else:
        print("没有客户编号，请先添加客户！")
        return
    
    while True:
        new_customer_id = input("请输入新的客户编号 (或按回车保持不变): ")
        if not new_customer_id:
            new_customer_id = sale_info[0]
            break
        if (new_customer_id,) not in existing_customer_ids:
            print("客户编号不存在，请重新输入。")
        else:
            break
    
    while True:
        new_sldate = input("请输入新的销售日期 (格式: YYYY-MM-DD，或按回车保持不变): ")
        if not new_sldate:
            new_sldate = sale_info[1]
            break
        if not is_valid_date(new_sldate):
            print("日期格式错误，请重新输入。")
        else:
            break
    
    query = "UPDATE Sale_list SET CID = %s, SLDate = %s WHERE SLID = %s"
    cursor.execute(query, (new_customer_id, new_sldate, slid))
    db.commit()

    total_amount = 0

    for item in sale_items:
        gid, current_gnum, current_price = item

        while True:
            print(f"当前商品编号: {gid}, 销售数量: {current_gnum}, 商品单价: {current_price}")
            gnum = input("请输入新的销售数量 (或按回车保持不变): ")
            if not gnum:
                gnum = current_gnum
                break
            try:
                gnum = int(gnum)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        while True:
            price = input("请输入新的商品单价 (或按回车保持不变): ")
            if not price:
                price = current_price
                break
            try:
                price = float(price)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        query = "UPDATE Sale_updates_inventory SET GNum = %s, Price = %s WHERE SLID = %s AND GID = %s"
        cursor.execute(query, (gnum, price, slid, gid))
        db.commit()

        quantity_difference = gnum - current_gnum
        query = "UPDATE Goods SET IQuantity = IQuantity - %s WHERE GID = %s"
        cursor.execute(query, (quantity_difference, gid))
        db.commit()

        total_amount += gnum * price

    cursor.execute("SELECT SUM(GNum * Price) FROM Sale_updates_inventory WHERE SLID = %s", (slid,))
    total_amount = cursor.fetchone()[0]

    query = "UPDATE Sale_list SET Amount_paid = %s WHERE SLID = %s"
    cursor.execute(query, (total_amount, slid))
    db.commit()

    print("销售单修改成功,库存更新成功！")
    cursor.close()

# 删除销售单
def delete_sale_order():
    cursor = db.cursor()
    
    # 获取已有的销售单编号
    cursor.execute("SELECT SLID FROM Sale_list")
    existing_slids = cursor.fetchall()
    
    if existing_slids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的销售订单号"])
        for slid in existing_slids:
            table.add_row([slid[0]])
        
        print(table.draw())
    else:
        print("没有现有的销售订单号。")
        return
    
    while True:
        slid = input("请输入要删除的销售单编号: ")
        if (slid,) not in existing_slids:
            print("销售单编号不存在，请重新输入。")
        else:
            break
    
    cursor.execute("SELECT CID, SLDate FROM Sale_list WHERE SLID = %s", (slid,))
    sale_info = cursor.fetchone()
    print(f"当前客户编号: {sale_info[0]}")
    print(f"当前销售日期: {sale_info[1]}")
    
    cursor.execute("SELECT GID, GNum, Price FROM Sale_updates_inventory WHERE SLID = %s", (slid,))
    sale_items = cursor.fetchall()
    
    if sale_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "销售数量", "商品单价"])
        for item in sale_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该销售单没有商品信息。")

    confirm = input("确定要删除这个销售单吗？(yes/no): ")
    if confirm.lower() != 'yes':
        print("取消删除操作。")
        cursor.close()
        return

    for item in sale_items:
        gid, gnum, _ = item
        query = "UPDATE Goods SET IQuantity = IQuantity + %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

    query = "DELETE FROM Sale_updates_inventory WHERE SLID = %s"
    cursor.execute(query, (slid,))
    db.commit()

    query = "DELETE FROM Sale_list WHERE SLID = %s"
    cursor.execute(query, (slid,))
    db.commit()

    print("销售单删除成功,库存更新成功！")
    cursor.close()

# 客户退货单明细查询
def query_customer_return_details():
    cursor = db.cursor()
    cursor.execute("SELECT CRID FROM Customer_return_list")
    return_ids = cursor.fetchall()
    
    if return_ids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["可查询的客户退货订单号"])
        for rid in return_ids:
            table.add_row([rid[0]])
        
        print(table.draw())
    else:
        print("没有可查询的客户退货订单号。")
    
    while True:
        order_id = input("请输入要查询的客户退货订单号：")
        if (order_id,) not in return_ids:
            print("订单号不存在，请重新输入。")
        else:
            break
    
    query = "SELECT GID, GNum, Price FROM Customer_return_updates_inventory WHERE CRID = %s"
    cursor.execute(query, (order_id,))
    results = cursor.fetchall()
    
    if results:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "退货数量", "商品单价"])
        
        for row in results:
            table.add_row([row[0], row[1], row[2]])
        
        print(f"客户退货订单号 {order_id} 的商品详细信息如下：")
        print(table.draw())
    else:
        print("该订单号没有商品详细信息。")
    cursor.close()

# 添加客户退货单
def add_customer_return_order():
    cursor = db.cursor()
    cursor.execute("SELECT CRID FROM Customer_return_list")
    existing_crids = cursor.fetchall()
    
    if existing_crids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的客户退货订单号"])
        for crid in existing_crids:
            table.add_row([crid[0]])
        
        print(table.draw())
    else:
        None
    
    while True:
        crid = input("请输入客户退货单编号: ")
        if (crid,) in existing_crids:
            print("客户退货单编号已存在，请重新输入。")
        else:
            break

    cursor.execute("SELECT CID FROM Customer")
    existing_customer_ids = cursor.fetchall()
    
    if existing_customer_ids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的客户编号"])
        for cid in existing_customer_ids:
            table.add_row([cid[0]])
        
        print(table.draw())
    else:
        print("没有客户编号，请先添加客户！")
        return
    
    while True:
        customer_id = input("请输入客户编号: ")
        if (customer_id,) not in existing_customer_ids:
            print("客户编号不存在，请重新输入。")
        else:
            break

    total_amount = float(0)
    
    while True:
        crdate = input("请输入客户退货日期 (格式: YYYY-MM-DD): ")
        if not is_valid_date(crdate):
            print("日期格式错误，请重新输入。")
        else:
            break

    query = "INSERT INTO Customer_return_list (CRID, CID, Amount_paid, CRDate) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (crid, customer_id, total_amount, crdate))
    db.commit()

    total_amount = 0

    while True:
        cursor.execute("SELECT GID, GName FROM Goods")
        existing_goods = cursor.fetchall()
        
        if existing_goods:
            table = Texttable()
            table.set_deco(Texttable.BORDER | Texttable.HEADER)
            table.set_cols_align(["c", "c"])
            table.set_cols_valign(["m", "m"])
            table.header(["商品编号", "商品名称"])
            for goods in existing_goods:
                table.add_row([goods[0], goods[1]])
            print(table.draw())
        else:
            print("不存在任何商品，请先添加商品！")
            return
        
        gid = input("请输入商品编号 (输入0结束): ")
        if gid == '0':
            break
        if gid not in [item[0] for item in existing_goods]:
            print("商品编号不存在，请重新输入。")
            continue

        gnum = int(input("请输入退货数量: "))
        price = float(input("请输入商品单价: "))

        cursor.execute("SELECT COUNT(*) FROM Customer_return_updates_inventory WHERE CRID = %s AND GID = %s", (crid, gid))
        if cursor.fetchone()[0] > 0:
            print("该商品已经在当前客户退货单中，请选择其他商品。")
            continue

        query = "INSERT INTO Customer_return_updates_inventory (CRID, GID, GNum, Price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (crid, gid, gnum, price))
        db.commit()

        query = "UPDATE Goods SET IQuantity = IQuantity + %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

        total_amount += gnum * price

    query = "UPDATE Customer_return_list SET Amount_paid = %s WHERE CRID = %s"
    cursor.execute(query, (total_amount, crid))
    db.commit()

    print("客户退货单添加成功,库存更新成功！")
    cursor.close()

# 修改客户退货单
def modify_customer_return_order():
    cursor = db.cursor()
    
    cursor.execute("SELECT CRID FROM Customer_return_list")
    existing_crids = cursor.fetchall()
    
    if existing_crids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的客户退货订单号"])
        for crid in existing_crids:
            table.add_row([crid[0]])
        
        print(table.draw())
    else:
        print("没有现有的客户退货订单号。")
        return
    
    while True:
        crid = input("请输入要修改的客户退货单编号: ")
        if (crid,) not in existing_crids:
            print("客户退货单编号不存在，请重新输入。")
        else:
            break
    
    cursor.execute("SELECT CID, CRDate FROM Customer_return_list WHERE CRID = %s", (crid,))
    return_info = cursor.fetchone()
    print(f"当前客户编号: {return_info[0]}")
    print(f"当前退货日期: {return_info[1]}")
    
    cursor.execute("SELECT GID, GNum, Price FROM Customer_return_updates_inventory WHERE CRID = %s", (crid,))
    return_items = cursor.fetchall()
    
    if return_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "退货数量", "商品单价"])
        for item in return_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该客户退货单没有商品信息。")

    cursor.execute("SELECT CID FROM Customer")
    existing_customer_ids = cursor.fetchall()
    
    if existing_customer_ids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的客户编号"])
        for cid in existing_customer_ids:
            table.add_row([cid[0]])
        
        print(table.draw())
    else:
        print("没有客户编号，请先添加客户！")
        return
    
    while True:
        new_customer_id = input("请输入新的客户编号 (或按回车保持不变): ")
        if not new_customer_id:
            new_customer_id = return_info[0]
            break
        if (new_customer_id,) not in existing_customer_ids:
            print("客户编号不存在，请重新输入。")
        else:
            break
    
    while True:
        new_crdate = input("请输入新的退货日期 (格式: YYYY-MM-DD，或按回车保持不变): ")
        if not new_crdate:
            new_crdate = return_info[1]
            break
        if not is_valid_date(new_crdate):
            print("日期格式错误，请重新输入。")
        else:
            break
    
    query = "UPDATE Customer_return_list SET CID = %s, CRDate = %s WHERE CRID = %s"
    cursor.execute(query, (new_customer_id, new_crdate, crid))
    db.commit()

    total_amount = 0

    for item in return_items:
        gid, current_gnum, current_price = item

        while True:
            print(f"当前商品编号: {gid}, 退货数量: {current_gnum}, 商品单价: {current_price}")
            gnum = input("请输入新的退货数量 (或按回车保持不变): ")
            if not gnum:
                gnum = current_gnum
                break
            try:
                gnum = int(gnum)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        while True:
            price = input("请输入新的商品单价 (或按回车保持不变): ")
            if not price:
                price = current_price
                break
            try:
                price = float(price)
                break
            except ValueError:
                print("输入无效，请输入一个有效的数字。")

        query = "UPDATE Customer_return_updates_inventory SET GNum = %s, Price = %s WHERE CRID = %s AND GID = %s"
        cursor.execute(query, (gnum, price, crid, gid))
        db.commit()

        quantity_difference = gnum - current_gnum
        query = "UPDATE Goods SET IQuantity = IQuantity + %s WHERE GID = %s"
        cursor.execute(query, (quantity_difference, gid))
        db.commit()

        total_amount += gnum * price

    cursor.execute("SELECT SUM(GNum * Price) FROM Customer_return_updates_inventory WHERE CRID = %s", (crid,))
    total_amount = cursor.fetchone()[0]

    query = "UPDATE Customer_return_list SET Amount_paid = %s WHERE CRID = %s"
    cursor.execute(query, (total_amount, crid))
    db.commit()

    print("客户退货单修改成功,库存更新成功！")
    cursor.close()

# 删除客户退货单
def delete_customer_return_order():
    cursor = db.cursor()
    
    cursor.execute("SELECT CRID FROM Customer_return_list")
    existing_crids = cursor.fetchall()
    
    if existing_crids:
        table = Texttable()
        table.set_cols_align(["c"])
        table.set_cols_valign(["m"])
        table.header(["已有的客户退货订单号"])
        for crid in existing_crids:
            table.add_row([crid[0]])
        
        print(table.draw())
    else:
        print("没有现有的客户退货订单号。")
        return
    
    while True:
        crid = input("请输入要删除的客户退货单编号: ")
        if (crid,) not in existing_crids:
            print("客户退货单编号不存在，请重新输入。")
        else:
            break
    
    cursor.execute("SELECT CID, CRDate FROM Customer_return_list WHERE CRID = %s", (crid,))
    return_info = cursor.fetchone()
    print(f"当前客户编号: {return_info[0]}")
    print(f"当前退货日期: {return_info[1]}")
    
    cursor.execute("SELECT GID, GNum, Price FROM Customer_return_updates_inventory WHERE CRID = %s", (crid,))
    return_items = cursor.fetchall()
    
    if return_items:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        table.header(["商品编号", "退货数量", "商品单价"])
        for item in return_items:
            table.add_row([item[0], item[1], item[2]])
        
        print(table.draw())
    else:
        print("该客户退货单没有商品信息。")

    confirm = input("确定要删除这个客户退货单吗？(yes/no): ")
    if confirm.lower() != 'yes':
        print("取消删除操作。")
        cursor.close()
        return

    for item in return_items:
        gid, gnum, _ = item
        query = "UPDATE Goods SET IQuantity = IQuantity - %s WHERE GID = %s"
        cursor.execute(query, (gnum, gid))
        db.commit()

    query = "DELETE FROM Customer_return_updates_inventory WHERE CRID = %s"
    cursor.execute(query, (crid,))
    db.commit()

    query = "DELETE FROM Customer_return_list WHERE CRID = %s"
    cursor.execute(query, (crid,))
    db.commit()

    print("客户退货单删除成功,库存更新成功！")
    cursor.close()

# 库存查询
def inventory_query():
    cursor = db.cursor()
    cursor.execute("SELECT GID, GName, IQuantity, IMin, IMax FROM Goods")
    goods = cursor.fetchall()
    table = Texttable()
    table.header(["商品编号", "商品名称", "库存数量", "库存下限", "库存上限"])
    for gid, gname, iquantity, imin, imax in goods:
        table.add_row([gid, gname, iquantity, imin, imax])
    print(table.draw())
    
    cursor.close()

# 库存上下限预警
def inventory_warning():
    cursor = db.cursor()
    cursor.execute("SELECT GID, GName, IQuantity, IMin, IMax FROM Goods WHERE IQuantity < IMin OR IQuantity > IMax")
    goods = cursor.fetchall()
    if goods:
        table = Texttable()
        table.header(["商品编号", "商品名称", "库存数量", "库存下限", "库存上限"])
        for gid, gname, iquantity, imin, imax in goods:
            table.add_row([gid, gname, iquantity, imin, imax])
        print(table.draw())
        print("以上为所有库存预警商品的库存信息。")
    else:
        print("所有商品的库存均在正常范围内。")
    cursor.close()

# 获取可查询的月份
def get_available_months():
    cursor = db.cursor()
    cursor.execute("""
        SELECT DISTINCT YEAR(PDate) AS Year, MONTH(PDate) AS Month 
        FROM Purchase_list 
        UNION 
        SELECT DISTINCT YEAR(SLDate) AS Year, MONTH(SLDate) AS Month 
        FROM Sale_list 
        UNION 
        SELECT DISTINCT YEAR(RDate) AS Year, MONTH(RDate) AS Month 
        FROM Return_list 
        UNION 
        SELECT DISTINCT YEAR(CRDate) AS Year, MONTH(CRDate) AS Month 
        FROM Customer_return_list 
        ORDER BY Year, Month
    """)
    months = cursor.fetchall()
    cursor.close()
    return months

# 月度结账
def monthly_settlement(month, year):
    cursor = db.cursor()
    # 查询本月的进货总额
    cursor.execute("""
        SELECT SUM(Amount_paid) AS total_purchase
        FROM Purchase_list 
        WHERE MONTH(PDate) = %s AND YEAR(PDate) = %s 
    """, (month, year))
    total_purchase = cursor.fetchone()[0] or 0

    # 查询本月的销售总额
    cursor.execute("""
        SELECT SUM(Amount_paid) AS total_sales
        FROM Sale_list 
        WHERE MONTH(SLDate) = %s AND YEAR(SLDate) = %s
    """, (month, year))
    total_sales = cursor.fetchone()[0] or 0

    # 查询本月的退货总额
    cursor.execute("""
        SELECT SUM(Amount_paid) AS total_returns
        FROM Return_list 
        WHERE MONTH(RDate) = %s AND YEAR(RDate) = %s
    """, (month, year))
    total_returns = cursor.fetchone()[0] or 0

    # 查询本月的客户退货总额
    cursor.execute("""
        SELECT SUM(Amount_paid) AS total_customer_returns
        FROM Customer_return_list 
        WHERE MONTH(CRDate) = %s AND YEAR(CRDate) = %s
    """, (month, year))
    total_customer_returns = cursor.fetchone()[0] or 0
    cursor.close()

    # 计算本月的净利润
    net_sales = total_sales - total_customer_returns - total_purchase + total_returns

    print(f"总进货金额: {total_purchase}")
    print(f"总销售金额: {total_sales}")
    print(f"总退货金额: {total_returns}")
    print(f"总客户退货金额: {total_customer_returns}")
    print(f"净利润: {net_sales}")

# 查询结账根函数
def choose_and_settle_month():
    months = get_available_months()
    if not months:
        print("没有可查询的月份。")
        return

    print("可查询的月份如下：")
    for idx, (year, month) in enumerate(months, start=1):
        print(f"{idx}. {year}年{month}月")

    while True:
        try:
            choice = int(input("请输入要查询的月份编号："))
            if 1 <= choice <= len(months):
                selected_month = months[choice - 1]
                year, month = selected_month
                print(f"查询 {year}年{month}月 的结算情况：")
                monthly_settlement(month, year)
                break
            else:
                print("输入的编号不在有效范围内，请重新输入。")
        except ValueError:
            print("输入无效，请输入数字编号。")

# 财务统计
def financial_statistics():
    cursor = db.cursor()

    # 查询总进货金额
    cursor.execute("SELECT SUM(Amount_paid) AS total_purchase FROM Purchase_list")
    total_purchase = cursor.fetchone()[0] or 0

    # 查询总销售金额
    cursor.execute("SELECT SUM(Amount_paid) AS total_sales FROM Sale_list")
    total_sales = cursor.fetchone()[0] or 0

    # 查询总退货金额
    cursor.execute("SELECT SUM(Amount_paid) AS total_returns FROM Return_list")
    total_returns = cursor.fetchone()[0] or 0

    # 查询总客户退货金额
    cursor.execute("SELECT SUM(Amount_paid) AS total_customer_returns FROM Customer_return_list")
    total_customer_returns = cursor.fetchone()[0] or 0

    cursor.close()

    # 计算总收入和总支出
    total_income = total_sales - total_customer_returns
    total_expense = total_purchase - total_returns

    # 计算净利润
    net_profit = total_income - total_expense

    print(f"总收入: {total_income}")
    print(f"总支出: {total_expense}")
    print(f"净利润: {net_profit}")

user = {} # 全局变量，登录之后就会被赋值
# 登录函数
def login():
    cursor = db.cursor(as_dict=True)  # 使用字典游标，方便访问字段
    sql = "select * from Users;"
    cursor.execute(sql)
    re = cursor.fetchall()
    users = {row['UserID']: row['Passwords'] for row in re} # 记录用户表的用户名与密码
    cursor.close()

    id = input('请输入唯一id：\n')
    password = input('请输入密码：\n')

    # 判断用户是否存在
    if id not in users.keys():
        print('用户不存在')
        return False
    
    global user # 声明全局变量

    # 判断密码是否正确
    for i in range(2): # 如果错误可以再次输入两次
        if users[id] == password:
            cursor = db.cursor(as_dict=True)
            cursor.execute('SELECT * FROM Users WHERE UserID = %s', (id,))
            result = cursor.fetchone()
            user = {'UserID':result['UserID'],
                    'UName':result['UName'],
                    'Passwords':result['Passwords'],
                    'Permission':result['Permission'],}  # 将登录成功的用户信息赋给全局变量user
            cursor.close()
            print('登录成功')
            return True
        else:
            password = input('密码错误，请重新请输入密码：\n')
    else:
        print('密码错误三次')
        return False
    
# 主菜单
def show():
    table = Texttable()
    table.set_deco(Texttable.BORDER | Texttable.HEADER)
    table.set_cols_align(["c", "c", "c"])
    table.set_cols_valign(["m", "m", "m"])
    
    # 表格内容
    table.header([''] + ["进销存管理主菜单\n制作人：瞿成乐"] + [''])
    menu_data = [
        ["1. 资料管理", "2. 采购管理", "3. 销售管理"],
        ["4. 库存管理", "5. 财务管理", "6. 系统管理"],
        ["0. 退出系统"]
    ]

    # 添加每行到表格
    for row in menu_data:
        if len(row) == 1:
            table.add_row([""] + row + [""])
        else:
            table.add_row(row)

    print(table.draw())

# 资料管理
def show1():
    os.system('pause')
    os.system('cls')
    while True:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])
        
        # 表格内容
        table.header([''] + ["资料管理子菜单"] + [''])
        submenu_data = [
            ["商品资料", "供货商资料", "客户资料"],
            ["1.查询", "5.查询", "9.查询"],
            ["2.添加", "6.添加", "10.添加"],
            ["3.修改", "7.修改", "11.修改"],
            ["4.删除", "8.删除", "12.删除"],
            ["0.退出子菜单"]
        ]
        
        # 添加每行到表格
        for row in submenu_data:
            if len(row) == 1:
                table.add_row([""] + row + [""])
            else:
                table.add_row(row)
        
        print(table.draw())
        choice = input("请选择操作：")
        if choice == '0':
            break
        elif choice == '1':
            query('Goods')
        elif choice == '2':
            add_goods()
        elif choice == '3':
            modify_goods()
        elif choice == '4':
            delete_goods()
        elif choice == '5':
            query('Supplier')
        elif choice == '6':
            add_supplier()
        elif choice == '7':
            modify_supplier()
        elif choice == '8':
            delete_supplier()
        elif choice == '9':
            query('Customer')
        elif choice == '10':
            add_customer()
        elif choice == '11':
            modify_customer()
        elif choice == '12':
            delete_customer()
        else:
            print("输入错误，请重新选择。")
        os.system('pause')
        os.system('cls')

# 采购管理
def show2():
    os.system('pause')
    os.system('cls')
    while True:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])

        # 表格内容
        table.header([''] + ["采购管理子菜单"] + [''])
        submenu_data = [
            ["进货单", '', "退货单"],
            ["1.查询", '', "6.查询"],
            ["2.明细查询", '', "7.明细查询"],
            ["3.添加", '', "8.添加"],
            ["4.修改", '', "9.修改"],
            ["5.删除", '', "10.删除"],
            ["0.退出子菜单"]
        ]
        
        # 添加每行到表格
        for row in submenu_data:
            if len(row) == 1:
                table.add_row([""] + row + [""])
            else:
                table.add_row(row)
        
        print(table.draw())
        choice = input("请选择操作：")
        if choice == '0':
            break
        elif choice == '1':
            query('Purchase_list')
        elif choice == '2':
            query_purchase_details()
        elif choice == '3':
            add_purchase_order()
        elif choice == '4':
            modify_purchase_order()
        elif choice == '5':
            delete_purchase_order()
        elif choice == '6':
            query('Return_list')
        elif choice == '7':
            query_return_details()
        elif choice == '8':
            add_return_order()
        elif choice == '9':
            modify_return_order()
        elif choice == '10':
            delete_return_order()
        else:
            print("输入错误，请重新选择。")
        os.system('pause')
        os.system('cls')

# 销售管理
def show3():
    os.system('pause')
    os.system('cls')
    while True:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])

        # 表格内容
        table.header([''] + ["销售管理子菜单"] + [''])
        submenu_data = [
            ["销售单", '', "客户退货单"],
            ["1.查询", '', "6.查询"],
            ["2.明细查询", '', "7.明细查询"],
            ["3.添加", '', "8.添加"],
            ["4.修改", '', "9.修改"],
            ["5.删除", '', "10.删除"],
            ["0.退出子菜单"]
        ]
        
        # 添加每行到表格
        for row in submenu_data:
            if len(row) == 1:
                table.add_row([""] + row + [""])
            else:
                table.add_row(row)
        
        print(table.draw())
        choice = input("请选择操作：")
        if choice == '0':
            break
        elif choice == '1':
            query('Sale_list')
        elif choice == '2':
            query_sale_details()
        elif choice == '3':
            add_sale_order()
        elif choice == '4':
            modify_sale_order()
        elif choice == '5':
            delete_sale_order()
        elif choice == '6':
            query('Customer_return_list')
        elif choice == '7':
            query_customer_return_details()
        elif choice == '8':
            add_customer_return_order()
        elif choice == '9':
            modify_customer_return_order()
        elif choice == '10':
            delete_customer_return_order()
        else:
            print("输入错误，请重新选择。")
        os.system('pause')
        os.system('cls')

# 库存管理
def show4():
    os.system('pause')
    os.system('cls')
    while True:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])

        # 表格内容
        table.header([''] + ["库存管理子菜单"] + [''])
        submenu_data = [
            ["1.库存查询"],
            ["2.库存预警"],
            ["0.退出子菜单"]
        ]
        
        # 添加每行到表格
        for row in submenu_data:
            if len(row) == 1:
                table.add_row([""] + row + [""])
            else:
                table.add_row(row)
        
        print(table.draw())
        choice = input("请选择操作：")
        if choice == '0':
            break
        elif choice == '1':
            inventory_query()
        elif choice == '2':
            inventory_warning()
        else:
            print("输入错误，请重新选择。")
        os.system('pause')
        os.system('cls')

# 财务管理
def show5():
    os.system('pause')
    os.system('cls')
    while True:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])

        # 表格内容
        table.header([''] + ["财务管理子菜单"] + [''])
        submenu_data = [
            ["1.月度结账"],
            ["2.财务统计"],
            ["0.退出子菜单"]
        ]

        # 添加每行到表格
        for row in submenu_data:
            if len(row) == 1:
                table.add_row([""] + row + [""])
            else:
                table.add_row(row)

        print(table.draw())
        choice = input("请选择操作：")
        if choice == '0':
            break
        elif choice == '1':
            choose_and_settle_month()
        elif choice == '2':
            financial_statistics()
        else:
            print("输入错误，请重新选择。")
        os.system('pause')
        os.system('cls')

# 系统管理
def show6():
    os.system('pause')
    os.system('cls')
    while True:
        table = Texttable()
        table.set_deco(Texttable.BORDER | Texttable.HEADER)
        table.set_cols_align(["c", "c", "c"])
        table.set_cols_valign(["m", "m", "m"])

        # 表格内容
        table.header([''] + ["系统管理子菜单"] + [''])
        submenu_data = [
            ["1.查看用户资料"],
            ["2.添加用户资料"],
            ["3.修改用户资料"],
            ["4.删除用户资料"],
            ["0.退出子菜单"]
        ]

        # 添加每行到表格
        for row in submenu_data:
            if len(row) == 1:
                table.add_row([""] + row + [""])
            else:
                table.add_row(row)

        print(table.draw())
        choice = input("请选择操作：")
        if choice == '0':
            break
        elif choice == '1':
            query('Users')
        elif choice == '2':
            add_user()
        elif choice == '3':
            modify_user()
        elif choice == '4':
            delete_user()
        else:
            print("输入错误，请重新选择。")
        os.system('pause')
        os.system('cls')

def main():
    if login(): # 根据登录函数返回的布尔值，判断是否该执行以下程序
        # print(user)
        os.system('pause')
        os.system('cls')
        while True: # 永真循环，输入指定数字才会跳出
            show() # 展示菜单
            n = input("请输入操作序号：")
            if n == '0':
                break
            elif n == '1':
                show1() # 资料管理
            elif n == '2':
                show2() # 采购管理
            elif n == '3':
                show3() # 销售管理
            elif n == '4':
                show4() # 库存管理
            elif n == '5':
                if user['Permission'] == 'A':
                    show5() # 财务管理
                else:
                    print("抱歉，您的权限不够，无法进行财务管理")
            elif n == '6':
                if user['Permission'] == 'A':
                    show6() # 系统管理
                else:
                    print("抱歉，您的权限不够，无法进行系统管理")
            else:
                print("输入格式错误，请重新输入！")
            os.system('pause')
            os.system('cls')
    else:
        print('登录失败') 

if __name__ == '__main__':
    os.system('cls')
    # 连接数据库
    db = pymssql.connect(host='SEELE\\MSSQLSERVER1',
                         user='sa',
                         password='Qlihuazou276492',
                         database='IMS',
                         charset='utf8')
    main() # 执行主函数
    print("系统登出")
    db.close() # 关闭数据库