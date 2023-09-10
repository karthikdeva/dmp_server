import graphene
import graphql_jwt
import django_filters
import datetime as dt
from functools import reduce
from graphql_jwt.decorators import login_required, permission_required

from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.filter import DjangoFilterConnectionField
from .models import Products, PurchaseOrder, Category, UnitOfMeasurement,  Customer, PaymentTypes, LoanAccounts, MasterExpenses
from .model_input import ProductInput, PurchaseOrderInput, PurchaseOrderItemInput, CustomerInput, MasterExpenseInput, PaymentTypeInput, LoanAccountInput
from .model_node import CategoryNode, PurchaseOrderNode, PurchaseOrderItemNode, UnitOfMeasurementNode, ProductNode, CustomerNode, MasterExpensesNode, PaymentTypesNode, LoanAccountsNode, UserNode


def change_case(str):
    return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, str).lower()


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserNode)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class CustomFilter(django_filters.FilterSet):
    # Do case-insensitive lookups on 'name'
    name = django_filters.CharFilter(lookup_expr=['exact', 'icontains', 'istartswith'])

    class Meta:
        # Assume you have an Animal model defined with the following fields
        abstract = True
        fields = ['name', 'genus', 'is_domesticated']


class Query(graphene.ObjectType):
    me = graphene.Field(UserNode)
    category = graphene.List(CategoryNode)
    units = graphene.List(UnitOfMeasurementNode)
    customers = DjangoFilterConnectionField(CustomerNode)
    loanAccounts = DjangoFilterConnectionField(LoanAccountsNode)
    paymentTypes = DjangoFilterConnectionField(PaymentTypesNode)
    masterExpenses = DjangoFilterConnectionField(MasterExpensesNode)
    products = DjangoFilterConnectionField(ProductNode)
    purchaseOrder = DjangoFilterConnectionField(PurchaseOrderNode)
    purchaseOrderItem = graphene.List(PurchaseOrderItemNode)

    @staticmethod
    @login_required
    def resolve_me(self, info):
        user = info.context.user
        return user

    @staticmethod
    @login_required
    def resolve_customers(root, info, **kwargs):
        return Customer.objects.filter(status=False).order_by('-modified_at') #code

    @staticmethod
    @login_required
    def resolve_masterExpenses(root, info, **kwargs):
        return MasterExpenses.objects.filter(status=False).order_by('-code')

    @staticmethod
    @login_required
    def resolve_loanAccounts(root, info,  **kwargs):
        return LoanAccounts.objects.filter(status=False).order_by('-code')

    @staticmethod
    @login_required
    def resolve_paymentTypes(root, info,  **kwargs):
        return PaymentTypes.objects.filter(status=False).order_by('-code')

    @staticmethod
    @login_required
    def resolve_products(root, info, **kwargs):
        return Products.objects.filter(status=False).order_by('-code')

    @staticmethod
    @login_required
    def resolve_purchaseOrder(root, info, **kwargs):
        return PurchaseOrder.objects.filter(status=False).order_by('-code')

    @staticmethod
    @login_required
    def resolve_category(root, info, **kwargs):
        return Category.objects.filter(status=False).order_by('-category_name')

    @staticmethod
    @login_required
    def resolve_units(root, info, **kwargs):
        return UnitOfMeasurement.objects.filter(status=False).order_by('-unit_name')


#
# ###
# # Product starts here
# ###

class CreatePurchaseOrder(graphene.Mutation):
    class Arguments:
        purchaseOrder_data = ProductInput(required=True)
    product = graphene.Field(ProductNode)

    @staticmethod
    @login_required
    def mutate(root, info, product_data=None):
        product = Products.objects.filter(name=product_data.name).first()
        category = Category.objects.filter(id=product_data.categoryId).first()
        unit = UnitOfMeasurement.objects.filter(id=product_data.unitId).first()
        if product:
            raise Exception('Duplicate Entry, Product name already exist!')
        if not category:
            raise Exception('Invalid category!')
        if not unit:
            raise Exception('Invalid unit!')

        product = Products(
            name=product_data.name,
            price=product_data.price,
            hsn_code=product_data.hsn_code,
            min_stock=product_data.min_stock,
            current_stock=product_data.current_stock,
            tax=product_data.tax,
            image=product_data.image,
            category=category,
            unit=unit,
            created_at=dt.datetime.now(),
            modified_at=dt.datetime.now()
        )
        product.save()
        return CreateProduct(product)


# class UpdateProduct(graphene.Mutation):
#     class Arguments:
#         product_data = ProductInput(required=True)
#
#     product = graphene.Field(ProductNode)
#
#     @staticmethod
#     @login_required
#     def mutate(root, info, product_data=None):
#         product = Products.objects.get(code=product_data.id)
#         product_data.pop('id')
#         product_data['modified_at'] = dt.datetime.now()
#         if product is not None:
#
#             for key, value in product_data.items():
#                 key = change_case(key)
#                 setattr(product, key, value)
#             product.save()
#
#         return UpdateProduct(product)
#
#
# class DeleteProduct(graphene.Mutation):
#     class Arguments:
#         id = graphene.String()
#     product = graphene.Field(ProductNode)
#
#     @staticmethod
#     @login_required
#     def mutate(root, info, id):
#         product = Products.objects.get(code=id)
#         if product is not None:
#             product.status = True
#             product.modified_at = dt.datetime.now()
#             product.save()
#         return DeleteProduct(product)

