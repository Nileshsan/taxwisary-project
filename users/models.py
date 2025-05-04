from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Model 1: User Profile (Basic Info)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    pan = models.CharField(max_length=10, unique=True)
    uid = models.CharField(max_length=12, unique=True)
    dob = models.DateField(default='2000-01-01')
    phone = models.CharField(max_length=10, default='1234567890')
    email = models.EmailField(default='user@server.com')

    address = models.TextField(default='flat no. 123, street 456, city, state, country')
    employment = models.CharField(max_length=50, choices=[('Salaried', 'Salaried'), ('Business', 'Business'),], default= 'Salaried')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name



#  Model 2: Income Details

class IncomeDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Salary Income
    employer_name = models.CharField(max_length=100, blank=True, null=True)
    tan = models.CharField(max_length=10, blank=True, null=True)
    salary_income = models.FloatField(default=0)

    # House Rent Exemption
    house_rent_applied = models.BooleanField(default=False)
    house_rent_amount = models.FloatField(blank=True, null=True)
    landlord_pan = models.CharField(max_length=10, blank=True, null=True)
    house_rent_exemption = models.FloatField(default=0)

    # Travel Allowance
    travel_allowance_applied = models.BooleanField(default=False)
    travel_allowance_amount = models.FloatField(default=0)

    # Other Income
    other_income_applied = models.BooleanField(default=False)
    other_income_source = models.CharField(max_length=100, blank=True, null=True)
    other_income_amount = models.FloatField(default=0)

    # Primary Income Calculation
    proprietary_income = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Income for {self.user.username}"


# Model 3: Deductions

class Deductions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Section 80C
    epf_amount = models.FloatField(default=0)
    life_insurance_amount = models.FloatField(default=0)
    mutual_fund_value = models.FloatField(default=0)
    ppf_value = models.FloatField(default=0)
    nsc_value = models.FloatField(default=0)
    home_loan_principal = models.FloatField(default=0)
    child_tuition_fees = models.FloatField(default=0)
    other_80C_amount = models.FloatField(default=0)
    Deduction_A = models.FloatField(default=0)

    # Section 80D (Health Insurance)
    Deduction_B1 = models.FloatField(default=0)
    Deduction_B2 = models.FloatField(default=0)
    Deduction_B = models.FloatField(default=0)

    # Section 80E (Education Loan)
    education_loan_interest = models.FloatField(default=0)
    Deduction_C = models.FloatField(default=0)

    # Section CCD(1B) (NPS Investment)
    nps_amount = models.FloatField(default=0)
    Deduction_D = models.FloatField(default=0)

class incomes_on_investment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    home_loan_interest = models.FloatField(default=0)
    Deduction_H = models.FloatField(default=0)

    interest_on_savings = models.FloatField(default=0)
    Deduction_F = models.FloatField(default=0)


    interest_on_FD_senior_citizen = models.FloatField(default=0)
    Deduction_G = models.FloatField(default=0)

    Divident = models.FloatField(default=0)

    primary_income = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deductions for {self.user.username}"

