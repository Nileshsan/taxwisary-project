// Chat Utilities Module
const chatUtils = (function() {
    // States enum
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

    // Private state
    const state = {
        currentState: null,
        awaitingConfirmation: false,
        currentConfirmationCleanup: null,
        confirmationTimeout: 300000, // 5 minutes
        formData: {
            personal: null,
            income: null,
            deductions: null,
            capital_gains: null
        }
    };

    // DOM Elements
    let chatBox, inputField, sendButton;

    // Initialize the chat elements
    function init() {
        chatBox = document.getElementById("chat-box");
        inputField = document.getElementById("user-input");
        sendButton = document.getElementById("send-btn");

        if (!chatBox || !inputField || !sendButton) {
            console.error("Chat elements not found");
            return;
        }

        // Set up event listeners
        sendButton.addEventListener("click", handleSendMessage);
        inputField.addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                handleSendMessage();
            }
        });
    }

    // Message handling
    function appendMessage(text, sender, isHTML = false) {
        if (!chatBox) return;

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

    function handleSendMessage(e) {
        if (e) e.preventDefault();
        if (state.awaitingConfirmation) return;

        const message = inputField.value.trim();
        if (message === "") return;

        appendMessage(message, "user");
        inputField.value = "";
    }

    // Form handling in chat
    function renderFormInChat(formHtml, formId, submitHandler) {
        const formContainer = document.createElement("div");
        formContainer.classList.add("message", "bot-message", "form-container");
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

    // User confirmation handling
    function waitForUserConfirmation(callback, timeoutDuration = state.confirmationTimeout) {
        if (!inputField || !sendButton) return;

        // Set the confirmation state
        state.awaitingConfirmation = true;
        let timeoutId;

        const confirmationHandler = function(e) {
            if (e.type === "keypress" && e.key !== "Enter") return;
            e.preventDefault();
            
            const response = inputField.value.trim();
            if (response === "") return;
            
            // Clear timeout and cleanup
            clearTimeout(timeoutId);
            cleanupListeners();
            
            // Send response and execute callback
            appendMessage(response, "user");
            inputField.value = "";
            state.awaitingConfirmation = false;
            callback(response);
        };

        const cleanupListeners = () => {
            inputField.removeEventListener("keypress", confirmationHandler);
            sendButton.removeEventListener("click", confirmationHandler);
            clearTimeout(timeoutId);
            state.currentConfirmationCleanup = null;
        };

        // Add event listeners
        inputField.addEventListener("keypress", confirmationHandler);
        sendButton.addEventListener("click", confirmationHandler);
        
        // Set timeout
        timeoutId = setTimeout(() => {
            cleanupListeners();
            state.awaitingConfirmation = false;
            appendMessage("No response received. Please try again.", "bot");
        }, timeoutDuration);
        
        // Store cleanup function
        state.currentConfirmationCleanup = cleanupListeners;
    }

    // Summary rendering
    function renderSummary(title, data, onConfirm) {
        appendMessage(`Here is the ${title.toLowerCase()} you provided:`, "bot");
        
        const summaryHtml = Object.entries(data)
            .map(([key, value]) => `<strong>${key.replace(/_/g, ' ')}:</strong> ${value || 'N/A'}<br>`)
            .join('\n');
        
        appendMessage(summaryHtml, "bot", true);
        appendMessage("Is this information correct? (Type 'yes' or 'no')", "bot");
        
        waitForUserConfirmation(function(response) {
            if (response.toLowerCase().startsWith("y")) {
                onConfirm();
            } else {
                const currentState = window.taxAdvisory.getState();
                window.taxAdvisory.updateState(currentState.replace('_SUMMARY', '_FORM'));
            }
        });
    }

    // Report rendering
    function renderFinalReport() {
        const calculateTotalIncome = () => {
            const salary = Number(state.formData.income.salary);
            const otherIncome = Number(state.formData.income.other_income);
            return salary + otherIncome;
        };

        const calculateTotalDeductions = () => {
            return Number(state.formData.deductions.section_80c) +
                   Number(state.formData.deductions.section_80d) +
                   Number(state.formData.deductions.home_loan_interest) +
                   Number(state.formData.deductions.education_loan);
        };

        const calculateCapitalGains = () => {
            if (state.formData.capital_gains.has_capital_gains === 'no') return 0;
            return Number(state.formData.capital_gains.sale_value) - Number(state.formData.capital_gains.purchase_value);
        };

        const totalIncome = calculateTotalIncome();
        const totalDeductions = calculateTotalDeductions();
        const capitalGains = calculateCapitalGains();
        const taxableIncome = totalIncome - totalDeductions + capitalGains;

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
                <div class="report-section">
                    <h4>Tax Saving Recommendations</h4>
                    <ul>
                        ${totalDeductions < 150000 ? '<li>You can still invest ₹' + (150000 - totalDeductions).toLocaleString() + ' under Section 80C</li>' : ''}
                        <li>Consider investing in tax-saving instruments like ELSS funds or PPF.</li>
                        <li>If eligible, explore NPS contributions for additional tax benefits.</li>
                        <li>Keep proper documentation of all your investments and expenses claimed as deductions.</li>
                    </ul>
                </div>
                <button class="btn btn-primary mt-3" onclick="chatUtils.startNewAssessment()">Start New Assessment</button>
            </div>
        `;
        
        appendMessage(reportHtml, "bot", true);
    }

    function renderState(newState) {
        state.currentState = newState;
        switch (newState) {
            case states.WELCOME:
                appendMessage("Hello! Welcome to our Tax Advisory System.", "bot");
                setTimeout(() => {
                    appendMessage("Our system will ask you a series of questions about your income and deductions to help with your tax filing.", "bot");
                    setTimeout(() => {
                        appendMessage("Let's start with your personal information.", "bot");
                        renderState(states.PERSONAL);
                    }, 1000);
                }, 1000);
                break;
            case states.PERSONAL:
                renderPersonalForm();
                break;
            case states.PERSONAL_SUMMARY:
                renderSummary('Personal Information', state.formData.personal, states.INCOME);
                break;
            case states.INCOME:
                renderIncomeForm();
                break;
            case states.INCOME_SUMMARY:
                renderSummary('Income Details', state.formData.income, states.DEDUCTIONS);
                break;
            case states.DEDUCTIONS:
                renderDeductionsForm();
                break;
            case states.DEDUCTIONS_SUMMARY:
                renderSummary('Deductions Details', state.formData.deductions, states.CAPITAL_GAINS);
                break;
            case states.CAPITAL_GAINS:
                renderCapitalGainsForm();
                break;
            case states.CAPITAL_GAINS_SUMMARY:
                renderSummary('Capital Gains Details', state.formData.capital_gains, states.FINAL_REPORT);
                break;
            case states.FINAL_REPORT:
                renderFinalReport();
                break;
            default:
                appendMessage("Unknown state", "bot");
        }
    }

    function startNewAssessment() {
        state.formData = {
            personal: null,
            income: null,
            deductions: null,
            capital_gains: null
        };
        renderState(states.WELCOME);
    }

    // Public API
    window.chatUtils = {
        init,
        appendMessage,
        renderFormInChat,
        waitForUserConfirmation,
        renderSummary,
        renderFinalReport,
        renderPersonalForm,
        renderIncomeForm,
        renderDeductionsForm,
        renderCapitalGainsForm,
        startNewAssessment
    };

    // Initialize when DOM is loaded
    document.addEventListener("DOMContentLoaded", init);
})();
