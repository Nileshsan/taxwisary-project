// Tax Advisory Forms Module
(function() {
    // Form Templates
    const formTemplates = {
        personal: `
            <form id="personalForm" class="tax-form">
                <h3>Personal Information</h3>
                <div class="form-group">
                    <label for="full_name">Full Name (first and last):</label>
                    <input type="text" class="form-control" id="full_name" name="full_name" placeholder="Enter your name" required>
                </div>
                <div class="form-group">
                    <label for="dob">Date of Birth:</label>
                    <input type="date" class="form-control" id="dob" name="dob" required>
                </div>
                <div class="form-group">
                    <label for="phone">Phone Number:</label>
                    <input type="text" class="form-control" id="phone" name="phone" placeholder="10-digit number" required>
                </div>
                <div class="form-group">
                    <label for="email">Email Address:</label>
                    <input type="email" class="form-control" id="email" name="email" placeholder="Enter your email" required>
                </div>
                <div class="form-group">
                    <label for="address">Residential Address:</label>
                    <textarea class="form-control" id="address" name="address" placeholder="Enter your address" required></textarea>
                </div>
                <button type="submit" class="btn btn-success btn-block">Next</button>
            </form>
        `,
        income: `
            <form id="incomeForm" class="tax-form">
                <h3>Income Details</h3>
                <div class="form-group">
                    <label for="salary">Annual Salary:</label>
                    <input type="number" class="form-control" id="salary" name="salary" required>
                </div>
                <div class="form-group">
                    <label for="other_income">Other Income:</label>
                    <input type="number" class="form-control" id="other_income" name="other_income" value="0">
                </div>
                <div class="form-group">
                    <label>Do you receive HRA?</label>
                    <select class="form-control" id="has_hra" name="has_hra">
                        <option value="no">No</option>
                        <option value="yes">Yes</option>
                    </select>
                </div>
                <div id="hraDetails" style="display: none;">
                    <div class="form-group">
                        <label for="hra_amount">HRA Amount:</label>
                        <input type="number" class="form-control" id="hra_amount" name="hra_amount">
                    </div>
                    <div class="form-group">
                        <label for="rent_paid">Annual Rent Paid:</label>
                        <input type="number" class="form-control" id="rent_paid" name="rent_paid">
                    </div>
                </div>
                <button type="submit" class="btn btn-success btn-block">Next</button>
            </form>
        `,
        deductions: `
            <form id="deductionsForm" class="tax-form">
                <h3>Deductions & Investments</h3>
                <div class="form-group">
                    <label for="section_80c">Section 80C Investments:</label>
                    <input type="number" class="form-control" id="section_80c" name="section_80c" required>
                    <small class="form-text text-muted">EPF, PPF, ELSS, Life Insurance, etc.</small>
                </div>
                <div class="form-group">
                    <label for="section_80d">Section 80D Health Insurance:</label>
                    <input type="number" class="form-control" id="section_80d" name="section_80d" value="0">
                    <small class="form-text text-muted">Medical Insurance Premium</small>
                </div>
                <div class="form-group">
                    <label for="home_loan_interest">Home Loan Interest:</label>
                    <input type="number" class="form-control" id="home_loan_interest" name="home_loan_interest" value="0">
                </div>
                <div class="form-group">
                    <label for="education_loan">Education Loan Interest:</label>
                    <input type="number" class="form-control" id="education_loan" name="education_loan" value="0">
                </div>
                <button type="submit" class="btn btn-success btn-block">Next</button>
            </form>
        `,
        capitalGains: `
            <form id="capitalGainsForm" class="tax-form">
                <h3>Capital Gains & Investment Income</h3>
                <div class="form-group">
                    <label>Did you sell any capital assets this year?</label>
                    <select class="form-control" id="has_capital_gains" name="has_capital_gains">
                        <option value="no">No</option>
                        <option value="yes">Yes</option>
                    </select>
                </div>
                <div id="capitalGainsDetails" style="display: none;">
                    <div class="form-group">
                        <label>Type of Asset:</label>
                        <div class="checkbox-group">
                            <label><input type="checkbox" name="asset_type" value="stocks"> Stocks/Mutual Funds</label>
                            <label><input type="checkbox" name="asset_type" value="property"> Property</label>
                            <label><input type="checkbox" name="asset_type" value="gold"> Gold/Jewelry</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="sale_value">Total Sale Value:</label>
                        <input type="number" class="form-control" id="sale_value" name="sale_value">
                    </div>
                    <div class="form-group">
                        <label for="purchase_value">Original Purchase Value:</label>
                        <input type="number" class="form-control" id="purchase_value" name="purchase_value">
                    </div>
                    <div class="form-group">
                        <label for="holding_period">Holding Period (in years):</label>
                        <input type="number" class="form-control" id="holding_period" name="holding_period">
                    </div>
                </div>
                <button type="submit" class="btn btn-success btn-block">Next</button>
            </form>
        `
    };

    // Form rendering functions
    function renderPersonalForm() {
        window.chatUtils.renderFormInChat(formTemplates.personal, "personalForm", handlePersonalFormSubmit);
    }

    function renderIncomeForm() {
        window.chatUtils.renderFormInChat(formTemplates.income, "incomeForm", handleIncomeFormSubmit);
        setupHraToggle();
    }

    function renderDeductionsForm() {
        window.chatUtils.renderFormInChat(formTemplates.deductions, "deductionsForm", handleDeductionsFormSubmit);
    }

    function renderCapitalGainsForm() {
        window.chatUtils.renderFormInChat(formTemplates.capitalGains, "capitalGainsForm", handleCapitalGainsFormSubmit);
        setupCapitalGainsToggle();
    }

    // Form submit handlers
    function handlePersonalFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        window.taxAdvisory.updateState('personal_summary', {
            personal: {
                full_name: form.full_name.value,
                dob: form.dob.value,
                phone: form.phone.value,
                email: form.email.value,
                address: form.address.value
            }
        });
    }

    function handleIncomeFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        window.taxAdvisory.updateState('income_summary', {
            income: {
                salary: form.salary.value,
                other_income: form.other_income.value,
                has_hra: form.has_hra.value,
                hra_amount: form.has_hra.value === 'yes' ? form.hra_amount.value : 0,
                rent_paid: form.has_hra.value === 'yes' ? form.rent_paid.value : 0
            }
        });
    }

    function handleDeductionsFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        window.taxAdvisory.updateState('deductions_summary', {
            deductions: {
                section_80c: form.section_80c.value,
                section_80d: form.section_80d.value,
                home_loan_interest: form.home_loan_interest.value,
                education_loan: form.education_loan.value
            }
        });
    }

    function handleCapitalGainsFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const assetTypes = Array.from(form.querySelectorAll('input[name="asset_type"]:checked'))
            .map(cb => cb.value);

        window.taxAdvisory.updateState('capital_gains_summary', {
            capital_gains: {
                has_capital_gains: form.has_capital_gains.value,
                asset_types: form.has_capital_gains.value === 'yes' ? assetTypes : [],
                sale_value: form.has_capital_gains.value === 'yes' ? form.sale_value.value : 0,
                purchase_value: form.has_capital_gains.value === 'yes' ? form.purchase_value.value : 0,
                holding_period: form.has_capital_gains.value === 'yes' ? form.holding_period.value : 0
            }
        });
    }

    // Helper functions
    function setupHraToggle() {
        const hasHraSelect = document.getElementById('has_hra');
        const hraDetails = document.getElementById('hraDetails');
        if (hasHraSelect && hraDetails) {
            hasHraSelect.addEventListener('change', function() {
                hraDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            });
        }
    }

    function setupCapitalGainsToggle() {
        const hasCapitalGainsSelect = document.getElementById('has_capital_gains');
        const capitalGainsDetails = document.getElementById('capitalGainsDetails');
        if (hasCapitalGainsSelect && capitalGainsDetails) {
            hasCapitalGainsSelect.addEventListener('change', function() {
                capitalGainsDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            });
        }
    }

    // Public API
    window.taxForms = {
        renderPersonalForm,
        renderIncomeForm,
        renderDeductionsForm,
        renderCapitalGainsForm
    };
})();
