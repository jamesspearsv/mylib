// Success color #4CAF50
// Failure color #F24336
// Set disabled attribute of submit button
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('form-btn').disabled = true; 
});

// tracker for form requirements
let tracker = [false, false]
function enable_button () {
    if (tracker[0] && tracker[1]) {
        document.getElementById('form-btn').disabled = false; 
    } else {
        document.getElementById('form-btn').disabled = true; 
    }
}

// grab needed elements from DOM
let password = document.querySelector('#password');
let confirmation = document.querySelector('#confirmation');

// TODO: implement check for username availability. Ajax requests to server


// Check that password meets requirements
password.addEventListener('keyup', () => {
    // Get current value from password field
    value = password.value;

    // Initilize couters to track requirements
    let upper_case = 0;
    let digit = 0;
    let length = 0;

    // Loop though value to check against password reqs
    for (let i = 0; i < value.length; i++) {
        // If current character is a digit increment digit
        if ($.isNumeric(value[i])) {
            digit ++;
        } 

        // if current character is upper-case increment upper
        if (value[i] >= 'A' && value[i] <= 'Z') {
            upper_case ++;
        }
        // Increment length on each ineration
        length++;
    }

    // Grab reqs-feedback elements from DOM and update based on current value
    if (length > 5) {
        document.getElementById('req1').style.color = '#4CAF50'
    } else {
        document.getElementById('req1').style.color = '#F24336'

    }
    if (digit > 0) {
        document.getElementById('req2').style.color = '#4CAF50'
    } else {
        document.getElementById('req2').style.color = '#F24336'

    }
    if (upper_case > 0) {
       document.getElementById('req3').style.color = '#4CAF50'
    } else {
        document.getElementById('req3').style.color = '#F24336'
    }

    if (length > 5 && digit > 0 && upper_case > 0) {
        tracker[0] = true;
    } else {
        tracker[0] = false;
    }

    // check if button can be enabled
    enable_button()
    
});

// check for password and confimation equality
confirmation.addEventListener('keyup', () => {
    // Compare values from confirmation and password fields
    if (confirmation.value == password.value) {
        tracker[1] = true;
        document.getElementById('req4').style.color = '#4CAF50'
    } else {
        tracker[1] = false;
        document.getElementById('req4').style.color = '#F24336'
    }
    
    // check if button can be enabled
    enable_button()
});