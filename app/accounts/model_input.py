import graphene


class PurchaseOrderInput(graphene.InputObjectType):
    id = graphene.ID()
    sellerId = graphene.ID()
    invoice_no = graphene.String()
    invoice_date = graphene.DateTime()
    hsn_code = graphene.String()
    purchase_type = graphene.String()
    tax_type = graphene.String()
    value = graphene.Decimal()
    discount = graphene.Decimal()
    gst = graphene.Decimal()
    igst = graphene.Decimal()
    final_value = graphene.Decimal()
    is_paid = graphene.Boolean()
    status = graphene.String()
    created_at = graphene.String()


class PurchaseOrderItemInput(graphene.InputObjectType):
    id = graphene.ID()
    productId = graphene.ID()
    orderId = graphene.ID()
    qty = graphrice = graphene.Decimal()
    final_price = graphene.Decimal()
    total_pricene.Decimal()
    price = graphene.Decimal()
    discount_pe = graphene.ID()
    status = graphene.String()
    created_at = graphene.String()


class ProductInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    price = graphene.String()
    hsn_code = graphene.String()
    min_stock = graphene.String()
    current_stock = graphene.Int()
    tax = graphene.String()
    image = graphene.String()
    categoryId = graphene.Int()
    unitId = graphene.Int()
    status = graphene.String()
    created_at = graphene.String()


class CustomerInput(graphene.InputObjectType):
    id = graphene.ID()
    firstName = graphene.String()
    lastName = graphene.String()
    phoneNumber = graphene.String()
    email = graphene.String()
    tinNumber = graphene.String()
    panNumber = graphene.String()
    gstNumber = graphene.String()
    openingBalance = graphene.String()
    image = graphene.String()
    joinedOn = graphene.String()
    address = graphene.String()
    state = graphene.String()
    pinCode = graphene.String()


class MasterExpenseInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    notes = graphene.String()


class PaymentTypeInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()


class LoanAccountInput(graphene.InputObjectType):
    id = graphene.ID()
    owners_name = graphene.String()
    company_name = graphene.String()
    phone_number = graphene.String()
    notes = graphene.String()
    address = graphene.String()
    bank_name = graphene.String()