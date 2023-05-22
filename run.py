from airbnb.main_class import Airbnb
import airbnb.const as const
from airbnb.urls_to_xls import send_data_to_xl



def main():
    sk = Airbnb()
    sk.max_price = 80000
    sk.start_date = '2023-10-01'
    sk.end_date = '2023-10-31'
    data = sk.run(const.LOCATION)
    send_data_to_xl(data, const.LOCATION)

main()