#
# ###
# # Product starts here
# ###

class CreateProduct(graphene.Mutation):
    class Arguments:
        product_data = ProductInput(required=True)
    product = graphene.Field(ProductNode)

    @staticmethod
    @login_required
    def mutate(root, info, product_data=None):
        product = Products.objects.filter(name=product_data.name).first()
        category = Category.objects.filter(id=product_data.categoryId).first()
        unit = UnitOfMeasurement.objects.filter(id=product_data.unitId).first()
        if product:
            raise Exception('Duplicate Entry, Product name already exist!')
        if not category:
            raise Exception('Invalid category!')
        if not unit:
            raise Exception('Invalid unit!')

        product = Products(
            name=product_data.name,
            price=product_data.price,
            hsn_code=product_data.hsn_code,
            min_stock=product_data.min_stock,
            current_stock=product_data.current_stock,
            tax=product_data.tax,
            image=product_data.image,
            category=category,
            unit=unit,
            created_at=dt.datetime.now(),
            modified_at=dt.datetime.now()
        )
        product.save()
        return CreateProduct(product)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        product_data = ProductInput(required=True)

    product = graphene.Field(ProductNode)

    @staticmethod
    @login_required
    def mutate(root, info, product_data=None):
        product = Products.objects.get(code=product_data.id)
        product_data.pop('id')
        product_data['modified_at'] = dt.datetime.now()
        if product is not None:

            for key, value in product_data.items():
                key = change_case(key)
                setattr(product, key, value)
            product.save()

        return UpdateProduct(product)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.String()
    product = graphene.Field(ProductNode)

    @staticmethod
    @login_required
    def mutate(root, info, id):
        product = Products.objects.get(code=id)
        if product is not None:
            product.status = True
            product.modified_at = dt.datetime.now()
            product.save()
        return DeleteProduct(product)


###
# Customer starts here
###

class CreateCustomer(graphene.Mutation):
    class Arguments:
        customer_data = CustomerInput(required=True)
    customer = graphene.Field(CustomerNode)

    @staticmethod
    @login_required
    def mutate(root, info, customer_data=None):
        customer = Customer(
            first_name=customer_data.firstName,
            last_name=customer_data.lastName,
            phone_number=customer_data.phoneNumber,
            email=customer_data.email,
            tin_number=customer_data.tinNumber,
            pan_number=customer_data.panNumber,
            gst_number=customer_data.gstNumber,
            opening_balance=customer_data.openingBalance,
            image=customer_data.image,
            joined_on=dt.datetime.now(),
            address=customer_data.address,
            state=customer_data.state,
            pin_code=customer_data.pinCode,
            created_at=dt.datetime.now(),
            modified_at=dt.datetime.now()
        )
        customer.save()
        return CreateCustomer(customer)


class UpdateCustomer(graphene.Mutation):
    class Arguments:
        customer_data = CustomerInput(required=True)

    customer = graphene.Field(CustomerNode)

    @staticmethod
    @login_required
    def mutate(root, info, customer_data=None):
        customer = Customer.objects.get(code=customer_data.id)
        customer_data.pop('id')
        customer_data['modified_at'] = dt.datetime.now()
        if customer is not None:

            for key, value in customer_data.items():
                key = change_case(key)
                setattr(customer, key, value)
            customer.save()

        return UpdateCustomer(customer)


class DeleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.String()
    customer = graphene.Field(CustomerNode)

    @staticmethod
    @login_required
    def mutate(root, info, id):
        customer = Customer.objects.get(code=id)
        if customer is not None:
            customer.status = True
            customer.modified_at = dt.datetime.now()
            customer.save()
        return DeleteCustomer(customer)


###
# Expenses starts here
###

class CreateMasterExpense(graphene.Mutation):
    class Arguments:
        master_expense_data = MasterExpenseInput(required=True)
    master_expense = graphene.Field(MasterExpensesNode)

    @staticmethod
    @login_required
    def mutate(root, info, master_expense_data=None):
        master_expense = MasterExpenses(
            name=master_expense_data.name,
            notes=master_expense_data.notes,
            created_at=dt.datetime.now(),
            modified_at=dt.datetime.now(),
        )
        master_expense.save()
        return CreateMasterExpense(master_expense)


class UpdateMasterExpense(graphene.Mutation):
    class Arguments:
        master_expense_data = MasterExpenseInput(required=True)

    master_expense = graphene.Field(MasterExpensesNode)

    @staticmethod
    @login_required
    def mutate(root, info, master_expense_data=None):
        master_expense = MasterExpenses.objects.get(code=master_expense_data.id)
        master_expense_data.pop('id')
        master_expense_data['modified_at'] = dt.datetime.now()
        if master_expense is not None:
            for key, value in master_expense_data.items():
                setattr(master_expense, key, value)
            # print(payment_type_data)
            master_expense.save()

        return UpdateMasterExpense(master_expense)


