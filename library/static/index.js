const stars = document.querySelectorAll('body > main > div > div.detail-reply.detail-row > form > div > input');

function checkStar(e) {
    const v = e.target.value;

    if (e.target.checked ===true) {
        for(i=0; i<v; i++){
            stars[i].checked=true;
        }
    } if (e.target.checked === false) {
        for(i=0; i<stars.length; i++){
            stars[i].checked=false;
        }
        for(i=0; i<v; i++){
            stars[i].checked=true;
        }
    }
}



for(i=0; i<stars.length; i++) {
    stars[i].addEventListener('click', checkStar);
}