'''This is created by https://developers.google.com/drive/api/v3/quickstart/python
元はGoogle Drive for DevelopersのPyton Quickstartだが、それに手を加えている
'''
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# 追加
import os, json
from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

import datetime

class GoogleDrive:
  """Google Drive APIのクラス。基本的にドライブ上のファイルの重複はないものとして実装している。
  """
  def __init__(self):
    self.service = build('drive', 'v3', credentials=self.Create_credentials())
    """Drive上のファイル操作などに使用するサービス"""
    self.APP_DATA_FOLDER = '.appdata'
    """アプリのデータを格納するフォルダの名前"""
    self.MIMETYPES = { 'folder': 'application/vnd.google-apps.folder', 'json': 'application/json' }
    """mimeTypeの辞書（間違えやすいので）"""
    self.APP_DATA_FOLDER_ID = self.App_Data_Folder_ID()
    """アプリのデータを格納するフォルダのID"""


  def Update_File(self, filename):
    """ファイルをドライブ上のアプリデータフォルダ内にアップロードし、既に存在していれば上書きする。
    具体的な動作としては、まず指定された名前の古いファイルがフォルダ内に存在するか検索し、
    存在すればアップロード後に古いファイルを削除する。
    
    Args:
        filename (str): アップロードするjsonファイルのファイル名（拡張子含む）
    
    Returns:
        file: 'id' が入っている。file.get('id')などで取得可能。
    """
    file_old = self.Search_a_file_from_Appdir(filename)
    file = self.Upload_File(filename)

    # file_oldがNoneでなければアップロード後に古いやつを削除する。
    # 一応file_oldとfileのID被りもチェックしておく。
    if file_old == None or file_old.get('id') == file.get('id'):
      return file
    
    self.Delete_File(file_old.get('id'))
    print(f"The file of Drive is updated.\n  (name, ID) is: ({filename}, {file.get('id')})")
    return file


  def Upload_File(self, filename):
    """ファイルをドライブ上のアプリデータフォルダ内にアップロードする。

    Args:
        filename (str): アップロードするファイルのファイル名（拡張子含む）

    Returns:
        file: 'id' が入っている。file.get('id')などで取得可能。
    """
    file_metadata = {
      'name': filename,
      'parents': [self.APP_DATA_FOLDER_ID],
    }
    localpath = filename
    media = MediaFileUpload(
      filename, resumable=True
    )
    file = self.service.files().create(
      body=file_metadata, media_body=media, fields='id'
    ).execute()

    print(f"The file uploaded.\n  (name, ID) is: ({filename}, {file.get('id')})")
    return file


  def Download_File_from_Appdir(self, filename, output_dir='.'):
    """ドライブ上のアプリデータフォルダ内のファイルをダウンロードする。

    Args:
        filename (str): ダウンロードするファイルのファイル名（拡張子含む）
        output_dir (str): 出力フォルダのパス
    """
    file = self.Search_a_file_from_Appdir(filename)
    if file == None:
      print("The file you requested is not found.")
      return
    
    self.Download_File(file.get('id'), filename, output_dir)
  

  def Download_File(self, file_id, filename, output_dir='.'):
    """ドライブ上のファイルをダウンロードする。

    Args:
        file_id (str): ドライブ上のファイルのID
        filename (str): 出力ファイル名
        output_dir (str): 出力フォルダのパス
    """
    request = self.service.files().get_media(fileId=file_id)
    print(f"The file is being downloaded...\n  (name, ID) is: ({filename}, {file_id})")
    with open(os.path.join(output_dir, filename), 'wb') as f:
      downloader = MediaIoBaseDownload(f, request)
      done = False
      while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")
    print("Download completed.")


  def Delete_File(self, file_id):
    """ドライブ上のファイルを削除する。

    Args:
        file_id (str): ドライブ上のファイルのID
    
    Returns:
    """
    self.service.files().delete(fileId=file_id).execute()
    print(f"The file deleted.\n  ID is: {file_id}")
    return


  def App_Data_Folder_ID(self):
    """Drive上のアプリのデータを格納するフォルダのIDを返す。
    
    Returns:
        str: アプリデータフォルダのIDの文字列。
    """
    folder = self.Search_a_file(self.APP_DATA_FOLDER, mimeType='folder')

    # 存在しなければ作成
    if (folder == None):
      file_metadata = { 'name': self.APP_DATA_FOLDER, 'mimeType': self.MIMETYPES['folder'] }
      folder = self.service.files().create(body=file_metadata, fields='id').execute()
    print(f"Got the folder this app uses.\n  ID is: {folder.get('id')}")
    return folder.get('id')


  def Search_a_file_from_Appdir(self, filename, mimeType=None, trashed=False):
    """クエリにマッチするファイルを一つ、アプリデータフォルダの中から検索し、存在すればそのファイルを、なければNoneを返す。
    
    Args:
        filename (str): 検索するファイル名。
        mimeType (str): 検索するファイルのmimeType。厳密には、self.MIMETYPE辞書のキーのいずれか。
        trashed (bool): 検索対象がゴミ箱の中のファイルか否か

    Returns:
        file: 'id' と 'name' が入っている。file.get('id')などで取得可能。
    """
    return self.Search_a_file(filename, parent_dir_id=self.APP_DATA_FOLDER_ID, mimeType=mimeType, trashed=trashed)


  def Search_a_file(self, filename, parent_dir_id=None, mimeType=None, trashed=False):
    """指定した名前のファイルを指定したIDのフォルダから一つ検索し、
    存在すればそのファイルを、なければNoneを返す。

    Args:
        filename (str): 検索するファイル名。
        parent_dir_id (str): ファイルを検索するフォルダのID。
        mimeType (str): 検索するファイルのmimeType。厳密には、self.MIMETYPE辞書のキーのいずれか。
        trashed (bool): 検索対象がゴミ箱の中のファイルか否か

    Returns:
        file: 'id' と 'name' が入っている。file.get('id')などで取得可能。
    """
    # クエリ列はここで構成する。
    queries = [f"name = '{filename}'"]
    if parent_dir_id != None:
      queries.append(f"'{parent_dir_id}' in parents")
    if mimeType != None:
      queries.append(f"mimeType = '{self.MIMETYPES[mimeType]}'")
    trashed_str = 'true' if trashed else 'false'
    queries.append(f"trashed = {trashed_str}")

    page_token = None
    while True:
      response = self.service.files().list(
        q=" and ".join(queries), fields='nextPageToken, files(id, name)', pageToken=page_token
      ).execute()

      for file in response.get('files', []):
        # Process change
        print(f"Found a searched file!\n  (name, ID) is: ({file.get('name')}, {file.get('id')})")
        return file

      page_token = response.get('nextPageToken', None)
      if page_token is None:
        break
    return None


  def Create_credentials(self):
    """Google Drive for DevelopersのPythonのQuickStartのmain()の改変。認証情報を返す。
    Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    '''jsonファイルの存在確認ではなく、環境変数キーの存在確認を行う。
    '''
    # if os.path.exists('token.json'):
    if 'GOOGLE_TOKEN_JSON' in os.environ:
        '''token.jsonの内容を環境変数にブチ込んだものを使用
        '''
        creds = Credentials.from_authorized_user_info(json.loads(os.environ['GOOGLE_TOKEN_JSON']), SCOPES)
        # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            '''client_secret_XXXXXX.jsonの内容を環境変数にブチ込んだものを使用
            '''
            flow = InstalledAppFlow.from_client_config(json.loads(os.environ['GOOGLE_CLIENT_SECRET_JSON']), SCOPES)
            # flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        '''token.jsonに保存するはずの内容を環境変数に入れる。
        但しプログラムによる環境変数の変更はそのPythonプログラム中でのみ有効らしく、この操作は意味なさそうな気がする。
        '''
        os.environ['GOOGLE_TOKEN_JSON'] = creds.to_json()
        # with open('token.json', 'w') as token:
        #     token.write(creds.to_json())
    return creds



DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

# def something_json(filename):
#   """jsonファイルに対してなんかやる

#   Args:
#       filename (str): jsonファイルのファイル名
#   """
#   with open(filename, 'r', encoding='utf-8') as f:
#     json_dict = json.load(f)
  
#   date_str = json_dict.get('last_updated')
#   date_dt = datetime.datetime.strptime(date_str, DATETIME_FORMAT)
#   print(date_dt)
#   dt_now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
#   json_dict['last_updated'] = dt_now_jst.strftime(DATETIME_FORMAT)

#   with open(filename, 'w', encoding='utf-8') as f:
#     json.dump(json_dict, f, ensure_ascii=False, indent=4, sort_keys=True)



if __name__ == '__main__':
  # 環境変数を.envファイルから読み込む
  load_dotenv()
  
  drive = GoogleDrive()
  filename = 'config.json'
  drive.Download_File_from_Appdir(filename)
  # 何らかのjsonファイルに対する処理
  # something_json(filename)
  drive.Update_File(filename)

