function loginButton() {
    window.location.replace("/login");
}

function registerButton() {
    window.location.replace("/register");
}

function searchPost(e) {
    e.preventDefault();
    const text = document.getElementById('searchInputField').value.trim();
    if (text) {
        window.location.replace('/search/' + encodeURIComponent(text));
    }
}

document.getElementById('searchInputField').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchPost();
    }
});

function onclick(elmId, value) {
    const elem = document.getElementById(elmId);
    if (typeof elem !== 'undefined' && elem !== null) {
        elem.onclick = value;
    }
}

onclick("searchSubmitBtn", searchPost)
onclick("logBtn", loginButton)
onclick("regBtn", registerButton)
