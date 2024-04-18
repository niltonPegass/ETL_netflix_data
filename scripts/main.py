import pandas as pd
import os
import glob
import openpyxl
import xlsxwriter

# caminho para ler os arquivos
folder_path_raw = '/home/niltonp/Documentos/repo-local/DIO_challenges/python/netflix-test-resolved-main/src/data/raw'
folder_path_ready = '/home/niltonp/Documentos/repo-local/DIO_challenges/python/netflix-test-resolved-main/src/data/ready'

# lista todos os arquivos de excel
excel_files = glob.glob(os.path.join(folder_path_raw , '*.xlsx'))
# campaigns_groups = glob.glob(os.path.join(folder_path_ready , '*.xlsx'))

# dfs_sec_campaigns = pd.read_excel(campaigns_groups)

if not excel_files:
  print("nenhum arquivo compativel encontrado")

  dir_list = os.listdir(folder_path_raw) 
  print("Files and directories in '", folder_path_raw, "' :") 
  print(dir_list) 

else:

  # dataframe  = tabela na memória para guardar os conteúdos dos arquivos
  dfs_primary = []

  for excel_file in excel_files:
    
    try:
      # leio o arquivo de excel
      df_temp = pd.read_excel(excel_file)
          
      # pegar o nome do arquivo
      file_name = os.path.basename(excel_file)
          
      df_temp['filename'] = file_name

      # criamos uma nova coluna chamada location
      if 'brasil' in file_name.lower():
        df_temp['location'] = 'brazil'
      elif 'france' in file_name.lower():
        df_temp['location'] = 'france'
      elif 'italian' in file_name.lower():
        df_temp['location'] = 'italy'

      # criamos uma nova coluna chamada campaign
      df_temp['campaign'] = df_temp['utm_link'].str.extract(r'utm_campaign=([a-z]*)')
      df_temp['Contracted Plan'] = df_temp['Contracted Plan'].str.extract(r'Plano (\w*)')

      if df_temp['Contracted Plan'].str.contains('Básico').any():
        df_temp.loc[df_temp['Contracted Plan'].str.contains('Básico'), 'Contracted Plan'] = 'basic'
      if df_temp['Contracted Plan'].str.contains('Padrão').any():
        df_temp.loc[df_temp['Contracted Plan'].str.contains('Padrão'), 'Contracted Plan'] = 'standard'
      if df_temp['Contracted Plan'].str.contains('Premium').any():
        df_temp.loc[df_temp['Contracted Plan'].str.contains('Premium'), 'Contracted Plan'] = 'premium'

      # guarda dados tratados dentro de uma dataframe
      dfs_primary.append(df_temp)

    except Exception as e:
      print(f"Erro ao ler o arquivo {excel_file} : {e}")

  if dfs_primary:

    # concatena todas as tabelas salvas no dfs_primary em uma unica tabela
    result = pd.concat(dfs_primary, ignore_index=True)

    # caminho de saída
    output_file = os.path.join(folder_path_ready, 'netflix_data_v1.xlsx')

    # configurou o motor de escrita
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # leva os dados do resultado a serem escritos no motor de excel configurado
    result.to_excel(writer, index=False)

    # salva o arquivo de excel
    writer._save()
    print(f'\n>> arquivo salvo em: \n>> {folder_path_ready}\n')
    print(df_temp)

  else:
    print("nenhum dado para ser salvo")
