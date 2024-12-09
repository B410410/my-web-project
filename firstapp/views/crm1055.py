from erp.viewsbasis import *
from erp.viewspublic import *
from erp.public.viewsdate import *

"""
Database Process
"""


class DataDemand(ErpDb):

    def __init__(self, username):
        super().__init__()
        self.username = username

    # 全自送區郵遞區號
    def stmt_select_zip_delive(self):
        t1 = 'erp_zip_delive'
        stmt = f"""
                SELECT
                    {t1}.city, {t1}.district, {t1}.zip
                FROM
                    {t1}
                WHERE is_self_delive;
                """
        rows = self.erpdb_fetchall(stmt)
        return rows

    # 自送區郵遞區號(僅顯示有資料的地區)
    def stmt_select_zip_delive_search(self):
        t1 = 'erp_crm_namelist_crm'
        stmt = f"""
                SELECT
                    {t1}.city, {t1}.district, {t1}.role1_call_status
                FROM
                    {t1}
                WHERE
                    {t1}.role1_call_status in ('C27', 'C29', 'C32', 'C36', 'C57', 'C59')
                    AND {t1}.gb_cust_no IS NULL
                    AND (NOT {t1}.is_ng OR {t1}.is_ng is null)
                    AND NOT {t1}.forever_shelve
                    AND {t1}.zip in (SELECT zip FROM erp_zip_delive where is_self_delive);
                """
        rows = self.erpdb_fetchall(stmt)
        return rows
        
    # 查詢客戶資料(未處理過的部分)
    def stmt_get_uncalled_list(self, status, city, district):
        t1 = 'erp_crm_namelist_crm'
        t2 = 'erp_zip_delive'
        district_value = f"AND {t1}.district = '{district}'" if district not in (None, '') else ''
        stmt = f"""
                SELECT
                    {t1}.cust_no, 
                    {t1}.cust_brief, 
                    {t1}.role2_call_time, 
                    {t1}.role2_call_status,
                    {t1}.city, 
                    {t1}.district,
                    {t1}.zip,
                    {t1}.addr,
                    {t1}.employee_nums,
                    {t1}.tel,
                    {t1}.fax,
                    {t1}.industry,
                    {t1}.rcontact_date
                FROM
                    {t1}
                JOIN 
                    {t2} ON {t1}.zip = {t2}.zip
                WHERE
                    {t1}.role1_call_status = '{status}'
                    AND {t1}.city = '{city}'
                    {district_value}
                    AND {t1}.role2_call_time is null
                    AND {t1}.role2_call_status is null
                    AND (NOT {t1}.is_ng OR {t1}.is_ng is null)
                    AND NOT {t1}.forever_shelve
                    AND {t2}.is_self_delive
                ORDER BY
                    {t1}.role1_call_time
                LIMIT 20;
        """
        rows = self.erpdb_fetchall(stmt)
        return rows

    # 查詢客戶資料(當天已聯絡過的部分)
    def stmt_get_called_today_list(self, status, city, district):
        t1 = 'erp_crm_namelist_crm'
        t2 = 'erp_zip_delive'
        t3 = 'erp_survey_detail'
        district_value = f"AND {t1}.district = '{district}'" if district not in (None, '') else ''
        stmt = f"""
                SELECT
                    {t1}.cust_no, 
                    {t1}.cust_brief, 
                    {t1}.role2_call_time, 
                    {t3}.caption AS role2_call_status,
                    {t1}.city, 
                    {t1}.district,
                    {t1}.zip,
                    {t1}.addr,
                    {t1}.employee_nums,
                    {t1}.tel,
                    {t1}.fax,
                    {t1}.industry,
                    {t1}.rcontact_date,
                    {t1}.gb_cust_no
                FROM
                    {t1}
                JOIN 
                    {t2} ON {t1}.zip = {t2}.zip
                JOIN 
                    {t3} ON {t1}.role2_call_status = {t3}.caption_no
                WHERE
                    {t1}.role1_call_status = '{status}'
                    AND {t1}.city = '{city}'
                    {district_value}
                    AND {t1}.role2_call_time is not null
                    AND {t1}.role2_call_time::date = CURRENT_DATE
                    AND {t1}.role2_call_status is not null
                    AND (NOT {t1}.is_ng OR {t1}.is_ng is null)
                    AND {t2}.is_self_delive
                    AND {t3}.survey_no = 'CRMHANDLE'
                ORDER BY
                    {t1}.role2_call_time;
        """
        rows = self.erpdb_fetchall(stmt)
        return rows
    
    # 查詢客戶資料(非當天已聯絡過的部分)
    def stmt_get_called_list(self, status, city, district):
        t1 = 'erp_crm_namelist_crm'
        t2 = 'erp_zip_delive'
        t3 = 'erp_survey_detail'
        district_value = f"AND {t1}.district = '{district}'" if district not in (None, '') else ''
        stmt = f"""
                SELECT
                    {t1}.cust_no, 
                    {t1}.cust_brief, 
                    {t1}.role2_call_time, 
                    {t3}.caption AS role2_call_status,
                    {t1}.city, 
                    {t1}.district,
                    {t1}.zip,
                    {t1}.addr,
                    {t1}.employee_nums,
                    {t1}.tel,
                    {t1}.fax,
                    {t1}.industry,
                    {t1}.rcontact_date
                FROM
                    {t1}
                JOIN 
                    {t2} ON {t1}.zip = {t2}.zip
                JOIN 
                    {t3} ON {t1}.role2_call_status = {t3}.caption_no
                WHERE
                    {t1}.role1_call_status = '{status}'
                    AND {t1}.city = '{city}'
                    {district_value}
                    AND {t1}.role2_call_time IS NOT NULL
                    AND {t1}.role2_call_time::date < CURRENT_DATE
                    AND {t1}.role2_call_status IS NOT NULL 
                    AND {t1}.role2_call_status in('C01', 'C03', 'C14', 'C62')
                    AND {t1}.gb_cust_no IS NULL
                    AND (NOT {t1}.is_ng OR {t1}.is_ng IS NULL)
                    AND NOT {t1}.forever_shelve
                    AND {t2}.is_self_delive
                    AND {t3}.survey_no = 'CRMHANDLE'
                ORDER BY
                    {t1}.last_call_time;
        """
        rows = self.erpdb_fetchall(stmt)
        return rows


    # 聯絡人資料(底下那排)
    def stmt_select_erp_crm_namelist_contact_bottom(self, cust_no):
        t1 = 'erp_crm_namelist_contact'
        stmt = f"""
                SELECT
                    cust_no, id, contacter, last_call_time, memo, rcontact_date
                FROM
                    {t1}
                WHERE
                    cust_no = '{cust_no}'
                    AND is_ng is not TRUE;
                """
        rows = self.erpdb_fetchall(stmt)
        return rows

    # 詳細聯絡人資料(點底下那排其中一個聯絡人後查的資料)
    def stmt_select_erp_crm_namelist_contact_detail(self, cust_no, cont_id):
        t1 = 'erp_crm_namelist_crm'
        t2 = 'erp_crm_namelist_contact'
        t3 = 'erp_crm_namelist_special'
        stmt = f"""
                SELECT
                    {t1}.cust_no, {t1}.cust_brief, {t1}.tel AS cust_tel, {t1}.fax AS cust_fax, {t1}.gb_cust_no,
                    {t1}.city, {t1}.district, {t1}.zip, {t1}.addr, {t1}.employee_nums, {t1}.industry,
                    {t2}.id, {t2}.contacter, {t2}.tel AS cont_tel, {t2}.tel_ext AS cont_tel_ext, {t2}.mobile, {t2}.fax AS cont_fax,
                    {t3}.is_email, {t3}.is_fax, {t3}.is_line
                FROM
                    {t1}
                JOIN
                    {t2} ON {t1}.cust_no = {t2}.cust_no
                LEFT JOIN
                    {t3} ON {t1}.cust_no = {t3}.cust_no AND {t3}.role = 'role2'
                WHERE
                    {t1}.cust_no = '{cust_no}'
                    AND {t2}.id = '{cont_id}'
                    AND {t1}.is_ng IS NOT TRUE
                ORDER BY
                    {t3}.call_time
                LIMIT 1;
        """
        rows = self.erpdb_fetchall(stmt)
        return rows

    # 行業別
    def stmt_select_erp_crm_industry(self):
        stmt = f"""SELECT 
                        industry_no, industry_name
                    FROM
                        erp_crm_industry;
                """
        rows = self.erpdb_fetchall(stmt)
        return rows
    
    # 聯絡狀態
    def stmt_select_erp_survey_detail(self):
        t1 = 'erp_survey_detail'
        stmt = f"""SELECT
                        caption_no, caption
                    FROM
                        {t1}
                    WHERE 
                        survey_no = 'CRMH55';
                """
        rows = self.erpdb_fetchall(stmt)
        return rows
    
    # 文宣類別
    def stmt_select_erp_promo_leader(self):
        t1 = 'erp_promo_leader'
        stmt = f"""SELECT
                        promo_ld_no, promo_ld_name
                    FROM
                        {t1}
                    WHERE
                        is_active2 is TRUE;
                """
        rows = self.erpdb_fetchall(stmt)
        return rows

    # 儲存客戶資訊
    def update_erp_crm_namelist_crm(self, data_d):
        t1 = 'erp_crm_namelist_crm'
        role_shelve = ""
        # 如果是無效名單('C63')
        if data_d['last_call_status'] == 'C63':
            role_shelve = f""",
                "role1_shelve" = TRUE,
                "role2_shelve" = TRUE,
                "role3_shelve" = TRUE,
                "forever_shelve" = TRUE
            """

        stmt = f"""
                UPDATE
                    {t1}
                SET
                    tel = {f"'{data_d['cust_tel']}'" if data_d['cust_tel'] is not None else 'NULL'},
                    fax = {f"'{data_d['cust_fax']}'" if data_d['cust_fax'] is not None else 'NULL'},
                    industry = {f"'{data_d['industry']}'" if data_d['industry'] is not None else 'NULL'},
                    city = {f"'{data_d['city']}'" if data_d['city'] is not None else 'NULL'},
                    district = {f"'{data_d['district']}'" if data_d['district'] is not None else 'NULL'},
                    zip = {f"'{data_d['zip']}'" if data_d['zip'] is not None else 'NULL'},
                    addr = {f"'{data_d['addr']}'" if data_d['addr'] is not None else 'NULL'},
                    employee_nums = {f"'{data_d['employee_nums']}'" if data_d['employee_nums'] is not None else 'NULL'},
                    gb_cust_no = {f"'{data_d['gb_cust_no']}'" if data_d['gb_cust_no'] is not None else 'NULL'},
                    last_call_status = {f"'{data_d['last_call_status']}'" if data_d['last_call_status'] is not None else 'NULL'},
                    last_call_time = NOW(),
                    role2_call_status = {f"'{data_d['last_call_status']}'" if data_d['last_call_status'] is not None else 'NULL'},
                    role2_call_time = NOW(),
                    last_call_role = 'role2',
                    update_name = '{data_d['sales_name']}',
                    update_time = NOW(),
                    rcontact_date = {f"'{data_d['rcontact_date']}'" if data_d['rcontact_date'] is not None else 'NULL'}
                    {role_shelve}
                WHERE
                    cust_no = '{data_d['cust_no']}';
                """
        rows = self.erpdb_execute(stmt)
        return rows

    # 更新聯絡人資訊
    def update_erp_crm_namelist_contact(self, data_d):
        t1 = 'erp_crm_namelist_contact'
        
        stmt = f"""
                UPDATE
                    {t1}
                SET
                    tel = {f"'{data_d['cont_tel']}'" if data_d['cont_tel'] is not None else 'NULL'},
                    tel_ext = {f"'{data_d['cont_tel_ext']}'" if data_d['cont_tel_ext'] is not None else 'NULL'},
                    mobile = {f"'{data_d['mobile']}'" if data_d['mobile'] is not None else 'NULL'},
                    fax = {f"'{data_d['cont_fax']}'" if data_d['cont_fax'] is not None else 'NULL'},
                    last_contact_status = {f"'{data_d['last_call_status']}'" if data_d['last_call_status'] is not None else 'NULL'},
                    last_call_time = NOW(),
                    update_name = '{data_d['sales_name']}',
                    update_time = NOW(),
                    rcontact_date = {f"'{data_d['rcontact_date']}'" if data_d['rcontact_date'] is not None else 'NULL'}
                WHERE
                    id = '{data_d['cont_id']}';
                """
        
        rows = self.erpdb_execute(stmt)
        return rows


    # 儲存聯絡人資訊
    def insert_erp_crm_namelist_contact(self, data_d):
        t1 = 'erp_crm_namelist_contact'
        stmt = f"""
            INSERT INTO {t1} (
                cust_no, contacter, depart, job_title, tel, tel_ext, mobile, input_time, input_name
            ) VALUES (
                '{data_d['cust_no']}', 
                {f"'{data_d['contacter']}'" if data_d['contacter'] is not None else 'NULL'}, 
                {f"'{data_d['depart']}'" if data_d['depart'] is not None else 'NULL'}, 
                {f"'{data_d['job_title']}'" if data_d['job_title'] is not None else 'NULL'}, 
                {f"'{data_d['tel']}'" if data_d['tel'] is not None else 'NULL'}, 
                {f"'{data_d['tel_ext']}'" if data_d['tel_ext'] is not None else 'NULL'}, 
                {f"'{data_d['mobile']}'" if data_d['mobile'] is not None else 'NULL'},
                NOW(), 
                '{data_d['sales_name']}'
            );
        """

        self.erpdb_execute(stmt)
        # 查詢id
        query_stmt = "SELECT currval('erp_crm_namelist_contact_id_seq');"
        self.erpdb_execute(query_stmt)
        ret_id = self.erpdb_fetchone(query_stmt)

        return ret_id[0] if ret_id else None

    

    # 如果送文宣要存文宣類別
    def upsert_erp_crm_namelist_special(self, data_d):
        t1 = 'erp_crm_namelist_special'
        stmt = f"""
            INSERT INTO {t1} (
                cust_no, cust_brief, "role", sales_no, sales_name, call_time, call_status, is_email, is_fax, is_line, promo_document, document_date
            ) VALUES (
                '{data_d['cust_no']}', 
                {f"'{data_d['cust_brief']}'" if data_d['cust_brief'] is not None else 'NULL'}, 
                'role2', 
                '{data_d['sales_no']}',
                '{data_d['sales_name']}',
                NOW(),
                {f"'{data_d['last_call_status']}'" if data_d['last_call_status'] is not None else 'NULL'},
                {'TRUE' if data_d['is_mail'] else 'FALSE'},
                {'TRUE' if data_d['is_fax'] else 'FALSE'},
                {'TRUE' if data_d['is_line'] else 'FALSE'},
                {f"'{data_d['pomoDocuItems']}'" if data_d['pomoDocuItems'] is not None else 'NULL'},
                NOW()
            )
            ON CONFLICT (cust_no, sales_no, "role") 
            DO UPDATE SET
                cust_brief = EXCLUDED.cust_brief,
                sales_name = EXCLUDED.sales_name,
                call_time = NOW(),
                call_status = EXCLUDED.call_status,
                is_email = EXCLUDED.is_email,
                is_fax = EXCLUDED.is_fax,
                is_line = EXCLUDED.is_line,
                promo_document = EXCLUDED.promo_document,
                document_date = NOW()
        """
        rows = self.erpdb_execute(stmt)
        return rows

    

    # 儲存 erp_crm_log
    def stmt_insert_erp_crm_log(self, data_d):
        t1 = 'erp_crm_log'
        stmt = f"""
            INSERT INTO {t1} (
                event_id,
                appname,
                cust_no,
                cust_brief,
                contacter,
                contacter_id,
                sales_no,
                tel,
                mobile,
                role,
                call_time,
                call_status,
                advice,
                input_time,
                input_name,
                start_date,
                is_document
            ) VALUES (
                '{data_d['event_id']}',
                '{data_d['appname']}',
                '{data_d['cust_no']}', 
                {f"'{data_d['cust_brief']}'" if data_d['cust_brief'] is not None else 'NULL'}, 
                {f"'{data_d['contacter']}'" if data_d['contacter'] is not None else 'NULL'}, 
                {f"'{data_d['cont_id']}'" if data_d['cont_id'] is not None else 'NULL'},
                '{data_d['sales_no']}', 
                {f"'{data_d['cust_tel']}'" if data_d['cust_tel'] is not None else 'NULL'},
                {f"'{data_d['mobile']}'" if data_d['mobile'] is not None else 'NULL'},
                'role2',
                NOW(),  -- call_time
                {f"'{data_d['last_call_status']}'" if data_d['last_call_status'] is not None else 'NULL'},
                {f"'{data_d['memo']}'" if data_d['memo'] is not None else 'NULL'},
                NOW(),  -- input_time
                '{data_d['sales_name']}',
                '9999-12-31',
                {f"'{data_d['is_document']}'" if data_d['is_document'] is not None else 'NULL'}
            )
        """
        rows = self.erpdb_execute(stmt)
        return rows


    # 儲存 erp_crm_last_log
    def stmt_insert_erp_crm_last_log(self, data_d):
        t1 = 'erp_crm_last_log'
        stmt = f"""
            INSERT INTO {t1} (
                event_id,
                appname,
                cust_no,
                cust_brief,
                contacter,
                contacter_id,
                sales_no,
                tel,
                mobile,
                role,
                call_time,
                call_status,
                advice,
                input_time,
                input_name,
                start_date,
                is_document
            ) VALUES (
                '{data_d['event_id']}',
                '{data_d['appname']}',
                '{data_d['cust_no']}',
                {f"'{data_d['cust_brief']}'" if data_d['cust_brief'] is not None else 'NULL'},
                {f"'{data_d['contacter']}'" if data_d['contacter'] is not None else 'NULL'},
                {f"'{data_d['cont_id']}'" if data_d['cont_id'] is not None else 'NULL'},
                '{data_d['sales_no']}',
                {f"'{data_d['cust_tel']}'" if data_d['cust_tel'] is not None else 'NULL'},
                {f"'{data_d['mobile']}'" if data_d['mobile'] is not None else 'NULL'},
                'role2',
                NOW(),
                {f"'{data_d['last_call_status']}'" if data_d['last_call_status'] is not None else 'NULL'},
                {f"'{data_d['memo']}'" if data_d['memo'] is not None else 'NULL'},
                NOW(),
                '{data_d['sales_name']}',
                '9999-12-31',
                {f"'{data_d['is_document']}'" if data_d['is_document'] is not None else 'NULL'}
            )
            ON CONFLICT (event_id, start_date, cust_no, contacter_id)
            DO UPDATE SET
                appname = EXCLUDED.appname,
                cust_brief = EXCLUDED.cust_brief,
                sales_no = EXCLUDED.sales_no,
                tel = EXCLUDED.tel,
                mobile = EXCLUDED.mobile,
                role = EXCLUDED.role,
                call_time = NOW(),
                call_status = EXCLUDED.call_status,
                advice = EXCLUDED.advice,
                input_time = NOW(),
                input_name = EXCLUDED.input_name,
                is_document = EXCLUDED.is_document
        """
        rows = self.erpdb_execute(stmt)
        return rows
    
    # 儲存 erp_crm_custom_phase
    def stmt_insert_erp_crm_custom_phase(self, data_d):
        t1 = 'erp_crm_custom_phase'
        stmt = f"""
            INSERT INTO {t1} (
                event_id,
                appname,
                cust_no,
                cust_brief,
                contacter,
                contacter_id,
                sales_no,
                sales,
                tel,
                city,
                district,
                addr,
                zip,
                gb_cust_no,
                industry,
                employee_nums,
                role,
                last_call_time,
                last_contact_status,
                memo,
                input_time,
                input_name,
                start_date,
                end_date
            ) VALUES (
                '{data_d['event_id']}',
                '{data_d['appname']}',
                '{data_d['cust_no']}', 
                {f"'{data_d['cust_brief']}'" if data_d['cust_brief'] is not None else 'NULL'}, 
                {f"'{data_d['contacter']}'" if data_d['contacter'] is not None else 'NULL'}, 
                {f"'{data_d['cont_id']}'" if data_d['cont_id'] is not None else 'NULL'},
                '{data_d['sales_no']}',
                '{data_d['sales_name']}',
                {f"'{data_d['cust_tel']}'" if data_d['cust_tel'] is not None else 'NULL'},
                {f"'{data_d['city']}'" if data_d['city'] is not None else 'NULL'},
                {f"'{data_d['district']}'" if data_d['district'] is not None else 'NULL'},
                {f"'{data_d['addr']}'" if data_d['addr'] is not None else 'NULL'},
                {f"'{data_d['zip']}'" if data_d['zip'] is not None else 'NULL'},
                {f"'{data_d['gb_cust_no']}'" if data_d['gb_cust_no'] is not None else 'NULL'},
                {f"'{data_d['industry']}'" if data_d['industry'] is not None else 'NULL'},
                {f"'{data_d['employee_nums']}'" if data_d['employee_nums'] is not None else 'NULL'},
                'role2',
                NOW(),  -- call_time
                {f"'{data_d['last_call_status']}'" if data_d['last_call_status'] is not None else 'NULL'},
                {f"'{data_d['memo']}'" if data_d['memo'] is not None else 'NULL'},
                NOW(),  -- input_time
                '{data_d['sales_name']}',
                '9999-12-31',
                '9999-12-31'
            )
        """
    
        rows = self.erpdb_execute(stmt)
        return rows




