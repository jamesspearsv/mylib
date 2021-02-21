let edit_btns = document.querySelectorAll('.edit-btn');

for (let i = 0; i < edit_btns.length; i++ ) {
    edit_btns[i].addEventListener('click', () => {
        let type = edit_btns[i].getAttribute('value');
        console.log(type)
        if (type == 'username') {
            let form = document.getElementById('username-form');
            if (form.hasAttribute('hidden')) {
                form.removeAttribute('hidden')
            } else {
                form.setAttribute('hidden', true)
            }
        } else {
            let form = document.getElementById('email-form');
            if (form.hasAttribute('hidden')) {
                form.removeAttribute('hidden')
            } else {
                form.setAttribute('hidden', true)
            }
        }
    });
}