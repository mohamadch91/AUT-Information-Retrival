import pandas

excel_data_df = pandas.read_excel('IR01_3_test_4k.xlsx', sheet_name='Sheet1')

json_str = excel_data_df.to_json()
f=open('IR01_3_test_4k.json','x')
f.write(json_str)
f.close()

excel_data_df = pandas.read_excel('IR01_3_46k.xlsx', sheet_name='Sheet1')

json_str = excel_data_df.to_json()
f=open('IR01_3_46k.json','x')
f.write(json_str)
f.close()
