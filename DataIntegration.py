import pandas as pd

# read csv files
ETMall_df = pd.read_csv('ETMall_output.csv')
Momo_df = pd.read_csv('momo_output.csv')
PCHome_df = pd.read_csv('output.csv')

# create global dataframe
df = pd.DataFrame()

# data pre-processing
def preProcessing():

    global df
    ETMall_df['platform'] = 'ETMall'
    Momo_df['platform'] = 'Momo'
    PCHome_df['platform'] = 'PCHome'

    # deal with proce column, make the values all numeric and remove symbols
    ETMall_df['price'] = ETMall_df['price'].str.replace(',', '').astype(float)
    Momo_df['price'] = Momo_df['price'].str.replace(',', '')
    Momo_df['price'] = Momo_df['price'].str.replace('$', '',regex=False).astype(float)

    # concant dataframes
    df = pd.concat([ETMall_df, Momo_df, PCHome_df])

    # remove products "non TV" products
    df = df[~df["prodName"].str.contains('電視櫃|電視移動架|護目鏡|電視立架|壁掛架|支架|電視架|電視護目防撞保護鏡')]
    df = df[df["prodName"].str.contains('吋|型')]

def ProductNameHandling():
    # 從商品名稱中擷取 “品牌”
    brands = ['小米','瑞軒', 'JVC', 'Panasonic','國際牌','DecaMax','志佳', '聲寶', '歌林', '台灣三洋', '東芝', '夏普', 'AOC', 'BenQ', '三星', '大同', '東元', '禾聯', '山水', '海爾', '飛利浦', 'DECAMAX', 'Sony','SONY', 'LG', '奇美', '愛華', 'TCL', 'TEGA', 'OVO', '雷鳥', '嘉豐', '特佳', 'JINDI', 'CHIQ', '聯碩', '創維', 'DigiKing', 'IMARFLEX', 'SKYWORTH', 'realme', 'PERSONA','Dennys','Atima']
    # 從上面的list 中尋找, 如果有兩個對照上的, 會先用list中纖出現的那個

    # 下面要用 extract, 不能用 extract all （extract只返回第一个匹配到的字符；extractall将匹配所有返回的字符）
    s = df['prodName'].str.extract(f'({"|".join(brands)})')

    ## 上面 join 那一句就是轉換成下面這個形式,用｜( or expression ), 讓extractall function 可以從中去尋找（）中相對的詞
    ## s = df['prodName'].str.extractall(f'(瑞軒|JVC|Panasonic)')

    df['brand'] = s

    # 從商品名稱中擷取尺寸, 找出 "吋" 或 "型" 的前面兩個數字, 擷取出來存取成 "size"
    df['size'] = df['prodName'].str.split("吋|型").str[0].str[-2:]

    # is4K, 從商品名稱中擷取 4k 的詞, 並存取成是否為 4k
    df.loc[df['prodName'].str.contains("4K"),'is4K'] = "1"
    df.loc[~df['prodName'].str.contains("4K"),'is4K'] = "0"

preProcessing()
ProductNameHandling()
df.to_csv('final_output.csv',index=False)