"""
Process Function
"""


def crm1055_save(username, data_form, emp_no):
    dbh = DataDemand(username)
    ret_json = {'status': 'ERROR', 'msg': '儲存失敗'}
    industry = None if data_form['fmText06'] == '空白' else data_form['fmText06']
    # 預防可能沒輸入值的欄位
    def set_None_value(key):
        value = data_form.get(key)
        return value if value not in (None, '') else None

    last_call_status = data_form.get('fmText12')
    if last_call_status != 'C14':
        rcontact_date = None
    else:
        rcontact_date = set_None_value('fmText13')
    
    if last_call_status == 'C62':
        is_document = True
    else:
        is_document = None

    data_d = {
        'cust_no': set_None_value('CustNo'),
        'cust_brief': set_None_value('CustName'),
        'cust_tel': set_None_value('fmText04'),
        'cust_fax': set_None_value('fmText05'),
        'industry': industry,
        'cont_id': set_None_value('ContId'),
        'contacter': set_None_value('fmText07'),
        'cont_tel': set_None_value('fmText08'),
        'cont_tel_ext': set_None_value('fmText09'),
        'mobile': set_None_value('fmText10'),
        'cont_fax': set_None_value('fmText11'),
        'last_call_status': set_None_value('fmText12'),
        'rcontact_date': rcontact_date,
        'pomoDocuItems': data_form.get('fmText14', ''),
        'is_fax': data_form.get('fmText15') == 'true',
        'is_mail': data_form.get('fmText16') == 'true',
        'is_line': data_form.get('fmText17') == 'true',
        'memo': set_None_value('fmText18'),
        'city': set_None_value('fmText19'),
        'district': set_None_value('fmText20'),
        'zip': set_None_value('fmText21'),
        'addr': set_None_value('fmText22'),
        'employee_nums': set_None_value('fmText23'),
        'gb_cust_no' : set_None_value('fmText24'),
        'sales_no' : emp_no,
        'event_id' : 'CRM1041',
        'appname' : 'CRM1055',
        'sales_name' : username,
        'is_document' : is_document,
    }

    try:
        dbh.stmt_insert_erp_crm_log(data_d)
        dbh.stmt_insert_erp_crm_last_log(data_d)
        dbh.update_erp_crm_namelist_crm(data_d)
        dbh.stmt_insert_erp_crm_custom_phase(data_d)
        # 如果有聯絡人
        if data_d['cont_id'] is not None:
            # print("data_d['cont_id']", data_d['cont_id'])
            dbh.update_erp_crm_namelist_contact(data_d)

        # 如果送文宣
        if data_d['last_call_status'] == 'C62':
            dbh.upsert_erp_crm_namelist_special(data_d)

        ret_json = {'msg': '儲存成功', 'status': 'OK'}
    except Exception as e:
        print('儲存資料錯誤:', e)
        ret_json['mag'] = str(e)
    finally:
        dbh.close()

    return ret_json

