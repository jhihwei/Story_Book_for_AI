import json
from linebot import LineBotApi

secretFileContentJson = json.load(open("./line_secret_key", 'r', encoding='utf8'))
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))


def generate_rich_menu_id():
    rich_menu_array = ['rich_menu_b']

    from linebot.models import RichMenu

    for rich_menu_name in rich_menu_array:
        # 創建菜單，取得menuId
        lineRichMenuId = line_bot_api.create_rich_menu(rich_menu=RichMenu.new_from_json_dict(
            json.load(open("素材/" + rich_menu_name + '/rich_menu.json', 'r', encoding='utf8'))))
        print("-設定檔上傳結果")
        print(lineRichMenuId)

        # id寫入本地端
        f = open("素材/" + rich_menu_name + "/rich_menu_id", "w", encoding='utf8')
        f.write(lineRichMenuId)
        f.close()

        # 上傳照片至該id
        set_image_response = ''
        with open("素材/" + rich_menu_name + '/rich_menu.jpg', 'rb') as f:
            set_image_response = line_bot_api.set_rich_menu_image(lineRichMenuId, 'image/jpeg', f)

        print("-圖片上傳結果")
        print(set_image_response)


def unboundle():
    # rich_menu_id_array = ["rich_menu_0"]
    secretFileContentJson = json.load(open("./line_secret_key", 'r', encoding='utf8'))
    line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))

    self_user_id = secretFileContentJson.get('self_user_id')
    print(line_bot_api.unlink_rich_menu_from_user(self_user_id))


def remove(id:str):
    secretFileContentJson = json.load(open("./line_secret_key", 'r', encoding='utf8'))
    line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))

    # 設定要移除的rich_menu
    rich_menu_name_array = ["rich_menu_b"]

    for rich_menu_name in rich_menu_name_array:
        # 讀取rich_menu_id檔案，並告知 Line 進行刪除，並在刪除後，把本地檔案內容清除
        with open("素材/" + rich_menu_name + '/rich_menu_id', 'r') as myfile:
            rich_menu_id = myfile.read()
            deleteResult = line_bot_api.delete_rich_menu(id)
            print(deleteResult)

        f = open("素材/" + rich_menu_name + "/rich_menu_id", "w")
        f.write('')
        f.close()


def get_list():
    from linebot import (LineBotApi)
    import json

    secretFileContentJson = json.load(open("./line_secret_key", 'r', encoding='utf8'))
    line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
    rich_menus = line_bot_api.get_rich_menu_list()
    for r in rich_menus:
        print(r)


if __name__ == '__main__':
    generate_rich_menu_id()
    # remove("richmenu-d33bc6b739a041348d4ad9c90b08a9ca")
    get_list()
    # unboundle()
