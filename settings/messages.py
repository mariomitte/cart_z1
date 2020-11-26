from .environment import env

message = {
    # WARNING
    'MESSAGE_WARNING_CUSTOMER_EXISTS': env.str("MESSAGE_WARNING_CUSTOMER_EXISTS",
        default="Unable to create order. Email already exists. Please login to continue. Is this your email address?"),
    'MESSAGE_WARNING_CUSTOMER_NOT_EXISTS': env.str("MESSAGE_WARNING_CUSTOMER_NOT_EXISTS",
        default="Fill out form to create an order."),
    'MESSAGE_WARNING_ORDER_NOT_EXISTS': env.str("MESSAGE_WARNING_ORDER_NOT_EXISTS",
        default="You have not placed an order yet."),
    'MESSAGE_WARNING_ORDER_UPDATE_FOR_AUTHENTICATED_USER': env.str("MESSAGE_WARNING_ORDER_UPDATE_FOR_AUTHENTICATED_USER",
        default="Please use Dashbord from menu to change your personal information."),
    'MESSAGE_WARNING_SHIPPING_ADDRESS_NOT_EXISTS': env.str("MESSAGE_WARNING_SHIPPING_ADDRESS_NOT_EXISTS",
        default="There are no details associated with your account. Have you created an address?"),
    'MESSAGE_WARNING_ADDRESS_OR_CREDIT_CARD_EXISTS': env.str("MESSAGE_WARNING_ADDRESS_OR_CREDIT_CARD_EXISTS",
        default="Please Login to create an order."),
    'MESSAGE_WARNING_CREDIT_CARD': env.str("MESSAGE_WARNING_CREDIT_CARD",
        default="You don't have any credit card record saved."),

    # SUCCESS
    'MESSAGE_SUCCESS_SHIPPING_ADDRESS': env.str("MESSAGE_SUCCESS_SHIPPING_ADDRESS",
        default="Updated customer details."),
    'MESSAGE_SUCCESS_UPDATE_PASSWORD': env.str("MESSAGE_SUCCESS_UPDATE_PASSWORD",
        default="User password updated."),
    'MESSAGE_SUCCESS_NEW_ORDER': env.str("MESSAGE_SUCCESS_NEW_ORDER",
        default="Created new order"),
    'MESSAGE_SUCCESS_NEW_USER': env.str("MESSAGE_SUCCESS_NEW_USER",
        default="Created new user"),
    'MESSAGE_SUCCESS_NEW_PROFILE': env.str("MESSAGE_SUCCESS_NEW_PROFILE",
        default="Created new profile"),
    'MESSAGE_SUCCESS_NEW_CREDIT_CARD': env.str("MESSAGE_SUCCESS_NEW_CREDIT_CARD",
        default="Created new profile"),
    'MESSAGE_SUCCESS_PROFILE_UPDATED': env.str("MESSAGE_SUCCESS_PROFILE_UPDATED",
        default="Profile updated successfully"),
    'MESSAGE_SUCCESS_CART_UPDATED': env.str("MESSAGE_SUCCESS_CART_UPDATED",
        default="Cart updated successfully"),
    'MESSAGE_SUCCESS_CREDIT_CARD_UPDATED': env.str("MESSAGE_SUCCESS_CREDIT_CARD_UPDATED",
        default="Credit card updated successfully"),
    'MESSAGE_SUCCESS_CART_ITEM_REMOVED': env.str("MESSAGE_SUCCESS_CART_ITEM_REMOVED",
        default="Cart item removed successfully"),
    'MESSAGE_SUCCESS_COUPON_ADDED': env.str("MESSAGE_SUCCESS_COUPON_ADDED",
        default="Coupon added to cart"),
    'MESSAGE_SUCCESS_COUPON_REMOVED': env.str("MESSAGE_SUCCESS_COUPON_REMOVED",
        default="Coupon removed from cart"),

    # FAILED
    'MESSAGE_FAILED_PROFILE_UPDATE': env.str("MESSAGE_FAILED_PROFILE_UPDATE",
        default="Error updating your profile"),
    'MESSAGE_ERROR_CREDIT_CARD_UPDATE': env.str("MESSAGE_ERROR_CREDIT_CARD_UPDATE",
        default="Error updating your credit card details"),
    'MESSAGE_ERROR_COUPON_NOT_EXISTS': env.str("MESSAGE_ERROR_COUPON_NOT_EXISTS",
        default="Coupon code does not exist"),
    'MESSAGE_ERROR_COUPON_CANNOT_COMBINE': env.str("MESSAGE_ERROR_COUPON_CANNOT_COMBINE",
        default="Please use other coupon combinations."),
    'MESSAGE_ERROR_COUPON_CODE_EXPIRED': env.str("MESSAGE_ERROR_COUPON_CODE_EXPIRED",
        default="Sorry, but your coupon has expired or does not exist."),
}
