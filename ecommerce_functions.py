from datetime import datetime, timedelta


def generate_monthly_sales_report(orders, month, year):
    start_date = datetime(year, month, 1)
    end_date = start_date + timedelta(days=30)  # Assuming a 30-day month

    monthly_orders = [order for order in orders if start_date <=
                      order['timestamp'] <= end_date]
    total_sales = sum(order['total_price'] for order in monthly_orders)

    return total_sales, len(monthly_orders)


def calculate_loyalty_status(total_purchases, total_spent):
    if total_purchases >= 5 and total_spent >= 200:
        return "Gold"
    elif total_purchases >= 3 and total_spent >= 100:
        return "Silver"
    else:
        return "Bronze"


def generate_recommendations(customer_id, purchase_history, all_products):
    # Placeholder logic for recommendation generation
    recommended_products = [product for product in all_products if product['category'] in [
        'Electronics', 'Clothing']]
    return recommended_products


def process_bulk_order(items, discount_percent):
    # Placeholder logic for bulk order processing
    total_price = sum(item['quantity'] * item['unit_price'] for item in items)
    discounted_price = apply_discount(total_price, discount_percent)
    return discounted_price


def check_delivery_status(order_id, expected_delivery_date):
    current_date = datetime.now().date()
    if current_date > expected_delivery_date:
        return f"Order #{order_id} delivered"
    else:
        return f"Order #{order_id} on the way"


def calculate_total_price(quantity, unit_price, tax_rate):
    subtotal = quantity * unit_price
    tax_amount = subtotal * (tax_rate / 100)
    total_price = subtotal + tax_amount
    return total_price


def apply_discount(total_price, discount_percent):
    discount_amount = total_price * (discount_percent / 100)
    discounted_price = total_price - discount_amount
    return discounted_price


def check_stock(product_id, requested_quantity, available_stock):
    if requested_quantity <= available_stock:
        return True
    else:
        return False


def generate_order_confirmation(order_id, products, total_price):
    confirmation_message = f"Order #{order_id} confirmed. "
    confirmation_message += "Items: " + ", ".join(products) + ". "
    confirmation_message += f"Total Price: ${total_price:.2f}."
    return confirmation_message


def process_refund(order_id, original_payment_amount, refund_amount):
    if refund_amount > original_payment_amount:
        raise ValueError(
            "Refund amount cannot exceed the original payment amount")
    # Placeholder logic for refund processing
    refunded_amount = refund_amount
    remaining_amount = original_payment_amount - refunded_amount
    return remaining_amount