def crm1055_query(username, data_form):
    # 查詢客戶詳細資料，包含聯絡人資料(如果有)
    cust_no = data_form.get('fmTextCUSNO', '')
    cont_id = data_form.get('fmTextCONID', '')
    dbh = DataDemand(username)
    cont_data_d = dict()
    ret_json = {'status': 'ERROR', 'msg': '查詢失敗'}
    try:
        contact_detail_data = dbh.stmt_select_erp_crm_namelist_contact_detail(cust_no, cont_id)
        if contact_detail_data:
            contact_info = contact_detail_data[0]
            cont_data_d = {
                'cust_no': contact_info.get('cust_no'),
                'cust_brief': contact_info.get('cust_brief'),
                'cust_tel': contact_info.get('cust_tel'),
                'cust_fax': contact_info.get('cust_fax'),
                'city': contact_info.get('city'),
                'district': contact_info.get('district'),
                'zip': contact_info.get('zip'),
                'addr': contact_info.get('addr'),
                'employee_nums': contact_info.get('employee_nums'),
                'gb_cust_no' : contact_info.get('gb_cust_no'),
                'industry': contact_info.get('industry'),
                'cont_id': contact_info.get('id'),
                'contacter': contact_info.get('contacter'),
                'cont_tel': contact_info.get('cont_tel'),
                'cont_tel_ext': contact_info.get('cont_tel_ext'),
                'mobile': contact_info.get('mobile'),
                'cont_fax': contact_info.get('cont_fax'),
                'is_email': contact_info.get('is_email'),
                'is_fax': contact_info.get('is_fax'),
                'is_line': contact_info.get('is_line')
            }
        else:
            cont_data_d = None 

        ret_json = {'data': cont_data_d, 'status': 'OK', 'msg' :'查詢成功'}
    except Exception as e:
        print('查詢詳細聯絡人資料錯誤:', e)
        ret_json['msg'] = str(e)
    finally:
        dbh.close()
    
    return ret_json



