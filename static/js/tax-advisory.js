// Tax Advisory System Core Module
(function() {
    // Private state
    const state = {
        formData: {
            personal: null,
            income: null,
            deductions: null,
            capital_gains: null
        },
        currentState: null
    };

    // States enum
    const STATES = {
        GREETING: 'greeting',
        PERSONAL_FORM: 'personal_form',
        PERSONAL_SUMMARY: 'personal_summary',
        INCOME_FORM: 'income_form',
        INCOME_SUMMARY: 'income_summary',
        DEDUCTIONS_FORM: 'deductions_form',
        DEDUCTIONS_SUMMARY: 'deductions_summary',
        CAPITAL_GAINS_FORM: 'capital_gains_form',
        CAPITAL_GAINS_SUMMARY: 'capital_gains_summary',
        REPORT: 'report'
    };

    // State management
    function updateState(newState, data) {
        state.currentState = newState;
        if (data) {
            state.formData = {...state.formData, ...data};
        }
        renderCurrentState();
    }

    function renderCurrentState() {
        switch(state.currentState) {
            case STATES.GREETING:
                renderGreeting();
                break;
            case STATES.PERSONAL_FORM:
                window.taxForms.renderPersonalForm();
                break;
            case STATES.PERSONAL_SUMMARY:
                renderSummary('Personal Information', state.formData.personal, () => updateState(STATES.INCOME_FORM));
                break;
            case STATES.INCOME_FORM:
                window.taxForms.renderIncomeForm();
                break;
            case STATES.INCOME_SUMMARY:
                renderSummary('Income Details', state.formData.income, () => updateState(STATES.DEDUCTIONS_FORM));
                break;
            case STATES.DEDUCTIONS_FORM:
                window.taxForms.renderDeductionsForm();
                break;
            case STATES.DEDUCTIONS_SUMMARY:
                renderSummary('Deductions', state.formData.deductions, () => updateState(STATES.CAPITAL_GAINS_FORM));
                break;
            case STATES.CAPITAL_GAINS_FORM:
                window.taxForms.renderCapitalGainsForm();
                break;
            case STATES.CAPITAL_GAINS_SUMMARY:
                renderSummary('Capital Gains', state.formData.capital_gains, () => updateState(STATES.REPORT));
                break;
            case STATES.REPORT:
                renderReport();
                break;
            default:
                window.chatUtils.appendMessage("Unknown state", "bot");
        }
    }

    // Render functions
    function renderGreeting() {
        window.chatUtils.appendMessage("Welcome to the Tax Advisory System!", "bot");
        setTimeout(() => {
            window.chatUtils.appendMessage("I'll help you calculate your taxes and find potential deductions.", "bot");
            setTimeout(() => {
                window.chatUtils.appendMessage("Let's start with your personal information.", "bot");
                updateState(STATES.PERSONAL_FORM);
            }, 1000);
        }, 1000);
    }

    function renderSummary(title, data, onConfirm) {
        window.chatUtils.appendMessage(`Here is the ${title.toLowerCase()} you provided:`, "bot");
        const summaryHtml = Object.entries(data)
            .map(([key, value]) => `<strong>${key.replace('_', ' ')}:</strong> ${value || 'N/A'}<br>`)
            .join('\n');
        window.chatUtils.appendMessage(summaryHtml, "bot", true);
        window.chatUtils.appendMessage("Is this information correct? (Type 'yes' or 'no')", "bot");
        window.chatUtils.waitForUserConfirmation(function(response) {
            if (response.toLowerCase().startsWith("y")) {
                onConfirm();
            } else {
                // Go back to form
                updateState(state.currentState.replace('_SUMMARY', '_FORM'));
            }
        });
    }

    function renderReport() {
        const calculations = calculateTaxInfo();
        const reportHtml = generateReportHtml(calculations);
        window.chatUtils.appendMessage(reportHtml, "bot", true);
    }

    function calculateTaxInfo() {
        const income = Number(state.formData.income?.salary || 0) + 
                      Number(state.formData.income?.other_income || 0);
        const deductions = Number(state.formData.deductions?.section_80c || 0) + 
                         Number(state.formData.deductions?.section_80d || 0);
        const capitalGains = state.formData.capital_gains?.has_capital_gains === 'yes' ? 
            Number(state.formData.capital_gains.sale_value || 0) - 
            Number(state.formData.capital_gains.purchase_value || 0) : 0;

        return {
            totalIncome: income,
            totalDeductions: deductions,
            capitalGains: capitalGains,
            taxableIncome: income - deductions + capitalGains
        };
    }

    function generateReportHtml(calculations) {
        return `
            <div class="tax-report">
                <h3>Tax Assessment Report</h3>
                <div class="report-section">
                    <h4>Income Summary</h4>
                    <p>Total Income: ₹${calculations.totalIncome.toLocaleString()}</p>
                    <p>Total Deductions: ₹${calculations.totalDeductions.toLocaleString()}</p>
                    <p>Capital Gains: ₹${calculations.capitalGains.toLocaleString()}</p>
                    <p class="highlight">Taxable Income: ₹${calculations.taxableIncome.toLocaleString()}</p>
                </div>
                <div class="report-section">
                    <h4>Tax Saving Recommendations</h4>
                    <ul>
                        ${calculations.totalDeductions < 150000 ? 
                            `<li>You can still invest ₹${(150000 - calculations.totalDeductions).toLocaleString()} under Section 80C</li>` : ''}
                        <li>Consider investing in tax-saving instruments like ELSS funds or PPF</li>
                        <li>If eligible, explore NPS contributions for additional tax benefits</li>
                        <li>Keep proper documentation of all investments and expenses claimed as deductions</li>
                    </ul>
                </div>
            </div>`;
    }

    function resetState() {
        state.formData = {
            personal: null,
            income: null,
            deductions: null,
            capital_gains: null
        };
        updateState(STATES.GREETING);
    }

    // Public API
    window.taxAdvisory = {
        updateState,
        getState: () => state.currentState,
        getFormData: () => state.formData,
        resetState,
        init: () => {
            updateState(STATES.GREETING);
        }
    };

    // Initialize when DOM is loaded
    document.addEventListener("DOMContentLoaded", function() {
        window.taxAdvisory.init();
    });
})();
