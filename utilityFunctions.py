def reshapeDataFrame(list,future):
    """
    reshapeDataFrame(list,future):

    Parameters:
        list: data to be reshape
        future: future name
    """

    df=pd.DataFrame(list)
    df.drop(columns='id',axis=1,inplace=True)

    # 更換時區到台北
    df.index = pd.to_datetime(df.pop('time'), utc=True)
    df.index = df.index.tz_convert('Asia/Taipei')  
    # df.reset_index()
    return df

# line_token='hvkQ8UzJkdSDfvKUXPOtzRSMbXprnpy5XV5pgx7C7IM'
def Line_Notify(message, img=None, token=line_token):
    #設定群組對應的權杖
    headers = {"Authorization": "Bearer " + token}
    #填入想傳送的訊息
    param = {'message': message}
    #上傳想要傳送的圖片
    if(img):
        image = {'imageFile' : open(str(img), 'rb')}
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = param, files = image)
    else:
    #傳送
        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = param)
    return r.status_code