def crm1055_search(username, data_form):
    data_ld = list()

    dbh = DataDemand(username)
    status = data_form.get('fmText01', '')
    city = data_form.get('fmText02', '')
    district = data_form.get('fmText03', '')
    ret_json = {'status': 'ERROR', 'msg': '查詢失敗'}
    try:
        # 未處理過的名單
        uncalled_list_rows = dbh.stmt_get_uncalled_list(status, city, district)
        # 非當天已處理過的名單
        called_list_rows = dbh.stmt_get_called_list(status, city, district)
        # 當天已處理過的名單
        called_today_list_rows = dbh.stmt_get_called_today_list(status, city, district)

        # 整理未處理過的名單
        for row in uncalled_list_rows:
            city = row.get('city', '')
            district = row.get('district', '') or ''
            addr = row.get('addr', '') or ''
            address = f"{city}{district}{addr}"
            data_ld.append({
                'cust_no': row['cust_no'],
                'cust_brief': row['cust_brief'],
                'role2_call_time': row['role2_call_time'],
                'role2_call_status': row['role2_call_status'],
                'rcontact_date': '',
                'city': city,
                'district': district,
                'zip': row['zip'],
                'addr': addr,
                'address': address,
                'employee_nums': row['employee_nums'],
                'gb_cust_no': '',
                'tel': row['tel'],
                'fax': row['fax'],
                'industry': row['industry'],
                'rcontact_date': row['rcontact_date']
            })

        # 整理 '非當天' 已處理過的名單
        for row in called_list_rows:
            city = row.get('city', '')
            district = row.get('district', '') or ''
            addr = row.get('addr', '') or ''
            address = f"{city}{district}{addr}"
            data_ld.append({
                'cust_no': row['cust_no'],
                'cust_brief': row['cust_brief'],
                'role2_call_time': row['role2_call_time'],
                'role2_call_status': row['role2_call_status'],
                'rcontact_date': '',
                'city': city,
                'district': district,
                'zip': row['zip'],
                'addr': addr,
                'address': address,
                'employee_nums': row['employee_nums'],
                'gb_cust_no': '',
                'tel': row['tel'],
                'fax': row['fax'],
                'industry': row['industry'],
                'rcontact_date': row['rcontact_date']
            })

        # 整理 '當天' 已處理過的名單
        for row in called_today_list_rows:
            city = row.get('city', '')
            district = row.get('district', '') or ''
            addr = row.get('addr', '') or ''
            address = f"{city}{district}{addr}"
            role2_call_status = row['role2_call_status']
            if row['gb_cust_no']:
                role2_call_status += '(已有進銷存編號)'
            data_ld.append({
                'cust_no': row['cust_no'],
                'cust_brief': row['cust_brief'],
                'role2_call_time': row['role2_call_time'],
                'role2_call_status': role2_call_status,
                'rcontact_date': '',
                'city': city,
                'district': district,
                'zip': row['zip'],
                'addr': addr,
                'address': address,
                'employee_nums': row['employee_nums'],
                'gb_cust_no': row['gb_cust_no'],
                'tel': row['tel'],
                'fax': row['fax'],
                'industry': row['industry'],
                'rcontact_date': row['rcontact_date']
            })

        if data_ld:
            ret_json = {'data': data_ld, 'status': 'OK', 'msg' :'查詢成功'}
        else:
            ret_json['msg'] = '查無資料'
    except Exception as e:
        print('查詢名單錯誤:', e)
        ret_json['msg'] = str(e)
    finally:
        dbh.close()

    return ret_json


