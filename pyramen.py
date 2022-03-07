import csv
from pathlib import Path

# Make list from csv file
def make_list(file_path):
    csv_list = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            csv_list.append(row)
    return csv_list


# Make report from lists
def make_report(menu_list, sales_list):
    # Initialize dict object to hold our key-value pairs of items and metrics
    report = {}

    # Loop over every row in the sales list object
    for row in sales_list:
        # Line_Item_ID,Date,Credit_Card_Number,Quantity,Menu_Item
        quantity = row[3]
        sales_item = row[4]

        # If the item value not in the report, add it as a new entry with initialized metrics
        if sales_item not in report:
            report[sales_item] = {'count': 0,
                                  'revenue': 0, 'cost': 0, 'profit': 0}

        # For every row in our sales data, loop over the menu records to determine a match
        for menu_item in menu_list:
            # Item,Category,Description,Price,Cost
            menu_item_name = menu_item[0]
            menu_item_price = menu_item[3]
            menu_item_cost = menu_item[4]

            # Calculate profit of each item in the menu data
            profit = float(menu_item_price) - float(menu_item_cost)

            # Update the report with the new metrics
            if sales_item == menu_item_name:
                cur_item = report[sales_item]
                cur_item['count'] += int(quantity)
                cur_item['revenue'] += float(menu_item_price) * int(quantity)
                cur_item['cost'] += float(menu_item_cost) * int(quantity)
                cur_item['profit'] += profit * int(quantity)
    return report


# Write the report as a table in markdown format
def write_table_report(report, report_path, mode):
    with open(report_path, mode) as report_file:
        report_file.write('# PyRamen Report\n')
        report_file.write('\n|Item|Count|Revenue|Cost|Profit|\n')
        report_file.write('|---|---|---|---|---|\n')
        for item in report:
            cur = report[item]
            report_file.write(
                f'|{item.title()}|{cur["count"]}|{cur["revenue"]}|{cur["cost"]}|{cur["profit"]}|\n')


# Write the report as a list in markdown format
def write_list_report(report, report_path, mode):
    with open(report_path, mode) as report_file:
        for item in report:
            cur_item = report[item]
            report_file.write(f'\n## {item.title()}\n')
            report_file.write(f'\n- Count: {cur_item["count"]}\n')
            report_file.write(f'- Revenue: {cur_item["revenue"]}\n')
            report_file.write(f'- Cost: {cur_item["cost"]}\n')
            report_file.write(f'- Profit: {cur_item["profit"]}\n')


if __name__ == '__main__':
    # Set file paths for data and report
    menu_data = Path('data/menu_data.csv')
    sales_data = Path('data/sales_data.csv')
    report_file = Path('gen/report.md')

    # Initialize list objects to hold our menu and sales data
    menu = make_list(menu_data)
    sales = make_list(sales_data)

    # Generate the report
    report = make_report(menu, sales)

    # Write the report to the report file
    write_table_report(report, report_file, 'w')
    write_list_report(report, report_file, 'a')
