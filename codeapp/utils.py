# built-in imports
# standard library imports
import csv
from datetime import datetime

# external imports
from codeapp.models import EuropeSalesRecords

# internal imports


def get_data_list() -> list[EuropeSalesRecords]:
    data_list = []
    with open("Europe_Sales_Records.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            order_id = int(row["Order ID"])
            country = row["Country"]
            item_type = row["Item Type"]
            order_priority = row["Order Priority"]
            order_date = datetime.strptime(row["Order Date"], "%m/%d/%Y").date()
            ship_date = datetime.strptime(row["Ship Date"], "%m/%d/%Y").date()
            units_sold = int(row["Units Sold"])
            profit = float(row["Total Profit"])
            data_list.append(
                EuropeSalesRecords(
                    order_id,
                    country,
                    item_type,
                    order_priority,
                    order_date,
                    ship_date,
                    units_sold,
                    profit,
                )
            )
    return data_list


def calculate_statistics(dataset: list[EuropeSalesRecords]) -> dict[str, int]:
    priority_count: dict[str, int] = {}
    for record in dataset:
        if record.order_priority in priority_count:
            priority_count[record.order_priority] += 1
        else:
            priority_count[record.order_priority] = 1
    return priority_count


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
