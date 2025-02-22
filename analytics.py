import os
from datetime import datetime
from collections import defaultdict
import re


class SalesAnalytics:
    def __init__(self):
        self.daily_volumes = defaultdict(int)  # date -> total volume
        self.daily_values = defaultdict(float)  # date -> total value
        self.product_volumes = defaultdict(int)  # productId -> total volume
        self.staff_monthly_sales = defaultdict(
            lambda: defaultdict(float)
        )  # (staff_id, month) -> total sales
        self.hourly_transactions = defaultdict(
            lambda: defaultdict(int)
        )  # hour --> date -> transaction count

    def parse_products(self, products_str):
        """Parse the products string into a list of (product_id, quantity) tuples"""
        pattern = r"\[([^\]]+)\]"
        products_str = re.search(pattern, products_str).group(1)
        products = products_str.split("|")
        result = []
        for product in products:
            pid, quantity = product.split(":")
            result.append((pid, int(quantity)))
        return result

    def process_transaction(self, line):
        """Process a single transaction line"""
        staff_id, timestamp, products_str, amount = line.strip().split(",")

        dt = None
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
        date_str = dt.strftime("%Y-%m-%d")
        month_str = dt.strftime("%Y-%m")
        hour = dt.hour

        products = self.parse_products(products_str)
        total_volume = sum(quantity for _, quantity in products)

        self.daily_volumes[date_str] += total_volume
        self.daily_values[date_str] += float(amount)

        for pid, quantity in products:
            self.product_volumes[pid] += quantity

        self.staff_monthly_sales[month_str][staff_id] += float(amount)
        self.hourly_transactions[hour][date_str] += 1

    def process_file(self, filename):
        """Process a single transaction file"""
        with open(filename, "r") as f:
            for line in f:
                self.process_transaction(line)

    def process_directory(self, directory):
        """Process all transaction files in a directory"""
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                self.process_file(os.path.join(directory, filename))

    def get_busiest_hour(self):
        """Calculate the hour with highest average transaction volume"""
        hour_averages = {}
        for hour, daily_counts in self.hourly_transactions.items():
            # Calculate average transactions for this hour across all days
            total_transactions = sum(daily_counts.values())
            num_days = len(daily_counts)  # Number of days this hour had transactions
            hour_averages[hour] = total_transactions / num_days if num_days > 0 else 0

        # Find hour with highest average
        busiest_hour = max(hour_averages.items(), key=lambda x: x[1])
        return {"hour": busiest_hour[0], "average_transactions": busiest_hour[1]}

    def generate_report(self):
        """Generate the analytics report"""
        report = {
            "highest_daily_volume": {
                "date": max(self.daily_volumes.items(), key=lambda x: x[1])[0],
                "volume": max(self.daily_volumes.values()),
            },
            "highest_daily_value": {
                "date": max(self.daily_values.items(), key=lambda x: x[1])[0],
                "value": max(self.daily_values.values()),
            },
            "most_sold_product": {
                "product_id": max(self.product_volumes.items(), key=lambda x: x[1])[0],
                "volume": max(self.product_volumes.values()),
            },
            "top_staff_by_month": {
                month: {
                    "staff_id": max(staff_sales.items(), key=lambda x: x[1])[0],
                    "sales": max(staff_sales.values()),
                }
                for month, staff_sales in self.staff_monthly_sales.items()
            },
            "busiest_hour": self.get_busiest_hour(),
        }
        return report


def show_report_in_console(report):
    print("\nMonieshop Sales Analytics Report")
    print("===============================")

    print(f"\nHighest Sales Volume in a Day:")
    print(f"Date: {report['highest_daily_volume']['date']}")
    print(f"Volume: {report['highest_daily_volume']['volume']} units")

    print(f"\nHighest Sales Value in a Day:")
    print(f"Date: {report['highest_daily_value']['date']}")
    print(f"Value: ${report['highest_daily_value']['value']:.2f}")

    print(f"\nMost Sold Product:")
    print(f"Product ID: {report['most_sold_product']['product_id']}")
    print(f"Total Volume: {report['most_sold_product']['volume']} units")

    print("\nTop Performing Staff by Month:")
    for month, data in report["top_staff_by_month"].items():
        print(f"{month}: Staff ID {data['staff_id']} (${data['sales']:.2f})")

    print("\nBusiest Hour of the Day:")
    print(
        f"{report['busiest_hour']['hour']}:00 (Average of {report['busiest_hour']['average_transactions']:.2f} transactions per day)"
    )
