# utilities.py
from .models import Product

from .models import StockChange

def log_stock_change(product, original_quantity, new_quantity, source=None):
    """
    Logs stock changes to the StockChange model.
    
    Args:
        product: The product whose stock is being changed.
        original_quantity: The original quantity of the product before the change.
        new_quantity: The new quantity of the product after the change.
        source: The source of the change ('admin' or 'api').
    """
    stock_difference = new_quantity - original_quantity
    print("stock_difference",stock_difference)
    if stock_difference != 0:
        change_type = "increased" if stock_difference > 0 else "decreased"
        reason = f"Stock {change_type} via {source} (from {original_quantity} to {new_quantity})"
        print("reason",reason)
        StockChange.objects.create(
            product=product,
            quantity_changed=stock_difference,
            reason=reason
        )

    return stock_difference