class HousePropertyIncome(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Salary Income
    Number_of_properties = models.CharField(max_length=100, blank=True, null=True)
    Are_Properties_rented = models.BooleanField(default=False)
    rent_income = models.FloatField(default=0)
    Municipal_Tax = models.FloatField(default=0)
    Maintenance_Charges = models.FloatField(default=0)
    Rental_Income = models.FloatField(default=0)
    Secondary_Income = models.FloatField(default=0)


#  Model 4: Capital Gain and Other Income
class CapitalGainAndOtherIncome(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    Conformation_on_capital_asset_sold = models.BooleanField(default=False)

    Determine_capital_gain_criteria = models.CharField(max_length=100, blank=True, null=True)

    was_Real_Estate_sold_before23rdJul2024 = models.BooleanField(default=False)
    when_asset_purchased = models.DateField()
    when_asset_sold = models.DateField()
    asset_type = models.CharField(max_length=100, blank=True, null=True)
    asset_purchase_price = models.FloatField(default=0)
    asset_sale_price = models.FloatField(default=0)
    profit_real_estate = models.FloatField(default=0)
    
    was_stock_listen_on_stock_exchange = models.BooleanField(default=False)
    when_stock_purchased = models.DateField()
    when_stock_sold = models.DateField()
    stock_purchase_price = models.FloatField(default=0)
    stock_sale_price = models.FloatField(default=0)
    Eligible_preferential_tax_treatment = models.BooleanField(default=False)
    profit_stocks = models.FloatField(default=0)
    
    involved_in_Other_assets = models.BooleanField(default=False)
    when_asset_purchased = models.DateField()
    when_asset_sold = models.DateField()
    asset_purchase_price = models.FloatField(default=0)
    asset_sale_price = models.FloatField(default=0)
    profit_other_assets = models.FloatField(default=0)

    total_capital_gain = models.FloatField(default=0)

   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Capital Gain for {self.user.username}"

class Advance_Tax_and_TDS(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    TDS_deducted = models.BooleanField(default=False)
    TDS_deducted_amount = models.FloatField(default=0)
    password_Income_Tax_ID = models.CharField(max_length=100, blank=True, null=True)
    Advance_Tax_paid = models.BooleanField(default=False)
    Advance_Tax_paid_amount = models.FloatField(default=0)
    additional_TDS_deducted_Fixed_Deposits_Interest_or_RentPayments = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


class OtherDisclosure(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foreign_Bank_Accounts = models.BooleanField(default=False)
    foreign_Bank_Accounts_details = models.CharField(max_length=100, blank=True, null=True)
    foreign_Assets = models.BooleanField(default=False)
    foreign_Assets_details = models.CharField(max_length=100, blank=True, null=True)
    foreign_Investment = models.BooleanField(default=False)
    foreign_Investment_details = models.CharField(max_length=100, blank=True, null=True)
    foreign_Income = models.BooleanField(default=False)
    foreign_Income_details = models.CharField(max_length=100, blank=True, null=True)

    Received_Gifts_above50k = models.BooleanField(default=False)
    Received_Gifts_above50k_details = models.CharField(max_length=100, blank=True, null=True)
    Gift_taxable_amount = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class Bank_Account_Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Bank_Accounts_number = models.CharField(max_length=100, blank=True, null=True)
    Bank_IFSC = models.CharField(max_length=100, blank=True, null=True)
    


class TaxReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_url = CloudinaryField('file', blank=True, null=True)

    status = models.CharField(max_length=50, default='Pending')
    total_income = models.FloatField(default=0)
    total_deductions = models.FloatField(default=0)
    net_taxable_income = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)

    # New field for deductions summary
    deductions_summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from users.models import UserProfile  # Import inside method to avoid circular import issues
        profile, created = UserProfile.objects.get_or_create(user=self.user, defaults={...})
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tax Report for {self.user.username}"



class TempUserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='Jhon Doe')
    pan = models.CharField(max_length=10, default='ABCDE1234Z')
    uid = models.CharField(max_length=12, default='123456789012')
    dob = models.DateField(default='2000-01-01')
    phone = models.CharField(max_length=10, default='1234567890')
    email = models.EmailField(default='user@server.com')
    address = models.TextField(default='flat no. 123, street 456, city, state, country')
    employment = models.CharField(max_length=50, default='default')


class TaxData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income = models.FloatField()
    deductions = models.FloatField()
    home_loan = models.FloatField()
    tax_report = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tax Data for {self.user.username}"
    





# Temp Models

class TempUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    pan = models.CharField(max_length=10, unique=True)
    uid = models.CharField(max_length=12, unique=True)
    dob = models.DateField(default='2000-01-01')
    phone = models.CharField(max_length=100, default='1234567890')
    email = models.EmailField(default='user@server.com')

    address = models.TextField(default='flat no. 123, street 456, city, state, country')
    employment = models.CharField(max_length=50, choices=[('Salaried', 'Salaried'), ('Business', 'Business'),], default= 'Salaried')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class TempIncomeDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=100, blank=True, null=True)
    tan = models.CharField(max_length=10, blank=True, null=True)
    salary_income = models.FloatField(default=0)
    house_rent_applied = models.BooleanField(default=False)
    house_rent_amount = models.FloatField(blank=True, null=True)
    landlord_pan = models.CharField(max_length=10, blank=True, null=True)
    house_rent_exemption = models.FloatField(default=0)
    travel_allowance_applied = models.BooleanField(default=False)
    travel_allowance_amount = models.FloatField(default=0)
    other_income_applied = models.BooleanField(default=False)
    other_income_source = models.CharField(max_length=100, blank=True, null=True)
    other_income_amount = models.FloatField(default=0)
    proprietary_income = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Income for {self.user.username}"


class TempDeductions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    epf_amount = models.FloatField(default=0)
    life_insurance_amount = models.FloatField(default=0)
    mutual_fund_value = models.FloatField(default=0)
    ppf_value = models.FloatField(default=0)
    nsc_value = models.FloatField(default=0)
    home_loan_principal = models.FloatField(default=0)
    child_tuition_fees = models.FloatField(default=0)
    other_80C_amount = models.FloatField(default=0)
    Deduction_A = models.FloatField(default=0)
    Deduction_B1 = models.FloatField(default=0)
    Deduction_B2 = models.FloatField(default=0)
    Deduction_B = models.FloatField(default=0)
    education_loan_interest = models.FloatField(default=0)
    Deduction_C = models.FloatField(default=0)
    nps_amount = models.FloatField(default=0)
    Deduction_D = models.FloatField(default=0)

class TempIncomesOnInvestment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_loan_interest = models.FloatField(default=0)
    Deduction_H = models.FloatField(default=0)
    interest_on_savings = models.FloatField(default=0)
    Deduction_F = models.FloatField(default=0)
    interest_on_FD_senior_citizen = models.FloatField(default=0)
    Deduction_G = models.FloatField(default=0)
    Divident = models.FloatField(default=0)
    primary_income = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deductions for {self.user.username}"

class TempHousePropertyIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Number_of_properties = models.CharField(max_length=100, blank=True, null=True)
    Are_Properties_rented = models.BooleanField(default=False)
    rent_income = models.FloatField(default=0)
    Municipal_Tax = models.FloatField(default=0)
    Maintenance_Charges = models.FloatField(default=0)
    Rental_Income = models.FloatField(default=0)
    Secondary_Income = models.FloatField(default=0)

class TempCapitalGainAndOtherIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Conformation_on_capital_asset_sold = models.BooleanField(default=False)
    Determine_capital_gain_criteria = models.CharField(max_length=100, blank=True, null=True)
    was_Real_Estate_sold_before23rdJul2024 = models.BooleanField(default=False)
    when_asset_purchased = models.DateField()
    when_asset_sold = models.DateField()
    asset_type = models.CharField(max_length=100, blank=True, null=True)
    asset_purchase_price = models.FloatField(default=0)
    asset_sale_price = models.FloatField(default=0)
    profit_real_estate = models.FloatField(default=0)
    was_stock_listen_on_stock_exchange = models.BooleanField(default=False)
    when_stock_purchased = models.DateField()
    when_stock_sold = models.DateField()
    stock_purchase_price = models.FloatField(default=0)
    stock_sale_price = models.FloatField(default=0)
    Eligible_preferential_tax_treatment = models.BooleanField(default=False)
    profit_stocks = models.FloatField(default=0)
    involved_in_Other_assets = models.BooleanField(default=False)
    when_asset_purchased = models.DateField()
    when_asset_sold = models.DateField()
    asset_purchase_price = models.FloatField(default=0)
    asset_sale_price = models.FloatField(default=0)
    profit_other_assets = models.FloatField(default=0)
    total_capital_gain = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Capital Gain for {self.user.username}"



class TempAdvanceTaxAndTDS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TDS_deducted = models.BooleanField(default=False)
    TDS_deducted_amount = models.FloatField(default=0)
    password_Income_Tax_ID = models.CharField(max_length=100, blank=True, null=True)
    Advance_Tax_paid = models.BooleanField(default=False)
    Advance_Tax_paid_amount = models.FloatField(default=0)
    additional_TDS_deducted_Fixed_Deposits_Interest_or_RentPayments = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

class TempOtherDisclosure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foreign_Bank_Accounts = models.BooleanField(default=False)
    foreign_Bank_Accounts_details = models.CharField(max_length=100, blank=True, null=True)
    foreign_Assets = models.BooleanField(default=False)
    foreign_Assets_details = models.CharField(max_length=100, blank=True, null=True)
    foreign_Investment = models.BooleanField(default=False)
    foreign_Investment_details = models.CharField(max_length=100, blank=True, null=True)
    foreign_Income = models.BooleanField(default=False)
    foreign_Income_details = models.CharField(max_length=100, blank=True, null=True)
    Received_Gifts_above50k = models.BooleanField(default=False)
    Received_Gifts_above50k_details = models.CharField(max_length=100, blank=True, null=True)
    Gift_taxable_amount = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

class TempBankAccountDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Bank_Name = models.CharField(max_length=100, blank=True, null=True)
    Bank_Accounts_number = models.CharField(max_length=100, blank=True, null=True)
    Bank_IFSC = models.CharField(max_length=100, blank=True, null=True)