class DeleteMasterExpense(graphene.Mutation):
    class Arguments:
        id = graphene.String()
    master_expense = graphene.Field(MasterExpensesNode)

    @staticmethod
    @login_required
    def mutate(root, info, id):
        master_expense = MasterExpenses.objects.get(code=id)
        if master_expense is not None:
            master_expense.status = True
            master_expense.modified_at = dt.datetime.now()
            master_expense.save()
        return DeleteMasterExpense(master_expense)


###
# Payment type starts here
###

class CreatePaymentType(graphene.Mutation):
    class Arguments:
        payment_type_data = PaymentTypeInput(required=True)

    payment_types = graphene.Field(PaymentTypesNode)

    @staticmethod
    @login_required
    def mutate(root, info, payment_type_data=None):
        payment_type = PaymentTypes(
            name=payment_type_data.name,
            description=payment_type_data.description,
            created_at=dt.datetime.now(),
            modified_at=dt.datetime.now(),
        )
        payment_type.save()
        return CreatePaymentType(payment_type)


class UpdatePaymentType(graphene.Mutation):
    class Arguments:
        payment_type_data = PaymentTypeInput(required=True)

    payment_type = graphene.Field(PaymentTypesNode)

    @staticmethod
    @login_required
    def mutate(root, info, payment_type_data=None):
        payment_type = PaymentTypes.objects.get(code=payment_type_data.id)
        payment_type_data.pop('id')
        payment_type_data['modified_at'] = dt.datetime.now()
        if payment_type is not None:
            for key, value in payment_type_data.items():
                setattr(payment_type, key, value)
            # print(payment_type_data)
            payment_type.save()

        return UpdatePaymentType(payment_type)


class DeletePaymentType(graphene.Mutation):
    class Arguments:
        id = graphene.String()
    payment_type = graphene.Field(PaymentTypesNode)

    @staticmethod
    @login_required
    def mutate(root, info, id):
        payment_type = PaymentTypes.objects.get(code=id)
        if payment_type is not None:
            payment_type.status = True
            payment_type.modified_at = dt.datetime.now()
            payment_type.save()
        return DeletePaymentType(payment_type)


###
# Loan account  starts here
###
class CreateLoanAccount(graphene.Mutation):
    class Arguments:
        loan_account_data = LoanAccountInput(required=True)

    loan_accounts = graphene.Field(LoanAccountsNode)

    @staticmethod
    @login_required
    def mutate(root, info, loan_account_data=None):
        loan_account = LoanAccounts(
            owners_name=loan_account_data.owners_name,
            company_name=loan_account_data.company_name,
            phone_number=loan_account_data.phone_number,
            address=loan_account_data.address,
            bank_name=loan_account_data.bank_name,
            notes=loan_account_data.notes,
            created_at=dt.datetime.now(),
            modified_at=dt.datetime.now(),
        )
        loan_account.save()
        return CreateLoanAccount(loan_account)


class UpdateLoanAccount(graphene.Mutation):
    class Arguments:
        loan_account_data = LoanAccountInput(required=True)
    loan_accounts = graphene.Field(LoanAccountsNode)

    @staticmethod
    @login_required
    def mutate(root, info, loan_account_data=None):
        loan_account = LoanAccounts.objects.get(code=loan_account_data.id)
        loan_account_data.pop('id')
        loan_account_data['modified_at'] = dt.datetime.now()
        if loan_account is not None:
            for key, value in loan_account_data.items():
                setattr(loan_account, key, value)
            # print(payment_type_data)
            loan_account.save()

        return UpdateLoanAccount(loan_account)


class DeleteLoanAccount(graphene.Mutation):
    class Arguments:
        id = graphene.String()
    loan_accounts = graphene.Field(LoanAccountsNode)

    @staticmethod
    @login_required
    def mutate(root, info, id):
        loan_account = LoanAccounts.objects.get(code=id)
        if loan_account is not None:
            loan_account.status = True
            loan_account.modified_at = dt.datetime.now()
            loan_account.save()
        return DeleteLoanAccount(loan_account)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_paymentType = CreatePaymentType.Field()
    update_paymentType = UpdatePaymentType.Field()
    delete_paymentType = DeletePaymentType.Field()

    create_LoanAccount = CreateLoanAccount.Field()
    update_LoanAccount = UpdateLoanAccount.Field()
    delete_LoanAccount = DeleteLoanAccount.Field()

    create_MasterExpense = CreateMasterExpense.Field()
    update_MasterExpense = UpdateMasterExpense.Field()
    delete_MasterExpense = DeleteMasterExpense.Field()

    create_customer = CreateCustomer.Field()
    update_customer = UpdateCustomer.Field()
    delete_customer = DeleteCustomer.Field()

    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