def crm1055_main(username):
    data_dl = dict()
    industry_d = dict()
    caption_d = dict()
    promo_d = dict()
    addr_d = dict()
    dbh = DataDemand(username)

    try:
        caption_data = dbh.stmt_select_erp_survey_detail() or []
        industry_data = dbh.stmt_select_erp_crm_industry() or []
        promo_data = dbh.stmt_select_erp_promo_leader() or []
        # 讀取使用者一開始查詢資料條件用的地區(只顯示有資料的自送區)
        select_zip_data = dbh.stmt_select_zip_delive_search() or []
        # 讀取全部自送地區
        addr_data = dbh.stmt_select_zip_delive() or []

        # 行業別
        for data in industry_data:
            industry_d[data['industry_no']] = data['industry_name']

        # 聯絡狀態
        for data in caption_data:
            caption_d[data['caption_no']] = data['caption']

        # 文宣類別
        for data in promo_data:
            promo_d[data['promo_ld_no']] = data['promo_ld_name']

        # 全部自送地區
        for data in addr_data:
            city = data['city']
            district = data['district'] if data['district'] is not None else ''
            zip_code = data['zip'] if data.get('zip') is not None else ''
            # 使用 setdefault 方法來初始化城市
            addr_d.setdefault(city, {})  # 確保城市是字典
            addr_d[city][district] = zip_code


        # 使用者一開始查詢資料條件用的地區(只顯示有資料的自送區)
        for city, district, status in select_zip_data:
            district = district if district is not None else ''
            data_dl.setdefault(city, {}).setdefault(district, set()).add(status)
        for city in data_dl:
            for district in data_dl[city]:
                data_dl[city][district] = list(data_dl[city][district])

    except Exception as e:
        print('查詢有資料地區錯誤 :', e)

    finally:
        dbh.close()

    outline_d = {
        'industry_d': industry_d,
        'caption_d': caption_d,
        'promo_d': promo_d,
        'addr_d': addr_d
    }

    return data_dl, outline_d


