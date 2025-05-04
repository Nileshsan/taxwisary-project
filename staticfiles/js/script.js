// Toggle Products Menu
function toggleProductsMenu() {
    var menu = document.getElementById('products-menu');
    menu.classList.toggle('open');
}

// FAQ Toggle Function
function toggleFAQ(element) {
    var answer = element.nextElementSibling;
    answer.style.display = answer.style.display === 'block' ? 'none' : 'block';
}

// Form Validation
function validateForm() {
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var contact = document.getElementById('contact').value;

    if (name.length < 3) {
        alert("Name must be at least 3 characters long.");
        return false;
    }
    if (!email.includes("@")) {
        alert("Enter a valid email address.");
        return false;
    }
    if (contact.length !== 10 || isNaN(contact)) {
        alert("Enter a valid 10-digit contact number.");
        return false;
    }
    alert("Form submitted successfully!");
    return true;
}
