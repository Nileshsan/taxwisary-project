from django.contrib import admin
from .models import (
    UserProfile, IncomeDetails, Deductions, HousePropertyIncome, CapitalGainAndOtherIncome,
    Advance_Tax_and_TDS, OtherDisclosure, Bank_Account_Details, TaxReport, TaxData,
    TempUserProfile, TempIncomeDetails, TempDeductions, TempIncomesOnInvestment,
    TempHousePropertyIncome, TempCapitalGainAndOtherIncome, TempAdvanceTaxAndTDS,
    TempOtherDisclosure, TempBankAccountDetails
)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(IncomeDetails)
admin.site.register(Deductions)
admin.site.register(HousePropertyIncome)
admin.site.register(CapitalGainAndOtherIncome)
admin.site.register(Advance_Tax_and_TDS)
admin.site.register(OtherDisclosure)
admin.site.register(Bank_Account_Details)
admin.site.register(TaxReport)
admin.site.register(TaxData)
admin.site.register(TempUserProfile)
admin.site.register(TempIncomeDetails)
admin.site.register(TempDeductions)
admin.site.register(TempIncomesOnInvestment)
admin.site.register(TempHousePropertyIncome)
admin.site.register(TempCapitalGainAndOtherIncome)
admin.site.register(TempAdvanceTaxAndTDS)
admin.site.register(TempOtherDisclosure)
admin.site.register(TempBankAccountDetails)