def crm1055_get_contact(data_uri, username):
    # 查詢聯絡人(下面那排)
    cust_no = data_uri['text01']
    dbh = DataDemand(username)
    try:
        rows = dbh.stmt_select_erp_crm_namelist_contact_bottom(cust_no)
        if rows:
            data_ld = [{**row,
                        'last_call_time': row['last_call_time'].strftime(
                            '%Y-%m-%d') if row['last_call_time'] else row['last_call_time']
                        } for row in rows]
            ret_json = dict(data = data_ld, status = 'OK')
        else:
            ret_json = dict(data=[], status='OK', msg='查無資料')
    except Exception as e:
        print('查詢聯絡人錯誤:', e)
        ret_json =  dict(status='ERROR', msg=str(e))
    finally:
        dbh.close()

    return ret_json

    
def crm1055_save_contact(data_form, username):
    # 新增聯絡人
    def set_None_value(key):
        return data_form.get(key) or None

    data_d = {
        'cust_no': set_None_value('cust_no'),
        'contacter': set_None_value('fmText52'),
        'tel': set_None_value('fmText53'),
        'tel_ext': set_None_value('fmText54'),
        'mobile': set_None_value('fmText55'),
        'tel_no': f"{set_None_value('fmText53') or ''}#{set_None_value('fmText54') or ''}" if set_None_value('fmText54') else set_None_value('fmText53'),
        'depart': set_None_value('fmText56'),
        'job_title': set_None_value('fmText57'),
        'sales_name': username
    }
    dbh = DataDemand(username)
    ret_json = {'status': 'ERROR', 'msg': '新增失敗'}

    try:
        ret_id = dbh.insert_erp_crm_namelist_contact(data_d)
        if ret_id is not None:
            ret_json = {'cont_id': ret_id, 'status': 'OK', 'msg': '新增成功'}
    except Exception as e:
        print('新增聯絡人錯誤:', e)
        ret_json['msg'] = str(e)
    finally:
        dbh.close()
    
    # print('cust_no', data_d['cust_no'])
    # print('cont_id', ret_id)
    return ret_json

