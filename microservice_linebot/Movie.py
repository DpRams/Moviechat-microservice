
class Movie:
    def __init__(self):
        self.movie_df = None

    def update_movie(self, movie_df):
        self.movie_df = movie_df

    def check_len(self, rank):
        if rank > len(self.movie_df):
            rank = len(self.movie_df)
        return rank

    def get_movie_name(self, id):
        return self.movie_df['片名'][id-1]

    def get_movie(self, rank=1, col=None):
        print(f'rank = {rank}, len(df) = {len(self.movie_df)}')
        if col == None:
            res = {}
            res = self.movie_df.iloc[rank-1].to_dict()
            return res
        if col in ("本周排名", "片名", "評分", "連結", '電影海報', "上映日期", "片長", "發行公司", "導演", "劇情介紹"):
            res = str(self.movie_df.iloc[rank-1][col])
            return res
        else:
            print("無此資訊")

    def get_movie_photo_urls(self, id):
        if id > len(self.movie_df):
            id = len(self.movie_df)
        image_url = eval(self.movie_df['劇照'][id-1])

        return image_url
