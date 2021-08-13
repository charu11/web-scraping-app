import pandas as pd
from scraping import db
import matplotlib.pyplot as plt

# adding saved image URL
plot_url = './scraping/static/images/image.png'


def plotting1():
        df = pd.read_sql('details', db.engine)
        # remove all the comma in price values
        df['price'] = df['price'].apply(lambda x: x.replace(',', ''))
        df['price'] = df['price'].astype(int)
        df_price = df[['state', 'price']]
        df_new = df_price.groupby(['state']).mean().reset_index()
        fig = plt.figure()
        state_name = df_new['state']
        price_tag = df_new['price']
        plt.xlabel("State Name")
        plt.ylabel('Estimated Price(million)')
        # plot the figure
        plt.plot(state_name, price_tag)
        # save the figure
        plt.savefig(plot_url)
        return None