"""
Main Entry
"""


class Crm1055(TemplateView):
    template_name = 'crm1055.html'

    def get(self, request, *args, **kwargs):
        if request_app_auth(request, 'crm', 'crm1055') is None:
            return HttpResponseRedirect('/')
        username = request.session['username']
        data_uri = get_uri_data(request)
        if 'text01' in data_uri:
            ret_json = crm1055_get_contact(data_uri, username)
            return JsonResponse(ret_json)
        data_dl, outline_d = crm1055_main(username)
        template_data = dict(
            data_dl=data_dl,
            outline_d=outline_d,
            facing_d=dict(username=username)
        )

        return render(request, self.template_name, template_data)

    def post(self, request):
        data_form = FormData(request).get_data()
        data_ld = list()
        username = request.session['username']
        emp_no = request.session['empno']
        op = data_form['fmTextOP']
        if op == 'SEARCH':
            ret_json = crm1055_search(username, data_form)
            return JsonResponse(ret_json)
        elif op == 'QUERY':
            ret_json = crm1055_query(username, data_form)
            return JsonResponse(ret_json)
        elif op == 'SAVE':
            ret_json = crm1055_save(username, data_form, emp_no)
            return JsonResponse(ret_json)
        elif op == "CONTACT":
            ret_json = crm1055_save_contact(data_form, username)
            return JsonResponse(ret_json)
        template_data = dict(
            form_d=data_form,
            data_ld=data_ld,
        )

        return render(request, self.template_name, template_data)
