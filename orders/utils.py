import datetime


def generate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%s")
    order_number = current_datetime + str(pk)
    print(order_number)
    return order_number[:20]
