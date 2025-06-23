// Chat states
const states = {
    WELCOME: 'welcome',
    PERSONAL: 'personal',
    PERSONAL_SUMMARY: 'personal_summary',
    INCOME: 'income',
    INCOME_SUMMARY: 'income_summary',
    DEDUCTIONS: 'deductions',
    DEDUCTIONS_SUMMARY: 'deductions_summary',
    CAPITAL_GAINS: 'capital_gains',
    CAPITAL_GAINS_SUMMARY: 'capital_gains_summary',
    FINAL_REPORT: 'final_report'
};

// Store form data
let formData = {
    personal: null,
    income: null,
    deductions: null,
    capital_gains: null
};

let currentState = null;
let awaitingConfirmation = false;
let currentConfirmationCleanup = null;

// Chat functionality
function initializeChat() {
    // Initialize chat elements
    const chatBox = document.getElementById("chat-box");
    const inputField = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");

    // Message handlers
    function appendMessage(text, sender, isHTML = false) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        if (isHTML) {
            messageDiv.innerHTML = text;
        } else {
            messageDiv.textContent = text;
        }
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function renderFormInChat(formHtml, formId, submitHandler) {
        const formContainer = document.createElement("div");
        formContainer.classList.add("message", "bot-message");
        formContainer.innerHTML = formHtml;
        chatBox.appendChild(formContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
        
        const form = document.getElementById(formId);
        if (form) {
            form.addEventListener("submit", submitHandler);
        } else {
            console.error(`Form with id ${formId} not found`);
        }
    }

    // State handlers
    function renderWelcome() {
        appendMessage("Hello! Welcome to our Tax Advisory System.", "bot");
        setTimeout(() => {
            appendMessage("Our system will ask you a series of questions about your income and deductions to help with your tax filing.", "bot");
            setTimeout(() => {
                appendMessage("Let's start with your personal information.", "bot");
                renderState(states.PERSONAL);
            }, 1000);
        }, 1000);
    }

    function renderState(state) {
        currentState = state;
        switch (state) {
            case states.WELCOME:
                renderWelcome();
                break;
            case states.PERSONAL:
                renderPersonalForm();
                break;
            case states.PERSONAL_SUMMARY:
                renderSummary('Personal Information', formData.personal, states.INCOME);
                break;
            case states.INCOME:
                renderIncomeForm();
                break;
            case states.INCOME_SUMMARY:
                renderSummary('Income Details', formData.income, states.DEDUCTIONS);
                break;
            case states.DEDUCTIONS:
                renderDeductionsForm();
                break;
            case states.DEDUCTIONS_SUMMARY:
                renderSummary('Deductions Details', formData.deductions, states.CAPITAL_GAINS);
                break;
            case states.CAPITAL_GAINS:
                renderCapitalGainsForm();
                break;
            case states.CAPITAL_GAINS_SUMMARY:
                renderSummary('Capital Gains Details', formData.capital_gains, states.FINAL_REPORT);
                break;
            case states.FINAL_REPORT:
                renderFinalReport();
                break;
            default:
                appendMessage("Unknown state", "bot");
        }
    }

    // Form rendering
    function renderPersonalForm() {
        const formHtml = `
            <form id="personalForm" class="chat-form">
                <div class="form-group">
                    <label for="full_name">Full Name:</label>
                    <input type="text" class="form-control" id="full_name" name="full_name" required>
                </div>
                <div class="form-group">
                    <label for="dob">Date of Birth:</label>
                    <input type="date" class="form-control" id="dob" name="dob" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" class="form-control" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="phone">Phone:</label>
                    <input type="tel" class="form-control" id="phone" name="phone" required>
                </div>
                <button type="submit" class="btn btn-success btn-block">Next</button>
            </form>
        `;

        renderFormInChat(formHtml, "personalForm", function(e) {
            e.preventDefault();
            const form = e.target;
            formData.personal = {
                full_name: form.full_name.value,
                dob: form.dob.value,
                email: form.email.value,
                phone: form.phone.value
            };
            renderState(states.PERSONAL_SUMMARY);
        });
    }

    function renderSummary(title, data, nextState) {
        let summaryHTML = `<div class="summary-container"><h3>${title}</h3><ul>`;
        for (const [key, value] of Object.entries(data)) {
            summaryHTML += `<li><strong>${key.replace('_', ' ')}:</strong> ${value}</li>`;
        }
        summaryHTML += '</ul></div>';
        appendMessage(summaryHTML, "bot", true);
        
        setTimeout(() => {
            appendMessage("Is this information correct? (yes/no)", "bot");
            waitForUserConfirmation((response) => {
                if (response.toLowerCase() === 'yes') {
                    renderState(nextState);
                } else {
                    renderState(currentState.replace('_SUMMARY', ''));
                }
            });
        }, 1000);
    }

    function renderIncomeForm() {
        const formHtml = `
            <form id="incomeForm" class="chat-form">
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
        `;

        renderFormInChat(formHtml, "incomeForm", function(e) {
            e.preventDefault();
            const form = e.target;
            formData.income = {
                salary: form.salary.value,
                other_income: form.other_income.value,
                has_hra: form.has_hra.value,
                hra_amount: form.has_hra.value === 'yes' ? form.hra_amount.value : 0,
                rent_paid: form.has_hra.value === 'yes' ? form.rent_paid.value : 0
            };
            renderState(states.INCOME_SUMMARY);
        });

        // Add HRA details toggle
        const hasHraSelect = document.getElementById('has_hra');
        const hraDetails = document.getElementById('hraDetails');
        if (hasHraSelect && hraDetails) {
            hasHraSelect.addEventListener('change', function() {
                hraDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            });
        }
    }

    function renderDeductionsForm() {
        const formHtml = `
            <form id="deductionsForm" class="chat-form">
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
        `;

        renderFormInChat(formHtml, "deductionsForm", function(e) {
            e.preventDefault();
            const form = e.target;
            formData.deductions = {
                section_80c: form.section_80c.value,
                section_80d: form.section_80d.value,
                home_loan_interest: form.home_loan_interest.value,
                education_loan: form.education_loan.value
            };
            renderState(states.DEDUCTIONS_SUMMARY);
        });
    }

    function renderCapitalGainsForm() {
        const formHtml = `
            <form id="capitalGainsForm" class="chat-form">
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
        `;

        renderFormInChat(formHtml, "capitalGainsForm", function(e) {
            e.preventDefault();
            const form = e.target;
            const assetTypes = Array.from(form.querySelectorAll('input[name="asset_type"]:checked'))
                .map(cb => cb.value);
            
            formData.capital_gains = {
                has_capital_gains: form.has_capital_gains.value,
                asset_types: form.has_capital_gains.value === 'yes' ? assetTypes : [],
                sale_value: form.has_capital_gains.value === 'yes' ? form.sale_value.value : 0,
                purchase_value: form.has_capital_gains.value === 'yes' ? form.purchase_value.value : 0,
                holding_period: form.has_capital_gains.value === 'yes' ? form.holding_period.value : 0
            };
            renderState(states.CAPITAL_GAINS_SUMMARY);
        });

        // Add capital gains details toggle
        const hasCapitalGainsSelect = document.getElementById('has_capital_gains');
        const capitalGainsDetails = document.getElementById('capitalGainsDetails');
        if (hasCapitalGainsSelect && capitalGainsDetails) {
            hasCapitalGainsSelect.addEventListener('change', function() {
                capitalGainsDetails.style.display = this.value === 'yes' ? 'block' : 'none';
            });
        }
    }

    // Regime calculation functions (2024-25)
    function calculateTaxOld(salary, hra, deductions) {
        let taxable = Math.max(salary - hra - deductions, 0);
        let tax = 0;
        if (taxable <= 250000) tax = 0;
        else if (taxable <= 500000) tax = (taxable - 250000) * 0.05;
        else if (taxable <= 1000000) tax = 12500 + (taxable - 500000) * 0.2;
        else tax = 112500 + (taxable - 1000000) * 0.3;
        if (taxable <= 500000) tax = 0;
        tax = tax * 1.04;
        return { tax: Math.round(tax), taxable };
    }
    function calculateTaxNew(salary) {
        let taxable = salary - 50000; // Standard deduction for new regime 2024-25
        let tax = 0;
        if (taxable <= 300000) tax = 0;
        else if (taxable <= 600000) tax = (taxable - 300000) * 0.05;
        else if (taxable <= 900000) tax = 15000 + (taxable - 600000) * 0.1;
        else if (taxable <= 1200000) tax = 45000 + (taxable - 900000) * 0.15;
        else if (taxable <= 1500000) tax = 90000 + (taxable - 1200000) * 0.2;
        else tax = 150000 + (taxable - 1500000) * 0.3;
        if (taxable <= 700000) tax = 0; // Rebate up to 7L
        tax = tax * 1.04;
        return { tax: Math.round(tax), taxable };
    }
    function calculateExcessDeduction(oldTax, newTax, taxableOld) {
        let diff = Math.abs(oldTax - newTax);
        let lakhs = taxableOld / 100000.0;
        if (lakhs > 10) return Math.round(diff / 0.3);
        if (lakhs > 5) return Math.round(diff / 0.2);
        return 0;
    }

    function renderFinalReport() {
        const calculateTotalIncome = () => {
            const salary = Number(formData.income.salary);
            const otherIncome = Number(formData.income.other_income);
            return salary + otherIncome;
        };
        const calculateTotalDeductions = () => {
            return Number(formData.deductions.section_80c) +
                   Number(formData.deductions.section_80d) +
                   Number(formData.deductions.home_loan_interest) +
                   Number(formData.deductions.education_loan);
        };
        const calculateCapitalGains = () => {
            if (formData.capital_gains.has_capital_gains === 'no') return 0;
            return Number(formData.capital_gains.sale_value) - Number(formData.capital_gains.purchase_value);
        };
        const totalIncome = calculateTotalIncome();
        const totalDeductions = calculateTotalDeductions();
        const capitalGains = calculateCapitalGains();
        const taxableIncome = totalIncome - totalDeductions + capitalGains;

        // Regime comparison (2024-25)
        const salary = Number(formData.income.salary);
        const hra = Number(formData.income.hra) || 0;
        const deductions = totalDeductions;
        const oldRegime = calculateTaxOld(salary, hra, deductions);
        const newRegime = calculateTaxNew(salary);
        let suggestion = oldRegime.tax < newRegime.tax ? "Old Tax Regime" : (newRegime.tax < oldRegime.tax ? "New Tax Regime" : "Either Regime");
        let recommended = oldRegime.tax < newRegime.tax ? oldRegime : newRegime;
        let excessDeduction = calculateExcessDeduction(oldRegime.tax, newRegime.tax, oldRegime.taxable);

        const regimeHtml = `
        <div class="glass p-6 rounded-2xl shadow-lg my-8">
          <h3 class="text-2xl font-bold mb-4 text-indigo-700">Tax Regime Recommendation</h3>
          <div class="mb-4">
            <b>Recommendation</b>
            <p>
              Based on the details you provided, I recommend you opt for the
              <b>${suggestion}</b>.<br>
              Under this regime, your estimated taxable income is
              <b>₹${recommended.taxable.toLocaleString()}</b>
              and your tax payable would be around
              <b>₹${recommended.tax.toLocaleString()}</b>.
            </p>
            <p>
              ${excessDeduction > 0
                ? `Excess Deduction Required for Break Even: <b>₹${excessDeduction.toLocaleString()}</b>`
                : "No extra tax benefit was calculated from the excess tax component."
              }
            </p>
            <p>
              This recommendation takes into account the available deductions and exemptions, aiming to minimize your tax burden in a simple manner.
              Please review your financial goals and consider consulting a tax advisor for personalized advice, as these estimates might vary based on changes to tax laws or your specific situation.
            </p>
            <p>Hope this helps you plan your finances better!</p>
          </div>
          <div class="regime-details mt-4">
            <b>For your reference:</b><br>
            Old Tax Regime – Taxable Income: ₹${oldRegime.taxable.toLocaleString()}, Tax: ₹${oldRegime.tax.toLocaleString()}<br>
            New Tax Regime – Taxable Income: ₹${newRegime.taxable.toLocaleString()}, Tax: ₹${newRegime.tax.toLocaleString()}<br>
            Excess Deduction Required for Break Even: ₹${excessDeduction.toLocaleString()}
            <br>
            <span class="text-muted" style="font-size:0.95em;">
              *Note: These calculations are estimates only and are subject to verification based on current tax laws and your full financial details.
            </span>
          </div>
        </div>
        `;

        const reportHtml = `
            <div class="final-report">
                <h3>Tax Advisory Report</h3>
                <div class="report-section">
                    <h4>Income Summary</h4>
                    <p>Total Income: ₹${totalIncome.toLocaleString()}</p>
                    <p>Total Deductions: ₹${totalDeductions.toLocaleString()}</p>
                    <p>Capital Gains: ₹${capitalGains.toLocaleString()}</p>
                    <p class="highlight">Taxable Income: ₹${taxableIncome.toLocaleString()}</p>
                </div>
                ${regimeHtml}
                <div class="report-section">
                    <h4>Tax Saving Recommendations</h4>
                    <ul>
                        ${totalDeductions < 150000 ? '<li>You can still invest ₹' + (150000 - totalDeductions).toLocaleString() + ' under Section 80C</li>' : ''}
                        <li>Consider investing in tax-saving instruments like ELSS funds or PPF.</li>
                        <li>If eligible, explore NPS contributions for additional tax benefits.</li>
                        <li>Keep proper documentation of all your investments and expenses claimed as deductions.</li>
                    </ul>
                </div>
                <button class="btn btn-primary mt-3" onclick="startNewAssessment()">Start New Assessment</button>
            </div>
        `;
        appendMessage(reportHtml, "bot", true);
    }

    function startNewAssessment() {
        formData = {
            personal: null,
            income: null,
            deductions: null,
            capital_gains: null
        };
        renderState(states.WELCOME);
    }

    function renderRegimeRecommendation(regimeResult) {
        console.log("Rendering Regime Recommendation:", regimeResult);  // Debug log
        const recommendation = `
            <div class="message bot-message">
                <h4>Tax Regime Recommendation</h4>
                <p><strong>Recommendation:</strong> ${regimeResult.suggestion}</p>
                <p><strong>Taxable Income:</strong> ₹${regimeResult.recommended.taxable_income.toLocaleString()}</p>
                <p><strong>Tax Payable:</strong> ₹${regimeResult.recommended.tax.toLocaleString()}</p>
                ${regimeResult.excess_deduction > 0
                    ? `<p><strong>Excess Deduction Required for Break Even:</strong> ₹${regimeResult.excess_deduction.toLocaleString()}</p>`
                    : `<p>No extra tax benefit was calculated from the excess tax component.</p>`}
            </div>
        `;
        appendMessage(recommendation, "bot", true);
    }

    // Initialize event listeners
    sendButton.addEventListener("click", handleUserInput);
    inputField.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            handleUserInput();
        }
    });

    function handleUserInput() {
        const message = inputField.value.trim();
        if (message === "") return;
        
        appendMessage(message, "user");
        inputField.value = "";
        
        if (awaitingConfirmation) return; // Let the confirmation handler deal with it
        
        // Handle user messages that aren't part of a form
        if (message.toLowerCase() === 'restart') {
            formData = {
                personal: null,
                income: null,
                deductions: null,
                capital_gains: null
            };
            renderState(states.WELCOME);
        }
    }

    function waitForUserConfirmation(callback, timeoutDuration = 300000) {
        if (currentConfirmationCleanup) {
            currentConfirmationCleanup();
        }
        
        awaitingConfirmation = true;
        let timeoutId;

        function handleResponse() {
            if (!awaitingConfirmation) return;
            const response = inputField.value.trim();
            if (response) {
                appendMessage(response, "user");
                inputField.value = "";
                cleanup();
                callback(response);
            }
        }

        function cleanup() {
            awaitingConfirmation = false;
            inputField.removeEventListener("keydown", handleKeydown);
            sendButton.removeEventListener("click", handleClick);
            if (timeoutId) clearTimeout(timeoutId);
            currentConfirmationCleanup = null;
        }

        function handleKeydown(event) {
            if (event.key === "Enter") {
                handleResponse();
            }
        }

        inputField.addEventListener("keydown", handleKeydown);
        sendButton.addEventListener("click", handleResponse);

        if (timeoutDuration > 0) {
            timeoutId = setTimeout(() => {
                if (awaitingConfirmation) {
                    appendMessage("No response received. Please try again.", "bot");
                    cleanup();
                }
            }, timeoutDuration);
        }

        currentConfirmationCleanup = cleanup;
    }

    // Start the chat
    renderState(states.WELCOME);
}

// Initialize when the DOM is loaded
document.addEventListener("DOMContentLoaded", initializeChat);
